from app.bmad.personas import get_persona_system_prompt, get_persona
from app.bmad.workflows import get_workflow, get_workflow_prompt
from app.bmad.templates import get_template_content


def build_system_prompt(
    persona_id: str,
    workflow_id: str | None = None,
    workflow_step: int = 0,
    project_context: str | None = None,
    language: str = "ko",
    project_name: str | None = None,
    project_description: str | None = None,
) -> str:
    """Build the complete system prompt for a chat session."""
    parts = []

    # 0. Project info
    if project_name:
        project_info = f"## Project: {project_name}"
        if project_description:
            project_info += f"\n{project_description}"
        parts.append(project_info)

    # 1. Persona character definition
    persona = get_persona(persona_id)
    persona_prompt = get_persona_system_prompt(persona_id)
    if persona_prompt:
        parts.append(persona_prompt)
    elif persona:
        parts.append(
            f"You are {persona['name']}, {persona['description']} "
            f"You help users in the '{persona['phase']}' phase of software development."
        )

    # 2. Workflow instructions (current step)
    if workflow_id:
        workflow = get_workflow(workflow_id)
        workflow_prompt = get_workflow_prompt(workflow_id)
        if workflow_prompt:
            parts.append(f"\n## Current Workflow: {workflow['name']}\n{workflow_prompt}")
        elif workflow:
            parts.append(f"\n## Current Workflow: {workflow['name']}")
            parts.append(f"Description: {workflow['description']}")

        # Always add current step context if available
        if workflow and workflow.get("steps") and workflow_step > 0:
            total_steps = len(workflow["steps"])
            current_step = next(
                (s for s in workflow["steps"] if s["step"] == workflow_step), None
            )
            if current_step:
                parts.append(
                    f"\n## Current Step ({current_step['step']}/{total_steps}): "
                    f"{current_step['name']}\n{current_step['description']}"
                )

        # Add A/P/C menu instruction if workflow supports it
        if workflow and workflow.get("supports_apc"):
            parts.append(
                "\n## Step Menu (A/P/R/C)\n"
                "At the end of your response for each step, remind the user of available actions:\n"
                "- **[A] Advanced Elicitation** — Deeper critique (Socratic, pre-mortem, red team)\n"
                "- **[P] Party Mode** — Multi-agent collaborative discussion\n"
                "- **[R] Propose Mode** — Persona drafts the step content automatically for review\n"
                "- **[C] Continue** — Save progress and proceed to next step"
            )

        # 3. Template
        template_id = workflow.get("template") if workflow else None
        if template_id:
            template_content = get_template_content(template_id)
            if template_content:
                parts.append(
                    f"\n## Output Template\n"
                    f"When generating or saving the deliverable, you MUST structure the content according to this template. "
                    f"Do NOT save raw chat conversation — compile and organize all discussed information into the proper document format:\n"
                    f"```markdown\n{template_content}\n```"
                )

    # 4. File save instruction
    file_path_map = (
        "Known artifact file paths:\n"
        "- Product Brief → `planning-artifacts/product-brief.md`\n"
        "- PRD → `planning-artifacts/PRD.md`\n"
        "- Architecture → `planning-artifacts/architecture.md`\n"
        "- UX Spec → `planning-artifacts/ux-spec.md`\n"
        "- Epics → `planning-artifacts/epics.md`\n"
        "- Story → `implementation-artifacts/E{epicNum}-S{storyNum}-{story-slug}.md` "
        "(e.g., `implementation-artifacts/E1-S3-user-login.md`). "
        "ALWAYS use this dynamic naming — NEVER save as `story.md` (it would overwrite previous stories). "
        "`story-slug` must be kebab-case, lowercase, English, derived from the story title.\n"
        "- Project Context → `planning-artifacts/project-context.md`\n"
        "- Sprint Status → `implementation-artifacts/sprint-status.md`\n"
        "- Code Skeleton → `construction-artifacts/E{epicNum}-S{storyNum}-skeleton.md`\n"
        "- Test Plan → `construction-artifacts/E{epicNum}-S{storyNum}-test-plan.md`\n"
        "- CI Pipeline → `construction-artifacts/ci-pipeline.yaml`\n"
        "- IaC → `construction-artifacts/iac.yaml`\n"
    )

    # Get template content for current workflow if available
    template_ref = ""
    if workflow_id:
        wf = get_workflow(workflow_id)
        tid = wf.get("template") if wf else None
        if tid:
            tc = get_template_content(tid)
            if tc:
                template_ref = (
                    f"\nIMPORTANT: When saving this artifact, the content MUST follow the BMad template structure below. "
                    f"Do NOT just copy the chat conversation. Instead, compile and organize all discussed content "
                    f"into the proper template format with all sections filled in based on the conversation.\n\n"
                    f"Template structure:\n```markdown\n{tc}\n```\n"
                )

    parts.append(
        "\n## File Save Instructions\n"
        "When the user asks you to create, update, or save an artifact file, "
        "you MUST wrap the file content with the following markers:\n\n"
        "```\n"
        "<!-- SAVE_FILE: path/filename.md -->\n"
        "(full file content here)\n"
        "<!-- END_FILE -->\n"
        "```\n\n"
        "CRITICAL Rules:\n"
        "- The saved content MUST be a properly structured document following the BMad template format — NOT a copy of the chat conversation.\n"
        "- Compile all information discussed in the conversation into the appropriate template sections.\n"
        "- Fill in every relevant section of the template. Leave placeholder markers only for sections not yet discussed.\n"
        "- Use the exact file path from the project artifacts list when updating an existing file.\n"
        f"{file_path_map}"
        "- Always include the COMPLETE file content between the markers — do not abbreviate or truncate.\n"
        "- You may include explanation text before or after the markers.\n"
        "- The system will automatically save the file when these markers are detected.\n"
        f"{template_ref}"
    )

    parts.append(
        "\n## Anchor & Traceability Convention\n"
        "Every requirement, decision, and component you write MUST carry a stable anchor ID so that "
        "downstream artifacts can be traced back to it. NEVER renumber an existing anchor.\n\n"
        "Anchor types by artifact:\n"
        "- PRD → `FR-001` (functional req), `NFR-001` (non-functional req), `UJ-001` (user journey)\n"
        "- Architecture → `ADR-001` (decision), `C-1` (component, used as section heading)\n"
        "- UX Spec → `UF-001` (user flow), `CMP-001` (UI component)\n"
        "- Epics → `E-001`\n"
        "- Stories → `S-001` or per-epic `E1-S3`\n\n"
        "When an artifact element derives from upstream items, place a derivation marker on the\n"
        "line immediately under the heading — e.g.:\n\n"
        "```markdown\n"
        "### C-1: API Gateway\n"
        "<!-- derived_from: PRD#FR-001, PRD#NFR-002 -->\n"
        "```\n\n"
        "Allowed prefixes inside derived_from: `PRD`, `BRIEF`, `ARCH`, `UX`, `EPIC`, `STORY`.\n"
        "Only declare derivations you are confident about — do NOT invent links.\n"
    )

    # 5. Project context
    if project_context:
        parts.append(
            f"\n## Project Artifacts (Files)\n"
            f"Below are the current project artifacts. Reference them when relevant.\n\n"
            f"{project_context}"
        )
    else:
        parts.append(
            "\n## Project Artifacts\n"
            "No project artifacts exist yet."
        )

    # 5. Language instruction
    lang_map = {"ko": "Korean", "en": "English", "ja": "Japanese"}
    lang_name = lang_map.get(language, language)
    parts.append(f"\nPlease respond in {lang_name}.")

    return "\n\n".join(parts)
