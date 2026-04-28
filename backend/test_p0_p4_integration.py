"""Integration test for P0~P4 features.

Runs against an isolated temp SQLite DB so it cannot touch the developer's
working DB. Skips paths that require live LLM credentials but verifies the
plumbing is callable end-to-end.

Run: .venv/bin/python test_p0_p4_integration.py
"""

from __future__ import annotations

import asyncio
import os
import sys
import tempfile
import traceback


# --- Bootstrap: redirect DB to a temp file BEFORE importing app modules. ----

_TMP_DB_FD, _TMP_DB_PATH = tempfile.mkstemp(suffix=".db", prefix="testp0p4_")
os.close(_TMP_DB_FD)
os.environ["DATABASE_URL"] = f"sqlite+aiosqlite:///{_TMP_DB_PATH}"

from app.database import async_session, init_db  # noqa: E402
from app.models.bolt import Bolt  # noqa: E402
from app.models.project import Project  # noqa: E402
from app.models.project_file import ProjectFile  # noqa: E402
from app.models.project_member import ProjectMember  # noqa: E402
from app.models.traceability_link import TraceabilityLink  # noqa: E402
from app.models.user import User  # noqa: E402
from app.models.validation import ValidationIssue, ValidationRun  # noqa: E402


# --- Test reporter -----------------------------------------------------------

PASSED: list[str] = []
FAILED: list[tuple[str, str]] = []


def assert_eq(actual, expected, label: str) -> None:
    if actual == expected:
        PASSED.append(label)
        print(f"  ✓ {label}")
    else:
        FAILED.append((label, f"expected {expected!r}, got {actual!r}"))
        print(f"  ✗ {label}: expected {expected!r}, got {actual!r}")


def assert_true(cond, label: str) -> None:
    if cond:
        PASSED.append(label)
        print(f"  ✓ {label}")
    else:
        FAILED.append((label, "condition was false"))
        print(f"  ✗ {label}: condition was false")


def assert_in(needle, haystack, label: str) -> None:
    if needle in haystack:
        PASSED.append(label)
        print(f"  ✓ {label}")
    else:
        FAILED.append((label, f"{needle!r} not in {haystack!r}"))
        print(f"  ✗ {label}: {needle!r} not in {haystack!r}")


# --- Fixture content --------------------------------------------------------

PRD_CONTENT = """\
# PRD

## 5. User Journeys

### UJ-001: Buyer onboarding
Buyer signs up, picks plan, makes first purchase.

## 8. Functional Requirements

| ID | Requirement | Priority | Acceptance Criteria |
|----|------------|----------|---------------------|
| FR-001 | Login | Must | User can log in with email/password |
| FR-002 | Logout | Must | User can log out |
| FR-003 | Profile | Should | User can update profile |
| FR-004 | Search | Should | User can search items |

## 9. Non-Functional Requirements

| ID | Requirement |
|----|------------|
| NFR-001 | p95 latency < 200ms |
| NFR-002 | Uptime 99.9% |
"""

ARCH_CONTENT = """\
# Architecture

## 3. ADRs

### ADR-001: Use FastAPI
Decision rationale.

## 5.1 Components

### C-1: API Gateway
<!-- derived_from: PRD#FR-001, PRD#NFR-001 -->
- Responsibility: routing
- Tech: FastAPI

### C-2: Auth Service
<!-- derived_from: PRD#FR-001, PRD#FR-002 -->
- Responsibility: login/logout
- Tech: Python
"""

UX_CONTENT = """\
# UX Spec

## 3. User Flows

### UF-001: Login flow
<!-- derived_from: PRD#UJ-001 -->
Email → password → 2FA → home.

### UF-002: Search flow
Search bar → results → detail.
"""

EPIC_CONTENT = """\
# Epics

## Epic 1: Authentication (E-001)
<!-- derived_from: PRD#FR-001, PRD#FR-002 -->

**ID:** E-001
**Complexity:** S

### Stories
- E1-S1, E1-S2
"""

STORY_CONTENT = """\
# Story: User Login

<!-- derived_from: PRD#FR-001, ARCH#C-2 -->

**ID:** E1-S1
**Points:** 3

## Story
As a user, I want to log in.
"""


# --- Setup -------------------------------------------------------------------

async def setup_project(db) -> tuple[int, int, dict[str, int]]:
    """Create user, project, member, and 5 artifact files. Returns (user_id, project_id, file_ids)."""
    user = User(
        email="tester@example.com",
        hashed_password="x",
        display_name="Tester",
    )
    db.add(user)
    await db.flush()

    project = Project(
        name="Test Project",
        description="P0~P4 integration test",
        phase="planning",
        created_by=user.id,
    )
    db.add(project)
    await db.flush()

    member = ProjectMember(project_id=project.id, user_id=user.id, role="owner")
    db.add(member)
    await db.flush()

    files = {}
    fixtures = [
        ("planning-artifacts/PRD.md", "PRD.md", PRD_CONTENT),
        ("planning-artifacts/architecture.md", "architecture.md", ARCH_CONTENT),
        ("planning-artifacts/ux-spec.md", "ux-spec.md", UX_CONTENT),
        ("planning-artifacts/epics.md", "epics.md", EPIC_CONTENT),
        ("implementation-artifacts/E1-S1-login.md", "E1-S1-login.md", STORY_CONTENT),
    ]
    for path, name, content in fixtures:
        f = ProjectFile(
            project_id=project.id,
            file_path=path,
            file_name=name,
            file_type="deliverable",
            content=content,
            file_size=len(content),
            created_by=user.id,
            updated_by=user.id,
        )
        db.add(f)
        await db.flush()
        files[name] = f.id

    await db.commit()
    return user.id, project.id, files


# --- P0 tests ---------------------------------------------------------------

async def test_p0(user_id: int, project_id: int, file_ids: dict[str, int]) -> None:
    print("\n=== P0 Goal-Backward Traceability ===")
    from app.services.traceability_service import (
        ANCHOR_RE,
        detect_file_prefix,
        extract_anchors,
        extract_explicit_links,
        get_graph,
        get_orphan_anchors,
        get_trace_for_anchor,
        rebuild_all_explicit_links,
    )

    # Anchor detection
    anchors_in_prd = sorted(set(ANCHOR_RE.findall(PRD_CONTENT)))
    assert_in("FR-001", anchors_in_prd, "P0: FR-001 detected in PRD")
    assert_in("NFR-001", anchors_in_prd, "P0: NFR-001 detected in PRD")
    assert_in("UJ-001", anchors_in_prd, "P0: UJ-001 detected in PRD")

    # File prefix
    assert_eq(detect_file_prefix("PRD.md"), "PRD", "P0: PRD prefix detected")
    assert_eq(detect_file_prefix("architecture.md"), "ARCH", "P0: ARCH prefix detected")
    assert_eq(detect_file_prefix("E1-S1-login.md"), "STORY", "P0: STORY prefix detected (dynamic name)")
    assert_eq(detect_file_prefix("ux-spec.md"), "UX", "P0: UX prefix detected")

    # Explicit link extraction (Architecture file)
    async with async_session() as db:
        from sqlalchemy import select
        arch_file = (await db.execute(
            select(ProjectFile).where(ProjectFile.id == file_ids["architecture.md"])
        )).scalar_one()
        links_drafts = extract_explicit_links(arch_file)
        # Expect: C-1 → PRD#FR-001, C-1 → PRD#NFR-001, C-2 → PRD#FR-001, C-2 → PRD#FR-002
        assert_eq(len(links_drafts), 4, "P0: 4 explicit links extracted from architecture")
        sources = {(l.source_anchor, l.target_anchor) for l in links_drafts}
        assert_in(("C-1", "FR-001"), sources, "P0: C-1 → FR-001 link present")
        assert_in(("C-2", "FR-002"), sources, "P0: C-2 → FR-002 link present")

    # Persist links across all files
    async with async_session() as db:
        count = await rebuild_all_explicit_links(db, project_id)
        await db.commit()
    # Expected links:
    #   ARCH: C-1→FR-001, C-1→NFR-001, C-2→FR-001, C-2→FR-002         (4)
    #   UX:   UF-001→UJ-001                                              (1)
    #   EPIC: file→FR-001, file→FR-002 (header marker, source_anchor=__file__) (2)
    #   STORY: file→FR-001, file→C-2                                     (2)
    assert_eq(count, 9, "P0: total explicit links persisted = 9")

    # Graph
    async with async_session() as db:
        graph = await get_graph(db, project_id)
    assert_true(len(graph["nodes"]) > 0, "P0: graph has nodes")
    assert_true(len(graph["edges"]) == 9, "P0: graph has 9 edges")

    # Trace upstream from C-1
    async with async_session() as db:
        trace = await get_trace_for_anchor(
            db, project_id, file_ids["architecture.md"], "C-1", direction="upstream"
        )
    upstream_anchors = {hop["to"]["anchor"] for hop in trace["upstream"]}
    assert_in("FR-001", upstream_anchors, "P0: trace from C-1 reaches FR-001")
    assert_in("NFR-001", upstream_anchors, "P0: trace from C-1 reaches NFR-001")

    # Orphans
    async with async_session() as db:
        orphans = await get_orphan_anchors(db, project_id)
    orphan_anchors = {(o["prefix"], o["anchor"]) for o in orphans}
    # FR-003, FR-004, NFR-002 are not covered by any link
    assert_in(("PRD", "FR-003"), orphan_anchors, "P0: FR-003 detected as orphan (no Story covers it)")
    assert_in(("PRD", "NFR-002"), orphan_anchors, "P0: NFR-002 detected as orphan")
    # ADR-001 is not linked anywhere either
    assert_in(("ARCH", "ADR-001"), orphan_anchors, "P0: ADR-001 detected as orphan")
    # UF-002 has no derived_from
    assert_in(("UX", "UF-002"), orphan_anchors, "P0: UF-002 detected as orphan")


# --- P1 tests ---------------------------------------------------------------

async def test_p1() -> None:
    print("\n=== P1 Construction Phase ===")
    from app.bmad.personas import PERSONAS, get_persona_system_prompt
    from app.bmad.templates import TEMPLATES, get_template_content
    from app.bmad.workflows import WORKFLOWS, get_workflow_prompt

    for pid in ["developer", "qa-engineer", "devops-engineer"]:
        assert_in(pid, PERSONAS, f"P1: persona '{pid}' registered")
        assert_true(bool(get_persona_system_prompt(pid)), f"P1: persona '{pid}' system prompt loaded")

    for wid in ["generate-code-skeleton", "create-test-plan", "design-ci-pipeline", "create-iac"]:
        assert_in(wid, WORKFLOWS, f"P1: workflow '{wid}' registered")
        assert_true(bool(get_workflow_prompt(wid)), f"P1: workflow '{wid}' instructions loaded")

    for tid in ["code-skeleton", "test-plan", "ci-pipeline", "iac"]:
        assert_in(tid, TEMPLATES, f"P1: template '{tid}' registered")
        assert_true(bool(get_template_content(tid)), f"P1: template '{tid}' content loaded")

    # tech-stack context category visible
    from app.services.context_service import CONTEXT_CATEGORIES
    assert_in("tech-stack", CONTEXT_CATEGORIES, "P1: tech-stack category registered")
    assert_true(
        not CONTEXT_CATEGORIES["tech-stack"].get("_hidden", False),
        "P1: tech-stack category visible (not hidden)",
    )


# --- P2 tests ---------------------------------------------------------------

async def test_p2(user_id: int, project_id: int) -> None:
    print("\n=== P2 Bolt Mode ===")
    from app.services.bolt_service import (
        approve_bolt,
        block_bolt,
        complete_bolt,
        get_active_bolt_for_project,
        get_velocity,
        log_activity,
        start_bolt,
        unblock_bolt,
    )

    # Manual bolt creation + state machine
    async with async_session() as db:
        bolt = Bolt(
            project_id=project_id,
            bolt_number=1,
            title="Test bolt",
            persona_id="developer",
            workflow_id="generate-code-skeleton",
            estimated_minutes=60,
            approval_required=True,
            created_by=user_id,
        )
        db.add(bolt)
        await db.flush()
        await log_activity(db, bolt.id, "checkpoint", {"event": "manual_create"}, user_id)
        await db.commit()
        bolt_id = bolt.id

    # Start
    async with async_session() as db:
        from sqlalchemy import select
        bolt = (await db.execute(select(Bolt).where(Bolt.id == bolt_id))).scalar_one()
        await start_bolt(db, bolt, user_id)
        await db.commit()
    assert_eq(bolt.status, "in_bolt", "P2: bolt transitions to in_bolt after start")
    assert_true(bolt.started_at is not None, "P2: started_at timestamp set")

    # get_active_bolt_for_project
    async with async_session() as db:
        active = await get_active_bolt_for_project(db, project_id)
    assert_true(active is not None, "P2: active bolt found via get_active_bolt_for_project")

    # Cannot start a second bolt while one is active (we test via service, not API)
    # The single-active enforcement is at the API layer; the service has no constraint.

    # Complete (approval required → awaiting_approval)
    async with async_session() as db:
        bolt = (await db.execute(select(Bolt).where(Bolt.id == bolt_id))).scalar_one()
        await complete_bolt(db, bolt, user_id, notes="finished")
        await db.commit()
    assert_eq(bolt.status, "awaiting_approval", "P2: bolt → awaiting_approval after complete")

    # Approve
    async with async_session() as db:
        bolt = (await db.execute(select(Bolt).where(Bolt.id == bolt_id))).scalar_one()
        await approve_bolt(db, bolt, user_id)
        await db.commit()
    assert_eq(bolt.status, "done", "P2: bolt → done after approve")

    # Velocity
    async with async_session() as db:
        v = await get_velocity(db, project_id, days=7)
    assert_eq(v["total_completed"], 1, "P2: velocity counts completed bolt")

    # Block / unblock on a fresh bolt
    async with async_session() as db:
        bolt2 = Bolt(
            project_id=project_id,
            bolt_number=2,
            title="Bolt 2",
            persona_id="qa-engineer",
            estimated_minutes=45,
            created_by=user_id,
        )
        db.add(bolt2)
        await db.flush()
        await block_bolt(db, bolt2, user_id, "waiting on PRD clarification")
        await db.commit()
        bolt2_id = bolt2.id
    assert_eq(bolt2.status, "blocked", "P2: bolt → blocked")
    assert_eq(bolt2.blocker_reason, "waiting on PRD clarification", "P2: blocker reason stored")

    async with async_session() as db:
        bolt2 = (await db.execute(select(Bolt).where(Bolt.id == bolt2_id))).scalar_one()
        await unblock_bolt(db, bolt2, user_id)
        await db.commit()
    assert_eq(bolt2.status, "todo", "P2: bolt → todo after unblock")


# --- P3 tests ---------------------------------------------------------------

async def test_p3() -> None:
    print("\n=== P3 Multi-Agent Orchestration ===")
    from app.llm.orchestrator import SubAgent, run_parallel, synthesize, SubAgentResult

    # Smoke: dataclass + scenarios constant
    a = SubAgent(name="Test", system_prompt="x", user_query="y")
    assert_eq(a.name, "Test", "P3: SubAgent constructible")
    assert_eq(a.timeout_seconds, 60.0, "P3: default timeout = 60s")

    from app.api.orchestrate import SCENARIOS
    assert_in("review-prd", SCENARIOS, "P3: review-prd scenario registered")

    # Synthesis with empty results returns a string (no crash)
    # Skipped: would call real LLM. We assert the function exists.
    assert_true(callable(synthesize), "P3: synthesize callable")
    assert_true(callable(run_parallel), "P3: run_parallel callable")


# --- P4 tests ---------------------------------------------------------------

async def test_p4(user_id: int, project_id: int) -> None:
    print("\n=== P4 Spec Validation Engine ===")
    from app.services.validation.registry import all_rules
    from app.services.validation_service import (
        get_issue_counts_by_file,
        get_latest_run,
        run_validation,
    )

    # Registry
    rule_ids = [r.id for r in all_rules()]
    for rid in [
        "fr_covered_by_story",
        "nfr_referenced_in_architecture",
        "ux_flow_aligned_with_journey",
        "orphan_anchor",
        "estimation_sanity",
        "contradictory_terms",
    ]:
        assert_in(rid, rule_ids, f"P4: rule '{rid}' registered")

    # Run validation (rule-based only)
    async with async_session() as db:
        run = await run_validation(
            db,
            project_id=project_id,
            user_id=user_id,
            include_llm_rules=False,
        )
        await db.commit()

    assert_true(run.id is not None, "P4: ValidationRun persisted")
    assert_true(run.duration_ms >= 0, "P4: duration_ms recorded")
    assert_eq(run.rules_executed, 5, "P4: 5 rule-based rules executed (LLM skipped)")
    assert_true(run.issues_open > 0, "P4: at least one open issue surfaced")
    assert_true(0.0 <= run.health_score <= 100.0, "P4: health_score in [0, 100]")

    # Issue counts by file
    async with async_session() as db:
        by_file = await get_issue_counts_by_file(db, project_id)
    assert_true(len(by_file) > 0, "P4: per-file issue counts available")

    # Verify FR coverage rule fires for FR-003, FR-004 (no Story covers them)
    async with async_session() as db:
        from sqlalchemy import select
        result = await db.execute(
            select(ValidationIssue).where(
                ValidationIssue.project_id == project_id,
                ValidationIssue.rule_id == "fr_covered_by_story",
            )
        )
        fr_issues = list(result.scalars().all())
    fr_anchors = {i.anchor for i in fr_issues}
    # E1-S1 story has derived_from PRD#FR-001, so FR-001 is covered.
    # FR-002 is covered via E1-S1 → ARCH#C-2 → which derives from FR-002.
    # Wait — FR-002 coverage only via Story link, not transitive. Let me check.
    # Story `derived_from PRD#FR-001, ARCH#C-2`. Only PRD#FR-001 is a direct
    # Story→PRD link. So FR-002, FR-003, FR-004 should all flag uncovered.
    assert_in("FR-002", fr_anchors, "P4: FR-002 flagged uncovered by story")
    assert_in("FR-003", fr_anchors, "P4: FR-003 flagged uncovered by story")
    assert_in("FR-004", fr_anchors, "P4: FR-004 flagged uncovered by story")
    assert_true("FR-001" not in fr_anchors, "P4: FR-001 NOT flagged (covered by E1-S1)")

    # NFR-002 should be flagged (Architecture only references NFR-001)
    async with async_session() as db:
        from sqlalchemy import select
        result = await db.execute(
            select(ValidationIssue).where(
                ValidationIssue.project_id == project_id,
                ValidationIssue.rule_id == "nfr_referenced_in_architecture",
            )
        )
        nfr_issues = list(result.scalars().all())
    nfr_anchors = {i.anchor for i in nfr_issues}
    assert_in("NFR-002", nfr_anchors, "P4: NFR-002 flagged unreferenced")
    assert_true("NFR-001" not in nfr_anchors, "P4: NFR-001 NOT flagged (referenced by C-1)")

    # UX flow rule: UF-002 has no derived_from to UJ-
    async with async_session() as db:
        from sqlalchemy import select
        result = await db.execute(
            select(ValidationIssue).where(
                ValidationIssue.project_id == project_id,
                ValidationIssue.rule_id == "ux_flow_aligned_with_journey",
            )
        )
        ux_issues = list(result.scalars().all())
    ux_anchors = {i.anchor for i in ux_issues}
    assert_in("UF-002", ux_anchors, "P4: UF-002 flagged unaligned with journey")
    assert_true("UF-001" not in ux_anchors, "P4: UF-001 NOT flagged (links to UJ-001)")

    # Diff: re-run should not duplicate
    async with async_session() as db:
        run2 = await run_validation(
            db, project_id=project_id, user_id=user_id, include_llm_rules=False
        )
        await db.commit()
    assert_eq(run2.issues_open, run.issues_open, "P4: re-run yields stable open issue count")

    # Resolve an issue → next run should mark its fingerprint as keep, status stays.
    # Then add a derived_from for FR-003 in the story file → next run should
    # mark FR-003's fingerprint as resolved.
    async with async_session() as db:
        from sqlalchemy import select
        story_file = (await db.execute(
            select(ProjectFile).where(ProjectFile.file_name == "E1-S1-login.md")
        )).scalar_one()
        # Add FR-003 to the story's derived_from to "cover" it.
        story_file.content = STORY_CONTENT.replace(
            "<!-- derived_from: PRD#FR-001, ARCH#C-2 -->",
            "<!-- derived_from: PRD#FR-001, PRD#FR-003, ARCH#C-2 -->",
        )
        await db.commit()

    # Rebuild traceability so the new link is real.
    async with async_session() as db:
        from app.services.traceability_service import rebuild_all_explicit_links
        await rebuild_all_explicit_links(db, project_id)
        await db.commit()

    async with async_session() as db:
        run3 = await run_validation(
            db, project_id=project_id, user_id=user_id, include_llm_rules=False
        )
        await db.commit()
    # FR-003 should no longer be flagged.
    async with async_session() as db:
        from sqlalchemy import select
        result = await db.execute(
            select(ValidationIssue).where(
                ValidationIssue.project_id == project_id,
                ValidationIssue.rule_id == "fr_covered_by_story",
                ValidationIssue.status == "open",
            )
        )
        open_fr = list(result.scalars().all())
    open_fr_anchors = {i.anchor for i in open_fr}
    assert_true("FR-003" not in open_fr_anchors, "P4: FR-003 resolved after coverage added")
    assert_true(run3.issues_resolved >= 1, "P4: re-run reports >= 1 newly resolved issue")

    # Latest run helper
    async with async_session() as db:
        latest = await get_latest_run(db, project_id)
    assert_eq(latest.id, run3.id, "P4: get_latest_run returns most recent run")


# --- API smoke (FastAPI TestClient) -----------------------------------------

def test_api_smoke() -> None:
    print("\n=== API smoke (FastAPI app) ===")
    # Just verify the app loads with all our routes registered.
    from app.main import app
    paths = sorted({getattr(r, "path", "") for r in app.routes})
    expected_substrings = [
        "/projects/{project_id}/traceability",
        "/projects/{project_id}/bolts",
        "/projects/{project_id}/orchestrate",
        "/projects/{project_id}/validation",
    ]
    for sub in expected_substrings:
        any_match = any(sub in p for p in paths)
        assert_true(any_match, f"API: route prefix '{sub}' present")
    assert_true(len(paths) > 100, f"API: route count > 100 (got {len(paths)})")


# --- Main --------------------------------------------------------------------

async def main():
    await init_db()
    async with async_session() as db:
        user_id, project_id, file_ids = await setup_project(db)

    try:
        await test_p0(user_id, project_id, file_ids)
    except Exception:
        print("  ✗ P0 raised an exception:")
        traceback.print_exc()
        FAILED.append(("P0 group", "exception"))

    try:
        await test_p1()
    except Exception:
        print("  ✗ P1 raised an exception:")
        traceback.print_exc()
        FAILED.append(("P1 group", "exception"))

    try:
        await test_p2(user_id, project_id)
    except Exception:
        print("  ✗ P2 raised an exception:")
        traceback.print_exc()
        FAILED.append(("P2 group", "exception"))

    try:
        await test_p3()
    except Exception:
        print("  ✗ P3 raised an exception:")
        traceback.print_exc()
        FAILED.append(("P3 group", "exception"))

    try:
        await test_p4(user_id, project_id)
    except Exception:
        print("  ✗ P4 raised an exception:")
        traceback.print_exc()
        FAILED.append(("P4 group", "exception"))

    try:
        test_api_smoke()
    except Exception:
        print("  ✗ API smoke raised an exception:")
        traceback.print_exc()
        FAILED.append(("API group", "exception"))

    print("\n" + "=" * 60)
    print(f"PASSED: {len(PASSED)}    FAILED: {len(FAILED)}")
    if FAILED:
        print("\nFailures:")
        for label, reason in FAILED:
            print(f"  - {label}: {reason}")
        sys.exit(1)
    print("\nAll P0~P4 feature tests passed ✓")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        try:
            os.unlink(_TMP_DB_PATH)
        except OSError:
            pass
