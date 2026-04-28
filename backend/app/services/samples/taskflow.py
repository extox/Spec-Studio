TASKFLOW_FILES = [
    {
        "file_name": "product-brief.md",
        "file_path": "planning-artifacts/product-brief.md",
        "content": """---
stepsCompleted: [1,2,3,4,5]
inputDocuments: []
workflowType: 'brief'
---
# Product Brief - TaskFlow

**Author:** BMad Sample
**Date:** 2026-03-21
**Status:** Complete

---

## Executive Summary

TaskFlow는 AI를 활용하여 할일의 맥락을 자동으로 분석하고, 카테고리 분류·우선순위 지정·최적 실행 순서를 제안하는 차세대 스마트 할일 관리 웹 앱입니다. 단순 목록 관리를 넘어 "무엇을 먼저 해야 하는가"라는 핵심 질문에 AI로 답하여, 바쁜 직장인의 의사결정 피로를 획기적으로 줄입니다.

## The Problem

현대 직장인은 이메일, 메신저, 회의록, 프로젝트 도구 등 다양한 채널에서 쏟아지는 업무를 수동으로 정리하고 있습니다. 하루 평균 30분 이상을 "무엇부터 해야 하는가"를 판단하는 데 소비하며, 이 과정에서 중요한 업무가 묻히거나 마감을 놓치는 경우가 빈번합니다. 이 문제가 해결되지 않으면 생산성 저하, 번아웃, 업무 누락에 의한 신뢰도 하락이 지속됩니다.

### Current Alternatives

- **수첩 / 스프레드시트:** 구조화되지 않아 할일이 묻히고 우선순위 판단 불가
- **기존 할일 앱 (Todoist, Things, TickTick):** 수동 분류 필요, AI 지원 없음, 사용자가 직접 판단해야 함
- **프로젝트 관리 도구 (Jira, Asana, Monday):** 개인 할일 관리에는 과도하게 복잡, 학습 곡선 높음
- **Apple Reminders / Google Tasks:** 기본 기능만 제공, 분류·우선순위 자동화 없음

## The Solution

자연어로 할일을 입력하면 AI가 자동으로 카테고리를 분류하고, 마감일·중요도·소요시간·의존성을 고려한 최적 순서를 제안하는 개인 할일 관리 웹 앱. 사용자는 AI가 정렬한 목록을 따라 실행하기만 하면 됩니다.

### Core Capabilities

- **AI 자동 분류:** 할일 입력 시 카테고리(업무/개인/학습/건강), 우선순위(긴급/높음/보통/낮음) 자동 태깅
- **자연어 입력:** "내일까지 분기 보고서 작성" → 마감일, 제목, 카테고리 자동 파싱
- **스마트 일일 일정:** 오늘 할일을 AI가 최적 순서로 배치하여 "오늘의 플랜" 제공
- **생산성 대시보드:** 완료율, 주간 트렌드, 카테고리별 분포 시각화
- **원클릭 완료:** 체크박스 토글 + 되돌리기 토스트 (3초)

## What Makes This Different

**AI 기반 자동 우선순위 조정** — 사용자가 직접 분류하지 않아도 AI가 할일의 텍스트 맥락, 마감일 긴급도, 과거 패턴을 종합하여 가장 중요한 일을 상위에 배치합니다. 기존 앱의 "수동 드래그 정렬"과 근본적으로 다릅니다.

## Who This Serves

### Primary Users

**바쁜 직장인 (25-45세):** 마케팅 매니저, 개발자, 기획자 등 다양한 프로젝트를 병행하며, 매일 10-30개의 할일을 처리하는 지식 노동자. 기존 도구의 수동 정리에 피로감을 느끼고, "AI가 대신 정리해줬으면"이라는 니즈가 명확한 사용자.

### Secondary Users

**프리랜서:** 여러 클라이언트의 업무를 동시에 관리해야 하는 1인 사업자. 카테고리 자동 분류가 특히 유용.
**대학생:** 과제, 시험, 동아리 활동 등을 관리하며, 마감일 기반 자동 정렬에 가치를 느끼는 사용자.

## Success Criteria

| Criteria | Target | Measurement |
|----------|--------|-------------|
| 일일 활성 사용자 (DAU) | 1,000명 (출시 3개월) | Firebase Analytics |
| 할일 완료율 | 기존 대비 30% 향상 | A/B 테스트 (기존 앱 사용자 비교) |
| AI 제안 채택률 | 50% 이상 | 이벤트 로그 (제안 순서대로 완료한 비율) |
| 사용자 만족도 (NPS) | 50 이상 | 월간 인앱 설문 |
| 일일 재방문율 | 60% 이상 | Analytics (D1 Retention) |

## Scope

### In Scope (MVP)

- 이메일/비밀번호 기반 사용자 인증 (회원가입, 로그인, 로그아웃)
- 할일 CRUD (생성, 조회, 수정, 삭제, 완료 토글)
- 자연어 할일 입력 및 AI 파싱 (날짜, 키워드 추출)
- AI 자동 카테고리 분류 및 우선순위 지정
- 스마트 일일 일정 제안 ("오늘의 추천 순서")
- 기본 대시보드 (오늘 완료/미완료, 주간 완료율 차트)
- 반응형 웹 디자인 (데스크톱 + 모바일 브라우저)

### Out of Scope

- 팀 협업 기능 (공유 할일, 할당)
- 캘린더 앱 연동 (Google Calendar, Apple Calendar)
- 모바일 네이티브 앱 (iOS/Android)
- 음성 입력
- 반복 할일 자동 생성
- 이메일/메신저 연동 자동 수집

## Vision

**1년:** AI 기반 개인 할일 관리의 대표 서비스. DAU 10,000명 돌파. 유료 프리미엄 모델 전환 (월 ₩4,900).
**3년:** 팀 협업 기능 추가, Google/Apple 캘린더 통합, 크로스플랫폼 (Web + iOS + Android). AI가 프로젝트 단위 일정을 관리하는 "AI 비서" 수준으로 진화. MAU 100만 목표.
""",
    },
    {
        "file_name": "PRD.md",
        "file_path": "planning-artifacts/PRD.md",
        "content": """---
stepsCompleted: [1,2,3,4,5,6,7,8,9,10,11,12]
inputDocuments: ['product-brief.md']
workflowType: 'prd'
---
# Product Requirements Document - TaskFlow

**Author:** BMad Sample
**Date:** 2026-03-21
**Version:** 1.0
**Status:** Complete

---

## 1. Executive Summary

TaskFlow는 AI 기반 스마트 할일 관리 웹 앱입니다. 자연어로 할일을 입력하면 GPT-4o-mini가 자동으로 카테고리를 분류하고 우선순위를 지정합니다. 기존 할일 앱이 "목록을 보여주는 도구"라면, TaskFlow는 "무엇을 먼저 해야 하는지 판단해주는 AI 비서"입니다.

바쁜 직장인이 매일 겪는 "무엇부터 해야 하지?"라는 의사결정 피로를 AI가 해소합니다. 사용자는 할일을 입력하기만 하면, AI가 분류하고, 우선순위를 매기고, 오늘의 최적 실행 순서를 제안합니다.

Python/FastAPI 백엔드, Next.js 프론트엔드, PostgreSQL 데이터베이스, OpenAI API를 활용하며, AWS 위에 배포됩니다.

## 2. Project Classification

| Attribute | Value |
|-----------|-------|
| Project Type | Web Application (SPA + REST API) |
| Domain | 생산성 / 개인 관리 (Productivity) |
| Complexity | Moderate |
| Greenfield/Brownfield | Greenfield (신규 개발) |

## 3. Product Vision

### 1-Year Vision
AI 기반 개인 할일 관리의 대표 서비스. 높은 할일 완료율과 사용자 만족도 달성. DAU 10,000명.

### 3-Year Vision
팀 협업, 캘린더 통합, 크로스플랫폼을 지원하는 종합 AI 생산성 플랫폼. MAU 100만.

### Key Differentiator
맥락 인식 AI가 수동 개입 없이 할일의 최적 실행 순서를 결정. 사용자는 "판단"이 아닌 "실행"에만 집중.

## 4. Success Criteria

### User Success

| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| 할일 완료율 | 70% 이상 | 앱 내 완료/생성 비율 추적 |
| 일일 재방문율 (D1) | 60% 이상 | Firebase Analytics |
| AI 제안 채택률 | 50% 이상 | 이벤트 로그 (제안 순서대로 완료) |

### Business Success

| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| MAU | 5,000 (6개월) | Analytics |
| 유료 전환율 | 5% | 결제 시스템 |
| 월 이탈률 (Churn) | 10% 미만 | 코호트 분석 |

### Technical Success

| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| API p95 응답시간 | < 200ms | CloudWatch |
| 가용성 | 99.5% | Uptime 모니터링 |
| AI 분류 정확도 | 85% 이상 | 사용자 수정 비율 역추적 |

## 5. User Journeys

### UJ-001: 바쁜 직장인 지민 (마케팅 매니저, 32세)

**Discovery:** 매일 할일을 수첩에 적지만 우선순위가 뒤섞여 중요한 일을 놓치는 경험을 반복. "AI 할일 관리"를 검색하여 TaskFlow 발견. 랜딩 페이지의 "AI가 정렬해줍니다" 메시지에 관심.

**Onboarding:** 이메일로 30초 만에 가입. 샘플 할일 3개가 미리 등록되어 있어 AI 분류 기능을 즉시 체험. "분기 보고서 작성"을 입력하자 자동으로 [업무/높음/이번 주 금요일]로 분류되어 감탄. 카테고리 설정(업무/개인/학습) 완료.

**Core Usage:** 매일 아침 출근 후 TaskFlow를 열고 "오늘의 추천 순서" 확인. 자연어로 새 할일 추가 ("금요일까지 분기 보고서 작성"). AI가 제안한 순서대로 업무 처리. 완료 시 체크박스 토글 → 취소선 애니메이션 → 만족감.

**Edge Cases:** 급한 업무가 갑자기 추가되면 AI가 자동으로 순서를 재조정. 분류가 잘못된 경우 카테고리 뱃지를 클릭하여 수동 수정 → AI가 학습.

**Return Usage:** 퇴근 전 완료 현황 확인 (오늘 8/10 완료!). 대시보드에서 주간 생산성 트렌드 확인. 매일 사용하며 습관 형성.

### UJ-002: 프리랜서 수진 (웹 디자이너, 28세)

**Discovery:** 3개 클라이언트의 업무를 동시 관리 중. Todoist를 쓰지만 프로젝트별 분류가 번거로움. TaskFlow의 "자동 카테고리 분류" 기능에 관심.

**Core Usage:** 클라이언트별로 할일을 입력하면 AI가 자동 분류. "A사 로고 시안 수정"은 [업무-A사], "포트폴리오 업데이트"는 [개인-커리어]로 자동 태깅. 마감일이 급한 순서대로 "오늘의 플랜" 제공.

## 6. Domain Requirements

해당 없음 (규제 없는 일반 소비자 생산성 앱).

## 7. Scoping & Roadmap

### MVP (Phase 1) — Must-Have

- 이메일/비밀번호 인증 (회원가입, 로그인, 로그아웃, JWT)
- 할일 CRUD + 완료 토글
- 자연어 할일 입력 + AI 파싱 (날짜, 키워드)
- AI 자동 카테고리 분류 + 우선순위 지정
- 스마트 일일 일정 제안 ("오늘의 추천 순서")
- 기본 대시보드 (완료 현황, 주간 차트)
- 반응형 웹 디자인

### Growth (Phase 2) — Should-Have

- 반복 할일 (매일/매주/매월)
- 알림/리마인더 (웹 푸시, 이메일)
- 할일 검색 및 필터 (카테고리, 우선순위, 날짜)
- 생산성 리포트 (월간 요약, 카테고리별 시간 분석)
- 소셜 로그인 (Google, Apple)

### Vision (Phase 3) — Could-Have

- 팀 공유 할일 + 할당
- 캘린더 앱 연동 (Google Calendar, Apple Calendar)
- 모바일 네이티브 앱 (React Native)
- AI 습관 분석 + 자동 시간 블록 제안

### Won't-Have (Explicitly Excluded)

- 실시간 협업 편집 (Notion 스타일)
- 파일 첨부 및 문서 관리
- 음성 입력 / 음성 인식
- 화상 회의 / 채팅 기능

### Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| OpenAI API 비용 증가 | 중 | 높 | 캐싱, 배치 처리, 경량 모델 대체 |
| AI 분류 정확도 부족 | 중 | 중 | 사용자 피드백 루프, Few-shot 프롬프트 |
| 사용자 습관 형성 실패 | 높 | 높 | 온보딩 개선, 푸시 알림, 감마이피케이션 |
| 경쟁사 AI 기능 추가 | 높 | 중 | 빠른 MVP 출시, 차별화된 UX |

## 8. Functional Requirements

### 8.1 사용자 인증

| ID | Requirement | Priority | Acceptance Criteria |
|----|------------|----------|---------------------|
| FR-001 | 이메일/비밀번호로 회원가입 | Must | 유효한 이메일, 8자 이상 비밀번호, 중복 이메일 거부 |
| FR-002 | 이메일/비밀번호로 로그인 | Must | JWT access token (30분) + refresh token (7일) 발급 |
| FR-003 | 로그아웃 | Must | 클라이언트 토큰 삭제, 로그인 페이지 리다이렉트 |
| FR-004 | 토큰 자동 갱신 | Must | Access token 만료 시 refresh token으로 자동 갱신 |

### 8.2 할일 관리

| ID | Requirement | Priority | Acceptance Criteria |
|----|------------|----------|---------------------|
| FR-010 | 할일 생성 (제목, 설명, 마감일) | Must | DB 저장, 목록에 즉시 표시 |
| FR-011 | 자연어로 할일 생성 | Must | "내일까지 보고서" → 마감일 자동 파싱, 제목 추출 |
| FR-012 | 할일 목록 조회 | Must | 기본 정렬: AI 추천 순서, 페이지네이션 |
| FR-013 | 할일 상세 조회 | Must | 제목, 설명, 카테고리, 우선순위, 마감일, AI 메타데이터 |
| FR-014 | 할일 수정 | Must | 제목, 설명, 마감일, 카테고리, 우선순위 변경 가능 |
| FR-015 | 할일 삭제 | Must | 소프트 삭제 (deleted_at), 목록에서 즉시 제거 |
| FR-016 | 할일 완료 토글 | Must | 체크박스 토글, 완료 시각 기록, 3초 되돌리기 토스트 |
| FR-017 | 할일 검색 | Should | 제목, 설명 전문 검색 (PostgreSQL tsvector) |

### 8.3 AI 기능

| ID | Requirement | Priority | Acceptance Criteria |
|----|------------|----------|---------------------|
| FR-020 | AI 자동 카테고리 분류 | Must | 할일 생성 시 자동 태깅, JSON 구조화 출력 |
| FR-021 | AI 우선순위 지정 | Must | 긴급/높음/보통/낮음 4단계 자동 지정 |
| FR-022 | 스마트 일일 일정 제안 | Must | 마감일, 우선순위, 소요시간 고려 최적 순서 |
| FR-023 | 자연어 파싱 | Must | 날짜("내일", "금요일"), 시간, 키워드 추출 |
| FR-024 | 분류 결과 수동 수정 | Must | 카테고리/우선순위 뱃지 클릭으로 변경 가능 |

### 8.4 대시보드

| ID | Requirement | Priority | Acceptance Criteria |
|----|------------|----------|---------------------|
| FR-030 | 오늘 완료/미완료 현황 | Must | 실시간 카운트 + 프로그레스 바 |
| FR-031 | 주간 완료율 차트 | Must | 7일간 일별 완료율 라인 차트 |
| FR-032 | 카테고리별 분포 | Should | 도넛 차트 (업무/개인/학습/건강) |

## 9. Non-Functional Requirements

### 9.1 Performance — NFR-001

| Metric | Target |
|--------|--------|
| 페이지 초기 로드 (FCP) | < 1.5초 |
| API 응답 시간 (p95) | < 200ms (AI 제외) |
| AI 분류 응답 시간 | < 2초 |
| 동시 사용자 | 500명 |

### 9.2 Security — NFR-002

- 비밀번호: bcrypt (cost factor 12)
- 인증: JWT RS256, httpOnly cookie 옵션
- 통신: HTTPS 전용 (TLS 1.3)
- SQL Injection: SQLAlchemy ORM 사용, raw query 금지
- XSS: React 기본 이스케이프 + CSP 헤더
- API Key: 환경변수 관리, 절대 코드/로그에 노출 금지

### 9.3 Scalability — NFR-003

- 수평 확장: ECS 오토스케일링 (CPU 70% 기준)
- DB: RDS PostgreSQL Read Replica (읽기 부하 분산)
- AI: 요청 큐잉 + rate limiting (분당 60건)

### 9.4 Reliability — NFR-004

- 가용성: 99.5% (월간 다운타임 < 3.6시간)
- 백업: RDS 자동 백업 (7일 보존)
- 에러 추적: Sentry 연동

### 9.5 Accessibility — NFR-005

- WCAG 2.1 AA 준수
- 키보드 네비게이션 지원 (Tab, Enter, Space)
- 스크린 리더: aria-label, role 적용
- 색상 대비: 4.5:1 이상

## 10. Appendix

### Glossary

| Term | Definition |
|------|-----------|
| DAU | Daily Active Users, 일일 활성 사용자 수 |
| NPS | Net Promoter Score, 순추천고객지수 |
| FCP | First Contentful Paint, 첫 콘텐츠 렌더링 시점 |
| JWT | JSON Web Token, 무상태 인증 토큰 |
| tsvector | PostgreSQL 전문 검색 데이터 타입 |

### References

- OpenAI API Documentation: https://platform.openai.com/docs
- FastAPI Documentation: https://fastapi.tiangolo.com
- BMad Method V6: https://github.com/bmadcode/bmad-method
""",
    },
    {
        "file_name": "architecture.md",
        "file_path": "planning-artifacts/architecture.md",
        "content": """---
stepsCompleted: [1,2,3,4,5,6,7,8]
inputDocuments: ['product-brief.md', 'PRD.md']
workflowType: 'architecture'
---
# Architecture Decision Document - TaskFlow

**Author:** BMad Sample
**Date:** 2026-03-21
**Version:** 1.0
**Status:** Complete

---

## 1. Overview

### 1.1 Purpose
TaskFlow의 기술 아키텍처를 정의합니다. AI 기반 할일 분류, 자연어 처리, 실시간 일정 제안을 지원하는 웹 앱 구조를 설계합니다.

### 1.2 Scope
MVP 기능 전체 (인증, 할일 CRUD, AI 분류, 대시보드). 팀 협업, 모바일 앱은 범위 외.

### 1.3 Context
2인 개발팀, 3개월 MVP 목표. 클라우드 네이티브, AI API 의존.

## 2. Architecture Drivers

### 2.1 Key Requirements

| ID | Requirement | Impact Level |
|----|------------|-------------|
| FR-011 | 자연어 할일 입력 + AI 파싱 | High — AI 통합 아키텍처 결정 |
| FR-020 | AI 자동 카테고리 분류 | High — 외부 API 의존성 |
| FR-022 | 스마트 일일 일정 제안 | Medium — 알고리즘 설계 |
| NFR-001 | API p95 < 200ms | High — 캐싱, 비동기 전략 |
| NFR-002 | JWT + bcrypt + HTTPS | High — 인증 아키텍처 |

### 2.2 Quality Attributes

| Attribute | Priority | Target |
|-----------|----------|--------|
| Performance | High | API < 200ms, AI < 2s |
| Security | High | OWASP Top 10 방어 |
| Maintainability | High | 모듈 분리, 테스트 커버리지 80% |
| Scalability | Medium | 500 동시 사용자 → 수평 확장 |
| Reliability | Medium | 99.5% 가용성 |

### 2.3 Constraints

- 2인 개발팀 → 복잡한 마이크로서비스 불가
- OpenAI API 의존 → 비용 관리 필수
- 3개월 MVP → 기술 부채 최소화하며 빠른 출시

## 3. Architecture Decisions (ADRs)

### ADR-001: Architecture Style — 모놀리식 + SPA
<!-- derived_from: PRD#NFR-001 -->

- **Context:** 소규모 팀, 빠른 MVP, 기능 간 긴밀한 연동 필요
- **Decision:** 모놀리식 백엔드 (FastAPI) + SPA 프론트엔드 (Next.js)
- **Rationale:** 마이크로서비스의 운영 복잡도 불필요. 모듈 경계를 명확히 하여 추후 분리 가능
- **Consequences:** 빠른 개발, 단순 배포. 향후 AI 서비스 분리 시 리팩토링 필요
- **Alternatives:** 마이크로서비스 (과도), Serverless (콜드스타트 + AI 호출 제약)

### ADR-002: Backend Framework — FastAPI + Python 3.12
<!-- derived_from: PRD#FR-020, PRD#FR-022 -->

- **Context:** AI/ML 연동, 비동기 처리, 빠른 프로토타이핑 필요
- **Decision:** FastAPI
- **Rationale:** 네이티브 비동기, 자동 OpenAPI 문서, Pydantic 타입 검증, Python AI 생태계
- **Consequences:** 풍부한 AI 라이브러리 (openai, langchain 등) 직접 활용
- **Alternatives:** Django (동기 기반, 무거움), Express (AI 생태계 약함)

### ADR-003: Database — PostgreSQL 16
<!-- derived_from: PRD#FR-017 -->

- **Context:** 관계형 데이터 (User-Todo), AI 메타데이터 저장, 전문 검색
- **Decision:** PostgreSQL 16 (AWS RDS)
- **Rationale:** JSONB (AI 메타데이터), tsvector (전문 검색), 안정성, AWS 네이티브 지원
- **Consequences:** 검색 + AI 데이터 + 관계형 데이터를 단일 DB로 처리
- **Alternatives:** MySQL (JSONB 미지원), MongoDB (관계형 약함), SQLite (확장성 제한)

### ADR-004: AI Integration — OpenAI API (GPT-4o-mini) + Structured Output
<!-- derived_from: PRD#FR-020, PRD#FR-021, PRD#FR-022, PRD#FR-023 -->

- **Context:** 할일 분류 및 자연어 파싱에 LLM 필요
- **Decision:** OpenAI API, GPT-4o-mini 모델, JSON response_format
- **Rationale:** 비용 효율적 ($0.15/1M input), JSON 모드로 안정적 파싱, 충분한 분류 성능
- **Consequences:** 외부 의존성, API 비용 발생. 캐싱으로 비용 절감 필요
- **Alternatives:** Claude (비용 높음), 로컬 LLM (인프라 부담), Rule-based (정확도 낮음)

### ADR-005: Frontend — Next.js 14 + TypeScript
<!-- derived_from: PRD#FR-030, PRD#FR-031, PRD#FR-032 -->

- **Context:** 반응성 높은 SPA, SEO 불필요 (앱 특성)
- **Decision:** Next.js (App Router) + TypeScript + Tailwind CSS + shadcn/ui
- **Rationale:** React 생태계, 타입 안전성, 빠른 UI 개발
- **Consequences:** 풍부한 컴포넌트 라이브러리 활용

## 4. Technology Stack

| Layer | Technology | Version | Justification |
|-------|-----------|---------|---------------|
| Frontend | Next.js + TypeScript | 14.x | React 생태계, SSR 옵션 |
| State Mgmt | Zustand | 4.x | 경량, 직관적 API |
| UI Components | Tailwind CSS + shadcn/ui | 3.x / latest | 빠른 스타일링, 일관된 디자인 |
| Charts | Recharts | 2.x | React 네이티브, 가볍고 직관적 |
| Backend | FastAPI + Python | 3.12 | 비동기, AI 생태계 |
| ORM | SQLAlchemy (async) | 2.x | 비동기 지원, 성숙한 생태계 |
| Database | PostgreSQL | 16.x | 관계형 + JSONB + tsvector |
| Auth | JWT (PyJWT) | — | 무상태, access + refresh |
| AI | OpenAI API (GPT-4o-mini) | — | 비용 효율, JSON 모드 |
| Hosting | AWS ECS + RDS | — | 컨테이너 + 관리형 DB |
| CI/CD | GitHub Actions | — | PR 기반, 자동 테스트 + 배포 |

## 5. System Architecture

### 5.1 Components

#### C-1: Auth Module
<!-- derived_from: PRD#FR-001, PRD#FR-002, PRD#FR-003, PRD#FR-004, PRD#NFR-002 -->
- **Responsibility:** 회원가입 / 로그인 / 토큰 발급 + 갱신
- **Tech:** FastAPI + PyJWT + bcrypt
- **Interfaces:** `/api/auth/*`

#### C-2: Todo Module
<!-- derived_from: PRD#FR-010, PRD#FR-012, PRD#FR-013, PRD#FR-014, PRD#FR-015, PRD#FR-016, PRD#FR-017 -->
- **Responsibility:** Todo CRUD, 검색, 완료 토글, 소프트 삭제
- **Tech:** FastAPI + SQLAlchemy + PostgreSQL tsvector
- **Interfaces:** `/api/todos/*`

#### C-3: AI Module
<!-- derived_from: PRD#FR-011, PRD#FR-020, PRD#FR-021, PRD#FR-022, PRD#FR-023, PRD#FR-024 -->
- **Responsibility:** 자연어 파싱 + 자동 분류 + 일정 제안
- **Tech:** OpenAI API (GPT-4o-mini) + Structured Output
- **Interfaces:** Internal calls from C-2, `/api/ai/suggest-schedule`

#### C-4: Dashboard Module
<!-- derived_from: PRD#FR-030, PRD#FR-031, PRD#FR-032 -->
- **Responsibility:** 오늘 현황, 주간 차트, 카테고리 분포 집계
- **Tech:** FastAPI + SQL aggregations
- **Interfaces:** `/api/dashboard/*`

#### C-5: Frontend SPA
<!-- derived_from: PRD#FR-001, PRD#FR-010, PRD#FR-030 -->
- **Responsibility:** UI 렌더링, JWT 보관, REST 호출
- **Tech:** Next.js 14 + Zustand + Tailwind + shadcn/ui

### 5.1.1 Component Diagram

```
┌─────────────┐     HTTPS      ┌──────────────────────────┐
│   Browser   │ ←──────────→   │   Next.js SPA (Vercel)   │
└─────────────┘                └──────────┬───────────────┘
                                          │ REST API (JSON)
                                          ▼
                               ┌──────────────────────────┐
                               │      FastAPI Backend      │
                               │   (AWS ECS / Docker)      │
                               ├──────────┬───────────────┤
                               │ Auth     │ Todo Module   │
                               │ Module   ├───────────────┤
                               │          │ AI Module     │──→ OpenAI API
                               │          ├───────────────┤
                               │          │ Dashboard Mod │
                               └──────────┴───────┬───────┘
                                                  │
                                          ┌───────▼───────┐
                                          │  PostgreSQL   │
                                          │  (AWS RDS)    │
                                          └───────────────┘
```

### 5.2 Data Flow (할일 생성)

1. 사용자가 자연어로 할일 입력 ("금요일까지 분기 보고서 작성")
2. Frontend → POST /api/todos { raw_text: "금요일까지 분기 보고서 작성" }
3. Backend Todo Module → AI Module: classify_todo(raw_text)
4. AI Module → OpenAI API: JSON 모드 호출 → { title, due_date, category, priority }
5. AI Module → Todo Module: 파싱 결과 반환
6. Todo Module → DB: Todo 레코드 저장 (ai_metadata JSONB 포함)
7. Backend → Frontend: 201 Created + Todo JSON 응답

## 6. Data Architecture

### 6.1 Entity Relationship

```
User (1) ──→ (N) Todo
                  ├── id: SERIAL PK
                  ├── user_id: FK → users.id
                  ├── title: VARCHAR(500)
                  ├── description: TEXT (nullable)
                  ├── category: VARCHAR(50) — AI 분류
                  ├── priority: VARCHAR(20) — urgent/high/medium/low
                  ├── due_date: TIMESTAMPTZ (nullable)
                  ├── completed_at: TIMESTAMPTZ (nullable)
                  ├── ai_metadata: JSONB — AI 분류 원본 응답
                  ├── is_deleted: BOOLEAN — 소프트 삭제
                  ├── created_at: TIMESTAMPTZ
                  └── updated_at: TIMESTAMPTZ
```

### 6.2 Indexing Strategy

- `idx_todos_user_id_created`: (user_id, created_at DESC) — 목록 조회
- `idx_todos_user_id_due_date`: (user_id, due_date) — 일정 제안
- `idx_todos_search`: GIN(to_tsvector('korean', title || ' ' || description)) — 전문 검색

## 7. API Design

### 7.1 API Style
RESTful JSON API. 모든 요청/응답은 Pydantic 스키마로 검증.

### 7.2 Endpoint Structure

| Method | Path | Description |
|--------|------|-------------|
| POST | /api/auth/register | 회원가입 |
| POST | /api/auth/login | 로그인 → JWT 발급 |
| POST | /api/auth/refresh | 토큰 갱신 |
| GET | /api/todos | 할일 목록 (필터, 정렬, 페이지네이션) |
| POST | /api/todos | 할일 생성 (자연어 → AI 분류) |
| GET | /api/todos/{id} | 할일 상세 |
| PUT | /api/todos/{id} | 할일 수정 |
| DELETE | /api/todos/{id} | 할일 삭제 (소프트) |
| POST | /api/todos/{id}/complete | 완료 토글 |
| GET | /api/dashboard/summary | 대시보드 요약 |
| GET | /api/dashboard/weekly | 주간 차트 데이터 |
| GET | /api/ai/suggest-schedule | 오늘의 추천 순서 |

### 7.3 Error Handling

```json
{
  "detail": "Not found",
  "status_code": 404,
  "error_code": "TODO_NOT_FOUND"
}
```
표준 HTTP 상태 코드 + 커스텀 에러 코드.

## 8. Project Structure

```
taskflow/
├── frontend/
│   ├── src/
│   │   ├── app/              # Next.js App Router pages
│   │   ├── components/
│   │   │   ├── ui/           # shadcn/ui primitives
│   │   │   ├── todo/         # TodoList, TodoItem, TodoInput
│   │   │   └── dashboard/    # Charts, Summary
│   │   ├── lib/              # API client, utils
│   │   ├── stores/           # Zustand stores
│   │   └── types/            # TypeScript types
│   └── package.json
├── backend/
│   ├── app/
│   │   ├── api/              # Route handlers
│   │   │   ├── auth.py
│   │   │   ├── todos.py
│   │   │   └── dashboard.py
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Business logic
│   │   ├── ai/               # OpenAI integration
│   │   │   ├── classifier.py # 카테고리/우선순위 분류
│   │   │   ├── parser.py     # 자연어 파싱
│   │   │   └── scheduler.py  # 일정 제안
│   │   ├── core/             # Config, security, deps
│   │   └── main.py
│   ├── tests/
│   ├── alembic/              # DB migrations
│   └── requirements.txt
├── docker-compose.yml
├── Dockerfile
└── .github/workflows/ci.yml
```

## 9. Security Architecture

### 9.1 Authentication Flow
1. POST /auth/login → bcrypt 검증 → JWT access (30m) + refresh (7d) 발급
2. 모든 API 요청: Authorization: Bearer {access_token}
3. Access 만료 → POST /auth/refresh → 새 토큰 쌍 발급
4. Refresh 만료 → 재로그인

### 9.2 Data Protection
- 비밀번호: bcrypt (cost 12), 평문 절대 저장 금지
- API Key: 환경변수 (.env), AWS Secrets Manager
- HTTPS 전용, HSTS 헤더
- CORS: 프론트엔드 도메인만 허용

## 10. Infrastructure & DevOps

### 10.1 Environments

| Environment | Purpose | Configuration |
|------------|---------|---------------|
| Local | 개발 | Docker Compose (FastAPI + PostgreSQL) |
| Staging | QA/테스트 | AWS ECS + RDS (t3.micro) |
| Production | 서비스 | AWS ECS + RDS (t3.small), Auto Scaling |

### 10.2 Deployment Strategy
- GitHub Actions: PR → lint + test → staging 자동 배포
- main merge → production 배포 (수동 승인)
- Blue-Green 배포 (ECS rolling update)

### 10.3 Monitoring
- CloudWatch: API 지표, 에러율, 응답시간
- Sentry: 에러 추적 + 알림
- PostgreSQL: slow query log (100ms 이상)
""",
    },
    {
        "file_name": "epics.md",
        "file_path": "planning-artifacts/epics.md",
        "content": """---
stepsCompleted: [1,2,3,4]
inputDocuments: ['PRD.md', 'architecture.md']
workflowType: 'epics'
---
# Epics & Stories - TaskFlow

**Date:** 2026-03-21
**Status:** Complete

---

## Requirements Inventory

### Functional Requirements (from PRD)

| FR ID | Description | Priority | Epic |
|-------|------------|----------|------|
| FR-001~004 | 사용자 인증 (가입/로그인/로그아웃/토큰갱신) | Must | E-001 |
| FR-010~017 | 할일 CRUD + 완료 + 검색 | Must | E-002 |
| FR-020~024 | AI 자동 분류/우선순위/일정제안/파싱/수동수정 | Must | E-003 |
| FR-030~032 | 대시보드 (현황/주간차트/카테고리분포) | Must | E-004 |

## FR Coverage Map

| FR ID | Epic | Story | Status |
|-------|------|-------|--------|
| FR-001 | E-001 | S-001 | Covered |
| FR-002 | E-001 | S-002 | Covered |
| FR-003 | E-001 | S-002 | Covered |
| FR-004 | E-001 | S-002 | Covered |
| FR-010 | E-002 | S-003 | Covered |
| FR-011 | E-003 | S-006 | Covered |
| FR-012 | E-002 | S-003 | Covered |
| FR-013 | E-002 | S-003 | Covered |
| FR-014 | E-002 | S-004 | Covered |
| FR-015 | E-002 | S-004 | Covered |
| FR-016 | E-002 | S-004 | Covered |
| FR-020 | E-003 | S-005 | Covered |
| FR-021 | E-003 | S-005 | Covered |
| FR-022 | E-003 | S-007 | Covered |
| FR-023 | E-003 | S-006 | Covered |
| FR-024 | E-003 | S-005 | Covered |
| FR-030 | E-004 | S-008 | Covered |
| FR-031 | E-004 | S-008 | Covered |

---

## Epic 1: 사용자 인증 (E-001)
<!-- derived_from: PRD#FR-001, PRD#FR-002, PRD#FR-003, PRD#FR-004, ARCH#C-1 -->

**ID:** E-001 | **Priority:** Must | **Phase:** MVP | **Complexity:** S | **Dependencies:** None

### Description
이메일/비밀번호 기반 사용자 인증 시스템. JWT access + refresh 토큰, bcrypt 해싱.

### Stories

#### Story 1.1: 회원가입

**ID:** S-001 | **Points:** 3

**As a** 신규 사용자,
**I want** 이메일과 비밀번호로 회원가입을 하고 싶다,
**So that** TaskFlow 서비스를 이용할 수 있다.

**Acceptance Criteria:**

```gherkin
Given 회원가입 페이지에 접속한 상태에서
When 유효한 이메일과 비밀번호(8자 이상)를 입력하고 가입 버튼을 클릭하면
Then 계정이 생성되고 JWT 토큰이 발급되어 대시보드로 이동한다

Given 회원가입 페이지에서
When 이미 등록된 이메일로 가입을 시도하면
Then "이미 사용 중인 이메일입니다" 에러가 표시된다

Given 회원가입 페이지에서
When 8자 미만의 비밀번호를 입력하면
Then "비밀번호는 8자 이상이어야 합니다" 검증 에러가 표시된다
```

**Tasks:**
- [ ] POST /api/auth/register 엔드포인트 구현
- [ ] User SQLAlchemy 모델 생성 (id, email, hashed_password, display_name, created_at)
- [ ] Pydantic 스키마 (RegisterRequest, TokenResponse)
- [ ] bcrypt 해싱 유틸리티
- [ ] 프론트엔드 회원가입 폼 + 유효성 검증
- [ ] 단위 테스트 (중복 이메일, 짧은 비밀번호)

#### Story 1.2: 로그인 / 로그아웃 / 토큰 갱신

**ID:** S-002 | **Points:** 5

**As a** 기존 사용자,
**I want** 로그인하여 내 할일에 접근하고, 로그아웃하여 세션을 종료하고 싶다,
**So that** 안전하게 서비스를 이용할 수 있다.

**Acceptance Criteria:**

```gherkin
Given 로그인 페이지에서
When 올바른 이메일과 비밀번호를 입력하면
Then JWT access token(30분)과 refresh token(7일)이 발급되고 대시보드로 이동한다

Given 로그인된 상태에서
When 로그아웃 버튼을 클릭하면
Then 로컬 토큰이 삭제되고 로그인 페이지로 이동한다

Given access token이 만료된 상태에서
When API 요청을 보내면
Then refresh token으로 자동 갱신 후 원래 요청이 재시도된다
```

---

## Epic 2: 할일 CRUD (E-002)
<!-- derived_from: PRD#FR-010, PRD#FR-012, PRD#FR-013, PRD#FR-014, PRD#FR-015, PRD#FR-016, PRD#FR-017, ARCH#C-2 -->

**ID:** E-002 | **Priority:** Must | **Phase:** MVP | **Complexity:** M | **Dependencies:** E-001

### Description
할일의 생성, 조회, 수정, 삭제, 완료 처리 기본 기능. 소프트 삭제, 페이지네이션 포함.

### Stories

#### Story 2.1: 할일 생성 및 목록 조회

**ID:** S-003 | **Points:** 5

**As a** 로그인된 사용자,
**I want** 할일을 추가하고 목록에서 확인하고 싶다,
**So that** 해야 할 일을 체계적으로 관리할 수 있다.

**Acceptance Criteria:**

```gherkin
Given 대시보드에 접속한 상태에서
When 할일 입력창에 제목을 입력하고 추가 버튼을 클릭하면
Then 새 할일이 DB에 저장되고 목록에 즉시 표시된다

Given 할일이 20개 이상 등록된 상태에서
When 할일 목록 페이지에 접속하면
Then 페이지네이션이 적용되어 10개씩 표시된다
```

#### Story 2.2: 할일 수정, 삭제, 완료 토글

**ID:** S-004 | **Points:** 5

**As a** 사용자,
**I want** 할일을 수정하거나 삭제하거나 완료 처리하고 싶다,
**So that** 상황 변화에 맞게 관리할 수 있다.

**Acceptance Criteria:**

```gherkin
Given 할일이 존재하는 상태에서
When 체크박스를 클릭하면
Then 완료 상태로 변경되고 completed_at이 기록되며 취소선 애니메이션 표시

Given 방금 완료 처리한 상태에서
When 3초 내에 "되돌리기" 토스트를 클릭하면
Then 완료가 취소되고 미완료 상태로 복원된다

Given 할일을 삭제하면
When DB에서
Then is_deleted=true로 소프트 삭제되고 목록에서 제거된다
```

---

## Epic 3: AI 기능 (E-003)
<!-- derived_from: PRD#FR-011, PRD#FR-020, PRD#FR-021, PRD#FR-022, PRD#FR-023, PRD#FR-024, ARCH#C-3, ARCH#ADR-004 -->

**ID:** E-003 | **Priority:** Must | **Phase:** MVP | **Complexity:** L | **Dependencies:** E-002

### Description
OpenAI GPT-4o-mini를 활용한 자동 분류, 자연어 파싱, 스마트 일정 제안.

### Stories

#### Story 3.1: AI 자동 분류 + 수동 수정

**ID:** S-005 | **Points:** 8

**As a** 사용자,
**I want** 할일을 추가하면 AI가 자동으로 분류해주길 원한다,
**So that** 수동 분류의 번거로움 없이 체계적으로 관리할 수 있다.

**Acceptance Criteria:**

```gherkin
Given "분기 보고서 작성"을 입력하고
When 추가 버튼을 클릭하면
Then AI가 category="업무", priority="높음"으로 자동 지정하고 뱃지로 표시된다

Given AI가 분류한 결과에서
When 카테고리 뱃지를 클릭하면
Then 드롭다운으로 수동 변경 가능하다

Given OpenAI API 호출이 실패하면
When 할일을 생성하면
Then category="미분류", priority="보통"으로 기본값 적용 후 저장된다
```

**Tasks:**
- [ ] OpenAI client 래퍼 (ai/classifier.py)
- [ ] JSON response_format 프롬프트 설계
- [ ] 분류 결과 캐싱 (동일 텍스트 재분류 방지)
- [ ] 프론트엔드 분류 뱃지 + 수동 수정 드롭다운
- [ ] API 실패 시 폴백 로직
- [ ] 통합 테스트

#### Story 3.2: 자연어 할일 입력

**ID:** S-006 | **Points:** 5

**As a** 사용자,
**I want** "내일까지 보고서 작성"처럼 자연스럽게 입력하고 싶다,
**So that** 별도로 날짜를 설정하는 번거로움을 줄일 수 있다.

**Acceptance Criteria:**

```gherkin
Given 입력창에 "금요일까지 팀 미팅 자료 준비"를 입력하면
When 추가 버튼을 클릭하면
Then due_date=이번 주 금요일, title="팀 미팅 자료 준비"로 파싱된다

Given "다음 주 월요일 오후 2시 고객 미팅"을 입력하면
When 파싱되면
Then due_date=다음 주 월요일 14:00, title="고객 미팅"으로 파싱된다
```

#### Story 3.3: 스마트 일일 일정 제안

**ID:** S-007 | **Points:** 5

**As a** 사용자,
**I want** AI가 오늘 할 일의 최적 순서를 제안해주길 원한다,
**So that** "무엇부터 할까" 고민 시간을 줄일 수 있다.

**Acceptance Criteria:**

```gherkin
Given 오늘 마감인 할일이 5개 있는 상태에서
When 대시보드의 "오늘의 추천 순서"를 확인하면
Then AI가 우선순위와 마감 긴급도를 고려하여 정렬된 목록을 제안한다
```

---

## Epic 4: 대시보드 (E-004)
<!-- derived_from: PRD#FR-030, PRD#FR-031, PRD#FR-032, ARCH#C-4 -->

**ID:** E-004 | **Priority:** Must | **Phase:** MVP | **Complexity:** M | **Dependencies:** E-002

### Stories

#### Story 4.1: 대시보드 현황 및 차트

**ID:** S-008 | **Points:** 5

**Acceptance Criteria:**

```gherkin
Given 대시보드에 접속하면
When 페이지가 로드되면
Then 오늘 완료/전체 카운트 + 프로그레스 바 + 주간 완료율 라인 차트가 표시된다
```

---

## Summary

| Metric | Value |
|--------|-------|
| Total Epics | 4 |
| Total Stories | 8 |
| Total Story Points | 41 |
| Must-Have Points | 41 |
| Sprint 1 Target | E-001 + E-002 (18pt) |
| Sprint 2 Target | E-003 (18pt) |
| Sprint 3 Target | E-004 + 통합 테스트 (5pt+) |
""",
    },
    {
        "file_name": "project-context.md",
        "file_path": "planning-artifacts/project-context.md",
        "content": """---
workflowType: 'project-context'
---
# Project Context - TaskFlow

## Technology Stack & Versions

| Technology | Version | Purpose |
|-----------|---------|---------|
| Python | 3.12 | 백엔드 런타임 |
| FastAPI | 0.110+ | 비동기 웹 프레임워크 |
| SQLAlchemy | 2.x (async) | ORM |
| Alembic | 1.14+ | DB 마이그레이션 |
| PostgreSQL | 16.x | 데이터베이스 |
| Next.js | 14.x | 프론트엔드 프레임워크 |
| TypeScript | 5.x | 타입 안전성 |
| Tailwind CSS | 3.x | 유틸리티 퍼스트 CSS |
| shadcn/ui | latest | UI 컴포넌트 |
| Zustand | 4.x | 상태 관리 |
| Recharts | 2.x | 차트 라이브러리 |
| OpenAI SDK | 1.x | AI API 클라이언트 |
| Docker | latest | 컨테이너화 |
| AWS ECS | — | 컨테이너 오케스트레이션 |
| AWS RDS | — | 관리형 PostgreSQL |

## Critical Implementation Rules

1. **모든 API 응답은 Pydantic 스키마로 검증한다** — 프론트엔드 타입과 동기화. 스키마 없이 dict 반환 금지.
2. **AI 호출은 반드시 JSON response_format을 사용한다** — 파싱 실패를 방지하고 구조화된 출력 보장.
3. **AI 호출 실패 시 기본값 폴백** — category="미분류", priority="보통"으로 저장. 사용자 경험 중단 없음.
4. **비밀번호는 bcrypt (cost 12)로 해싱** — 평문 저장 절대 금지. verify_password()로만 비교.
5. **환경변수에 시크릿 저장** — API 키, DB 비밀번호 등을 코드/로그에 포함하지 않음.
6. **소프트 삭제를 기본으로** — is_deleted 또는 deleted_at 필드. 복구 가능성 유지.
7. **raw SQL 금지** — SQLAlchemy ORM만 사용. SQL Injection 방지.
8. **프론트엔드 상태는 Zustand** — React Context 사용 금지. store 파일 분리.

## Project Structure

```
taskflow/
├── frontend/
│   ├── src/
│   │   ├── app/              # Next.js App Router pages
│   │   ├── components/
│   │   │   ├── ui/           # shadcn/ui base components
│   │   │   ├── todo/         # TodoList, TodoItem, TodoInput, CategoryBadge
│   │   │   └── dashboard/    # SummaryCard, WeeklyChart, CategoryPie
│   │   ├── lib/              # api.ts (axios), utils.ts
│   │   ├── stores/           # authStore.ts, todoStore.ts
│   │   └── types/            # index.ts (all TypeScript interfaces)
│   ├── public/
│   └── package.json
├── backend/
│   ├── app/
│   │   ├── api/              # auth.py, todos.py, dashboard.py, ai_endpoints.py
│   │   ├── models/           # user.py, todo.py
│   │   ├── schemas/          # auth.py, todo.py, dashboard.py
│   │   ├── services/         # auth_service.py, todo_service.py, dashboard_service.py
│   │   ├── ai/               # classifier.py, parser.py, scheduler.py
│   │   ├── core/             # config.py, security.py, dependencies.py, exceptions.py
│   │   ├── database.py
│   │   └── main.py
│   ├── tests/
│   │   ├── test_auth.py
│   │   ├── test_todos.py
│   │   └── test_ai.py
│   ├── alembic/
│   └── requirements.txt
├── docker-compose.yml
├── Dockerfile
└── .github/workflows/ci.yml
```

## Development Conventions

### Naming Conventions
- **Python:** snake_case (변수, 함수), PascalCase (클래스, Pydantic 모델)
- **TypeScript:** camelCase (변수, 함수), PascalCase (컴포넌트, 타입/인터페이스)
- **파일명:** snake_case (Python), kebab-case (컴포넌트)
- **API 경로:** kebab-case, 복수형 (/api/todos, /api/auth/login)
- **DB 테이블:** snake_case, 복수형 (users, todos)

### Code Style
- Python: Ruff formatter + linter (line length 120)
- TypeScript: ESLint + Prettier (semi: true, singleQuote: false)
- 커밋 메시지: Conventional Commits (feat:, fix:, docs:, refactor:, test:)

### Git Workflow
- `main`: 프로덕션 배포 브랜치 (protected)
- `develop`: 개발 통합 브랜치
- `feature/*`: 기능 브랜치 (develop에서 분기)
- PR 리뷰 필수, CI 통과 후 Squash Merge

### Testing Strategy
- 백엔드: pytest + pytest-asyncio (단위 + 통합)
- 프론트엔드: Vitest + React Testing Library
- 커버리지 목표: 80% 이상
- AI 모듈: mock 기반 테스트 (실제 API 호출 금지)

## Environment Setup

### Prerequisites
- Python 3.12+
- Node.js 20+ (LTS)
- PostgreSQL 16+ (또는 Docker)
- OpenAI API Key

### Configuration (.env)
```
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/taskflow
SECRET_KEY=your-jwt-secret-key
OPENAI_API_KEY=sk-...
CORS_ORIGINS=http://localhost:3000
```

### Running Locally
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev  # http://localhost:3000
```
""",
    },
    {
        "file_name": "sprint-status.md",
        "file_path": "implementation-artifacts/sprint-status.md",
        "content": """---
workflowType: 'sprint-status'
---
# Sprint Status - TaskFlow

## Status Definitions

### Epic Status
- **backlog** — Not yet started
- **in-progress** — At least one story is in progress
- **done** — All stories completed

### Story Status
- **backlog** — Not yet started
- **ready-for-dev** — Detailed, estimated, and ready for implementation
- **in-progress** — Currently being implemented
- **review** — Implementation complete, awaiting review
- **done** — Reviewed and accepted

## Development Status

```yaml
development_status:
  # Epic E-001: 사용자 인증
  e-001:
    status: backlog
    stories:
      s-001:  # 회원가입 (3pt)
        status: ready-for-dev
      s-002:  # 로그인/로그아웃/토큰갱신 (5pt)
        status: ready-for-dev
    retrospective:
      status: optional

  # Epic E-002: 할일 CRUD
  e-002:
    status: backlog
    stories:
      s-003:  # 할일 생성 및 목록 조회 (5pt)
        status: ready-for-dev
      s-004:  # 할일 수정, 삭제, 완료 토글 (5pt)
        status: ready-for-dev
    retrospective:
      status: optional

  # Epic E-003: AI 기능
  e-003:
    status: backlog
    stories:
      s-005:  # AI 자동 분류 + 수동 수정 (8pt)
        status: backlog
      s-006:  # 자연어 할일 입력 (5pt)
        status: backlog
      s-007:  # 스마트 일일 일정 제안 (5pt)
        status: backlog
    retrospective:
      status: optional

  # Epic E-004: 대시보드
  e-004:
    status: backlog
    stories:
      s-008:  # 대시보드 현황 및 차트 (5pt)
        status: backlog
    retrospective:
      status: optional
```

## Sprint Plan

### Sprint 1 (Week 1-2)
**Goal:** 인증 + 할일 기본 CRUD
**Stories:** S-001 (3pt), S-002 (5pt), S-003 (5pt), S-004 (5pt)
**Total:** 18pt

### Sprint 2 (Week 3-4)
**Goal:** AI 기능 전체
**Stories:** S-005 (8pt), S-006 (5pt), S-007 (5pt)
**Total:** 18pt

### Sprint 3 (Week 5-6)
**Goal:** 대시보드 + 통합 테스트 + 배포
**Stories:** S-008 (5pt) + QA + 배포
**Total:** 5pt+

## Sprint Summary

| Metric | Value |
|--------|-------|
| Current Sprint | Sprint 1 |
| Sprint Goal | 인증 + 할일 기본 CRUD |
| Total Points | 41 |
| Completed Points | 0 |
| In Progress Points | 0 |
| Remaining Points | 41 |

## Blockers

| Story | Blocker | Status |
|-------|---------|--------|
| - | 없음 | - |
""",
    },
    # --- P1 Construction artifacts ------------------------------------------
    {
        "file_name": "tech-stack.yaml",
        "file_path": "context/tech-stack/tech-stack.yaml",
        "content": """# ===== TaskFlow 기술 스택 =====
# Construction 워크플로우(코드 스캐폴딩, 테스트, CI, IaC)가 항상 우선 참조합니다.

language: "Python 3.12 + TypeScript 5.4"

frameworks:
  backend: "FastAPI 0.115"
  frontend: "Next.js 14 (App Router)"
  mobile: ""

datastores:
  primary_db: "PostgreSQL 16 (AWS RDS)"
  cache: "Redis 7 (ElastiCache)"
  search: "PostgreSQL tsvector"
  object_store: "S3 (정적 자산)"

messaging: ""

cloud:
  provider: "aws"
  regions: ["ap-northeast-2"]
  managed_services: ["ECS Fargate", "RDS", "ElastiCache", "ALB", "CloudFront"]

auth:
  provider: "self-hosted JWT"
  protocols: ["OAuth2 (planned)", "JWT (Bearer)"]

observability:
  logs: "CloudWatch Logs"
  metrics: "CloudWatch Metrics"
  traces: "AWS X-Ray (planned)"

cicd:
  vendor: "github-actions"
  artifact_registry: "Amazon ECR"

testing:
  unit: "pytest (backend), Vitest (frontend)"
  integration: "pytest + httpx"
  e2e: "Playwright"
  coverage_min: 70

conventions:
  style_guide: "PEP8 (backend), Airbnb TS (frontend)"
  linter: "ruff, eslint"
  formatter: "black, prettier"

security:
  secret_store: "AWS Secrets Manager"
  scanning: ["SCA: Dependabot", "SAST: Semgrep", "container scan: Trivy"]

licenses:
  allow: ["MIT", "Apache-2.0", "BSD-3-Clause", "ISC"]
  deny: ["GPL-3.0", "AGPL-3.0"]
""",
    },
    {
        "file_name": "E1-S1-skeleton.md",
        "file_path": "construction-artifacts/E1-S1-skeleton.md",
        "content": """---
storyId: 'E1-S1'
workflowType: 'code-skeleton'
date: '2026-03-21'
---
# Code Skeleton — 회원가입 (E1-S1)

<!-- derived_from: STORY#E1-S1, ARCH#C-1 -->

**Story:** E1-S1 — 회원가입
**Date:** 2026-03-21
**Status:** Draft

---

## 1. Affected File Tree

```
taskflow/backend/
├── app/
│   ├── api/
│   │   └── auth.py                         # MODIFIED — POST /api/auth/register 추가
│   ├── models/
│   │   └── user.py                         # NEW — User SQLAlchemy 모델
│   ├── schemas/
│   │   └── auth.py                         # NEW — RegisterRequest / TokenResponse
│   ├── services/
│   │   └── auth_service.py                 # NEW — bcrypt 해싱 + 가입 로직
│   └── core/
│       └── security.py                     # MODIFIED — bcrypt 유틸 추가
└── tests/
    └── test_auth_register.py               # NEW — 회원가입 단위/통합 테스트
```

## 2. Module Signatures

### app/models/user.py
<!-- derived_from: ARCH#C-1 -->

```python
# Purpose: User 테이블 정의
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(Text, nullable=False)
    display_name: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    # TODO(E1-S1:SC1): bcrypt cost factor 12 사용
```

### app/schemas/auth.py

```python
class RegisterRequest(BaseModel):
    email: EmailStr
    password: constr(min_length=8)            # TODO(E1-S1:SC3): 8자 미만 검증
    display_name: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
```

### app/services/auth_service.py

```python
async def register_user(db: AsyncSession, req: RegisterRequest) -> User:
    # TODO(E1-S1:SC2): 중복 이메일 체크 → ConflictError 발생
    # TODO(E1-S1:SC1): bcrypt 해싱 후 User 생성
    # TODO(E1-S1:SC1): JWT access(30m) + refresh(7d) 발급
    raise NotImplementedError()
```

### app/api/auth.py

```python
@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(req: RegisterRequest, db: AsyncSession = Depends(get_db)):
    # TODO(E1-S1:SC1): register_user 호출 → 토큰 응답
    raise NotImplementedError()
```

## 3. BDD Scenario → Signature Map

| Scenario ID | Scenario | Signature that covers it |
|-------------|----------|--------------------------|
| E1-S1-SC1 | 정상 회원가입 + 토큰 발급 | `auth_service.register_user` + `api/auth.register` |
| E1-S1-SC2 | 중복 이메일 거부 | `auth_service.register_user` (ConflictError) |
| E1-S1-SC3 | 8자 미만 비밀번호 거부 | `schemas/auth.RegisterRequest.password` validator |

## 4. Out-of-Scope Notes

- 소셜 로그인은 별도 Story에서 다룹니다 (Should-Have).
- 이메일 인증 메일 발송은 MVP 범위 밖.

## 5. Next Steps

- [ ] Hand off to QA (Quinn) for E1-S1 test plan.
- [ ] Implement TODOs in BDD scenario priority order (SC1 → SC3 → SC2).
""",
    },
    {
        "file_name": "E1-S1-test-plan.md",
        "file_path": "construction-artifacts/E1-S1-test-plan.md",
        "content": """---
storyId: 'E1-S1'
workflowType: 'test-plan'
date: '2026-03-21'
---
# Test Plan — 회원가입 (E1-S1)

<!-- derived_from: STORY#E1-S1 -->

**Story:** E1-S1 — 회원가입
**Date:** 2026-03-21
**Status:** Draft

---

## 1. Scenario Inventory

| Scenario ID | BDD Summary | Source |
|-------------|-------------|--------|
| E1-S1-SC1 | 유효 입력 → 201 + JWT 발급 | Story §3 (Acceptance Criteria #1) |
| E1-S1-SC2 | 중복 이메일 → 409 | Story §3 (Acceptance Criteria #2) |
| E1-S1-SC3 | 8자 미만 비밀번호 → 422 | Story §3 (Acceptance Criteria #3) |

## 2. Test Matrix

| Test ID | Scenario | Level | Rationale | Input | Expected |
|---------|----------|-------|-----------|-------|----------|
| T-001 | E1-S1-SC1 | unit | bcrypt 해싱은 순수 로직 | `RegisterRequest("a@b.com", "password1", "Alice")` | `User.hashed_password != "password1"` |
| T-002 | E1-S1-SC1 | integration | DB 저장 + 토큰 발급 검증 | 동일 | 201, body에 access/refresh token |
| T-003 | E1-S1-SC2 | integration | 두 번째 호출에서 충돌 | 같은 이메일 2회 호출 | 두 번째 호출 409, error_code=USER_EXISTS |
| T-004 | E1-S1-SC3 | unit | Pydantic 검증 | `password="short"` | 422, validation_error "min_length" |
| T-005 | E1-S1-SC1-NEG1 | integration | XSS payload 거부 | display_name="<script>" | 가입은 성공, but 응답에서 escaped |
| T-006 | E1-S1-SC2-NEG1 | unit | 대소문자 다른 이메일 | "A@B.com" 후 "a@b.com" | 두 번째 호출 409 (대소문자 무시) |

## 3. Fixtures & Seed Data

| Name | Shape | Purpose | Scope |
|------|-------|---------|-------|
| `valid_register_payload` | dict | 정상 입력 베이스 | per-test |
| `existing_user` | User row | 충돌 시나리오용 사전 등록 | per-test (트랜잭션 롤백) |

## 4. Mocks & Stubs

| Interface | Strategy | Reset Point |
|-----------|----------|-------------|
| `bcrypt.hashpw` | real (no mock) | — |
| Email sending (future) | stub | per-suite |

## 5. Risk & Coverage Notes

### Untested Risks
- Rate limiting (브루트 포스 방어)는 별도 Story로 다룸.
- 비밀번호 강도 검증은 8자 길이만 체크 (사전 단어, 흔한 패턴 미검증).

### Flaky Test Risks
- bcrypt 해싱이 cost=12에서 ~250ms 소요 → 통합 테스트는 cost=4로 override (테스트 전용).

### Follow-up Tests
- 비밀번호 정책 강화 후 재테스트 필요.
- 동시 가입 race condition (UNIQUE constraint 신뢰).

## 6. Tooling

| Tool | Purpose | Notes |
|------|---------|-------|
| pytest + pytest-asyncio | 단위/통합 | async fixture |
| httpx.AsyncClient | API 통합 | 인메모리 ASGI |
| factory-boy | User/입력 팩토리 | optional |

## 7. Next Steps

- [ ] Developer (Dex)와 fixture 인터페이스 합의.
- [ ] 첫 개발 후 T-001~T-004 100% 통과 → Story 완료 게이트.
""",
    },
    {
        "file_name": "ci-pipeline.yaml",
        "file_path": "construction-artifacts/ci-pipeline.yaml",
        "content": """# ===== TaskFlow CI/CD Pipeline (vendor-neutral) =====
# derived_from: ARCH#C-1, ARCH#C-5
# Target vendor: github-actions
# Cloud target: aws

metadata:
  project: "TaskFlow"
  owners: ["taskflow-team"]
  version: "1.0"
  last_updated: "2026-03-21"

triggers:
  - event: push
    branches: [main]
    runs_stages: [build, lint, test, security-scan, package, deploy-staging]
  - event: pull_request
    runs_stages: [build, lint, test, security-scan]
  - event: tag
    pattern: "v*"
    runs_stages: [build, lint, test, security-scan, package, deploy-prod]

environments:
  - name: dev
    auto_deploy: true
  - name: staging
    auto_deploy: true
    requires: [dev]
  - name: prod
    auto_deploy: false
    requires: [staging]
    approval: manual

stages:
  - id: build
    runs_on: "linux"
    steps:
      - checkout
      - setup_toolchain: { language: "python", version: "3.12" }
      - setup_toolchain: { language: "node", version: "20" }
      - install_deps
      - compile
    success_criteria: "exit 0"
    on_failure: "block merge"
    artifacts: ["frontend/.next/", "backend/dist/"]

  - id: lint
    depends_on: [build]
    steps:
      - run: "ruff check backend/"
      - run: "npx eslint frontend/"
    on_failure: "block merge"

  - id: test
    depends_on: [build]
    steps:
      - run: "pytest backend/tests/ --cov=app --cov-report=xml"
      - run: "npx vitest run frontend/"
    success_criteria: "exit 0 AND coverage >= 70%"
    on_failure: "block merge"
    artifacts: ["coverage.xml"]

  - id: security-scan
    depends_on: [build]
    steps:
      - sca_scan: "Dependabot"
      - sast_scan: "Semgrep"
      - container_scan: "Trivy"
    success_criteria: "no HIGH or CRITICAL findings"
    on_failure: "block merge"

  - id: package
    depends_on: [test, security-scan]
    steps:
      - build_image: "taskflow-api:${{ github.sha }}"
      - push_image:
          registry: "${{ secrets.ECR_URL }}"

  - id: deploy-staging
    depends_on: [package]
    when: "branch == main"
    steps:
      - deploy: { env: staging, image: "taskflow-api:${{ github.sha }}" }
      - smoke_test: "/health"
    on_failure: "rollback to previous task definition"

  - id: deploy-prod
    depends_on: [deploy-staging]
    when: "tag matches v*"
    approval: manual
    steps:
      - deploy: { env: prod, image: "taskflow-api:${{ github.sha }}" }
      - smoke_test: "/health"
      - announce: "#release"
    on_failure: "rollback + page oncall"

quality_gates:
  coverage_line_min: 70
  coverage_branch_min: 60
  security_fail_on: ["HIGH", "CRITICAL"]
  required_reviews: 1

secrets:
  - name: ECR_URL
    used_by: [package]
  - name: AWS_DEPLOY_ROLE_ARN
    used_by: [deploy-staging, deploy-prod]
  - name: OPENAI_API_KEY
    used_by: [deploy-staging, deploy-prod]

rollback:
  strategy: previous-task-definition
  trigger: smoke-test-failure
  window_minutes: 5
""",
    },
    {
        "file_name": "iac.yaml",
        "file_path": "construction-artifacts/iac.yaml",
        "content": """# ===== TaskFlow Infrastructure-as-Code (vendor-neutral) =====
# derived_from: ARCH#C-1, ARCH#C-2, ARCH#C-3, ARCH#C-4
# Cloud target: aws

metadata:
  project: "TaskFlow"
  version: "1.0"
  last_updated: "2026-03-21"
  cloud: "aws"

environments:
  - name: dev
  - name: staging
  - name: prod

network:
  vpcs:
    - id: taskflow-vpc
      cidr: "10.0.0.0/16"
      envs: [dev, staging, prod]

  subnets:
    - id: public-subnet-a
      vpc: taskflow-vpc
      cidr: "10.0.1.0/24"
      public: true
    - id: public-subnet-b
      vpc: taskflow-vpc
      cidr: "10.0.2.0/24"
      public: true
    - id: private-subnet-a
      vpc: taskflow-vpc
      cidr: "10.0.10.0/24"
      public: false
    - id: private-subnet-b
      vpc: taskflow-vpc
      cidr: "10.0.11.0/24"
      public: false

  security_groups:
    - id: sg-alb
      vpc: taskflow-vpc
      rules:
        - { direction: ingress, protocol: tcp, ports: [443], source: "0.0.0.0/0" }
        - { direction: egress,  protocol: tcp, ports: [all], target: "0.0.0.0/0" }
    - id: sg-ecs
      vpc: taskflow-vpc
      rules:
        - { direction: ingress, protocol: tcp, ports: [8000], source_sg: "sg-alb" }
        - { direction: egress,  protocol: tcp, ports: [all],  target: "0.0.0.0/0" }
    - id: sg-rds
      vpc: taskflow-vpc
      rules:
        - { direction: ingress, protocol: tcp, ports: [5432], source_sg: "sg-ecs" }

resources:
  # derived_from: ARCH#C-1, ARCH#C-2, ARCH#C-3, ARCH#C-4
  - id: api-service
    type: container
    component: C-1
    image: "${{ secrets.ECR_URL }}/taskflow-api:${{ tag }}"
    cpu: 0.5
    memory_mb: 1024
    env:
      ENV: "${{ env }}"
      DB_HOST: "${{ resources.primary-db.endpoint }}"
      DB_PASSWORD: "${{ secrets.DB_PASSWORD }}"
      OPENAI_API_KEY: "${{ secrets.OPENAI_API_KEY }}"
    networks:
      - subnet: private-subnet-a
        security_group: sg-ecs
    depends_on: [primary-db, cache]
    scaling:
      min: 2
      max: 8
      target_cpu_percent: 60

  # derived_from: ARCH#ADR-003
  - id: primary-db
    type: managed-database
    component: C-2
    engine: postgres
    version: "16"
    storage_gb: 50
    backup_retention_days: 7
    multi_az: true
    subnet_group: [private-subnet-a, private-subnet-b]
    security_group: sg-rds

  - id: cache
    type: managed-cache
    engine: redis
    version: "7"
    node_type: "cache.t3.micro"
    subnet_group: [private-subnet-a, private-subnet-b]

  - id: alb
    type: load-balancer
    component: C-1
    listeners:
      - { protocol: HTTPS, port: 443, target: api-service }
    security_group: sg-alb
    subnets: [public-subnet-a, public-subnet-b]

  - id: cdn
    type: cdn
    component: C-5
    origin: alb
    cache_behaviors:
      - { path: "/_next/static/*", ttl_seconds: 86400 }

identity:
  service_accounts:
    - id: api-runtime
      used_by: [api-service]
      permissions:
        - "secretsmanager:GetSecretValue"
        - "logs:CreateLogStream"
        - "logs:PutLogEvents"
        - "s3:GetObject:taskflow-static/*"

secrets:
  - name: DB_PASSWORD
    used_by: [api-service]
    store: "secretsmanager"
    rotation_days: 90
  - name: OPENAI_API_KEY
    used_by: [api-service]
    store: "secretsmanager"
    rotation_days: 180
  - name: ECR_URL
    used_by: [api-service]

config:
  dev:
    LOG_LEVEL: debug
    OPENAI_MODEL: gpt-4o-mini
  staging:
    LOG_LEVEL: info
    OPENAI_MODEL: gpt-4o-mini
  prod:
    LOG_LEVEL: warn
    OPENAI_MODEL: gpt-4o-mini

outputs:
  - name: api_url
    value: "${{ resources.alb.dns_name }}"
  - name: cdn_url
    value: "${{ resources.cdn.domain_name }}"
""",
    },
]
