"""AI-powered document structuring — converts raw text to structured YAML context."""

from app.services.context_templates import CONTEXT_TEMPLATES
from app.services.context_service import CONTEXT_CATEGORIES
from app.llm.provider import non_stream_chat


STRUCTURING_PROMPT = """\
You are an expert document analyst and YAML structurer for IT project management.

## Task
Analyze the provided document text and convert it into a structured YAML format matching the specified category template.

## Rules
1. Extract relevant information from the document and map it to the YAML template fields.
2. Fill in [필수] (required) fields first — these MUST be populated with content from the document.
3. Fill in [선택] (optional) fields where the document provides relevant information.
4. Remove optional sections that have no data (don't leave empty placeholders).
5. Output ONLY valid YAML — no markdown fences, no explanations, no preamble.
6. Preserve the template's comment structure for clarity.
7. If the document language is Korean, keep the values in Korean. Otherwise, use the document's language.
8. For fields not found in the document, use reasonable inferences with a comment "# (추정)" to mark them.

## Category: {category_name}

## Template Structure
```yaml
{template}
```

## Document Text
{document_text}

## Output
Generate ONLY the YAML content below:
"""


async def structure_document(
    document_text: str,
    category: str,
    provider: str,
    model: str,
    api_key: str,
    base_url: str | None = None,
    custom_instruction: str | None = None,
) -> str:
    """Use LLM to structure document text into YAML for the given category.

    Returns the structured YAML string.
    """
    if category not in CONTEXT_TEMPLATES:
        raise ValueError(f"Unknown category: {category}")

    template = CONTEXT_TEMPLATES[category]
    category_info = CONTEXT_CATEGORIES[category]
    category_name = f"{category_info['name']} ({category_info['name_en']})"

    # Truncate very long documents (keep ~30K chars for LLM context)
    max_doc_chars = 30000
    if len(document_text) > max_doc_chars:
        document_text = document_text[:max_doc_chars] + f"\n\n... (문서가 너무 길어 {max_doc_chars}자까지만 포함됨, 전체 {len(document_text)}자)"

    prompt = STRUCTURING_PROMPT.format(
        category_name=category_name,
        template=template,
        document_text=document_text,
    )

    if custom_instruction:
        prompt += f"\n\n## Additional Instructions\n{custom_instruction}"

    messages = [
        {"role": "system", "content": "You are an expert YAML structurer. Output ONLY valid YAML, nothing else."},
        {"role": "user", "content": prompt},
    ]

    result = await non_stream_chat(
        provider=provider,
        model=model,
        api_key=api_key,
        messages=messages,
        base_url=base_url,
    )

    # Clean up: remove markdown code fences if LLM added them
    result = result.strip()
    if result.startswith("```yaml"):
        result = result[7:]
    elif result.startswith("```"):
        result = result[3:]
    if result.endswith("```"):
        result = result[:-3]
    result = result.strip()

    return result
