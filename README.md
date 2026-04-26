# Spec Studio

**한국어** | [English](./README.en.md)

**SDD(Spec-Driven Development) 기반 Enterprise AI-Driven Development 웹 서비스**

소프트웨어 개발의 전체 Spec lifecycle을 AI와 함께 체계적으로 관리하는 협업 플랫폼입니다. 기획부터 구현·검증·운영 준비까지를 하나의 워크스페이스에서 추적합니다.

---

## 비전

**Spec-Driven Development(SDD)** 를 핵심 방법론으로, AI가 분석·기획·설계·구현 전 단계의 산출물(Spec)을 주도적으로 생성·연결·검증하는 **Enterprise AI-Driven Development** 서비스를 목표로 합니다.

다음의 업계 선행 방법론을 참고·통합하여 설계되었습니다:

| 참고 방법론 | 핵심 차용 요소 |
|------------|---------------|
| **BMad Method V6** | AI 페르소나 기반 워크플로우, 단계별 아티팩트 생성 체계 |
| **GSD (Get Shit Done)** | Goal-Backward 분해, atomic 변경 추적, fresh-context subagent |
| **AWS AI-DLC** | Inception → Construction → Operations 3-Phase, "Bolt" 단위 실행, human-in-the-loop |

이들을 종합하여 **"Spec이 곧 개발의 출발점이자 품질 기준"** 이 되는 SDD 패러다임을 웹 환경에서 실현합니다.

---

## 핵심 가치

- **Spec → Code 추적성** — PRD의 모든 FR/NFR이 Architecture·UX·Story·코드 스캐폴딩까지 단방향 그래프로 연결되고 시각화됩니다.
- **9 AI 페르소나 협업** — Analyst, PM, Architect, UX Designer, Scrum Master, Tech Writer + Construction 3종(Developer, QA Engineer, DevOps Engineer)이 단계별로 협력합니다.
- **Inception → Construction 라이프사이클** — 기존 기획·설계 산출물에 더해 코드 스캐폴딩, 테스트 플랜, CI/CD, IaC 산출물까지 동일한 워크플로우 흐름에서 생성합니다.
- **Bolt 단위 실행** — Sprint를 1~3시간짜리 "Bolt"로 자동 분해하고 시작/완료/승인 라이프사이클과 활동 로그를 추적합니다.
- **Multi-Agent Orchestration** — 격리된 컨텍스트의 subagent들이 병렬로 산출물을 검토 후 종합 결과를 제공합니다 (메인 채팅 토큰 무영향).
- **Spec Health Score** — 6개 룰 엔진이 산출물 저장 시 자동으로 일관성을 검증하고 0~100점으로 가시화합니다.
- **다중 사용자 실시간 협업** — WebSocket 기반 실시간 채팅, 산출물 자동 저장, 버전 관리.
- **멀티 LLM 프로바이더** — OpenAI, Anthropic, Google, Ollama, Dify 등.

---

## 주요 기능

### SDD 워크플로우 (12종)

**Inception Phase**
- Create Brief, Create PRD, Validate PRD, Create UX Design, Create Architecture
- **Goal-Backward Analysis** — 목표를 검증 가능한 전제조건으로 역분해하고 PRD FR로 매핑

**Implementation Phase**
- Create Epics, Sprint Planning, Create Story

**Construction Phase**
- **Generate Code Skeleton** — Story → 디렉토리 트리 + 함수 시그니처 + BDD 시나리오에 묶인 TODO
- **Create Test Plan** — BDD → 단위/통합/E2E 분류 매트릭스 + 부정 케이스 + 픽스처
- **Design CI Pipeline** — 벤더 중립 YAML (트리거, 스테이지, 품질 게이트, 롤백)
- **Create IaC** — 벤더 중립 IaC 스케치 (네트워크/리소스/시크릿/환경)

**A/P/R/C 메뉴**: Advanced Elicitation · Party Mode · Propose Mode · Continue

### Goal-Backward Traceability

- 산출물 헤더에 stable anchor ID(`FR-001`, `C-1`, `ADR-001`, `UF-001`, `E1-S3` 등) 자동 부여
- `<!-- derived_from: PRD#FR-001, ARCH#C-1 -->` 마커로 산출물 간 파생 관계 선언
- 파일 저장 시 traceability 그래프 자동 재구축 (fire-and-forget)
- `Traceability` 페이지에서 ReactFlow 그래프 + orphan anchor 패널
- 단일 파일 LLM Suggest 버튼으로 추가 링크 추론

### Bolt Mode (단기 실행 사이클)

- Sprint Status를 LLM이 1~3시간짜리 Bolt로 자동 분해 (Story당 skeleton + test plan)
- 5단계 칸반: To Do · In Bolt · Awaiting Approval · Done · Blocked
- 단일 활성 Bolt 강제 (병렬 작업 방지)
- 시작/완료/승인/블록 모든 이벤트가 `bolt_activities`에 append-only 기록
- 활성 Bolt 상태에서 발생한 모든 파일 저장이 Bolt 활동에 자동 연결
- 7일 velocity 카운터

### Multi-Agent Orchestration

- 시나리오 기반 병렬 subagent 실행 (예: PRD Review = PM·Architect·UX·Analyst 4관점)
- 각 subagent는 fresh 시스템 프롬프트 + 격리된 컨텍스트 → 메인 채팅 토큰 사용량 영향 없음
- Critical/Major/Minor 분류 + 상충 의견 + 권장 액션으로 Synthesis 자동 생성
- 60초 개별 / 90초 전체 타임아웃, 부분 실패 허용

### Spec Validation Engine

- 6 룰 (5 결정적 + 1 LLM):
  - `fr_covered_by_story` (error) — 모든 PRD FR이 Story에 의해 커버되는지
  - `nfr_referenced_in_architecture` (warning) — NFR이 Architecture 컴포넌트에 참조되는지
  - `ux_flow_aligned_with_journey` (warning) — UX User Flow가 PRD User Journey에 연결되는지
  - `orphan_anchor` (info) — 어디에도 연결되지 않은 앵커
  - `estimation_sanity` (info) — Story points 합 vs Epic 복잡도
  - `contradictory_terms` (info, LLM) — PRD/Architecture 간 모순 탐지
- 파일 저장 시 자동 재실행 (룰 기반만, LLM 룰은 수동 트리거)
- Issue diff: 재실행 시 동일 fingerprint는 유지, 사라진 fingerprint는 자동 `resolved`
- **Spec Health Score** 0~100 (error=15·warning=4·info=1 가중치)
- 이슈별 Acknowledge / Resolve / Suppress 액션

### 컨텍스트 확장

- **System Architecture Modeling** — Xyflow 기반 시각 에디터 + AS-IS/To-Be YAML 관리
- **Tech Stack** — 언어/프레임워크/DB/클라우드/CI/보안 정책 YAML 선언, Construction 워크플로우가 항상 우선 참조

### 아티팩트 관리

- Markdown 파일 생성/편집/삭제, 드래그 앤 드롭 이동/이름 변경
- BMad 템플릿 기반 자동 생성
- 버전 관리 (YYMMDD_HHMMSS, 수정자 추적, Diff 비교, 복구)
- 디렉토리 그룹화: `planning-artifacts/`, `implementation-artifacts/`, `construction-artifacts/`, `context/`
- 전체 다운로드 (ZIP)
- 3종 샘플 프로젝트 (P0 anchor + P1 Construction 산출물 포함)

### 채팅 & AI

- WebSocket 기반 실시간 스트리밍 응답
- 페르소나별 시스템 프롬프트 + 우선순위 기반 프로젝트 컨텍스트 자동 로드 (60K 문자 예산, Context Expansion 별도 20K)
- A/P/R/C 퀵 액션, Party Mode, Propose Mode
- SAVE_FILE 마커 기반 채팅 내 아티팩트 자동 저장
- Story / Code Skeleton / Test Plan은 동적 파일명(`E{n}-S{n}-...`) 자동 처리

### 프로젝트 관리

- 프로젝트 생성/수정/삭제, Phase 관리
- 멤버 초대 및 역할 (Owner/Member)
- 활동 내역 피드

### 관리자 백오피스

- 접속 이력, 사용자 관리, 프로젝트 관리, LLM API 설정, Guide 페이지 관리

### UI/UX

- 한국어/영어 다국어
- 접기/펼치기 사이드바 (9 메뉴: Overview · Chat · Artifacts · Traceability · Validation · Bolts · Orchestrate · Context · Members · Settings)

---

## 기술 스택

### Frontend
| 기술 | 버전 | 용도 |
|------|------|------|
| Next.js | 14.x | React 프레임워크 (App Router) |
| TypeScript | 5.x | 타입 안전성 |
| Tailwind CSS | 3.x | 유틸리티 CSS |
| Zustand | 5.x | 상태 관리 |
| React Query | 5.x | 서버 상태 관리 |
| Axios | 1.x | HTTP 클라이언트 |
| @uiw/react-md-editor | 4.x | Markdown 에디터 |
| @xyflow/react | 12.x | 다이어그램 (System Architecture, Traceability Graph) |
| Sonner | 2.x | 토스트 알림 |
| Lucide React | — | 아이콘 |

### Backend
| 기술 | 버전 | 용도 |
|------|------|------|
| Python | 3.12+ | 런타임 |
| FastAPI | 0.115+ | 비동기 웹 프레임워크 |
| SQLAlchemy | 2.x (async) | ORM |
| SQLite / PostgreSQL | — | 데이터베이스 |
| Alembic | 1.14+ | DB 마이그레이션 |
| LiteLLM | 1.55+ | 멀티 LLM 프로바이더 |
| PyJWT | 2.x | JWT 인증 |
| bcrypt | 4.x | 비밀번호 해싱 |
| WebSockets | 14.x | 실시간 통신 |
| Uvicorn | 0.34+ | ASGI 서버 |

---

## 프로젝트 구조

```
Web_BMad01/
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── (auth)/                    # 로그인/회원가입
│   │   │   └── (app)/                     # 인증 필요 라우트
│   │   │       └── projects/[projectId]/
│   │   │           ├── (overview)/
│   │   │           ├── chat/
│   │   │           ├── files/
│   │   │           ├── traceability/      # P0 Goal-Backward 그래프
│   │   │           ├── validation/        # P4 Spec Health + 이슈
│   │   │           ├── bolts/             # P2 Bolt 칸반
│   │   │           ├── orchestrate/       # P3 Multi-Agent
│   │   │           ├── context/
│   │   │           ├── members/
│   │   │           └── settings/
│   │   ├── components/
│   │   │   ├── chat/                      # ChatWindow, PersonaSelector
│   │   │   ├── files/                     # FileTree, FileViewer, DiffView
│   │   │   │   ├── TraceGraph.tsx         # P0 ReactFlow 그래프
│   │   │   │   └── TracePanel.tsx
│   │   │   ├── bolts/BoltCard.tsx         # P2
│   │   │   ├── orchestrate/OrchestratePanel.tsx  # P3
│   │   │   ├── validation/                # P4
│   │   │   │   ├── SpecHealthScore.tsx
│   │   │   │   └── IssueList.tsx
│   │   │   ├── context/SystemDrawingCanvas.tsx
│   │   │   ├── layout/
│   │   │   ├── editor/
│   │   │   └── ui/
│   │   ├── lib/                           # API, i18n, WebSocket
│   │   ├── stores/                        # Zustand
│   │   └── types/
│   └── package.json
│
├── backend/
│   ├── app/
│   │   ├── api/                           # REST 엔드포인트
│   │   │   ├── traceability.py            # P0
│   │   │   ├── bolts.py                   # P2
│   │   │   ├── orchestrate.py             # P3
│   │   │   ├── validation.py              # P4
│   │   │   └── ... (auth, files, chat, context, ...)
│   │   ├── models/
│   │   │   ├── traceability_link.py       # P0
│   │   │   ├── bolt.py                    # P2 (Bolt + BoltActivity)
│   │   │   ├── validation.py              # P4 (Run + Issue)
│   │   │   └── ... (user, project, file, ...)
│   │   ├── schemas/
│   │   ├── services/
│   │   │   ├── traceability_service.py    # P0 anchor 추출 + LLM suggest
│   │   │   ├── bolt_service.py            # P2 plan/state-machine
│   │   │   ├── validation/                # P4 룰 프레임워크
│   │   │   │   ├── base.py
│   │   │   │   ├── registry.py
│   │   │   │   └── rules/                 # 6개 룰
│   │   │   ├── validation_service.py      # P4 orchestration + diff
│   │   │   ├── samples/                   # 샘플 아티팩트 데이터
│   │   │   └── ... (file_service, context_service, ...)
│   │   ├── llm/
│   │   │   ├── prompt_builder.py          # 시스템 프롬프트 + Anchor 컨벤션
│   │   │   ├── context_builder.py         # 우선순위 기반 컨텍스트 로드
│   │   │   ├── orchestrator.py            # P3 SubAgent + run_parallel
│   │   │   └── provider.py
│   │   ├── bmad/                          # 페르소나/워크플로우/템플릿 메타
│   │   └── core/                          # 보안, 의존성, 예외
│   ├── bmad_data/
│   │   ├── personas/                      # 9개 (Analyst·PM·Architect·UX·SM·TW·Developer·QA·DevOps)
│   │   ├── workflows/                     # 13개 (12 워크플로우 + goal-backward)
│   │   └── templates/                     # 12개 (기존 8 + code-skeleton·test-plan·ci-pipeline·iac)
│   ├── test_p0_p4_integration.py          # P0~P4 통합 회귀 테스트
│   ├── requirements.txt
│   └── .env.example
│
└── README.md
```

---

## 설치 및 실행

### 사전 요구 사항
- **Node.js** 20+ (LTS)
- **Python** 3.12+
- **LLM API Key** (OpenAI, Anthropic, Google 등 중 하나)

### 1. 저장소 클론

```bash
git clone https://github.com/extox/Spec-Studio.git
cd Spec-Studio
```

### 2. 백엔드 설정

```bash
cd backend

# 가상환경 생성 및 활성화
python3 -m venv .venv

# macOS/Linux:
source .venv/bin/activate

# Windows PowerShell:
# .venv\Scripts\Activate.ps1
# (실행 정책 오류 시: Set-ExecutionPolicy -Scope CurrentUser RemoteSigned)

# Windows CMD:
# .venv\Scripts\activate.bat

# 의존성 설치
pip install -r requirements.txt

# 환경변수 설정
cp .env.example .env        # Windows CMD: copy .env.example .env
# .env 파일을 편집하여 JWT_SECRET_KEY, ENCRYPTION_KEY를 변경하세요
```

### 3. 프론트엔드 설정

```bash
cd frontend

# 의존성 설치
npm install
```

### 4. 실행

**터미널 1 — 백엔드:**
```bash
cd backend
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**터미널 2 — 프론트엔드:**
```bash
cd frontend
npm run dev
```

### 5. 접속
- **프론트엔드:** http://localhost:3000
- **백엔드 API 문서:** http://localhost:8000/docs

### 6. 초기 설정
1. 회원가입 (첫 번째 사용자가 자동으로 관리자 권한 부여)
2. 설정 → LLM API 설정에서 LLM 프로바이더 및 API 키 등록
3. 프로젝트 생성 → 샘플 아티팩트 로드(권장) → 워크플로우 시작

### 7. 회귀 테스트 (선택)

```bash
cd backend
.venv/bin/python test_p0_p4_integration.py
```

격리된 임시 SQLite DB에서 P0~P4 86개 assertion이 실행됩니다.

---

## 환경 변수

| 변수명 | 설명 | 기본값 |
|--------|------|--------|
| `DATABASE_URL` | 데이터베이스 연결 문자열 | `sqlite+aiosqlite:///./web_bmad.db` |
| `JWT_SECRET_KEY` | JWT 서명 키 (프로덕션에서 반드시 변경) | `dev-secret-key-change-in-production` |
| `JWT_ALGORITHM` | JWT 알고리즘 | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access Token 만료 시간 (분) | `30` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh Token 만료 시간 (일) | `7` |
| `ENCRYPTION_KEY` | API 키 암호화 키 (프로덕션에서 변경) | `dev-encryption-key-change-in-production` |
| `CORS_ORIGINS` | 허용 CORS 출처 (쉼표 구분) | `http://localhost:3000` |
| `HOST` | 서버 호스트 | `0.0.0.0` |
| `PORT` | 서버 포트 | `8000` |

---

## 샘플 프로젝트

아티팩트가 없는 프로젝트에서 BMad V6 수준의 샘플 아티팩트를 로드할 수 있습니다. 모든 샘플은 P0 앵커 컨벤션과 `derived_from` 마커를 포함하므로 로드 즉시 Traceability 그래프와 Validation 결과가 의미 있게 표시됩니다.

| 샘플 | 기술 스택 | 설명 |
|------|----------|------|
| **TaskFlow** | Python, FastAPI, PostgreSQL, AWS | AI 기반 할일 관리. **Construction 산출물(skeleton/test-plan/CI/IaC) + tech-stack 컨텍스트 포함** |
| **SmartWork** | Java, Spring Boot, PostgreSQL, Azure | 기업용 그룹웨어 (포탈, 전자결재, 게시판) |
| **TradeHub** | Java, Spring Boot, PostgreSQL, Azure | B2B 이커머스 플랫폼 |

---

## SDD 라이프사이클

본 플랫폼은 SDD를 다음 4 Phase로 구현합니다.

### 1. Analysis (분석)
**Analyst (Mary)** 가 프로젝트 아이디어를 구체화하고 Product Brief를 작성합니다.
- Workflows: Create Brief, Goal-Backward Analysis

### 2. Planning (기획)
**PM (John)**, **UX Designer (Sally)** 가 PRD와 UX Spec을 작성합니다.
- Workflows: Create PRD, Validate PRD, Create UX Design

### 3. Solutioning (설계)
**Architect (Winston)** 가 시스템 아키텍처와 ADR을 작성합니다.
- Workflows: Create Architecture
- 산출물의 컴포넌트(C-1, C-2, ...)는 PRD의 FR/NFR에 자동 연결됩니다.

### 4. Implementation & Construction (구현 준비)
**Scrum Master (Bob)** 가 Epic/Story로 분해하고 Sprint를 계획합니다.
**Developer (Dex)**, **QA (Quinn)**, **DevOps (Ollie)** 가 Construction 산출물을 생성합니다.
- Workflows: Create Epics, Sprint Planning, Create Story, Generate Code Skeleton, Create Test Plan, Design CI Pipeline, Create IaC
- Bolt Mode로 Story를 1~3시간 단위 실행 사이클로 분해합니다.

### 단계별 보조 메뉴 (A/P/R/C)
- **[A] Advanced Elicitation** — 소크라틱 질문, 프리모텀, 레드팀 비평
- **[P] Party Mode** — 멀티 페르소나 3단계 토론
- **[R] Propose Mode** — AI가 현재 단계 내용을 자동 작성
- **[C] Continue** — 다음 단계로 진행

### 상위 레이어 (단계 무관)
- **Multi-Agent Orchestration** — PRD 등 핵심 산출물을 병렬 다관점 검토
- **Validation Engine** — 6개 룰로 cross-document 일관성 자동 검증
- **Spec Health Score** — 프로젝트 품질을 0~100점으로 가시화

### 참고 방법론
- [BMad Method V6](https://github.com/bmadcode/bmad-method) — AI 페르소나 및 워크플로우 체계
- [GSD (Get Shit Done)](https://github.com/gsd-build/get-shit-done) — Goal-Backward 분해, fresh-context subagent
- [AWS AI-DLC](https://github.com/awslabs/aidlc-workflows) — Inception → Construction → Operations 거버넌스

---

## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.
