import json
import traceback

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import async_session
from app.models.user import User
from app.models.chat_session import ChatSession
from app.models.project_member import ProjectMember
from app.models.llm_config import LLMConfig
from app.models.project_file import ProjectFile
from app.core.security import decode_token, decrypt_api_key
from app.services.chat_service import add_message, get_session_messages, get_session, update_workflow_step
from app.services.websocket_service import manager
from app.llm.provider import stream_chat, DifyResult
from app.llm.prompt_builder import build_system_prompt
from app.llm.context_builder import build_project_context
from app.bmad.workflows import get_workflow
from app.bmad.templates import get_template_content
from app.bmad.personas import get_persona, get_persona_system_prompt, get_all_personas
from app.services.file_save_helper import save_or_update_file

router = APIRouter()


async def _get_llm_config(db: AsyncSession, user_id: int, project_id: int) -> LLMConfig | None:
    """Get LLM config: user's default first, then project owner's default as fallback."""
    # 1. Try user's own default config
    result = await db.execute(
        select(LLMConfig).where(
            LLMConfig.user_id == user_id,
            LLMConfig.is_default == True,
        ).limit(1)
    )
    config = result.scalar_one_or_none()
    if config:
        return config

    # 2. Fallback: project owner's default config
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
                LLMConfig.user_id == owner_id,
                LLMConfig.is_default == True,
            ).limit(1)
        )
        return result.scalar_one_or_none()

    return None


def _get_conversation_id(chat_session: ChatSession, llm_config: LLMConfig) -> str | None:
    """Extract conversation_id only if it belongs to the current LLM config.

    Stored format: "config_id:conversation_id" (e.g. "1:abc-123").
    Legacy formats are discarded to avoid cross-config conflicts.
    """
    stored = chat_session.external_conversation_id
    if not stored:
        return None
    if ":" in stored:
        config_id_str, conv_id = stored.split(":", 1)
        try:
            if int(config_id_str) == llm_config.id:
                return conv_id
        except ValueError:
            pass
    return None


async def authenticate_ws(token: str) -> int | None:
    """Authenticate WebSocket connection via JWT token."""
    try:
        payload = decode_token(token)
        if payload.get("type") != "access":
            return None
        return int(payload["sub"])
    except Exception:
        return None


@router.websocket("/ws/chat/{session_id}")
async def websocket_chat(websocket: WebSocket, session_id: int, token: str = ""):
    user_id = await authenticate_ws(token)
    if not user_id:
        await websocket.close(code=4001, reason="Unauthorized")
        return

    async with async_session() as db:
        # Verify session exists and user has access
        session = await db.execute(
            select(ChatSession).where(ChatSession.id == session_id)
        )
        chat_session = session.scalar_one_or_none()
        if not chat_session:
            await websocket.close(code=4004, reason="Session not found")
            return

        member = await db.execute(
            select(ProjectMember).where(
                ProjectMember.project_id == chat_session.project_id,
                ProjectMember.user_id == user_id,
            )
        )
        if not member.scalar_one_or_none():
            await websocket.close(code=4003, reason="Forbidden")
            return

    await manager.connect(websocket, session_id)

    # Auto-start workflow step 1 if this is a new workflow session with no messages
    try:
        await _auto_start_workflow(websocket, session_id, user_id)
    except Exception:
        pass  # Non-critical, don't block the connection

    try:
        while True:
            data = await websocket.receive_json()
            msg_type = data.get("type")

            if msg_type == "chat_message":
                await handle_chat_message(
                    websocket, session_id, user_id, data.get("content", ""),
                    file_ids=data.get("file_ids"),
                )
            elif msg_type == "workflow_action":
                await handle_workflow_action(
                    websocket, session_id, data.get("action"), data.get("data", {})
                )
            elif msg_type == "apc_action":
                await handle_apc_action(
                    websocket, session_id, user_id, data.get("action"), data.get("data", {})
                )
            elif msg_type == "switch_persona":
                await handle_switch_persona(
                    websocket, session_id, data.get("persona_id", "")
                )
            elif msg_type == "save_deliverable":
                await handle_save_deliverable(
                    websocket, session_id, user_id,
                    data.get("content", ""),
                    data.get("file_name", ""),
                    data.get("file_path", ""),
                )

    except WebSocketDisconnect:
        manager.disconnect(websocket, session_id)
    except Exception as e:
        await manager.send_json(websocket, {"type": "error", "message": str(e)})
        manager.disconnect(websocket, session_id)


async def handle_chat_message(
    websocket: WebSocket,
    session_id: int,
    user_id: int,
    content: str,
    auto_trigger: bool = False,
    file_ids: list[str] | None = None,
):
    """Handle incoming chat message, call LLM, and stream response.

    If auto_trigger=True, the content is an internal prompt (not from user) —
    it won't be saved as a user message or broadcast.
    file_ids: list of provider file IDs (e.g., AI:ON-U uploaded file IDs)
    """
    async with async_session() as db:
        if not auto_trigger:
            # Get user info for message attribution
            user_result = await db.execute(select(User).where(User.id == user_id))
            user = user_result.scalar_one_or_none()
            user_meta = json.dumps({"user_id": user_id, "display_name": user.display_name if user else "Unknown"})

            # Save user message with author info
            await add_message(db, session_id, "user", content, user_meta)
            await db.commit()

            # Broadcast user message to all other users in this session
            await manager.broadcast(session_id, {
                "type": "user_message",
                "content": content,
                "user_id": user_id,
                "display_name": user.display_name if user else "Unknown",
            }, exclude=websocket)

        # For auto_trigger, add the prompt as a system-level instruction in the LLM call
        # but don't save it as a visible message
        auto_prompt = content if auto_trigger else None

        # Get session info
        chat_session = await get_session(db, session_id)

        # Get LLM config: user's default → project owner's default (fallback)
        llm_config = await _get_llm_config(db, user_id, chat_session.project_id)
        if not llm_config:
            await manager.send_json(websocket, {
                "type": "error",
                "message": "No default LLM configuration found. Please configure an LLM provider in settings.",
            })
            return

        try:
            api_key = decrypt_api_key(llm_config.api_key_encrypted)
        except Exception:
            await manager.send_json(websocket, {
                "type": "error",
                "message": "Failed to decrypt API key.",
            })
            return

        # Build messages for LLM
        project_context = await build_project_context(
            db, chat_session.project_id, chat_session.workflow
        )

        # Get project info
        from app.models.project import Project
        proj_result = await db.execute(select(Project).where(Project.id == chat_session.project_id))
        project = proj_result.scalar_one_or_none()

        system_prompt = build_system_prompt(
            persona_id=chat_session.persona,
            workflow_id=chat_session.workflow,
            workflow_step=chat_session.workflow_step,
            project_context=project_context,
            project_name=project.name if project else None,
            project_description=project.description if project else None,
        )

        # Get chat history
        history = await get_session_messages(db, session_id)
        messages = [{"role": "system", "content": system_prompt}]
        for msg in history:
            messages.append({"role": msg.role, "content": msg.content})

        # For auto-trigger (workflow auto-start), add the prompt as a user instruction
        if auto_prompt:
            messages.append({"role": "user", "content": auto_prompt})

        # Stream response — broadcast to ALL connected users
        msg_id = f"msg_{session_id}_{len(history)}"
        await manager.broadcast_all(session_id, {
            "type": "chat_stream_start",
            "message_id": msg_id,
        })

        full_content = ""
        dify_result = DifyResult() if llm_config.provider == "aion-u" else None

        # Only use external_conversation_id if it belongs to the current provider
        conversation_id = _get_conversation_id(chat_session, llm_config)

        try:
            async for chunk in stream_chat(
                provider=llm_config.provider,
                model=llm_config.model,
                api_key=api_key,
                messages=messages,
                base_url=llm_config.base_url,
                conversation_id=conversation_id,
                dify_result=dify_result,
                file_ids=file_ids if llm_config.provider == "aion-u" else None,
            ):
                full_content += chunk
                await manager.broadcast_all(session_id, {
                    "type": "chat_stream_chunk",
                    "message_id": msg_id,
                    "content": chunk,
                })
        except Exception as e:
            await manager.send_json(websocket, {
                "type": "error",
                "message": f"LLM error: {str(e)}",
            })
            return

        # Save conversation_id with provider prefix for session continuity
        if dify_result and dify_result.conversation_id:
            chat_session.external_conversation_id = f"{llm_config.id}:{dify_result.conversation_id}"

        # Save assistant message
        metadata = json.dumps({"persona": chat_session.persona})
        await add_message(db, session_id, "assistant", full_content, metadata)
        await db.commit()

        await manager.broadcast_all(session_id, {
            "type": "chat_stream_end",
            "message_id": msg_id,
            "full_content": full_content,
            "metadata": {"persona": chat_session.persona},
        })

        # Parse SAVE_FILE markers and auto-save files
        await _parse_and_save_files(db, chat_session, full_content, user_id)

        # Auto-generate deliverable if workflow is on the final step
        workflow = get_workflow(chat_session.workflow) if chat_session.workflow else None
        if workflow and workflow.get("template"):
            total_steps = len(workflow.get("steps", []))
            if total_steps > 0 and chat_session.workflow_step >= total_steps:
                await _auto_compile_deliverable(
                    db, websocket, chat_session, user_id, workflow
                )


async def handle_workflow_action(
    websocket: WebSocket,
    session_id: int,
    action: str,
    data: dict,
):
    """Handle workflow navigation actions."""
    async with async_session() as db:
        chat_session = await get_session(db, session_id)
        workflow = get_workflow(chat_session.workflow) if chat_session.workflow else None
        if not workflow:
            return

        total_steps = len(workflow.get("steps", []))

        if action == "next_step":
            new_step = min(chat_session.workflow_step + 1, total_steps)
        elif action == "skip_step":
            new_step = min(chat_session.workflow_step + 2, total_steps)
        elif action == "restart":
            new_step = 1
        else:
            return

        await update_workflow_step(db, session_id, new_step)
        await db.commit()

        step_info = next(
            (s for s in workflow["steps"] if s["step"] == new_step), None
        )

        await manager.broadcast_all(chat_session.id, {
            "type": "workflow_update",
            "current_step": new_step,
            "total_steps": total_steps,
            "step_name": step_info["name"] if step_info else "",
        })


async def handle_apc_action(
    websocket: WebSocket,
    session_id: int,
    user_id: int,
    action: str,
    data: dict,
):
    """Handle A/P/C menu actions at workflow steps.

    Actions:
    - 'advanced': Activate advanced elicitation (Socratic, pre-mortem, red team)
    - 'party': Activate party mode (multi-agent collaborative discussion)
    - 'continue': Save progress and proceed to next step
    """
    async with async_session() as db:
        chat_session = await get_session(db, session_id)
        workflow = get_workflow(chat_session.workflow) if chat_session.workflow else None
        if not workflow or not workflow.get("supports_apc"):
            await manager.send_json(websocket, {
                "type": "error",
                "message": "This workflow does not support A/P/C actions.",
            })
            return

        if action == "advanced":
            # Inject advanced elicitation prompt into the conversation
            elicitation_prompt = (
                "The user has requested Advanced Elicitation for this step. "
                "Apply deeper critique methods:\n"
                "- Socratic questioning: Challenge every assumption\n"
                "- First-principles thinking: Break down to fundamentals\n"
                "- Pre-mortem analysis: Imagine failure and work backward\n"
                "- Red team review: Adversarial critique\n\n"
                "Analyze the current step's content through these lenses and provide deeper insights."
            )
            await handle_chat_message(websocket, session_id, user_id, elicitation_prompt)

        elif action == "party":
            await handle_party_mode(websocket, session_id, user_id, chat_session)

        elif action == "propose":
            await handle_propose_mode(websocket, session_id, user_id, chat_session, workflow)

        elif action == "continue":
            # Save current progress and advance to next step
            total_steps = len(workflow.get("steps", []))
            new_step = min(chat_session.workflow_step + 1, total_steps)

            await update_workflow_step(db, session_id, new_step)
            await db.commit()

            is_final_step = new_step >= total_steps

            step_info = next(
                (s for s in workflow["steps"] if s["step"] == new_step), None
            )

            await manager.broadcast_all(chat_session.id, {
                "type": "workflow_update",
                "current_step": new_step,
                "total_steps": total_steps,
                "step_name": step_info["name"] if step_info else "",
                "step_description": step_info["description"] if step_info else "",
            })

            if step_info:
                step_msg = f"**Step {new_step}/{total_steps}: {step_info['name']}**"
                await add_message(db, session_id, "system", step_msg)
                await db.commit()
                await manager.broadcast_all(chat_session.id, {
                    "type": "step_transition",
                    "step": new_step,
                    "total_steps": total_steps,
                    "step_name": step_info["name"],
                    "step_description": step_info["description"],
                    "message": step_msg,
                })

            # When reaching the final step, auto-generate the deliverable
            if is_final_step and workflow.get("template"):
                async with async_session() as compile_db:
                    compile_session = await get_session(compile_db, session_id)
                    await _auto_compile_deliverable(
                        compile_db, websocket, compile_session, user_id, workflow
                    )
            elif step_info and not is_final_step:
                # Auto-generate persona's guidance for the new step
                step_guide_prompt = (
                    f"The workflow has moved to Step {new_step}/{total_steps}: {step_info['name']}.\n"
                    f"Step description: {step_info['description']}\n\n"
                    f"Guide the user through this step. Explain what needs to be done and ask "
                    f"the relevant questions to gather the necessary information.\n"
                    f"Respond in the same language as the conversation."
                )
                await handle_chat_message(websocket, session_id, user_id, step_guide_prompt, auto_trigger=True)


async def handle_propose_mode(
    websocket: WebSocket,
    session_id: int,
    user_id: int,
    chat_session: ChatSession,
    workflow: dict,
):
    """Propose Mode: Personas autonomously draft the current step's content.

    Instead of asking questions, personas analyze the project context and
    existing artifacts to generate a concrete proposal for the current step.
    The user only needs to review, approve, or request modifications.
    """
    # Get current step info
    step_info = None
    if workflow.get("steps") and chat_session.workflow_step > 0:
        step_info = next(
            (s for s in workflow["steps"] if s["step"] == chat_session.workflow_step), None
        )

    if not step_info:
        await manager.send_json(websocket, {
            "type": "error",
            "message": "No current step found.",
        })
        return

    # Build the propose prompt
    propose_prompt = (
        f"## Propose Mode\n"
        f"The user has requested Propose Mode for the current step.\n\n"
        f"**Current Step: {step_info['name']}**\n"
        f"Step description: {step_info['description']}\n\n"
        f"**YOUR TASK:**\n"
        f"Instead of asking the user questions, YOU must:\n"
        f"1. Analyze the project name, description, and all existing artifacts in the project context\n"
        f"2. Use your expertise to INFER and REASON about what the answers should be\n"
        f"3. Write a COMPLETE, CONCRETE draft/proposal for this step's deliverable content\n"
        f"4. Present it as a ready-to-review proposal, not as questions\n\n"
        f"**FORMAT:**\n"
        f"Start with: \"Based on the project context, here is my proposal for this step:\"\n"
        f"Then provide the full drafted content.\n"
        f"End with: \"Please review this proposal. You can:\"\n"
        f"- Say **'좋습니다'** or **'Approve'** to accept and move to the next step\n"
        f"- Point out specific parts to modify\n"
        f"- Request a completely different approach\n\n"
        f"**IMPORTANT:** Do NOT ask questions. Make decisions based on your expertise and the available context. "
        f"If information is missing, make reasonable assumptions and state them clearly. "
        f"The goal is to minimize the user's effort — they should only need to review and approve.\n\n"
        f"Respond in the same language as the conversation."
    )

    await handle_chat_message(websocket, session_id, user_id, propose_prompt, auto_trigger=True)


_auto_start_lock: set[int] = set()


async def _auto_start_workflow(
    websocket: WebSocket,
    session_id: int,
    user_id: int,
):
    """Auto-start workflow step 1 when a new workflow session is created."""
    # Prevent duplicate triggers
    if session_id in _auto_start_lock:
        return
    _auto_start_lock.add(session_id)

    try:
        async with async_session() as db:
            chat_session = await get_session(db, session_id)

            if not chat_session.workflow:
                return
            existing = await get_session_messages(db, session_id)
            if existing:
                return

            wf = get_workflow(chat_session.workflow)
            if not wf or not wf.get("steps"):
                return

            # Get project info for the intro
            from app.models.project import Project
            proj_result = await db.execute(select(Project).where(Project.id == chat_session.project_id))
            project = proj_result.scalar_one_or_none()
            project_info = ""
            if project:
                project_info = f"The project name is '{project.name}'."
                if project.description:
                    project_info += f" Project description: {project.description}"

            step = wf["steps"][0]

            intro_prompt = (
                f"You are starting the workflow '{wf['name']}' with the user.\n"
                f"{project_info}\n\n"
                f"This is Step 1: {step['name']} — {step['description']}\n\n"
                f"Greet the user, mention the project name and its context, "
                f"explain what this workflow will accomplish, "
                f"and then guide them through Step 1. Ask the questions or request the information "
                f"needed for this step.\n\n"
                f"IMPORTANT: You already know the project name and description from the system prompt. "
                f"Reference them in your greeting to show you understand the project context.\n\n"
                f"Respond in the same language the user's system is set to (check the language instruction)."
            )

            await handle_chat_message(websocket, session_id, user_id, intro_prompt, auto_trigger=True)
    finally:
        _auto_start_lock.discard(session_id)


async def handle_switch_persona(
    websocket: WebSocket,
    session_id: int,
    persona_id: str,
):
    """Switch the active persona for a chat session."""
    persona = get_persona(persona_id)
    if not persona:
        await manager.send_json(websocket, {
            "type": "error",
            "message": f"Unknown persona: {persona_id}",
        })
        return

    async with async_session() as db:
        chat_session = await get_session(db, session_id)
        chat_session.persona = persona_id
        await db.flush()
        await db.commit()

    await manager.broadcast_all(session_id, {
        "type": "persona_switched",
        "persona_id": persona_id,
        "persona_name": persona["name"],
        "persona_avatar": persona["avatar"],
    })


# Persona relevance mapping for party mode
PARTY_PERSONAS = {
    "create-brief": ["analyst", "pm"],
    "create-prd": ["pm", "architect", "ux-designer"],
    "validate-prd": ["pm", "architect", "analyst"],
    "create-architecture": ["architect", "pm", "scrum-master"],
    "create-ux-design": ["ux-designer", "pm", "analyst"],
    "create-epics": ["scrum-master", "pm", "architect"],
    "sprint-planning": ["scrum-master", "pm"],
    "create-story": ["scrum-master", "architect", "pm"],
}


async def _party_stream_persona(
    websocket, session_id, user_id, llm_config, api_key,
    persona_id, system_prompt, messages, db,
):
    """Stream a single persona's response in party mode."""
    persona = get_persona(persona_id)
    if not persona:
        return ""

    msg_id = f"party_{session_id}_{persona_id}"
    await manager.broadcast_all(session_id, {
        "type": "chat_stream_start",
        "message_id": msg_id,
        "persona_id": persona_id,
        "persona_name": persona["name"],
        "persona_avatar": persona["avatar"],
    })

    full_content = ""
    try:
        async for chunk in stream_chat(
            provider=llm_config.provider,
            model=llm_config.model,
            api_key=api_key,
            messages=[{"role": "system", "content": system_prompt}] + messages,
            base_url=llm_config.base_url,
        ):
            full_content += chunk
            await manager.broadcast_all(session_id, {
                "type": "chat_stream_chunk",
                "message_id": msg_id,
                "content": chunk,
            })
    except Exception as e:
        await manager.send_json(websocket, {
            "type": "error",
            "message": f"Party mode error ({persona['name']}): {str(e)}",
        })
        return ""

    metadata = json.dumps({"persona": persona_id, "party_mode": True})
    await add_message(db, session_id, "assistant", full_content, metadata)
    await db.commit()

    await manager.broadcast_all(session_id, {
        "type": "chat_stream_end",
        "message_id": msg_id,
        "full_content": full_content,
        "metadata": {"persona": persona_id, "party_mode": True},
    })
    return full_content


async def handle_party_mode(
    websocket: WebSocket,
    session_id: int,
    user_id: int,
    chat_session: ChatSession,
):
    """Multi-persona party mode with interactive discussion rounds and synthesis.

    Round 1: Each guest persona gives their initial take on the current discussion.
    Round 2: Each guest persona responds to the other's points (cross-discussion).
    Final: The lead persona synthesizes all perspectives into actionable conclusions.
    """
    workflow_id = chat_session.workflow
    current_persona_id = chat_session.persona
    party_list = PARTY_PERSONAS.get(workflow_id, ["analyst", "pm", "architect"])
    guest_personas = [p for p in party_list if p != current_persona_id][:2]

    async with async_session() as db:
        chat_session_fresh = await get_session(db, session_id)

        llm_config = await _get_llm_config(db, user_id, chat_session_fresh.project_id)
        if not llm_config:
            await manager.send_json(websocket, {"type": "error", "message": "No LLM configuration found."})
            return
        try:
            api_key = decrypt_api_key(llm_config.api_key_encrypted)
        except Exception:
            await manager.send_json(websocket, {"type": "error", "message": "Failed to decrypt API key."})
            return

        project_context = await build_project_context(db, chat_session_fresh.project_id, workflow_id)

        # Build workflow step context
        workflow_context = ""
        wf = get_workflow(workflow_id) if workflow_id else None
        if wf and wf.get("steps") and chat_session_fresh.workflow_step > 0:
            step = next((s for s in wf["steps"] if s["step"] == chat_session_fresh.workflow_step), None)
            if step:
                workflow_context = (
                    f"Workflow: {wf['name']}\n"
                    f"Current Step ({step['step']}/{len(wf['steps'])}): {step['name']} — {step['description']}"
                )

        # Get conversation history
        history = await get_session_messages(db, session_id)
        base_history = [{"role": msg.role, "content": msg.content} for msg in history if msg.role != "system"]

        # Guest persona names for reference
        guest_names = []
        for pid in guest_personas:
            p = get_persona(pid)
            if p:
                guest_names.append(p["name"])

        # --- Party intro ---
        party_intro = f"🎉 **Party Mode** — {', '.join(guest_names)}이(가) 토론에 참여합니다.\n"
        await add_message(db, session_id, "system", party_intro)
        await db.commit()
        await manager.broadcast_all(session_id, {
            "type": "step_transition",
            "step": chat_session_fresh.workflow_step,
            "step_name": "Party Mode",
            "message": party_intro,
        })

        artifacts_section = f"\n\n## Project Artifacts\n{project_context}" if project_context else ""

        # Build a summary of what's being discussed
        # Collect last few meaningful messages for context
        recent_context_parts = []
        for m in base_history[-8:]:
            role_label = "User" if m["role"] == "user" else f"Lead Persona ({current_persona_id})"
            snippet = m["content"][:1500]
            recent_context_parts.append(f"**{role_label}:**\n{snippet}")

        if not recent_context_parts:
            await manager.send_json(websocket, {
                "type": "error",
                "message": "Party Mode requires an active discussion. Please have a conversation first.",
            })
            return

        recent_conversation = "\n\n---\n\n".join(recent_context_parts)

        discussion_context = (
            f"## Current Discussion (Recent Messages)\n"
            f"Below is the recent conversation in this workflow session. "
            f"READ IT CAREFULLY before providing your feedback.\n\n"
            f"{recent_conversation}\n\n"
            f"{workflow_context}"
        )

        # === ROUND 1: Initial perspectives ===
        round1_responses = {}
        for persona_id in guest_personas:
            persona = get_persona(persona_id)
            if not persona:
                continue

            system = (
                f"You are {persona['name']}, {persona['description']}\n\n"
                f"## Party Mode — Round 1\n"
                f"You have been invited to review and provide feedback on an ongoing discussion.\n\n"
                f"{discussion_context}\n\n"
                f"INSTRUCTIONS:\n"
                f"1. You MUST read the conversation above before responding\n"
                f"2. Reference SPECIFIC points from the conversation in your feedback\n"
                f"3. From YOUR expertise as {persona['name']}, provide:\n"
                f"   - What you agree with in the current approach\n"
                f"   - What concerns or risks you see (be specific)\n"
                f"   - What you would suggest changing or adding\n\n"
                f"CRITICAL: Do NOT say 'Hello', do NOT introduce yourself, do NOT ask 'How can I help?'. "
                f"Jump DIRECTLY into substantive feedback about the discussion content. "
                f"If you cannot find discussion content above, summarize what the workflow step requires and propose your expert perspective.\n\n"
                f"Respond in the same language as the conversation."
                f"{artifacts_section}"
            )

            content = await _party_stream_persona(
                websocket, session_id, user_id, llm_config, api_key,
                persona_id, system, base_history, db,
            )
            round1_responses[persona_id] = content

        # === ROUND 2: Cross-discussion ===
        round1_with_content = {k: v for k, v in round1_responses.items() if v}
        if len(round1_with_content) >= 2:
            for persona_id in guest_personas:
                persona = get_persona(persona_id)
                if not persona or not round1_responses.get(persona_id):
                    continue

                other_responses = "\n\n".join(
                    f"**{get_persona(pid)['name']}:**\n{resp}"
                    for pid, resp in round1_with_content.items() if pid != persona_id
                )

                system = (
                    f"You are {persona['name']}.\n\n"
                    f"## Party Mode — Round 2: Respond to Other Experts\n"
                    f"Other experts have shared their feedback. Now respond to their points:\n\n"
                    f"{other_responses}\n\n"
                    f"Your task:\n"
                    f"- Where do you agree or disagree? Why?\n"
                    f"- Are there conflicts between views? How to resolve them?\n\n"
                    f"Be concise (2-3 points). Do NOT repeat Round 1. "
                    f"Respond in the same language as the conversation."
                )

                await _party_stream_persona(
                    websocket, session_id, user_id, llm_config, api_key,
                    persona_id, system,
                    base_history + [{"role": "assistant", "content": v} for v in round1_with_content.values()],
                    db,
                )

        # === FINAL: Lead persona synthesizes ===
        all_history = await get_session_messages(db, session_id)
        all_messages = [{"role": msg.role, "content": msg.content} for msg in all_history if msg.role != "system"]

        lead_persona = get_persona(current_persona_id)
        lead_name = lead_persona["name"] if lead_persona else current_persona_id

        synthesis_system = (
            f"You are {lead_name}, the lead expert for this workflow.\n\n"
            f"## Party Mode — Final Synthesis\n"
            f"A multi-expert discussion just concluded. Synthesize ALL perspectives into a clear conclusion:\n\n"
            f"### 합의 사항\n(What did the experts agree on?)\n\n"
            f"### 논쟁 포인트와 결론\n(Where did they disagree? What's the best resolution?)\n\n"
            f"### 액션 아이템\n(What concrete changes or decisions should be made?)\n\n"
            f"### 이 단계에 대한 최종 권고\n(Your refined recommendation incorporating the discussion)\n\n"
            f"Respond in the same language as the conversation."
            f"{artifacts_section}"
        )

        await _party_stream_persona(
            websocket, session_id, user_id, llm_config, api_key,
            current_persona_id, synthesis_system, all_messages, db,
        )


import re

SAVE_FILE_PATTERN = re.compile(
    r'<!--\s*SAVE_FILE:\s*(.+?)\s*-->\s*\n(.*?)\n\s*<!--\s*END_FILE\s*-->',
    re.DOTALL,
)


async def _parse_and_save_files(
    db: AsyncSession,
    chat_session: ChatSession,
    content: str,
    user_id: int,
):
    """Parse SAVE_FILE markers in LLM response and auto-save files."""
    matches = SAVE_FILE_PATTERN.findall(content)
    if not matches:
        return

    for file_path_raw, file_content in matches:
        file_path = file_path_raw.strip()
        file_content = file_content.strip()

        if not file_path or not file_content:
            continue

        file_name = file_path.split("/")[-1]
        await save_or_update_file(
            db, chat_session.project_id, user_id,
            file_path, file_name, file_content,
            session_id=chat_session.id,
            broadcast_session_id=chat_session.id,
        )


FILE_NAME_MAP = {
    "product-brief": ("planning-artifacts/product-brief.md", "product-brief.md"),
    "prd": ("planning-artifacts/PRD.md", "PRD.md"),
    "architecture": ("planning-artifacts/architecture.md", "architecture.md"),
    "epic": ("planning-artifacts/epics.md", "epics.md"),
    "story": ("implementation-artifacts/story.md", "story.md"),
    "ux-spec": ("planning-artifacts/ux-spec.md", "ux-spec.md"),
    "project-context": ("planning-artifacts/project-context.md", "project-context.md"),
    "sprint-status": ("implementation-artifacts/sprint-status.md", "sprint-status.md"),
}


async def _auto_compile_deliverable(
    db: AsyncSession,
    websocket: WebSocket,
    chat_session: ChatSession,
    user_id: int,
    workflow: dict,
):
    """Auto-compile deliverable using BMad template when workflow final step completes.

    1. Load the BMad template for this workflow
    2. Send compilation prompt to LLM with template format
    3. Stream the response to the user
    4. Auto-save the result as a deliverable file
    5. Notify the user
    """
    template_id = workflow.get("template")
    if not template_id:
        return

    mapping = FILE_NAME_MAP.get(template_id)
    if not mapping:
        return

    file_path, file_name = mapping

    # Load BMad template
    template_content = get_template_content(template_id)

    # Notify user that compilation is starting
    compile_msg = f"Workflow **{workflow['name']}** complete. Auto-generating **{file_name}**..."
    await add_message(db, chat_session.id, "system", compile_msg)
    await db.commit()

    await manager.broadcast_all(chat_session.id, {
        "type": "deliverable_compiling",
        "file_name": file_name,
        "message": compile_msg,
    })

    # Build compilation prompt with template
    compile_prompt = (
        f"The workflow '{workflow['name']}' is now complete. "
        f"Based on EVERYTHING we discussed throughout all steps, "
        f"compile the final deliverable document.\n\n"
        f"IMPORTANT RULES:\n"
        f"- Output ONLY the markdown document, no explanations or commentary\n"
        f"- Start with a level-1 heading (#)\n"
        f"- Fill in ALL sections with concrete content from our conversation\n"
        f"- Replace ALL placeholder text ({{{{...}}}}) with actual content\n"
        f"- Remove any template instructions or comments\n"
        f"- Keep the document structure consistent with the template below\n"
    )

    if template_content:
        compile_prompt += (
            f"\n## Template Format (follow this structure):\n"
            f"```markdown\n{template_content}\n```\n"
        )

    # Save as user message (hidden from normal display via metadata)
    meta = json.dumps({"type": "auto_compile", "hidden": True})
    await add_message(db, chat_session.id, "user", compile_prompt, meta)
    await db.commit()

    # Get LLM config: user's default → project owner's fallback
    llm_config = await _get_llm_config(db, user_id, chat_session.project_id)
    if not llm_config:
        await manager.send_json(websocket, {
            "type": "error",
            "message": "No default LLM configuration. Cannot auto-generate deliverable.",
        })
        return

    try:
        api_key = decrypt_api_key(llm_config.api_key_encrypted)
    except Exception:
        await manager.send_json(websocket, {
            "type": "error",
            "message": "Failed to decrypt API key.",
        })
        return

    # Build context with prioritized project files
    project_context = await build_project_context(
        db, chat_session.project_id, chat_session.workflow
    )

    # Get project info
    from app.models.project import Project
    proj_result = await db.execute(select(Project).where(Project.id == chat_session.project_id))
    project = proj_result.scalar_one_or_none()

    system_prompt = build_system_prompt(
        persona_id=chat_session.persona,
        workflow_id=chat_session.workflow,
        workflow_step=chat_session.workflow_step,
        project_context=project_context,
        project_name=project.name if project else None,
        project_description=project.description if project else None,
    )

    # Build message history for LLM
    history = await get_session_messages(db, chat_session.id)
    messages = [{"role": "system", "content": system_prompt}]
    for msg in history:
        if msg.role != "system":
            messages.append({"role": msg.role, "content": msg.content})

    # Stream response
    msg_id = f"deliverable_{chat_session.id}_{file_name}"
    await manager.broadcast_all(chat_session.id, {
        "type": "chat_stream_start",
        "message_id": msg_id,
    })

    full_content = ""
    dify_result = DifyResult() if llm_config.provider == "aion-u" else None
    conversation_id = _get_conversation_id(chat_session, llm_config)
    try:
        async for chunk in stream_chat(
            provider=llm_config.provider,
            model=llm_config.model,
            api_key=api_key,
            messages=messages,
            base_url=llm_config.base_url,
            conversation_id=conversation_id,
            dify_result=dify_result,
        ):
            full_content += chunk
            await manager.broadcast_all(chat_session.id, {
                "type": "chat_stream_chunk",
                "message_id": msg_id,
                "content": chunk,
            })
    except Exception as e:
        await manager.send_json(websocket, {
            "type": "error",
            "message": f"Deliverable generation failed: {str(e)}",
        })
        return

    if dify_result and dify_result.conversation_id:
        chat_session.external_conversation_id = f"{llm_config.id}:{dify_result.conversation_id}"

    # Save assistant response
    resp_meta = json.dumps({"persona": chat_session.persona, "deliverable": file_name})
    await add_message(db, chat_session.id, "assistant", full_content, resp_meta)
    await db.commit()

    await manager.broadcast_all(chat_session.id, {
        "type": "chat_stream_end",
        "message_id": msg_id,
        "full_content": full_content,
        "metadata": {"persona": chat_session.persona},
    })

    # Auto-save to file (with version tracking)
    await save_or_update_file(
        db, chat_session.project_id, user_id,
        file_path, file_name, full_content,
        session_id=chat_session.id,
        broadcast_session_id=chat_session.id,
    )

    await manager.broadcast_all(chat_session.id, {
        "type": "workflow_complete",
        "file_name": file_name,
        "file_path": file_path,
    })


async def handle_save_deliverable(
    websocket: WebSocket,
    session_id: int,
    user_id: int,
    content: str,
    file_name: str,
    file_path: str,
):
    """Manually save a chat message as a deliverable file."""
    if not content or not file_name:
        await manager.send_json(websocket, {
            "type": "error",
            "message": "Content and file name are required.",
        })
        return

    async with async_session() as db:
        chat_session = await get_session(db, session_id)

        # Default file_path if not provided
        if not file_path:
            file_path = f"planning-artifacts/{file_name}"

        await save_or_update_file(
            db, chat_session.project_id, user_id,
            file_path, file_name, content,
            session_id=chat_session.id,
            broadcast_session_id=chat_session.id,
        )


