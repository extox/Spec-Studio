"""Multi-agent orchestrator with fresh-context subagents.

The orchestrator spawns N independent SubAgents (each with its own focused
system prompt and curated context window), runs them in parallel via
asyncio.gather, then runs ONE final "synthesis" call that consolidates the
results.

Key property: subagent contexts are NEVER merged into the main chat session,
so the user's chat session keeps its small token footprint. Only the
synthesized result is returned (and optionally appended to chat history).
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field

from sqlalchemy.ext.asyncio import AsyncSession

from app.llm.provider import non_stream_chat


# --- Subagent ----------------------------------------------------------------

@dataclass
class SubAgent:
    """A single fresh-context worker with its own system prompt + question."""

    name: str
    system_prompt: str
    user_query: str
    timeout_seconds: float = 60.0


@dataclass
class SubAgentResult:
    name: str
    output: str
    error: str | None = None
    duration_seconds: float = 0.0


async def _run_one(
    agent: SubAgent,
    provider: str,
    model: str,
    api_key: str,
    base_url: str | None,
) -> SubAgentResult:
    import time
    start = time.monotonic()
    try:
        coro = non_stream_chat(
            provider=provider,
            model=model,
            api_key=api_key,
            messages=[
                {"role": "system", "content": agent.system_prompt},
                {"role": "user", "content": agent.user_query},
            ],
            base_url=base_url,
        )
        out = await asyncio.wait_for(coro, timeout=agent.timeout_seconds)
        return SubAgentResult(
            name=agent.name,
            output=out.strip(),
            duration_seconds=time.monotonic() - start,
        )
    except asyncio.TimeoutError:
        return SubAgentResult(
            name=agent.name,
            output="",
            error=f"timeout after {agent.timeout_seconds}s",
            duration_seconds=time.monotonic() - start,
        )
    except Exception as e:  # noqa: BLE001 — surface any provider error
        return SubAgentResult(
            name=agent.name,
            output="",
            error=str(e)[:500],
            duration_seconds=time.monotonic() - start,
        )


async def run_parallel(
    agents: list[SubAgent],
    provider: str,
    model: str,
    api_key: str,
    base_url: str | None = None,
    overall_timeout_seconds: float = 90.0,
) -> list[SubAgentResult]:
    """Run all agents concurrently with a hard overall timeout."""
    tasks = [_run_one(a, provider, model, api_key, base_url) for a in agents]
    try:
        return await asyncio.wait_for(
            asyncio.gather(*tasks),
            timeout=overall_timeout_seconds,
        )
    except asyncio.TimeoutError:
        # Return partial-best-effort: collect whatever finished, mark the rest as timeout.
        results: list[SubAgentResult] = []
        for agent, task in zip(agents, tasks, strict=False):
            if task.done() and not task.cancelled():
                try:
                    results.append(task.result())
                except Exception as e:  # noqa: BLE001
                    results.append(SubAgentResult(name=agent.name, output="", error=str(e)[:500]))
            else:
                task.cancel()
                results.append(
                    SubAgentResult(
                        name=agent.name,
                        output="",
                        error="overall_timeout",
                    )
                )
        return results


# --- Synthesis ---------------------------------------------------------------

SYNTHESIS_SYSTEM = """\
You are a multi-perspective synthesizer. You will receive several independent
expert reports on the same artifact. Produce ONE consolidated review with:

## Critical Issues
(High-confidence findings that block ship.)

## Major Issues
(Important findings that should be addressed soon.)

## Minor Issues / Suggestions
(Nice-to-haves and small inconsistencies.)

## Conflicting Opinions
(Cases where the experts disagreed — explain the disagreement and recommend a resolution.)

## Suggested Next Actions
(Concrete edits or follow-up workflows to run.)

Be concise. Cite which expert raised each issue. Use the same language as the inputs.
"""


async def synthesize(
    results: list[SubAgentResult],
    provider: str,
    model: str,
    api_key: str,
    base_url: str | None = None,
    timeout_seconds: float = 60.0,
) -> str:
    """Run a synthesis call over subagent results."""
    parts: list[str] = []
    for r in results:
        if r.error:
            parts.append(f"## {r.name}\n_Error: {r.error}_")
        else:
            parts.append(f"## {r.name}\n{r.output}")

    user_query = "\n\n---\n\n".join(parts) if parts else "(no expert outputs)"

    try:
        coro = non_stream_chat(
            provider=provider,
            model=model,
            api_key=api_key,
            messages=[
                {"role": "system", "content": SYNTHESIS_SYSTEM},
                {"role": "user", "content": user_query},
            ],
            base_url=base_url,
        )
        out = await asyncio.wait_for(coro, timeout=timeout_seconds)
        return out.strip()
    except asyncio.TimeoutError:
        return "_Synthesis call timed out — see individual subagent outputs above._"
    except Exception as e:  # noqa: BLE001
        return f"_Synthesis failed: {str(e)[:300]}_"


# --- High-level scenarios ---------------------------------------------------

@dataclass
class ScenarioResult:
    scenario: str
    subagents: list[SubAgentResult] = field(default_factory=list)
    synthesis: str = ""


async def review_prd_scenario(
    db: AsyncSession,
    project_id: int,
    provider: str,
    model: str,
    api_key: str,
    base_url: str | None = None,
) -> ScenarioResult:
    """Run a parallel 4-perspective review of the project's PRD.

    Each subagent receives ONLY the PRD content (curated context) — the main
    chat session's context window is untouched.
    """
    from sqlalchemy import select
    from app.bmad.personas import get_persona_system_prompt
    from app.models.project_file import ProjectFile

    # Load PRD content.
    result = await db.execute(
        select(ProjectFile).where(
            ProjectFile.project_id == project_id,
            ProjectFile.file_path.like("%PRD%"),
        ).limit(1)
    )
    prd_file = result.scalar_one_or_none()
    if not prd_file or not prd_file.content:
        return ScenarioResult(
            scenario="review-prd",
            synthesis="_No PRD found in this project. Create one first._",
        )

    prd_content = prd_file.content[:40_000]

    # Define the 4 perspectives.
    perspectives = [
        ("PM (John)", "pm", "Critique the PRD from a Product Management perspective. Are the requirements complete, prioritized, and measurable? Any FRs missing acceptance criteria? Any scope creep risk?"),
        ("Architect (Winston)", "architect", "Critique the PRD from a System Architecture perspective. Are the NFRs achievable? Any hidden technical complexity? Any FRs that look infeasible without architectural changes?"),
        ("UX Designer (Sally)", "ux-designer", "Critique the PRD from a UX perspective. Are user journeys complete? Any edge cases or accessibility gaps? Are user types well-defined?"),
        ("Analyst (Mary)", "analyst", "Critique the PRD from a Business Analyst perspective. Are the success criteria measurable? Is the problem statement defensible? Any market/competitive blind spots?"),
    ]

    agents: list[SubAgent] = []
    for label, persona_id, focus in perspectives:
        persona_prompt = get_persona_system_prompt(persona_id) or f"You are {label}."
        system_prompt = (
            f"{persona_prompt}\n\n"
            f"## Review Focus\n{focus}\n\n"
            f"Output a concise critique (max 400 words). Use bullet points. "
            f"Reference specific FR/NFR/UJ anchors when applicable."
        )
        user_query = f"## PRD to review\n\n{prd_content}"
        agents.append(SubAgent(name=label, system_prompt=system_prompt, user_query=user_query))

    sub_results = await run_parallel(
        agents, provider=provider, model=model, api_key=api_key, base_url=base_url,
        overall_timeout_seconds=90.0,
    )
    synthesis = await synthesize(
        sub_results, provider=provider, model=model, api_key=api_key, base_url=base_url,
    )

    return ScenarioResult(
        scenario="review-prd",
        subagents=sub_results,
        synthesis=synthesis,
    )
