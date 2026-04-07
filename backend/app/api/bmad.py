from fastapi import APIRouter

from app.bmad.personas import get_all_personas, get_persona, get_persona_system_prompt
from app.bmad.workflows import get_all_workflows, get_workflow
from app.bmad.templates import get_all_templates, get_template_content
from app.core.exceptions import NotFoundError

router = APIRouter()


@router.get("/personas")
async def list_personas():
    return get_all_personas()


@router.get("/personas/{persona_id}")
async def get_persona_detail(persona_id: str):
    persona = get_persona(persona_id)
    if not persona:
        raise NotFoundError("Persona not found")
    return {
        **persona,
        "system_prompt_preview": get_persona_system_prompt(persona_id)[:200] + "...",
    }


@router.get("/workflows")
async def list_workflows():
    return get_all_workflows()


@router.get("/workflows/{workflow_id}")
async def get_workflow_detail(workflow_id: str):
    workflow = get_workflow(workflow_id)
    if not workflow:
        raise NotFoundError("Workflow not found")
    return workflow


@router.get("/templates")
async def list_templates():
    return get_all_templates()


@router.get("/templates/{template_id}/content")
async def get_template(template_id: str):
    content = get_template_content(template_id)
    if not content:
        raise NotFoundError("Template not found")
    return {"id": template_id, "content": content}
