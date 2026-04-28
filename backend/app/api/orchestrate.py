"""Orchestrate API — fresh-context multi-agent scenarios."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_project_member
from app.core.security import decrypt_api_key
from app.database import get_db
from app.llm.orchestrator import review_prd_scenario, ScenarioResult
from app.models.llm_config import LLMConfig
from app.models.project_member import ProjectMember
from app.models.user import User

router = APIRouter()


SCENARIOS = ["review-prd"]


async def _get_llm_config(db: AsyncSession, project_id: int, user_id: int):
    result = await db.execute(
        select(LLMConfig).where(
            LLMConfig.user_id == user_id, LLMConfig.is_default == True
        ).limit(1)
    )
    cfg = result.scalar_one_or_none()
    if not cfg:
        owner_result = await db.execute(
            select(ProjectMember.user_id).where(
                ProjectMember.project_id == project_id,
                ProjectMember.role == "owner",
            )
        )
        owner_id = owner_result.scalar_one_or_none()
        if owner_id and owner_id != user_id:
            result = await db.execute(
                select(LLMConfig).where(
                    LLMConfig.user_id == owner_id, LLMConfig.is_default == True
                ).limit(1)
            )
            cfg = result.scalar_one_or_none()
    if not cfg:
        return None
    try:
        api_key = decrypt_api_key(cfg.api_key_encrypted)
    except Exception:
        return None
    return cfg.provider, cfg.model, api_key, cfg.base_url


def _scenario_to_payload(r: ScenarioResult) -> dict:
    return {
        "scenario": r.scenario,
        "synthesis": r.synthesis,
        "subagents": [
            {
                "name": s.name,
                "output": s.output,
                "error": s.error,
                "duration_seconds": round(s.duration_seconds, 2),
            }
            for s in r.subagents
        ],
    }


@router.get("/scenarios")
async def list_scenarios(
    project_id: int,
    member=Depends(get_project_member),
):
    return [{"id": s} for s in SCENARIOS]


@router.post("/{scenario}")
async def run_scenario(
    project_id: int,
    scenario: str,
    user: User = Depends(get_current_user),
    member=Depends(get_project_member),
    db: AsyncSession = Depends(get_db),
):
    if scenario not in SCENARIOS:
        raise HTTPException(status_code=404, detail=f"Unknown scenario: {scenario}")

    cfg = await _get_llm_config(db, project_id, user.id)
    if not cfg:
        raise HTTPException(
            status_code=400,
            detail="LLM 설정이 필요합니다. 설정 페이지에서 API를 등록해 주세요.",
        )
    provider, model, api_key, base_url = cfg

    if scenario == "review-prd":
        result = await review_prd_scenario(
            db, project_id, provider=provider, model=model,
            api_key=api_key, base_url=base_url,
        )
    else:  # pragma: no cover — guarded by SCENARIOS check above
        raise HTTPException(status_code=500, detail="Scenario not implemented")

    return _scenario_to_payload(result)
