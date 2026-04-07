"""BMad Best Practice 샘플 아티팩트 파일 (한국어)

3가지 샘플 프로젝트를 제공합니다.
"""

SAMPLE_CATALOG = [
    {
        "id": "taskflow",
        "name": "TaskFlow - AI 기반 할일 관리 서비스",
        "description": "Python/FastAPI/PostgreSQL/AWS 기술 기반의 AI 스마트 할일 관리 웹 앱 구축 프로젝트",
        "tech": "Python, FastAPI, PostgreSQL, AWS",
    },
    {
        "id": "groupware",
        "name": "SmartWork - 기업용 그룹웨어 시스템",
        "description": "JAVA/Spring/PostgreSQL/Azure 기술 기반의 포탈, 전자결재, 게시판을 포함하는 기업용 그룹웨어 구축 프로젝트",
        "tech": "Java, Spring Boot, PostgreSQL, Azure",
    },
    {
        "id": "b2b-commerce",
        "name": "TradeHub - B2B 이커머스 플랫폼",
        "description": "JAVA/Spring/PostgreSQL/Azure 기술 기반의 기업 간 거래를 위한 B2B 이커머스 플랫폼 구축 프로젝트",
        "tech": "Java, Spring Boot, PostgreSQL, Azure",
    },
]


def _taskflow_files():
    return [
        {
            "file_name": "product-brief.md",
            "file_path": "planning-artifacts/product-brief.md",
            "content": """# Product Brief - TaskFlow

**작성자:** BMad 샘플 | **날짜:** 2026-03-21 | **상태:** 완료

## 요약
TaskFlow는 AI를 활용하여 할일을 자동 분류하고 우선순위를 지정하는 스마트 할일 관리 웹 앱입니다.

## 문제 정의
직장인들이 다양한 채널에서 쏟아지는 업무를 효과적으로 관리하지 못하고 있습니다. 기존 할일 앱은 단순 목록 나열에 그쳐 우선순위 판단은 사용자 몫입니다.

## 솔루션
AI가 할일의 맥락을 분석하여 카테고리 분류, 우선순위 지정, 최적 일정을 제안하는 개인 할일 관리 앱.

### 핵심 기능
- AI 자동 분류 및 우선순위 태깅
- 자연어 입력 ("내일까지 보고서 작성")
- 스마트 일일 일정 제안
- 생산성 대시보드

## 차별화 포인트
AI 기반 자동 우선순위 조정 — 사용자 개입 없이 가장 중요한 일을 상위 배치

## 대상 사용자
- **주요:** 업무가 많은 직장인 (25-45세)
- **보조:** 프리랜서, 대학생

## 성공 기준
| 기준 | 목표 | 측정 |
|------|------|------|
| DAU | 1,000명 (3개월) | Analytics |
| 완료율 | 30% 향상 | A/B 테스트 |
| NPS | 50 이상 | 설문 |

## 범위
**MVP:** 할일 CRUD, AI 분류, 자연어 입력, 대시보드
**제외:** 팀 협업, 캘린더 연동, 모바일 앱

## 기술 스택
Python, FastAPI, PostgreSQL, AWS
""",
        },
        {
            "file_name": "PRD.md",
            "file_path": "planning-artifacts/PRD.md",
            "content": """# PRD - TaskFlow

**버전:** 1.0 | **상태:** 완료

## 1. 요약
TaskFlow는 AI 기반 스마트 할일 관리 웹 앱입니다. 자연어 입력 → AI 자동 분류 → 스마트 일정 제안 → 생산성 시각화.

## 2. 프로젝트 분류
| 속성 | 값 |
|------|-----|
| 유형 | 웹 앱 |
| 도메인 | 생산성 |
| 복잡도 | 보통 |
| 신규/기존 | 신규 (Greenfield) |

## 3. 기능 요구사항
### 3.1 인증 (FR-001~003)
- 이메일/비밀번호 회원가입, 로그인, 로그아웃

### 3.2 할일 관리 (FR-010~016)
- CRUD, 자연어 생성, 완료 처리, 검색

### 3.3 AI 기능 (FR-020~023)
- 자동 카테고리 분류, 우선순위 지정, 일정 제안, 자연어 파싱

### 3.4 대시보드 (FR-030~032)
- 완료 현황, 주간 차트, 카테고리 분포

## 4. 비기능 요구사항
- API 응답: <200ms (p95), 동시 사용자: 500명
- bcrypt 해싱, JWT 인증, HTTPS

## 5. 기술 스택
Python, FastAPI, SQLAlchemy, PostgreSQL, OpenAI API, AWS
""",
        },
        {
            "file_name": "architecture.md",
            "file_path": "planning-artifacts/architecture.md",
            "content": """# Architecture - TaskFlow

## 아키텍처 스타일
모놀리식 백엔드 + SPA 프론트엔드 (MVP 단계)

## 기술 스택
| 레이어 | 기술 |
|--------|------|
| 프론트엔드 | Next.js + TypeScript |
| 백엔드 | FastAPI + Python 3.12 |
| DB | PostgreSQL 16 |
| AI | OpenAI API (GPT-4o-mini) |
| 인프라 | AWS (ECS + RDS) |

## 시스템 구조
```
[Browser] ↔ [Next.js SPA] ↔ [FastAPI] ↔ [PostgreSQL]
                                ↕
                          [OpenAI API]
```

## 데이터 모델
- User (1) → (N) Todo
- Todo: id, user_id, title, category, priority, due_date, ai_metadata(JSONB)

## API 설계
RESTful JSON API, JWT 인증, /api/todos, /api/auth, /api/dashboard
""",
        },
        {
            "file_name": "epics.md",
            "file_path": "planning-artifacts/epics.md",
            "content": """# Epics & Stories - TaskFlow

## Epic 1: 사용자 인증 (E-001, 6pt)
- S-001: 회원가입 (3pt)
- S-002: 로그인/로그아웃 (3pt)

## Epic 2: 할일 CRUD (E-002, 10pt)
- S-003: 할일 생성 및 목록 (5pt)
- S-004: 수정, 삭제, 완료 (5pt)

## Epic 3: AI 기능 (E-003, 18pt)
- S-005: AI 자동 분류 (8pt)
- S-006: 자연어 입력 (5pt)
- S-007: 스마트 일정 제안 (5pt)

## Epic 4: 대시보드 (E-004, 5pt)
- S-008: 현황 및 차트 (5pt)

**총 39pt**
""",
        },
        {
            "file_name": "project-context.md",
            "file_path": "planning-artifacts/project-context.md",
            "content": """# Project Context - TaskFlow

## 기술 스택
Python 3.12, FastAPI, SQLAlchemy 2.x, PostgreSQL 16, Next.js 14, TypeScript, Tailwind CSS, AWS

## 핵심 규칙
1. API 응답은 Pydantic 스키마로 검증
2. AI 호출은 구조화된 출력 (JSON 모드) 사용
3. 비밀번호는 bcrypt 해싱
4. 환경변수에 시크릿 저장
5. 소프트 삭제 기본

## 컨벤션
- Python: snake_case, TypeScript: camelCase
- 커밋: Conventional Commits
- Git: main → develop → feature/*
""",
        },
        {
            "file_name": "sprint-status.md",
            "file_path": "implementation-artifacts/sprint-status.md",
            "content": """# Sprint Status - TaskFlow

## 현재 스프린트: Sprint 1
**목표:** 인증 + 할일 기본 CRUD

```yaml
development_status:
  e-001:
    status: backlog
    stories: { s-001: ready-for-dev, s-002: ready-for-dev }
  e-002:
    status: backlog
    stories: { s-003: ready-for-dev, s-004: ready-for-dev }
  e-003:
    status: backlog
    stories: { s-005: backlog, s-006: backlog, s-007: backlog }
  e-004:
    status: backlog
    stories: { s-008: backlog }
```

총 39pt | 완료 0pt | 잔여 39pt
""",
        },
    ]


def _groupware_files():
    return [
        {
            "file_name": "product-brief.md",
            "file_path": "planning-artifacts/product-brief.md",
            "content": """# Product Brief - SmartWork 그룹웨어

**작성자:** BMad 샘플 | **날짜:** 2026-03-21 | **상태:** 완료

## 요약
SmartWork는 기업 내부 업무 효율화를 위한 통합 그룹웨어 시스템입니다. 포탈, 전자결재, 게시판을 하나의 플랫폼에서 제공합니다.

## 문제 정의
중소·중견기업이 분산된 도구(이메일, 메신저, 문서 공유)로 업무를 처리하여 정보 사일로, 결재 지연, 공지사항 전달 누락 등의 문제가 발생합니다.

## 솔루션
포탈(대시보드), 전자결재(기안-승인-완료), 게시판(공지/자유/부서별)을 통합한 웹 기반 그룹웨어.

### 핵심 기능
- **포탈:** 개인화 대시보드, 공지사항, 일정, 결재 대기 현황
- **전자결재:** 기안 작성, 결재선 지정, 다단계 승인, 반려, 후결
- **게시판:** 공지, 자유, 부서별 게시판, 댓글, 첨부파일

## 차별화 포인트
직관적 UI + 유연한 결재선 + 부서 조직도 기반 권한 관리

## 대상 사용자
- **주요:** 50~500명 규모 기업 임직원
- **관리자:** 인사/총무 담당자

## 기술 스택
Java, Spring Boot, PostgreSQL, Azure
""",
        },
        {
            "file_name": "PRD.md",
            "file_path": "planning-artifacts/PRD.md",
            "content": """# PRD - SmartWork 그룹웨어

**버전:** 1.0 | **상태:** 완료

## 1. 요약
SmartWork는 포탈·전자결재·게시판을 통합한 기업용 그룹웨어입니다. 조직도 기반 권한 관리와 다단계 결재 프로세스를 지원합니다.

## 2. 프로젝트 분류
| 속성 | 값 |
|------|-----|
| 유형 | 웹 앱 (엔터프라이즈) |
| 도메인 | 기업 협업 / HR |
| 복잡도 | 높음 |
| 신규/기존 | 신규 |

## 3. 기능 요구사항
### 3.1 인증 및 조직 관리
- 로그인/SSO, 조직도 관리, 부서/직급 체계, 권한 그룹

### 3.2 포탈
- 개인 대시보드 (결재 대기, 공지, 일정 위젯)
- 회사 공지사항, 최근 게시글, 조직도 조회

### 3.3 전자결재
- 기안 작성 (서식 템플릿), 결재선 설정 (순차/병렬/합의)
- 승인/반려/후결/대결, 결재 이력 관리, 문서번호 자동 채번

### 3.4 게시판
- 공지/자유/부서별 게시판, 댓글, 첨부파일, 조회수
- 게시판 권한 설정 (읽기/쓰기/관리)

## 4. 비기능 요구사항
- 동시 접속: 500명, 응답시간: <500ms
- RBAC 권한 체계, 감사 로그, SSL/TLS
- Azure AD 연동 가능

## 5. 기술 스택
Java 17, Spring Boot 3.x, Spring Security, JPA/Hibernate, PostgreSQL, Azure App Service
""",
        },
        {
            "file_name": "architecture.md",
            "file_path": "planning-artifacts/architecture.md",
            "content": """# Architecture - SmartWork 그룹웨어

## 아키텍처 스타일
모듈러 모놀리스 (향후 마이크로서비스 분리 가능)

## 기술 스택
| 레이어 | 기술 |
|--------|------|
| 프론트엔드 | React + TypeScript + Ant Design |
| 백엔드 | Java 17 + Spring Boot 3.x |
| ORM | JPA/Hibernate |
| DB | PostgreSQL 16 (Azure DB) |
| 인증 | Spring Security + JWT + Azure AD |
| 파일 | Azure Blob Storage |
| 배포 | Azure App Service + Azure DB |

## 시스템 구조
```
[Browser] ↔ [React SPA]
                ↕ (REST API)
        [Spring Boot API]
        ├── Auth 모듈 (Spring Security)
        ├── Portal 모듈
        ├── Approval 모듈 (전자결재)
        ├── Board 모듈 (게시판)
        └── Org 모듈 (조직관리)
                ↕
        [PostgreSQL] + [Azure Blob]
```

## 주요 엔티티
- Organization → Department → User
- ApprovalDocument → ApprovalLine → ApprovalStep
- Board → Post → Comment → Attachment
""",
        },
        {
            "file_name": "epics.md",
            "file_path": "planning-artifacts/epics.md",
            "content": """# Epics & Stories - SmartWork

## Epic 1: 인증 및 조직 관리 (E-001)
- 로그인/로그아웃, 조직도 CRUD, 부서/직급 관리, 권한 그룹

## Epic 2: 포탈 대시보드 (E-002)
- 개인 대시보드 위젯, 공지사항 위젯, 결재 대기 위젯, 일정 위젯

## Epic 3: 전자결재 (E-003)
- 기안 작성 (서식 템플릿), 결재선 설정, 승인/반려/후결
- 결재 이력, 문서번호 채번, 첨부파일

## Epic 4: 게시판 (E-004)
- 게시판 유형 관리, 게시글 CRUD, 댓글, 첨부파일, 권한 설정

## Epic 5: 관리자 기능 (E-005)
- 사용자/조직 일괄 관리, 시스템 설정, 감사 로그
""",
        },
        {
            "file_name": "project-context.md",
            "file_path": "planning-artifacts/project-context.md",
            "content": """# Project Context - SmartWork

## 기술 스택
Java 17, Spring Boot 3.x, Spring Security, JPA/Hibernate, PostgreSQL 16, React, TypeScript, Ant Design, Azure

## 핵심 규칙
1. 모든 API는 Spring Security로 인증/인가 처리
2. 결재 문서는 상태 머신으로 관리 (DRAFT → PENDING → APPROVED/REJECTED)
3. 조직도 변경은 감사 로그 필수
4. 파일 업로드는 Azure Blob Storage 사용
5. 다국어 지원 (한국어/영어)

## 컨벤션
- Java: camelCase, DTO/Entity 분리
- 패키지 구조: domain 기반 (approval, board, portal, org)
- API: RESTful, /api/v1 prefix
""",
        },
        {
            "file_name": "sprint-status.md",
            "file_path": "implementation-artifacts/sprint-status.md",
            "content": """# Sprint Status - SmartWork

## 현재 스프린트: Sprint 1
**목표:** 인증 + 조직관리 기본 기능

```yaml
development_status:
  e-001: { status: backlog }
  e-002: { status: backlog }
  e-003: { status: backlog }
  e-004: { status: backlog }
  e-005: { status: backlog }
```
""",
        },
    ]


def _b2b_commerce_files():
    return [
        {
            "file_name": "product-brief.md",
            "file_path": "planning-artifacts/product-brief.md",
            "content": """# Product Brief - TradeHub B2B 이커머스

**작성자:** BMad 샘플 | **날짜:** 2026-03-21 | **상태:** 완료

## 요약
TradeHub는 기업 간(B2B) 거래를 위한 이커머스 플랫폼입니다. 도매/유통 업체가 온라인으로 상품을 등록하고, 구매 업체가 견적 요청, 주문, 정산까지 원스톱으로 처리합니다.

## 문제 정의
B2B 거래는 여전히 전화, 팩스, 이메일에 의존합니다. 가격 협상, 견적서, 발주서가 수작업으로 처리되어 오류와 비효율이 발생합니다.

## 솔루션
판매자(공급사)와 구매자(바이어) 간 거래 전 과정을 디지털화하는 B2B 이커머스 플랫폼.

### 핵심 기능
- **상품 카탈로그:** 대량 등록, 카테고리 관리, 가격 정책 (계약가/수량 할인)
- **견적/주문:** 견적 요청 → 견적서 발행 → 주문 확정 → 배송 추적
- **정산:** 월별 정산, 세금계산서 연동, 미수금 관리
- **거래처 관리:** 기업 회원 가입, 신용 등급, 거래 이력

## 차별화 포인트
기업 맞춤 가격 정책 + 견적-주문-정산 원스톱 프로세스

## 대상 사용자
- **판매자:** 제조사, 도매업체
- **구매자:** 소매업체, 기업 구매 담당자

## 기술 스택
Java, Spring Boot, PostgreSQL, Azure
""",
        },
        {
            "file_name": "PRD.md",
            "file_path": "planning-artifacts/PRD.md",
            "content": """# PRD - TradeHub B2B 이커머스

**버전:** 1.0 | **상태:** 완료

## 1. 요약
TradeHub는 B2B 거래의 전 과정(상품 등록 → 견적 → 주문 → 배송 → 정산)을 디지털화하는 이커머스 플랫폼입니다.

## 2. 프로젝트 분류
| 속성 | 값 |
|------|-----|
| 유형 | 웹 플랫폼 (마켓플레이스) |
| 도메인 | B2B 이커머스 |
| 복잡도 | 높음 |
| 신규/기존 | 신규 |

## 3. 기능 요구사항
### 3.1 회원 및 기업 관리
- 기업 회원 가입 (사업자 인증), 담당자 계정 관리, 거래처 등록/승인

### 3.2 상품 관리
- 상품 등록/수정, 카테고리 관리, 대량 업로드 (엑셀)
- 가격 정책: 기본가, 계약가, 수량 할인, 기간 프로모션

### 3.3 견적 및 주문
- 견적 요청 → 견적서 발행 → 협상 → 주문 확정
- 주문 상태 관리, 배송 추적, 반품/교환

### 3.4 정산
- 월별 거래 정산, 세금계산서 발행 연동
- 미수금 관리, 결제 조건 (선불/후불/외상)

### 3.5 관리자 (백오피스)
- 판매자/구매자 관리, 거래 모니터링, 통계 대시보드

## 4. 비기능 요구사항
- 동시 사용자: 1,000명, 상품 100만 건 처리
- 전자서명, 데이터 암호화, 감사 추적
- Elasticsearch 상품 검색

## 5. 기술 스택
Java 17, Spring Boot 3.x, JPA, PostgreSQL, Elasticsearch, Azure
""",
        },
        {
            "file_name": "architecture.md",
            "file_path": "planning-artifacts/architecture.md",
            "content": """# Architecture - TradeHub B2B 이커머스

## 아키텍처 스타일
모듈러 모놀리스 + 이벤트 기반 비동기 처리 (정산, 알림)

## 기술 스택
| 레이어 | 기술 |
|--------|------|
| 프론트엔드 | Next.js + TypeScript |
| 백엔드 | Java 17 + Spring Boot 3.x |
| 검색 | Elasticsearch 8.x |
| DB | PostgreSQL 16 (Azure DB) |
| 메시지큐 | Azure Service Bus |
| 파일 | Azure Blob Storage |
| 배포 | Azure AKS (Kubernetes) |

## 시스템 구조
```
[Buyer App] [Seller App]
        ↕         ↕
    [API Gateway (Azure APIM)]
            ↕
    [Spring Boot API]
    ├── Product 모듈
    ├── Quote/Order 모듈
    ├── Settlement 모듈
    ├── Company 모듈
    └── Search 모듈 → [Elasticsearch]
            ↕
    [PostgreSQL] + [Azure Blob]
            ↕
    [Azure Service Bus] → 비동기 처리 (정산, 알림)
```

## 주요 엔티티
- Company → User (담당자)
- Product → PricePolicy → Category
- Quote → QuoteLine → Order → OrderLine
- Settlement → Invoice
""",
        },
        {
            "file_name": "epics.md",
            "file_path": "planning-artifacts/epics.md",
            "content": """# Epics & Stories - TradeHub

## Epic 1: 회원 및 기업 관리 (E-001)
- 기업 회원 가입, 사업자 인증, 담당자 관리, 거래처 승인

## Epic 2: 상품 관리 (E-002)
- 상품 CRUD, 카테고리, 대량 업로드, 가격 정책, 검색 인덱싱

## Epic 3: 견적 및 주문 (E-003)
- 견적 요청/발행/협상, 주문 확정, 배송 추적, 반품/교환

## Epic 4: 정산 (E-004)
- 월별 정산, 세금계산서, 미수금 관리, 결제 조건

## Epic 5: 관리자 백오피스 (E-005)
- 판매자/구매자 관리, 거래 모니터링, 통계 대시보드
""",
        },
        {
            "file_name": "project-context.md",
            "file_path": "planning-artifacts/project-context.md",
            "content": """# Project Context - TradeHub

## 기술 스택
Java 17, Spring Boot 3.x, JPA/Hibernate, PostgreSQL 16, Elasticsearch 8.x, Next.js 14, Azure AKS

## 핵심 규칙
1. 금액 계산은 BigDecimal 사용 (부동소수점 금지)
2. 주문/정산 상태는 상태 머신으로 관리
3. 모든 거래 변경은 감사 로그 기록
4. 상품 검색은 Elasticsearch, CRUD는 PostgreSQL
5. 비동기 처리 (정산, 알림)는 Azure Service Bus 사용

## 컨벤션
- 패키지: domain 기반 (product, order, settlement, company)
- API: RESTful, /api/v1, 페이지네이션 필수
- 금액 단위: 원(KRW), 소수점 없음
""",
        },
        {
            "file_name": "sprint-status.md",
            "file_path": "implementation-artifacts/sprint-status.md",
            "content": """# Sprint Status - TradeHub

## 현재 스프린트: Sprint 1
**목표:** 회원/기업 관리 + 상품 기본 CRUD

```yaml
development_status:
  e-001: { status: backlog }
  e-002: { status: backlog }
  e-003: { status: backlog }
  e-004: { status: backlog }
  e-005: { status: backlog }
```
""",
        },
    ]


SAMPLE_FILES_MAP = {
    "taskflow": _taskflow_files,
    "groupware": _groupware_files,
    "b2b-commerce": _b2b_commerce_files,
}

# Backward compatibility
SAMPLE_FILES = _taskflow_files()
