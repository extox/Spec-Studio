"""YAML templates for context expansion categories."""

_SYSTEM_ARCH_TEMPLATE = """\
# ===== 시스템 아키텍처 모델링 =====
# [필수] 기본 정보
system_name: ""          # 시스템 이름 (예: "주문관리 ERP")
system_type: monolith    # monolith | microservice | saas | package | legacy | serverless
description: ""          # 시스템 개요

# [선택] 인프라 구성
infrastructure:
  - id: ""
    type: server         # server | database | storage | cache | container | load-balancer | switch | firewall | gateway | service | queue | client
    name: ""
    technology: ""
    connections:
      - target: ""
        label: ""

# [선택] 바운더리 (네트워크 영역)
boundaries:
  - id: ""
    type: internal       # vpc | dmz | internal | external | subnet | cluster
    name: ""
    color: "#10b981"
    children: []
"""

CONTEXT_TEMPLATES: dict[str, str] = {
    "system-architecture": _SYSTEM_ARCH_TEMPLATE,
    "legacy-system": """\
# ===== 레거시 시스템 모델 =====
# [필수] 기본 정보
system_name: ""          # 시스템 이름 (예: "주문관리 ERP")
system_type: monolith    # monolith | microservice | saas | package | legacy
description: ""          # 시스템 개요

# [선택] 기술 스택
technology:
  language: ""           # 예: Java, C#, Python
  framework: ""          # 예: Spring Boot, .NET, Django
  database: ""           # 예: Oracle 12c, PostgreSQL 14
  os: ""                 # 예: RHEL 8, Windows Server 2019
  middleware: ""         # 예: WebLogic, Tomcat, IIS

# [선택] 주요 기능/모듈
modules:
  - name: ""
    description: ""

# [선택] API / 인터페이스
apis:
  - name: ""
    method: REST         # REST | SOAP | gRPC | File | MQ
    endpoint: ""
    description: ""

# [선택] 객체 구성 (서버, 스토리지 등)
infrastructure:
  - id: ""
    type: server         # server | storage | container | switch | load-balancer | firewall | gateway
    name: ""
    technology: ""
    introduced_year: null
    connections:
      - target: ""
        protocol: ""
        port: null
    notes: ""

# [선택] 알려진 이슈/제약사항
pain_points:
  - ""

# [선택] 운영 정보
operations:
  eol_date: ""           # 서비스 종료 예정일
  sla: ""                # SLA 수준
  data_volume: ""        # 데이터 규모
  peak_tps: null         # 최대 TPS
""",

    "erd": """\
# ===== ERD / 데이터 모델 =====
# [필수] 기본 정보
model_name: ""           # 모델 이름 (예: "주문 도메인 ERD")
database_type: ""        # 예: Oracle, PostgreSQL, MySQL

# [필수] 엔티티 목록
entities:
  - name: ""             # 테이블/엔티티 이름
    description: ""
    columns:
      - name: ""
        type: ""         # 예: VARCHAR(100), INTEGER, TIMESTAMP
        nullable: false
        pk: false
        fk: ""           # 참조 테이블.컬럼 (예: users.id)
        description: ""

# [선택] 관계 정의
relationships:
  - from: ""             # 소스 엔티티
    to: ""               # 대상 엔티티
    type: "1:N"          # 1:1 | 1:N | N:M
    description: ""

# [선택] 인덱스
indexes:
  - table: ""
    columns: []
    unique: false
""",

    "code-convention": """\
# ===== 코드 컨벤션 =====
# [필수] 기본 정보
convention_name: ""      # 컨벤션 이름 (예: "프론트엔드 코드 규칙")
language: ""             # 대상 언어/프레임워크

# [필수] 규칙 목록
rules:
  - category: naming     # naming | formatting | structure | testing | git | other
    rule: ""             # 규칙 설명
    example: ""          # 예시 (선택)
    bad_example: ""      # 나쁜 예시 (선택)

# [선택] 디렉토리 구조
directory_structure: ""  # 프로젝트 디렉토리 구조 설명

# [선택] 사용 도구
tools:
  linter: ""             # 예: ESLint, Pylint
  formatter: ""          # 예: Prettier, Black
  test_framework: ""     # 예: Jest, Pytest
""",

    "architecture": """\
# ===== To-Be 아키텍처 =====
# [필수] 기본 정보
architecture_name: ""    # 아키텍처 이름
description: ""          # 아키텍처 개요

# [선택] 아키텍처 유형
style: microservice      # monolith | microservice | serverless | event-driven | layered

# [선택] 기술 스택
tech_stack:
  frontend: ""
  backend: ""
  database: ""
  cache: ""
  message_queue: ""
  cloud_provider: ""     # AWS | Azure | GCP | On-premise

# [선택] 서비스/컴포넌트 구성
components:
  - name: ""
    type: service        # service | gateway | database | cache | queue | storage
    technology: ""
    description: ""
    dependencies: []     # 의존하는 다른 컴포넌트 이름

# [선택] 주요 설계 결정 (ADR)
decisions:
  - title: ""
    status: accepted     # proposed | accepted | deprecated
    context: ""
    decision: ""
    consequences: ""
""",

    "rfp-summary": """\
# ===== RFP / 기획서 요약 =====
# [필수] 기본 정보
document_name: ""        # 문서 이름
document_type: rfp       # rfp | planning | proposal | requirement
summary: ""              # 핵심 요약 (1-3문장)

# [선택] 프로젝트 개요
project_overview:
  objective: ""          # 프로젝트 목적
  scope: ""              # 범위
  timeline: ""           # 일정
  budget: ""             # 예산 규모

# [선택] 주요 요구사항
requirements:
  functional:
    - ""
  non_functional:
    - ""
  constraints:
    - ""

# [선택] 이해관계자
stakeholders:
  - role: ""
    responsibility: ""
""",

    "ui-ux-guide": """\
# ===== UI/UX 가이드 =====
# [필수] 기본 정보
guide_name: ""           # 가이드 이름

# [선택] 디자인 원칙
principles:
  - ""

# [선택] 컬러 시스템
colors:
  primary: ""
  secondary: ""
  accent: ""
  background: ""
  text: ""

# [선택] 타이포그래피
typography:
  font_family: ""
  heading_sizes: ""
  body_size: ""

# [선택] 컴포넌트 목록
components:
  - name: ""
    description: ""
    variants: []

# [선택] 반응형 브레이크포인트
breakpoints:
  mobile: ""
  tablet: ""
  desktop: ""
""",

    "integration": """\
# ===== 외부 연동 =====
# [필수] 기본 정보
system_name: ""          # 연동 대상 시스템
interface_type: REST     # REST | SOAP | gRPC | File | MQ | CDC | Webhook

# [선택] 연동 상세
connection:
  endpoint: ""
  protocol: ""           # HTTPS | HTTP | SFTP | AMQP | Kafka
  auth_type: ""          # API Key | OAuth2 | Certificate | Basic

# [선택] 데이터 흐름
data_flows:
  - direction: inbound   # inbound | outbound | bidirectional
    data_type: ""
    format: JSON         # JSON | XML | CSV | Binary
    frequency: ""        # real-time | batch-daily | on-demand
    description: ""

# [선택] SLA / 제약
sla:
  availability: ""
  response_time: ""
  rate_limit: ""
""",

    "metadata": """\
# ===== 메타데이터 / 데이터 사전 =====
# [필수] 기본 정보
dictionary_name: ""      # 사전 이름

# [선택] 코드 체계
code_systems:
  - code_id: ""
    name: ""
    description: ""
    values:
      - code: ""
        label: ""

# [선택] 용어 사전
terms:
  - term: ""
    definition: ""
    domain: ""           # 업무 도메인
    synonym: ""

# [선택] 데이터 표준
standards:
  - field_name: ""
    data_type: ""
    length: null
    format: ""           # 예: YYYY-MM-DD, ###-####-####
    description: ""
""",

    "custom": """\
# ===== 커스텀 컨텍스트 =====
# 자유 형식으로 프로젝트에 필요한 컨텍스트를 작성하세요.
# YAML 형식을 유지해주세요.

title: ""
description: ""

# 내용을 자유롭게 구조화하세요
content:
  - ""
""",
}
