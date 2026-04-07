"""AI-powered architecture review — multi-perspective expert analysis and To-Be generation."""

from app.llm.provider import non_stream_chat


REVIEW_PROMPT = """\
You are a panel of expert architects conducting a comprehensive review of a system architecture.
You must review from ALL of the following perspectives simultaneously.

## Review Perspectives

1. **인프라 아키텍트 (Infrastructure Architect)**
   - 서버/스토리지/네트워크 구성의 적정성
   - 고가용성(HA), 재해복구(DR), 스케일링 전략
   - EOL 장비/기술, 성능 병목 지점

2. **클라우드 아키텍트 (Cloud Architect)**
   - 클라우드 네이티브 전환 가능성
   - 컨테이너화, 서버리스 적용 후보
   - 비용 최적화 관점

3. **보안 아키텍트 (Security Architect)**
   - 네트워크 세그멘테이션, 바운더리 적절성
   - 인증/인가 구조, 데이터 암호화
   - 컴플라이언스 리스크

4. **데이터 아키텍트 (Data Architect)**
   - 데이터 흐름, 정합성, 복제 전략
   - DB 선택의 적절성, 캐싱 전략
   - 데이터 마이그레이션 리스크

5. **애플리케이션 아키텍트 (Application Architect)**
   - 서비스 간 결합도, 의존성 관계
   - API 설계, 통신 패턴
   - 확장성, 유지보수성

## Architecture YAML to Review
```yaml
{architecture_yaml}
```

{custom_instruction}

## Output Format (Korean)
아래 형식으로 정확히 작성하세요:

### 종합 평가
(전체 아키텍처에 대한 1-2문단 요약 평가)

### 관점별 분석

#### 1. 인프라 관점
- **강점**: (bullet points)
- **개선필요**: (bullet points)
- **권장사항**: (bullet points)

#### 2. 클라우드 관점
- **강점**: (bullet points)
- **개선필요**: (bullet points)
- **권장사항**: (bullet points)

#### 3. 보안 관점
- **강점**: (bullet points)
- **개선필요**: (bullet points)
- **권장사항**: (bullet points)

#### 4. 데이터 관점
- **강점**: (bullet points)
- **개선필요**: (bullet points)
- **권장사항**: (bullet points)

#### 5. 애플리케이션 관점
- **강점**: (bullet points)
- **개선필요**: (bullet points)
- **권장사항**: (bullet points)

### 핵심 개선 우선순위
(가장 중요한 개선사항 3-5개를 우선순위대로 나열)
"""


TOBE_PROMPT = """\
You are a senior system architect. Based on the review of the current (AS-IS) architecture and the improvement recommendations, generate a To-Be architecture in YAML format.

## Current AS-IS Architecture
```yaml
{asis_yaml}
```

## Review & Improvement Recommendations
{review_result}

{custom_instruction}

## Rules
1. Output ONLY valid YAML — no markdown fences, no explanations.
2. Preserve the same YAML structure (system_name, system_type, description, boundaries, infrastructure).
3. Apply the recommended improvements: add/remove/modify components, boundaries, connections.
4. Update system_name to reflect the To-Be state (e.g., append "(To-Be)" or use a new name).
5. Set system_type to the recommended architecture style.
6. Add `_position` fields for each infrastructure item for canvas layout.
7. Add `_boundary` fields to assign items to boundaries.
8. Add connection labels and directions.
9. Include `_system_info_position` for the system info card.
10. Make the architecture realistic and implementable.

## Output
Generate ONLY the To-Be YAML:
"""


async def review_architecture(
    architecture_yaml: str,
    provider: str,
    model: str,
    api_key: str,
    base_url: str | None = None,
    custom_instruction: str | None = None,
) -> str:
    """Use LLM to review architecture from multiple expert perspectives."""
    prompt = REVIEW_PROMPT.format(
        architecture_yaml=architecture_yaml[:30000],
        custom_instruction=f"\n## Additional Instructions\n{custom_instruction}" if custom_instruction else "",
    )

    messages = [
        {"role": "system", "content": "You are a panel of expert system architects. Respond in Korean."},
        {"role": "user", "content": prompt},
    ]

    return await non_stream_chat(
        provider=provider, model=model, api_key=api_key,
        messages=messages, base_url=base_url,
    )


async def generate_tobe_architecture(
    asis_yaml: str,
    review_result: str,
    provider: str,
    model: str,
    api_key: str,
    base_url: str | None = None,
    custom_instruction: str | None = None,
) -> str:
    """Use LLM to generate To-Be architecture based on review."""
    prompt = TOBE_PROMPT.format(
        asis_yaml=asis_yaml[:20000],
        review_result=review_result[:15000],
        custom_instruction=f"\n## Additional Instructions\n{custom_instruction}" if custom_instruction else "",
    )

    messages = [
        {"role": "system", "content": "You are a senior system architect. Output ONLY valid YAML, nothing else."},
        {"role": "user", "content": prompt},
    ]

    result = await non_stream_chat(
        provider=provider, model=model, api_key=api_key,
        messages=messages, base_url=base_url,
    )

    # Clean markdown fences
    result = result.strip()
    if result.startswith("```yaml"):
        result = result[7:]
    elif result.startswith("```"):
        result = result[3:]
    if result.endswith("```"):
        result = result[:-3]
    return result.strip()
