# Spec Studio

**SDD(Spec-Driven Development) 기반 Enterprise AI-Driven Development 웹 서비스**

소프트웨어 개발의 전체 Spec lifecycle을 AI와 함께 체계적으로 관리하는 협업 플랫폼입니다.

---

## 비전

**Spec-Driven Development(SDD)** 를 핵심 방법론으로, AI가 분석·기획·설계·구현 전 단계의 산출물(Spec)을 주도적으로 생성하고 검증하는 **Enterprise AI-Driven Development** 서비스를 목표로 합니다.

다음의 업계 선행 방법론과 프레임워크를 참고·통합하여 설계되었습니다:

| 참고 방법론 | 핵심 차용 요소 |
|------------|---------------|
| **BMad Method V6** | AI 페르소나 기반 워크플로우, 단계별 아티팩트 생성 체계 |
| **GSD (Get Stuff Done)** | 실용적 산출물 중심 실행 프레임워크 |
| **AWS AI-DLC** | Enterprise급 AI-Driven Development Lifecycle 거버넌스 |

이들을 종합하여 **"Spec이 곧 개발의 출발점이자 품질 기준"** 이 되는 SDD 패러다임을 웹 환경에서 실현합니다.

---

## 핵심 가치

- **SDD 실현** — Spec(산출물)이 개발의 기준점이 되어, AI와 사람이 함께 분석→기획→설계→구현 전 과정의 Spec을 생성·검증·관리
- **AI 페르소나 기반 협업** — Analyst, PM, Architect, UX Designer, Scrum Master, Tech Writer 6명의 전문가 AI와 대화하며 산출물을 만들어갑니다
- **구조화된 워크플로우** — 단계별 워크플로우(Brief → PRD → Architecture → UX → Epics → Story)를 따라 체계적으로 진행
- **다중 사용자 실시간 협업** — WebSocket 기반 실시간 채팅으로 팀원들이 함께 페르소나와 상호작용
- **아티팩트 버전 관리** — 산출물의 생성, 수정, 버전 히스토리 추적 및 diff 비교, 복구 기능
- **멀티 LLM 프로바이더 지원** — OpenAI, Anthropic, Google, Ollama 등 다양한 LLM 연동

---

## 주요 기능

### SDD 워크플로우 실행
- 8개 워크플로우: Create Brief, Create PRD, Validate PRD, Create Architecture, Create UX Design, Create Epics, Sprint Planning, Create Story
- A/P/R/C 메뉴: Advanced Elicitation, Party Mode(멀티 페르소나 토론), Propose Mode(AI 자동 초안), Continue
- 대화 중 페르소나 전환 가능

### 아티팩트 관리
- Markdown 파일 생성/편집/삭제
- BMad 템플릿 기반 파일 생성
- 버전 관리 (YYMMDD_HHMMSS 포맷, 수정자 추적)
- 버전 간 Diff 비교 및 복구
- 드래그 앤 드롭 파일 이동, 이름 변경
- 전체 다운로드 (ZIP)
- 3종 샘플 프로젝트 아티팩트 제공

### 채팅 & AI
- WebSocket 기반 실시간 스트리밍 응답
- 페르소나별 시스템 프롬프트 + 프로젝트 컨텍스트 자동 로드
- Party Mode: 멀티 페르소나 3단계 토론 (의견 → 상호 토론 → 합의 정리)
- Propose Mode: AI가 현재 단계 내용을 자동 작성하여 제안
- SAVE_FILE 마커 기반 채팅 내 아티팩트 자동 저장
- 메시지 복사, Bold 텍스트 클릭 입력, A/P/R/C 퀵 액션 버튼

### 프로젝트 관리
- 프로젝트 생성/수정/삭제, 단계(Phase) 관리
- 멤버 초대 및 역할 관리 (Owner/Member)
- 아티팩트 진행 체크리스트
- 활동 내역 피드 (아티팩트 생성/수정, 채팅, 멤버 추가, 설정 변경)

### 관리자 백오피스
- 접속 이력 관리 (IP, 브라우저, 시간)
- 사용자 관리 (관리자 권한 부여/해제, 삭제)
- 프로젝트 관리 (멤버 관리, 단계 변경, 삭제)
- LLM API 설정 관리

### UI/UX
- 한국어/영어 다국어 지원 (KO/EN 스위치)
- 접기/펼치기 가능한 사이드바
- 마크다운 프리뷰/에디터
- 반응형 디자인

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
│   │   │   ├── (auth)/           # 로그인/회원가입
│   │   │   └── (app)/            # 인증 필요 라우트
│   │   │       ├── dashboard/    # 대시보드
│   │   │       ├── projects/     # 프로젝트 목록/상세
│   │   │       ├── admin/        # 관리자 백오피스
│   │   │       ├── profile/      # 프로필 관리
│   │   │       └── settings/     # LLM 설정
│   │   ├── components/
│   │   │   ├── chat/             # 채팅 (ChatWindow, ChatInput, PersonaSelector...)
│   │   │   ├── files/            # 아티팩트 (FileTree, FileViewer, DiffView...)
│   │   │   ├── layout/           # 레이아웃 (Header, Sidebar...)
│   │   │   ├── editor/           # Markdown 에디터/프리뷰
│   │   │   └── ui/               # 기본 UI 컴포넌트
│   │   ├── lib/                  # API 클라이언트, i18n, WebSocket
│   │   ├── stores/               # Zustand 스토어
│   │   └── types/                # TypeScript 타입
│   └── package.json
│
├── backend/
│   ├── app/
│   │   ├── api/                  # REST API 엔드포인트
│   │   ├── models/               # SQLAlchemy 모델
│   │   ├── schemas/              # Pydantic 스키마
│   │   ├── services/             # 비즈니스 로직
│   │   │   └── samples/          # 샘플 아티팩트 데이터
│   │   ├── llm/                  # LLM 통합 (프롬프트, 컨텍스트)
│   │   ├── bmad/                 # BMad 페르소나/워크플로우/템플릿
│   │   └── core/                 # 보안, 의존성, 예외
│   ├── bmad_data/
│   │   ├── personas/             # 페르소나 시스템 프롬프트
│   │   ├── workflows/            # 워크플로우 정의
│   │   └── templates/            # 아티팩트 템플릿
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
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 환경변수 설정
cp .env.example .env
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
source .venv/bin/activate
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
3. 프로젝트 생성 → 워크플로우 또는 페르소나 실행 시작

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

아티팩트가 없는 프로젝트에서 BMad V6 수준의 샘플 아티팩트를 로드할 수 있습니다:

| 샘플 | 기술 스택 | 설명 |
|------|----------|------|
| **TaskFlow** | Python, FastAPI, PostgreSQL, AWS | AI 기반 할일 관리 서비스 |
| **SmartWork** | Java, Spring Boot, PostgreSQL, Azure | 기업용 그룹웨어 (포탈, 전자결재, 게시판) |
| **TradeHub** | Java, Spring Boot, PostgreSQL, Azure | B2B 이커머스 플랫폼 |

각 샘플은 Product Brief, PRD, Architecture, Epics, Project Context, Sprint Status 6개 아티팩트를 포함합니다.

---

## SDD(Spec-Driven Development) 워크플로우

Spec-Driven Development의 핵심은 **개발 전 모든 단계의 산출물(Spec)을 AI와 함께 충분히 정의하고 검증한 후 구현에 진입하는 것**입니다. 본 플랫폼은 이를 다음 4단계로 구현합니다.

### 개발 단계
1. **Analysis (분석)** — Analyst가 프로젝트 아이디어를 구체화하고 Product Brief 작성
2. **Planning (기획)** — PM이 PRD 작성, UX Designer가 UX Spec 작성
3. **Solutioning (설계)** — Architect가 기술 아키텍처 설계
4. **Implementation (구현)** — Scrum Master가 Epic/Story 분해, Sprint 계획

### 워크플로우 메뉴 (A/P/R/C)
- **[A] Advanced Elicitation** — 소크라틱 질문, 프리모텀, 레드팀 비평
- **[P] Party Mode** — 멀티 페르소나 3단계 토론
- **[R] Propose Mode** — AI가 현재 단계 내용을 자동 작성
- **[C] Continue** — 다음 단계로 진행

### 참고 방법론
- [BMad Method V6](https://github.com/bmadcode/bmad-method) — AI 페르소나 및 워크플로우 체계
- GSD (Get Stuff Done) — 실용적 실행 프레임워크
- AWS AI-DLC — Enterprise AI Development Lifecycle

---

## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.
