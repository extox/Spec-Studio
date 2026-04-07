# Dev.AI Spec Studio 프로젝트 구조 분석 보고서

**작성일**: 2026-04-01  
**프로젝트**: Web_BMad01  
**버전**: 0.1.0

---

## 1. 프로젝트 개요

**프로젝트명**: Dev.AI Spec Studio  
**비전**: BMad Method V6 기반 AI-Driven Development 실행을 위한 웹기반 Spec lifecycle 관리 협업 서비스

### 핵심 가치
- **AI 페르소나 기반 협업**: 6 명의 전문가 AI(Analyst, PM, Architect, UX Designer, Scrum Master, Tech Writer) 와 대화하며 산출물 생성
- **구조화된 워크플로우**: Brief → PRD → Architecture → UX → Epics → Story 단계별 진행
- **실시간 다중 사용자 협업**: WebSocket 기반 채팅
- **아티팩트 버전 관리**: 생성/수정/비교/복구 기능
- **멀티 LLM 지원**: OpenAI, Anthropic, Google, Ollama 등

---

## 2. 기술 스택

### Frontend
| 기술 | 버전 | 용도 |
|------|------|------|
| Next.js | 14.2.35 | React 프레임워크 (App Router) |
| TypeScript | 5.x | 타입 안전성 |
| Tailwind CSS | 3.4.1 | 유틸리티 CSS |
| Zustand | 5.0.12 | 클라이언트 상태 관리 |
| React Query | 5.91.3 | 서버 상태 관리 |
| Axios | 1.13.6 | HTTP 클라이언트 (JWT interceptor 포함) |
| @uiw/react-md-editor | 4.0.11 | Markdown 에디터 |
| Sonner | 2.0.7 | 토스트 알림 |
| Lucide React | - | 아이콘 |
| shadcn | 4.1.0 | UI 컴포넌트 라이브러리 |
| @xyflow/react | 12.10.1 | 흐름도/그래프 시각화 |

### Backend
| 기술 | 버전 | 용도 |
|------|------|------|
| Python | 3.12+ | 런타임 |
| FastAPI | 0.115.6 | 비동기 웹 프레임워크 |
| SQLAlchemy | 2.0.36 (async) | ORM |
| SQLite/PostgreSQL | - | 데이터베이스 |
| Alembic | 1.14.0 | DB 마이그레이션 |
| LiteLLM | 1.55.8 | 멀티 LLM 프로바이더 통합 |
| PyJWT | 2.10.1 | JWT 인증 |
| bcrypt | 4.2.1 | 비밀번호 해싱 |
| WebSockets | 14.1 | 실시간 양방향 통신 |
| Pydantic | 2.10.3 | 데이터 검증 |
| python-multipart | 0.0.18 | 파일 업로드 |

---

## 3. 디렉토리 구조

```
Web_BMad01/
├── frontend/                 # Next.js 14 App Router
│   ├── src/
│   │   ├── app/
│   │   │   ├── (auth)/       # 로그인/회원가입 (route group)
│   │   │   │   ├── login/
│   │   │   │   └── register/
│   │   │   ├── (app)/        # 인증 필요 라우트
│   │   │   │   ├── dashboard/      # 대시보드
│   │   │   │   ├── projects/       # 프로젝트 목록/상세/아티팩트
│   │   │   │   ├── admin/          # 관리자 백오피스
│   │   │   │   ├── profile/        # 프로필 관리
│   │   │   │   └── settings/       # LLM 설정
│   │   │   ├── guide/        # BMad 가이드
│   │   │   ├── layout.tsx    # 루트 레이아웃 (QueryProvider, I18nWrapper)
│   │   │   └── page.tsx      # 랜딩 페이지
│   │   ├── components/
│   │   │   ├── chat/         # 채팅 컴포넌트
│   │   │   ├── files/        # 아티팩트 관리
│   │   │   ├── layout/       # 레이아웃 (Header, Sidebar)
│   │   │   ├── editor/       # Markdown 에디터/프리뷰
│   │   │   ├── context/      # 컨텍스트 관리
│   │   │   ├── project/      # 프로젝트 관련
│   │   │   ├── providers/    # Context Providers
│   │   │   └── ui/           # shadcn 기반 기본 UI
│   │   ├── lib/
│   │   │   ├── api.ts        # Axios 인스턴스
│   │   │   ├── websocket.ts  # WebSocket 클라이언트
│   │   │   ├── utils.ts      # 유틸 함수
│   │   │   └── i18n/         # 다국어 지원
│   │   ├── stores/           # Zustand 스토어
│   │   │   ├── authStore.ts
│   │   │   ├── chatStore.ts
│   │   │   ├── projectStore.ts
│   │   │   └── contextStore.ts
│   │   └── types/
│   │       └── index.ts      # 전체 타입 정의
│   ├── package.json
│   ├── tsconfig.json
│   └── tailwind.config.ts
│
├── backend/                  # FastAPI (Python)
│   ├── app/
│   │   ├── main.py           # FastAPI 앱 진입점
│   │   ├── config.py         # 환경 변수 설정
│   │   ├── database.py       # SQLAlchemy 설정
│   │   ├── api/              # REST API 엔드포인트
│   │   │   ├── auth.py       # /auth/*
│   │   │   ├── projects.py   # /api/projects
│   │   │   ├── chat.py       # /api/chat/*
│   │   │   ├── files.py      # /api/files
│   │   │   ├── context.py    # /api/context
│   │   │   ├── admin.py      # /api/admin
│   │   │   ├── llm_config.py # /api/llm-config
│   │   │   ├── websocket.py  # WebSocket 핸들러 (4000+ lines)
│   │   │   └── ...
│   │   ├── models/           # SQLAlchemy 모델
│   │   ├── schemas/          # Pydantic 스키마
│   │   ├── services/         # 비즈니스 로직
│   │   ├── llm/              # LLM 통합
│   │   ├── core/             # 설정, 보안, 의존성
│   │   └── bmad/             # BMad 메타데이터
│   ├── bmad_data/            # BMad 리소스
│   │   ├── personas/         # 6 개 페르소나
│   │   ├── workflows/        # 8 개 워크플로우
│   │   └── templates/        # 8 개 아티팩트 템플릿
│   ├── requirements.txt
│   └── .env
│
└── README.md
```

---

## 4. 핵심 모듈 분석

### 4.1 인증 시스템 (Auth)

**Flow**:
1. 로그인 → POST `/api/auth/login`
2. JWT 발급 (access_token 30 분, refresh_token 7 일)
3. Axios interceptor 자동 첨부
4. 401 발생 시 → `/api/auth/refresh` → 새 access_token
5. refresh_token 만료 시 → 로그인 페이지 리디렉션

**주요 파일**:
- `backend/app/api/auth.py`
- `backend/app/core/security.py`
- `frontend/src/lib/api.ts`
- `frontend/src/stores/authStore.ts`

---

### 4.2 실시간 채팅 (WebSocket)

**핵심 기능**:
- 스트리밍 응답 (`chat_stream_start` → `chunk` → `end`)
- `SAVE_FILE` 마커 감지 → 아티팩트 자동 저장
- 워크플로우 진행 추적
- Party Mode (멀티 페르소나 토론)
- Propose Mode (AI 자동 초안)

**주요 파일**:
- `backend/app/api/websocket.py` (41,565 lines - 핵심 로직)
- `frontend/src/lib/websocket.ts`
- `frontend/src/components/chat/ChatWindow.tsx`

---

### 4.3 아티팩트 관리 (Files)

**기능**:
- Markdown 파일 CRUD
- 버전 관리 (YYMMDD_HHMMSS 포맷)
- Diff 비교 (파일 간/버전 간)
- 드래그 앤 드롭 재배치
- 전체 다운로드 (ZIP)

**주요 파일**:
- `backend/app/api/files.py`
- `backend/app/services/file_service.py`
- `frontend/src/components/files/FileTree.tsx`
- `frontend/src/components/files/DiffView.tsx`

---

### 4.4 BMad 메타데이터

**페르소나 (6 개)**:
- Analyst, PM, Architect, UX Designer, Scrum Master, Tech Writer

**워크플로우 (8 개)**:
1. Create Brief
2. Create PRD
3. Validate PRD
4. Create Architecture
5. Create UX Design
6. Create Epics
7. Sprint Planning
8. Create Story

**주요 파일**:
- `backend/bmad_data/personas/*.md`
- `backend/bmad_data/workflows/*.md`
- `backend/bmad_data/templates/*.md`

---

### 4.5 컨텍스트 확장 (Context Expansion)

**기능**:
- 프로젝트 컨텍스트 카테고리 관리
- 문서 파싱 (PDF, DOCX, Markdown)
- LLM 프롬프트에 자동 포함

**주요 파일**:
- `backend/app/api/context.py`
- `backend/app/services/context_service.py`
- `backend/app/llm/context_builder.py`

---

### 4.6 LLM 통합

**기능**:
- LiteLLM 을 통한 멀티 프로바이더 지원
- 프로젝트별 LLM 설정 (API 키 암호화)
- 모델 목록 동적 조회
- 프롬프트 조립 (페르소나 + 워크플로우 + 컨텍스트)

**주요 파일**:
- `backend/app/llm/provider.py`
- `backend/app/llm/prompt_builder.py`
- `backend/app/api/llm_config.py`

---

## 5. 데이터 모델

```
User (1) ───< ProjectMember >─── (N) Project
User (1) ───< ChatSession >─── (N) ChatMessage
Project (1) ───< ChatSession >
Project (1) ───< ProjectFile >─── (N) FileVersion
User (1) ───< ActivityLog >
User (1) ───< LoginHistory >
Project (1) ───< LLMConfig >
```

### 주요 엔티티

**User**: id, email, password_hash, display_name, is_admin, created_at

**Project**: id, name, description, phase, created_by, created_at, updated_at

**ChatSession**: id, project_id, persona, workflow, workflow_step, title, created_by, created_at

**ChatMessage**: id, session_id, role, content, metadata_json, created_at

**ProjectFile**: id, project_id, file_path, file_name, file_type, content, file_size, version_label, created_at

**FileVersion**: id, file_id, version_label, file_size, updated_by, created_at

**LLMConfig**: id, provider, model, base_url, api_key_encrypted, is_default, created_at

---

## 6. 주요 기능 흐름

### 6.1 워크플로우 실행

```
1. 프로젝트 선택 → 워크플로우 선택 (예: Create PRD)
2. 페르소나 선택 (예: PM)
3. WebSocket 연결 → 워크플로우 시작
4. A/P/R/C 메뉴:
   - A (Advanced Elicitation): 소크라틱 질문, 프리모텀, 레드팀
   - P (Party Mode): 멀티 페르소나 토론
   - R (Propose Mode): AI 자동 초안 생성
   - C (Continue): 다음 단계
5. SAVE_FILE 마커 감지 → 아티팩트 자동 저장
6. 단계 완료 → 다음 단계로 진행
```

### 6.2 아티팩트 버전 관리

```
1. 파일 생성/수정 → 업로드
2. version_label 생성 (YYMMDD_HHMMSS_사용자이름)
3. ProjectFile 업데이트 + FileVersion 레코드 생성
4. 이전 버전은 보존 (soft delete 아님)
5. DiffView 에서 버전 간 비교
6. 복구 기능: 선택한 버전으로 내용 복원
```

### 6.3 실시간 협업

```
1. 여러 사용자가 동일 프로젝트 접속
2. WebSocket 연결 유지
3. 메시지 스트리밍 응답
4. 아티팩트 변경 사항 실시간 동기화
5. 활동 로그 (ActivityLog) 에 기록
```

---

## 7. 코드 품질 및 아키텍처 평가

### 장점
- **모듈화된 구조**: API, models, schemas, services 분리 명확
- **비동기 처리**: FastAPI + SQLAlchemy async 사용
- **타입 안전**: TypeScript + Pydantic 검증
- **실시간 기능**: WebSocket 기반 양방향 통신
- **확장성**: 컨텍스트 확장, 멀티 LLM 지원
- **버전 관리**: 아티팩트 버전 히스토리 추적

### 개선 필요 사항
- **WebSocket 파일 크기**: `websocket.py` 가 4000+ 라인으로 단일 파일이 너무 큼
- **테스트 커버리지**: 테스트 파일 발견 안됨 (pytest 등 필요)
- **로깅**: 로깅 전략 명확하지 않음
- **에러 핸들링**: 일부 모듈에서 예외 처리 일관성 부족 가능
- **보안**: `.env` 파일이 저장소에 포함되어 있음 (`.gitignore` 확인 필요)

---

## 8. 샘플 프로젝트

3 종 샘플 아티팩트 제공:

| 샘플 | 기술 스택 | 설명 |
|------|----------|------|
| **TaskFlow** | Python, FastAPI, PostgreSQL, AWS | AI 기반 할일 관리 서비스 |
| **SmartWork** | Java, Spring Boot, PostgreSQL, Azure | 기업용 그룹웨어 |
| **TradeHub** | Java, Spring Boot, PostgreSQL, Azure | B2B 이커머스 플랫폼 |

각 샘플은 Product Brief, PRD, Architecture, Epics, Project Context, Sprint Status 6 개 아티팩트 포함.

---

## 9. 실행 방법

### 백엔드
```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 프론트엔드
```bash
cd frontend
npm run dev
```

### 접속
- 프론트엔드: http://localhost:3000
- 백엔드 API 문서: http://localhost:8000/docs

---

## 10. 결론

**Dev.AI Spec Studio**는 BMad Method V6 를 웹 환경에서 구현한 잘 구조화된 Full-Stack 협업 플랫폼입니다.

- **강점**: AI 페르소나 기반 워크플로우, 실시간 협업, 아티팩트 버전 관리, 멀티 LLM 지원
- **기술적 성숙도**: 모던 스택 (Next.js 14, FastAPI, async SQLAlchemy) 사용, 타입 안전성 확보
- **확장성**: 컨텍스트 확장, 샘플 프로젝트 로드를 통한 온보딩 용이

**다음 단계 제안**:
1. 테스트 커버리지 확대 (pytest, jest)
2. WebSocket 모듈 리팩토링 (기능 분리)
3. 로깅/모니터링 강화
4. 프로덕션 배포 전략 (Docker, Kubernetes, CI/CD)
5. 성능 최적화 (DB 인덱싱, 캐싱 전략)

---

**분석 완료**: 2026-04-01  
**총 파일 수**: ~150+ (Frontend + Backend)  
**코드 라인**: ~20,000+ (추정)
