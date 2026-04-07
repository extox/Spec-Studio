"""Context Expansion service — categories, templates, and YAML validation."""

import yaml

CONTEXT_CATEGORIES = {
    "system-architecture": {
        "id": "system-architecture",
        "name": "시스템 아키텍처 모델링",
        "name_en": "System Architecture Modeling",
        "description": "AS-IS / To-Be 시스템 아키텍처를 시각적으로 모델링하고 YAML로 관리합니다.",
        "icon": "layers",
    },
    # Keep old IDs as aliases for backward compatibility
    "legacy-system": {
        "id": "legacy-system",
        "name": "시스템 아키텍처 모델링",
        "name_en": "System Architecture Modeling",
        "description": "AS-IS / To-Be 시스템 아키텍처를 시각적으로 모델링하고 YAML로 관리합니다.",
        "icon": "layers",
        "_hidden": True,
    },
    "architecture": {
        "id": "architecture",
        "name": "시스템 아키텍처 모델링",
        "name_en": "System Architecture Modeling",
        "description": "AS-IS / To-Be 시스템 아키텍처를 시각적으로 모델링하고 YAML로 관리합니다.",
        "icon": "layers",
        "_hidden": True,
    },
}

# Required fields per category
REQUIRED_FIELDS = {
    "system-architecture": {"system_name": "시스템 이름", "system_type": "시스템 유형"},
    "legacy-system": {"system_name": "시스템 이름", "system_type": "시스템 유형"},
    "architecture": {"system_name": "시스템 이름", "system_type": "시스템 유형"},
}


def validate_yaml(content: str) -> tuple[bool, dict | None, list[str]]:
    """Parse and validate YAML content.

    Returns (is_valid, parsed_dict_or_none, error_messages).
    """
    errors: list[str] = []
    if not content or not content.strip():
        return False, None, ["YAML 내용이 비어있습니다."]
    try:
        parsed = yaml.safe_load(content)
        if parsed is None:
            return False, None, ["YAML 내용이 비어있습니다."]
        if not isinstance(parsed, dict):
            return False, None, ["YAML 최상위는 객체(mapping) 형태여야 합니다."]
        return True, parsed, []
    except yaml.YAMLError as e:
        msg = str(e)
        errors.append(f"YAML 파싱 오류: {msg}")
        return False, None, errors


def validate_required_fields(category: str, parsed: dict) -> list[str]:
    """Check required fields for a given category. Returns list of warnings (not errors)."""
    warnings: list[str] = []
    required = REQUIRED_FIELDS.get(category, {})
    for field, label in required.items():
        if field not in parsed or parsed[field] is None or (isinstance(parsed[field], str) and not parsed[field].strip()):
            warnings.append(f"필수 필드 '{field}' ({label})이(가) 비어있습니다.")
    return warnings


def get_category_from_path(file_path: str) -> str | None:
    """Extract category from file_path like 'context/legacy-system/xxx.yaml'."""
    parts = file_path.split("/")
    if len(parts) >= 2 and parts[0] == "context":
        cat = parts[1]
        if cat in CONTEXT_CATEGORIES:
            return cat
    return None
