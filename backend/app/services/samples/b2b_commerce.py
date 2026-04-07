B2B_COMMERCE_FILES = [
    {
        "file_name": "product-brief.md",
        "file_path": "planning-artifacts/product-brief.md",
        "content": """---
stepsCompleted: [1,2,3,4,5]
inputDocuments: []
workflowType: 'brief'
---
# Product Brief - TradeHub

**Author:** BMad Sample
**Date:** 2026-03-23
**Status:** Complete

---

## Executive Summary

TradeHub는 제조업·유통업 중심의 B2B 이커머스 플랫폼으로, 기업 간 상품 검색·견적 요청·주문·정산을 하나의 플랫폼에서 처리합니다. 기존의 팩스·이메일·전화 기반 B2B 거래를 디지털화하여 거래 리드타임을 70% 단축하고, 정산 오류를 제거하며, 거래처 관계를 체계적으로 관리합니다.

## The Problem

한국 중소 제조·유통 기업의 B2B 거래는 여전히 팩스, 카카오톡, 이메일, 전화 등 비정형 채널에 의존합니다. 견적 요청부터 발주, 납품, 세금계산서 발행, 정산까지 평균 5~7영업일이 소요되며, 수작업 과정에서 단가 오류, 재고 불일치, 정산 누락이 빈번히 발생합니다. 이로 인해 연간 매출의 2~3%가 정산 오류 및 지연으로 손실됩니다.

### Current Alternatives

- **팩스/이메일 기반 견적:** 비구조화, 이력 추적 불가, 응답 지연 (평균 2일)
- **ERP 내장 영업 모듈 (SAP, 더존):** 도입 비용 과다 (수억 원), 중소기업 부적합, 거래처 간 연동 불가
- **오픈마켓 B2B (네이버 스마트스토어, 쿠팡 비즈):** B2C 중심 설계, 견적·정산 프로세스 미지원, 기업 인증 미흡
- **글로벌 B2B (Alibaba, Amazon Business):** 국내 세금계산서·정산 체계 미지원, 한국어 지원 부족

## The Solution

기업 인증 기반의 B2B 전용 이커머스 플랫폼. 판매자(공급사)가 상품 카탈로그를 등록하면, 구매자(바이어)가 검색·견적 요청·발주를 온라인으로 처리합니다. 견적 협상, 주문 확정, 배송 추적, 세금계산서 자동 발행, 월 단위 정산까지 전 과정을 디지털화합니다.

### Core Capabilities

- **상품 카탈로그:** 계층형 카테고리, 대량 상품 등록 (Excel 업로드), SKU 관리, 거래처별 차등 단가
- **견적/주문 관리:** 온라인 견적 요청 → 견적서 발행 → 발주 확정 → 배송 → 수령 확인 워크플로우
- **정산 시스템:** 월별 자동 정산, 세금계산서 자동 발행 (전자세금계산서 API 연동), 미수금 관리
- **거래처 관리:** 사업자등록번호 기반 기업 인증, 거래처 등급 (VIP/일반/신규), 신용 한도 관리
- **관리자 백오피스:** 플랫폼 전체 거래 모니터링, 분쟁 조정, 매출 통계, 수수료 관리

## What Makes This Different

**기업 간 거래 프로세스 전체를 관통하는 통합 플랫폼** — 단순 상품 판매가 아닌, 견적 협상부터 정산까지의 B2B 특화 워크플로우를 지원합니다. 거래처별 차등 단가, 신용 한도, 월 정산 등 B2B 고유 요구사항을 네이티브로 처리하며, 전자세금계산서 API 연동으로 세무 업무까지 자동화합니다.

## Who This Serves

### Primary Users

**중소 제조·유통 기업 (연매출 10억~500억):** 자체 ERP 시스템이 없거나 제한적인 중소기업. 3~50개 거래처와 정기적으로 거래하며, 팩스·전화 기반 주문 처리에 피로감을 느끼는 영업/구매 담당자. 거래처당 월 10~100건의 주문을 처리합니다.

### Secondary Users

**대기업 구매팀:** 중소 협력업체와의 거래 디지털화 수단으로 활용. 기존 ERP와 API 연동 가능.
**플랫폼 관리자:** TradeHub 운영팀. 거래 모니터링, 분쟁 조정, 수수료 정책 관리.

## Success Criteria

| Criteria | Target | Measurement |
|----------|--------|-------------|
| 등록 기업 수 | 500개사 (출시 6개월) | 가입 + 사업자 인증 완료 |
| 월 거래액 (GMV) | 50억 원 (12개월) | 주문 확정 금액 합계 |
| 거래 리드타임 단축 | 70% 감소 (5일 → 1.5일) | 견적 요청 ~ 발주 확정 시간 |
| 정산 오류율 | 0.1% 미만 | 정산 이의 건수 / 전체 정산 건수 |
| 월간 재주문율 | 70% 이상 | 재주문 기업 / 전체 주문 기업 |

## Scope

### In Scope (MVP)

- 사업자등록번호 기반 기업 회원가입 및 인증
- 상품 카탈로그 등록/검색 (카테고리, 키워드, 필터)
- 견적 요청 → 견적서 발행 → 발주 확정 워크플로우
- 주문 상태 관리 (발주 → 출하 → 배송 → 수령 확인)
- 월별 정산 자동 계산 및 정산서 생성
- 거래처 등록 및 관계 관리
- 관리자 백오피스 (거래 모니터링, 기업 승인, 통계)

### Out of Scope

- 물류 배송 직접 운영 (외부 택배사 연동만)
- 실시간 채팅/화상 미팅
- AI 기반 가격 추천 / 수요 예측
- 해외 거래 (다통화, 국제 물류)
- 모바일 네이티브 앱

## Vision

**1년:** 제조·유통 B2B 거래 디지털화의 대표 플랫폼. 등록 기업 500개사, 월 GMV 50억 원. 전자세금계산서 연동 완료.
**3년:** 산업별 특화 마켓플레이스 (건설자재, 식자재, 산업용품). 공급망 금융 (팩토링) 연계. 등록 기업 5,000개사, 월 GMV 500억 원. AI 기반 수요 예측 및 자동 재발주.
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
# Product Requirements Document - TradeHub

**Author:** BMad Sample
**Date:** 2026-03-23
**Version:** 1.0
**Status:** Complete

---

## 1. Executive Summary

TradeHub는 중소 제조·유통 기업을 위한 B2B 이커머스 플랫폼입니다. 상품 카탈로그 관리, 견적 협상, 주문 처리, 정산, 거래처 관리를 하나의 플랫폼에서 통합 제공합니다. 팩스·전화 기반의 아날로그 B2B 거래를 디지털화하여 거래 리드타임을 70% 단축하고, 정산 오류를 0.1% 미만으로 줄입니다.

Java 17/Spring Boot 3.x 백엔드, Next.js 14 프론트엔드, PostgreSQL 16 데이터베이스, Elasticsearch 8.x 검색엔진, Azure AKS 기반으로 운영됩니다.

## 2. Project Classification

| Attribute | Value |
|-----------|-------|
| Project Type | Web Application (SPA + REST API + 비동기 메시징) |
| Domain | B2B 이커머스 / 공급망 관리 (Supply Chain) |
| Complexity | High |
| Greenfield/Brownfield | Greenfield (신규 개발) |

## 3. Product Vision

### 1-Year Vision
제조·유통 B2B 거래 디지털화의 대표 플랫폼. 등록 기업 500개사, 월 GMV 50억 원.

### 3-Year Vision
산업별 특화 마켓플레이스. 공급망 금융 연계. 등록 기업 5,000개사, 월 GMV 500억 원. AI 기반 자동 재발주.

### Key Differentiator
견적 협상부터 정산까지 B2B 거래 전 과정을 커버. 거래처별 차등 단가, 신용 한도, 월 정산, 전자세금계산서 자동 발행 등 B2B 고유 요구사항을 네이티브 지원.

## 4. Success Criteria

### User Success

| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| 거래 리드타임 | 1.5일 이내 (기존 5일) | 견적 요청 → 발주 확정 시간 |
| 정산 오류율 | 0.1% 미만 | 정산 이의 건수 / 전체 정산 건수 |
| 월간 재주문율 | 70% 이상 | 재주문 기업 / 전체 주문 기업 |

### Business Success

| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| 등록 기업 수 | 500개사 (6개월) | 가입 + 사업자 인증 완료 |
| 월 GMV | 50억 원 (12개월) | 주문 확정 금액 합계 |
| 수수료 수익 | 월 1억 원 (12개월) | 거래 수수료 (GMV 2%) |

### Technical Success

| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| API p95 응답시간 | < 300ms | Azure Monitor |
| 가용성 | 99.9% (업무시간 기준) | Uptime 모니터링 |
| 검색 응답시간 | < 500ms | Elasticsearch 쿼리 로그 |

## 5. User Journeys

### User Type 1: 구매 담당자 김민수 (중소 제조업체 자재팀장, 42세)

**Discovery:** 월 30건 이상의 부품·자재를 팩스와 전화로 발주. 단가 비교를 위해 공급사 3곳에 각각 견적을 요청하며 이메일과 팩스를 뒤지는 데 하루 2시간 소비. "B2B 발주 시스템"을 검색하여 TradeHub 발견.

**Onboarding:** 사업자등록번호로 기업 인증 (1영업일 내 승인). 기존 거래처 3곳을 등록하고 거래 관계 설정. 구매 카탈로그에서 기존에 팩스로 주문하던 부품을 검색하여 확인.

**Core Usage:** 매주 월요일 아침 TradeHub에서 필요한 자재를 검색 → 3개 공급사에 동시 견적 요청 → 견적서 비교 테이블에서 단가·납기·결제조건 비교 → 최적 공급사에 발주 확정 → 배송 추적 → 수령 확인. 월말에 자동 정산 내역 확인 후 대금 이체.

**Edge Cases:** 긴급 발주 시 "긴급" 태그로 견적 요청 → 공급사에 푸시 알림. 납품 불량 시 반품/교환 요청 프로세스 → 정산에 자동 반영.

**Return Usage:** 매주 반복 발주 상품을 "자주 주문 목록"에서 원클릭 재발주. 월간 구매 분석 리포트로 비용 절감 포인트 파악.

### User Type 2: 공급사 영업 담당자 박서연 (유통업체 영업팀, 35세)

**Discovery:** 30개 거래처의 주문을 엑셀로 관리. 견적 요청 응답 지연으로 거래를 놓치는 경우 발생. 거래처가 TradeHub 사용을 제안하여 가입.

**Core Usage:** 견적 요청 알림 수신 → 사내 ERP에서 재고·단가 확인 → TradeHub에서 견적서 작성·발송 → 발주 확정 알림 → 출하 처리 → 배송 정보 입력. 월말 정산서 확인 후 세금계산서 자동 발행.

## 6. Domain Requirements

### 법적·규제 요구사항

- **전자세금계산서:** 부가가치세법에 따라 전자세금계산서 의무 발행 (국세청 API 연동)
- **전자상거래법:** 통신판매업 신고, 개인정보처리방침, 이용약관 게시
- **전자금융거래법:** 결제·정산 관련 보안 요구사항 (금융보안원 가이드라인)
- **개인정보보호법:** 사업자 정보 보호, 접근 제어, 로그 감사

## 7. Scoping & Roadmap

### MVP (Phase 1) — Must-Have

- 사업자등록번호 기반 기업 회원가입/인증
- 상품 카탈로그 CRUD + 카테고리 관리 + Elasticsearch 검색
- 견적 요청 → 견적서 발행 → 발주 확정 워크플로우
- 주문 상태 관리 (발주 → 출하 → 배송 → 수령 확인)
- 월별 정산 자동 계산 + 정산서 생성
- 거래처 등록 + 거래 관계 + 차등 단가
- 관리자 백오피스 (기업 승인, 거래 모니터링, 기본 통계)

### Growth (Phase 2) — Should-Have

- 전자세금계산서 자동 발행 (국세청 API 연동)
- 반품/교환 프로세스 + 정산 반영
- 대량 상품 등록 (Excel 업로드)
- 거래처 신용 한도 관리 + 여신 관리
- 알림 시스템 (견적 요청, 발주 확정, 납기 임박 등)
- 구매/판매 분석 리포트

### Vision (Phase 3) — Could-Have

- ERP 연동 API (더존, SAP 등)
- 공급망 금융 (팩토링, 선지급)
- AI 기반 수요 예측 + 자동 재발주
- 산업별 특화 마켓플레이스 (건설자재, 식자재)
- 모바일 네이티브 앱

### Won't-Have (Explicitly Excluded)

- 물류 직접 운영 (자체 배송)
- 실시간 채팅/화상 미팅
- 해외 거래 (다통화, 국제 물류)
- 소비자(B2C) 직접 판매

### Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| 기업 가입 전환율 저조 | 중 | 높 | 기존 거래 관계 기반 초대 시스템, 온보딩 컨시어지 |
| 전자세금계산서 연동 지연 | 중 | 높 | MVP에서 수동 발행 대안 제공, Phase 2에서 자동화 |
| 대형 거래 시 성능 이슈 | 낮 | 높 | 비동기 처리, 캐싱, DB 파티셔닝 |
| 정산 오류로 인한 신뢰도 하락 | 낮 | 높 | 이중 검증 로직, 정산 감사 로그, 이의 제기 프로세스 |
| 경쟁사 진입 (네이버, 쿠팡) | 높 | 중 | B2B 특화 깊이 차별화, 빠른 시장 선점 |

## 8. Functional Requirements

### 8.1 기업 인증 및 계정 관리

| ID | Requirement | Priority | Acceptance Criteria |
|----|------------|----------|---------------------|
| FR-001 | 사업자등록번호 기반 기업 회원가입 | Must | 사업자번호 유효성 검증 (국세청 API), 기업명·대표자명·업종 자동 조회 |
| FR-002 | 기업 인증 승인 프로세스 | Must | 관리자 승인 후 서비스 이용 가능, 승인/반려 사유 알림 |
| FR-003 | 직원 계정 초대 및 관리 | Must | 기업 관리자가 직원 이메일로 초대, 역할(구매/영업/관리자) 부여 |
| FR-004 | 로그인/로그아웃 (JWT) | Must | access token (1시간) + refresh token (14일), 역할 기반 접근 제어 |
| FR-005 | 기업 프로필 관리 | Must | 사업자정보, 정산 계좌, 배송지 주소 관리 |

### 8.2 상품 카탈로그

| ID | Requirement | Priority | Acceptance Criteria |
|----|------------|----------|---------------------|
| FR-010 | 상품 등록 (제목, 설명, 규격, 이미지) | Must | 상품명, SKU, 카테고리, 기본 단가, 최소 주문 수량, 이미지 (최대 10장) |
| FR-011 | 계층형 카테고리 관리 | Must | 3단계 카테고리 (대/중/소), 관리자 카테고리 CRUD |
| FR-012 | 상품 검색 (키워드 + 필터) | Must | Elasticsearch 기반 전문 검색, 카테고리·가격·공급사 필터, 자동완성 |
| FR-013 | 거래처별 차등 단가 설정 | Must | 공급사가 거래처별 특별 단가 지정 가능, 등급별 할인율 |
| FR-014 | 상품 상태 관리 | Must | 판매중/일시중지/단종 상태 전환, 재고 표시(충분/부족/품절) |
| FR-015 | 대량 상품 등록 (Excel) | Should | Excel 템플릿 다운로드, 업로드 → 검증 → 일괄 등록, 오류 리포트 |

### 8.3 견적 관리

| ID | Requirement | Priority | Acceptance Criteria |
|----|------------|----------|---------------------|
| FR-020 | 견적 요청 생성 | Must | 상품 목록 + 수량 + 희망 납기 + 메모, 복수 공급사에 동시 요청 가능 |
| FR-021 | 견적서 작성 및 발송 | Must | 공급사가 단가·납기·결제조건 작성, PDF 견적서 자동 생성 |
| FR-022 | 견적 비교 | Must | 동일 품목 복수 견적 비교 테이블 (단가, 납기, 결제조건) |
| FR-023 | 견적 협상 (카운터 오퍼) | Should | 바이어 ↔ 공급사 간 단가·조건 수정 요청, 이력 기록 |
| FR-024 | 견적 유효기간 관리 | Must | 견적 유효기간 설정, 만료 알림, 만료 시 자동 상태 변경 |

### 8.4 주문 관리

| ID | Requirement | Priority | Acceptance Criteria |
|----|------------|----------|---------------------|
| FR-030 | 견적서 기반 발주 확정 | Must | 견적서에서 원클릭 발주, 주문번호 자동 생성, 발주 확인 알림 |
| FR-031 | 주문 상태 관리 | Must | 발주접수 → 주문확인 → 출하준비 → 출하완료 → 배송중 → 수령확인 |
| FR-032 | 배송 정보 입력 및 추적 | Must | 택배사·송장번호 입력, 배송 상태 조회 (택배사 API 연동) |
| FR-033 | 수령 확인 및 검수 | Must | 바이어 수령 확인 → 정산 대상에 포함, 불량 시 반품/교환 요청 |

### 8.5 정산

| ID | Requirement | Priority | Acceptance Criteria |
|----|------------|----------|---------------------|
| FR-040 | 월별 자동 정산 | Must | 매월 1일 전월 수령 확인된 주문 자동 집계, 거래처별 정산서 생성 |
| FR-041 | 정산서 조회 및 다운로드 | Must | 거래처별 월간 정산서 (PDF/Excel), 거래 내역 상세 |
| FR-042 | 정산 이의 제기 | Must | 정산 항목별 이의 제기, 관리자 조정, 이력 기록 |
| FR-043 | 수수료 자동 계산 | Must | 거래 금액 대비 수수료 자동 계산 (기본 2%, 등급별 차등) |

### 8.6 거래처 관리

| ID | Requirement | Priority | Acceptance Criteria |
|----|------------|----------|---------------------|
| FR-050 | 거래처 등록 및 관계 설정 | Must | 사업자번호로 거래처 검색 → 거래 관계 요청 → 승인 |
| FR-051 | 거래처 등급 관리 | Must | VIP/일반/신규 등급, 등급별 결제조건·할인율 차등 |
| FR-052 | 거래 이력 조회 | Must | 거래처별 주문/정산 이력, 거래 금액 추이 차트 |

### 8.7 관리자 백오피스

| ID | Requirement | Priority | Acceptance Criteria |
|----|------------|----------|---------------------|
| FR-060 | 기업 가입 승인/반려 | Must | 사업자등록증 확인, 승인/반려 처리, 사유 기록 |
| FR-061 | 거래 모니터링 대시보드 | Must | 실시간 거래 현황, 일/주/월 GMV, 기업별 거래량 |
| FR-062 | 분쟁 조정 | Should | 거래 분쟁 접수, 조정 결과 기록, 정산 반영 |
| FR-063 | 수수료 정책 관리 | Must | 기본 수수료율 설정, 기업별·카테고리별 수수료 차등 |
| FR-064 | 시스템 설정 관리 | Must | 카테고리 관리, 공지사항, 약관 관리 |

## 9. Non-Functional Requirements

### 9.1 Performance

| Metric | Target |
|--------|--------|
| 페이지 초기 로드 (FCP) | < 2.0초 |
| API 응답 시간 (p95) | < 300ms |
| 검색 응답 시간 (p95) | < 500ms |
| 동시 사용자 | 2,000명 |
| 상품 카탈로그 | 100만 SKU 지원 |

### 9.2 Security

- 비밀번호: BCrypt (strength 12)
- 인증: JWT RS256, Spring Security + RBAC (역할 기반 접근 제어)
- 통신: HTTPS 전용 (TLS 1.3)
- SQL Injection: JPA/Hibernate ORM, Parameterized Query
- XSS: Next.js 기본 이스케이프 + CSP 헤더
- 민감 정보: Azure Key Vault, 환경변수 관리
- 감사 로그: 정산, 단가 변경, 기업 승인 등 주요 액션 로깅

### 9.3 Scalability

- 수평 확장: Azure AKS 오토스케일링 (CPU 70% 기준, pod 2~10개)
- DB: PostgreSQL Read Replica (읽기 분산), 정산 테이블 월별 파티셔닝
- 검색: Elasticsearch 클러스터 (3 노드, 샤드 분산)
- 메시징: Azure Service Bus (주문 이벤트, 정산 배치, 알림)

### 9.4 Reliability

- 가용성: 99.9% (업무시간 기준, 월간 다운타임 < 43분)
- 백업: Azure PostgreSQL 자동 백업 (30일 보존), PITR 지원
- 에러 추적: Application Insights + Sentry
- 정산 데이터: 이중 검증 (계산 결과 크로스체크), 감사 로그

### 9.5 Accessibility

- WCAG 2.1 AA 준수
- 키보드 네비게이션 지원
- 스크린 리더 호환 (aria-label, role)
- 색상 대비: 4.5:1 이상

## 10. Appendix

### Glossary

| Term | Definition |
|------|-----------|
| GMV | Gross Merchandise Volume, 총 거래액 |
| SKU | Stock Keeping Unit, 재고 관리 단위 |
| RFQ | Request for Quotation, 견적 요청 |
| PO | Purchase Order, 발주서/구매주문서 |
| 팩토링 | 매출채권을 금융기관에 매각하여 조기 현금화하는 금융 서비스 |
| PITR | Point-in-Time Recovery, 특정 시점 복구 |

### References

- Spring Boot Documentation: https://spring.io/projects/spring-boot
- Elasticsearch Guide: https://www.elastic.co/guide
- 국세청 전자세금계산서 API: https://www.hometax.go.kr
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
# Architecture Decision Document - TradeHub

**Author:** BMad Sample
**Date:** 2026-03-23
**Version:** 1.0
**Status:** Complete

---

## 1. Overview

### 1.1 Purpose
TradeHub B2B 이커머스 플랫폼의 기술 아키텍처를 정의합니다. 기업 인증, 상품 카탈로그, 견적/주문 워크플로우, 정산 시스템, 검색 엔진을 포함하는 엔터프라이즈 수준의 시스템을 설계합니다.

### 1.2 Scope
MVP 기능 전체 (기업 인증, 상품 관리, 견적/주문, 정산, 거래처 관리, 관리자 백오피스). ERP 연동, 공급망 금융, AI 기능은 범위 외.

### 1.3 Context
5인 개발팀, 6개월 MVP 목표. 엔터프라이즈 수준의 안정성과 보안 필요. 정산 데이터의 정합성이 핵심.

## 2. Architecture Drivers

### 2.1 Key Requirements

| ID | Requirement | Impact Level |
|----|------------|-------------|
| FR-012 | 상품 검색 (Elasticsearch) | High — 검색 엔진 아키텍처 결정 |
| FR-030~033 | 주문 워크플로우 (상태 머신) | High — 이벤트 기반 설계 |
| FR-040~043 | 월별 자동 정산 | High — 배치 처리, 데이터 정합성 |
| NFR-Performance | API p95 < 300ms | High — 캐싱, 비동기 전략 |
| NFR-Security | RBAC + 감사 로그 | High — 보안 아키텍처 |

### 2.2 Quality Attributes

| Attribute | Priority | Target |
|-----------|----------|--------|
| Reliability | Critical | 정산 데이터 정합성 100%, 가용성 99.9% |
| Security | Critical | RBAC, 감사 로그, 데이터 암호화 |
| Performance | High | API < 300ms, 검색 < 500ms |
| Scalability | High | 100만 SKU, 2,000 동시 사용자 |
| Maintainability | High | 도메인별 모듈 분리, 테스트 커버리지 80% |

### 2.3 Constraints

- 5인 개발팀 → 적정 수준의 서비스 분리 (과도한 마이크로서비스 지양)
- 정산 데이터 정합성이 비즈니스 핵심 → 트랜잭션 설계 최우선
- 한국 법규 (전자세금계산서, 개인정보보호법) 준수 필수
- 6개월 MVP → 모듈화된 모놀리스로 시작, 점진적 분리

## 3. Architecture Decisions (ADRs)

### ADR-001: Architecture Style — 모듈러 모놀리스 + 이벤트 기반

- **Context:** B2B 거래 프로세스는 견적→주문→정산이 긴밀히 연결. 5인 팀 규모에서 마이크로서비스는 운영 부담 과다. 동시에 도메인 간 느슨한 결합 필요 (상품 변경이 주문에 영향 최소화)
- **Decision:** 모듈러 모놀리스 (도메인별 패키지 분리) + Azure Service Bus를 통한 이벤트 기반 비동기 처리
- **Rationale:** 단일 배포 단위로 운영 단순화하면서, 도메인 경계를 명확히 하여 향후 마이크로서비스 분리 가능. 정산·알림 등 비동기 처리는 Service Bus로 분리
- **Consequences:** 빠른 개발 및 배포. 도메인 간 의존성 관리 규칙 필요. 향후 트래픽 증가 시 주문/정산 서비스 분리 가능
- **Alternatives:** 마이크로서비스 (운영 복잡도 과다), 전통적 모놀리스 (도메인 경계 불명확, 유지보수 어려움)

### ADR-002: Backend Framework — Spring Boot 3.x + Java 17

- **Context:** 엔터프라이즈 B2B 시스템, 트랜잭션 관리 중요, 장기 유지보수 필요
- **Decision:** Spring Boot 3.x + Java 17 (LTS)
- **Rationale:** 강력한 트랜잭션 관리 (@Transactional), Spring Security (RBAC), 성숙한 엔터프라이즈 생태계, 대규모 팀 확장 시 타입 안전성
- **Consequences:** 풍부한 라이브러리 (Spring Data JPA, Spring Security, Spring Batch), 검증된 안정성
- **Alternatives:** FastAPI/Python (트랜잭션 관리 약함), NestJS/Node (엔터프라이즈 생태계 부족), .NET (인력 수급 어려움)

### ADR-003: Database — PostgreSQL 16 + 파티셔닝

- **Context:** 주문·정산 데이터 대량 축적, 거래처별 차등 단가 등 복잡한 관계형 데이터, 전문 검색은 Elasticsearch로 분리
- **Decision:** PostgreSQL 16 (Azure Database for PostgreSQL Flexible Server)
- **Rationale:** JSONB (상품 속성, 견적 메타데이터), 테이블 파티셔닝 (정산 월별), 강력한 트랜잭션 (SERIALIZABLE 지원), Azure 네이티브 관리형 서비스
- **Consequences:** 정산 테이블 월별 파티셔닝으로 쿼리 성능 유지. Read Replica로 리포트 쿼리 분리
- **Alternatives:** MySQL (파티셔닝 제한적), Oracle (비용 과다), MongoDB (트랜잭션 약함)

### ADR-004: Search Engine — Elasticsearch 8.x

- **Context:** 100만 SKU 상품 검색, 자동완성, 카테고리·가격 필터, 한국어 형태소 분석 필요
- **Decision:** Elasticsearch 8.x (Azure 위 자체 운영, 3노드 클러스터)
- **Rationale:** 한국어 nori 분석기, 복합 필터·집계 지원, 자동완성 (completion suggester), 실시간 인덱싱
- **Consequences:** DB와 ES 간 데이터 동기화 필요 (이벤트 기반). 인프라 운영 부담 있으나 검색 품질 확보
- **Alternatives:** PostgreSQL tsvector (한국어 형태소 한계, 대규모 검색 부적합), Algolia (비용 높음, 자체 호스팅 불가), Azure Cognitive Search (nori 미지원)

### ADR-005: Frontend — Next.js 14 + TypeScript

- **Context:** 관리자 백오피스 + 바이어/공급사 포털, 복잡한 폼 및 테이블 UI
- **Decision:** Next.js 14 (App Router) + TypeScript + Tailwind CSS + Ant Design
- **Rationale:** React 생태계, SSR/SSG 선택적 활용, TypeScript 타입 안전성, Ant Design의 풍부한 B2B용 컴포넌트 (Table, Form, Steps)
- **Consequences:** 백오피스와 사용자 포털을 단일 Next.js 앱으로 통합 (라우팅 분리)
- **Alternatives:** Vue.js (React 대비 엔터프라이즈 생태계 약함), Angular (학습 곡선 높음)

### ADR-006: Messaging — Azure Service Bus

- **Context:** 주문 상태 변경 이벤트, 정산 배치 트리거, 알림 발송 등 비동기 처리 필요
- **Decision:** Azure Service Bus (Topics & Subscriptions)
- **Rationale:** Azure 네이티브, 메시지 순서 보장 (Sessions), Dead Letter Queue, 재시도 정책 내장
- **Consequences:** 주문 이벤트 발행 → 정산 모듈, 알림 모듈이 구독하여 처리. 느슨한 결합 달성
- **Alternatives:** Apache Kafka (소규모 과다), RabbitMQ (Azure 네이티브 아님), Azure Queue Storage (기능 제한)

### ADR-007: Infrastructure — Azure AKS + Helm

- **Context:** 컨테이너 기반 배포, 오토스케일링, 무중단 배포 필요
- **Decision:** Azure Kubernetes Service (AKS) + Helm Charts
- **Rationale:** 컨테이너 오케스트레이션 표준, 오토스케일링 (HPA), Rolling Update, Azure 서비스 네이티브 통합
- **Consequences:** Kubernetes 운영 경험 필요. Helm으로 환경별 설정 관리
- **Alternatives:** Azure App Service (커스터마이징 제한), Azure Container Apps (성숙도 부족), VM 직접 운영 (관리 부담)

## 4. Technology Stack

| Layer | Technology | Version | Justification |
|-------|-----------|---------|---------------|
| Frontend | Next.js + TypeScript | 14.x | React 생태계, SSR 옵션 |
| UI Components | Tailwind CSS + Ant Design | 3.x / 5.x | B2B 특화 컴포넌트 (Table, Form, Steps) |
| State Mgmt | Zustand + React Query | 4.x / 5.x | 경량 전역 상태 + 서버 상태 캐싱 |
| Backend | Spring Boot + Java | 3.x / 17 | 엔터프라이즈 트랜잭션 관리 |
| ORM | Spring Data JPA + Hibernate | 6.x | 타입 안전 쿼리, 관계 매핑 |
| Database | PostgreSQL | 16.x | JSONB + 파티셔닝 + 트랜잭션 |
| Search | Elasticsearch | 8.x | 한국어 nori, 자동완성, 집계 |
| Messaging | Azure Service Bus | — | 이벤트 기반 비동기 처리 |
| Auth | Spring Security + JWT | — | RBAC, 기업별 접근 제어 |
| Caching | Redis (Azure Cache) | 7.x | 세션, API 캐싱, 인기 상품 |
| Storage | Azure Blob Storage | — | 상품 이미지, 견적서 PDF |
| Hosting | Azure AKS | — | 컨테이너 오케스트레이션 |
| CI/CD | GitHub Actions + ArgoCD | — | GitOps 기반 배포 |
| Monitoring | Azure Monitor + Sentry | — | 메트릭 + 에러 추적 |

## 5. System Architecture

### 5.1 Component Diagram

```
┌──────────────┐     HTTPS      ┌─────────────────────────────────┐
│   Browser    │ ←────────────→ │   Next.js Frontend (AKS)        │
│  (Buyer /    │                │   ├── Buyer Portal               │
│   Supplier / │                │   ├── Supplier Portal            │
│   Admin)     │                │   └── Admin Back Office          │
└──────────────┘                └──────────┬──────────────────────┘
                                           │ REST API (JSON)
                                           ▼
                                ┌─────────────────────────────────┐
                                │     Spring Boot Backend (AKS)   │
                                ├─────────┬───────────┬───────────┤
                                │ Company │ Catalog   │ Quote     │
                                │ Module  │ Module    │ Module    │
                                ├─────────┼───────────┼───────────┤
                                │ Order   │ Settle-   │ Admin     │
                                │ Module  │ ment Mod  │ Module    │
                                └────┬────┴─────┬─────┴─────┬─────┘
                                     │          │           │
                          ┌──────────▼──┐  ┌────▼────┐  ┌───▼────────┐
                          │ PostgreSQL  │  │  Redis  │  │ Azure      │
                          │ (Azure DB)  │  │ (Cache) │  │ Service Bus│
                          └─────────────┘  └─────────┘  └────────────┘
                                     │                        │
                              ┌──────▼──────┐          ┌──────▼──────┐
                              │Elasticsearch│          │Azure Blob   │
                              │ (3-node)    │          │Storage      │
                              └─────────────┘          └─────────────┘
```

### 5.2 Data Flow (견적 → 주문 → 정산)

1. 바이어가 상품 검색 → Elasticsearch 쿼리 → 결과 반환
2. 바이어가 견적 요청 → POST /api/quotes/requests → DB 저장 + Service Bus 이벤트 발행
3. 공급사에 알림 → Service Bus 구독 → 푸시/이메일 알림 발송
4. 공급사가 견적서 작성 → POST /api/quotes → 견적서 PDF 생성 (Azure Blob 저장)
5. 바이어가 견적 비교 → 최적 견적 선택 → 발주 확정 (POST /api/orders)
6. 주문 이벤트 발행 → Service Bus → 재고 업데이트, 정산 대기열 등록
7. 공급사 출하 → 배송 정보 입력 → 바이어 수령 확인
8. 월말 정산 배치 → Spring Batch → 수령 확인된 주문 집계 → 정산서 생성

## 6. Data Architecture

### 6.1 Entity Relationship

```
Company (1) ──→ (N) User
    │                ├── id: BIGSERIAL PK
    │                ├── company_id: FK → companies.id
    │                ├── email: VARCHAR(255) UNIQUE
    │                ├── password_hash: VARCHAR(255)
    │                ├── name: VARCHAR(100)
    │                ├── role: VARCHAR(20) — BUYER/SUPPLIER/ADMIN
    │                └── created_at: TIMESTAMPTZ
    │
    ├──→ (N) Product
    │         ├── id: BIGSERIAL PK
    │         ├── company_id: FK → companies.id (공급사)
    │         ├── category_id: FK → categories.id
    │         ├── name: VARCHAR(500)
    │         ├── sku: VARCHAR(100) UNIQUE
    │         ├── description: TEXT
    │         ├── base_price: DECIMAL(15,2)
    │         ├── min_order_qty: INTEGER
    │         ├── status: VARCHAR(20) — ACTIVE/PAUSED/DISCONTINUED
    │         ├── attributes: JSONB — 규격, 사양 등 유동 속성
    │         ├── image_urls: JSONB — 이미지 URL 배열
    │         └── created_at: TIMESTAMPTZ
    │
    ├──→ (N) QuoteRequest
    │         ├── id: BIGSERIAL PK
    │         ├── buyer_company_id: FK → companies.id
    │         ├── supplier_company_id: FK → companies.id
    │         ├── status: VARCHAR(20) — PENDING/QUOTED/EXPIRED/ORDERED
    │         ├── desired_delivery_date: DATE
    │         ├── memo: TEXT
    │         ├── items: JSONB — [{product_id, qty, note}]
    │         └── expires_at: TIMESTAMPTZ
    │
    ├──→ (N) Order
    │         ├── id: BIGSERIAL PK
    │         ├── order_number: VARCHAR(20) UNIQUE
    │         ├── quote_id: FK → quote_requests.id
    │         ├── buyer_company_id: FK → companies.id
    │         ├── supplier_company_id: FK → companies.id
    │         ├── status: VARCHAR(20) — CONFIRMED/PREPARING/SHIPPED/DELIVERED/COMPLETED
    │         ├── total_amount: DECIMAL(15,2)
    │         ├── shipping_info: JSONB — {carrier, tracking_number, ...}
    │         ├── confirmed_at: TIMESTAMPTZ
    │         └── completed_at: TIMESTAMPTZ
    │
    └──→ (N) Settlement
              ├── id: BIGSERIAL PK
              ├── settlement_number: VARCHAR(20) UNIQUE
              ├── buyer_company_id: FK → companies.id
              ├── supplier_company_id: FK → companies.id
              ├── period_year: INTEGER
              ├── period_month: INTEGER
              ├── total_amount: DECIMAL(15,2)
              ├── commission_amount: DECIMAL(15,2)
              ├── net_amount: DECIMAL(15,2)
              ├── status: VARCHAR(20) — DRAFT/CONFIRMED/DISPUTED/PAID
              └── created_at: TIMESTAMPTZ

TradePartnership (거래 관계)
    ├── id: BIGSERIAL PK
    ├── buyer_company_id: FK → companies.id
    ├── supplier_company_id: FK → companies.id
    ├── grade: VARCHAR(20) — VIP/GENERAL/NEW
    ├── discount_rate: DECIMAL(5,2)
    ├── credit_limit: DECIMAL(15,2)
    ├── status: VARCHAR(20) — ACTIVE/SUSPENDED
    └── created_at: TIMESTAMPTZ

Category (계층형)
    ├── id: BIGSERIAL PK
    ├── parent_id: FK → categories.id (NULL이면 최상위)
    ├── name: VARCHAR(100)
    ├── depth: INTEGER — 1/2/3
    └── sort_order: INTEGER
```

### 6.2 Indexing Strategy

- `idx_products_company_status`: (company_id, status) — 공급사별 상품 조회
- `idx_products_category`: (category_id) — 카테고리별 필터
- `idx_orders_buyer_status`: (buyer_company_id, status, confirmed_at DESC) — 바이어 주문 목록
- `idx_orders_supplier_status`: (supplier_company_id, status) — 공급사 주문 관리
- `idx_settlements_period`: (period_year, period_month, buyer_company_id) — 월별 정산 조회
- `idx_trade_partnership`: UNIQUE(buyer_company_id, supplier_company_id) — 거래 관계 중복 방지

### 6.3 Partitioning Strategy

- `settlements` 테이블: 월별 파티셔닝 (period_year, period_month)
- `orders` 테이블: 연도별 파티셔닝 (confirmed_at 기준)
- `audit_logs` 테이블: 월별 파티셔닝 (created_at 기준)

## 7. API Design

### 7.1 API Style
RESTful JSON API. Spring Validation + DTO 패턴. API 버전 관리 (URI /api/v1/).

### 7.2 Endpoint Structure

| Method | Path | Description |
|--------|------|-------------|
| POST | /api/v1/auth/register | 기업 회원가입 (사업자번호 인증) |
| POST | /api/v1/auth/login | 로그인 → JWT 발급 |
| POST | /api/v1/auth/refresh | 토큰 갱신 |
| GET | /api/v1/companies/{id} | 기업 정보 조회 |
| PUT | /api/v1/companies/{id} | 기업 정보 수정 |
| POST | /api/v1/companies/{id}/invite | 직원 초대 |
| GET | /api/v1/products | 상품 목록 (검색 → Elasticsearch) |
| POST | /api/v1/products | 상품 등록 |
| GET | /api/v1/products/{id} | 상품 상세 |
| PUT | /api/v1/products/{id} | 상품 수정 |
| DELETE | /api/v1/products/{id} | 상품 삭제 (소프트) |
| GET | /api/v1/categories | 카테고리 트리 조회 |
| POST | /api/v1/quotes/requests | 견적 요청 생성 |
| GET | /api/v1/quotes/requests | 견적 요청 목록 |
| POST | /api/v1/quotes | 견적서 작성 (공급사) |
| GET | /api/v1/quotes/compare | 견적 비교 |
| POST | /api/v1/orders | 발주 확정 (견적 → 주문 전환) |
| GET | /api/v1/orders | 주문 목록 |
| PUT | /api/v1/orders/{id}/status | 주문 상태 변경 |
| PUT | /api/v1/orders/{id}/shipping | 배송 정보 입력 |
| POST | /api/v1/orders/{id}/confirm-receipt | 수령 확인 |
| GET | /api/v1/settlements | 정산 목록 |
| GET | /api/v1/settlements/{id} | 정산 상세 |
| POST | /api/v1/settlements/{id}/dispute | 정산 이의 제기 |
| GET | /api/v1/partners | 거래처 목록 |
| POST | /api/v1/partners | 거래 관계 요청 |
| PUT | /api/v1/partners/{id} | 거래처 등급/조건 수정 |
| GET | /api/v1/admin/companies/pending | 승인 대기 기업 목록 |
| PUT | /api/v1/admin/companies/{id}/approve | 기업 승인 |
| GET | /api/v1/admin/dashboard | 관리자 대시보드 |

### 7.3 Error Handling

```json
{
  "timestamp": "2026-03-23T10:15:30Z",
  "status": 400,
  "error": "Bad Request",
  "code": "QUOTE_EXPIRED",
  "message": "견적 유효기간이 만료되었습니다.",
  "path": "/api/v1/orders"
}
```
표준 HTTP 상태 코드 + 도메인 에러 코드. Spring @ControllerAdvice 글로벌 예외 처리.

## 8. Project Structure

```
tradehub/
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── (buyer)/          # 바이어 포털 라우트
│   │   │   ├── (supplier)/       # 공급사 포털 라우트
│   │   │   ├── (admin)/          # 관리자 백오피스 라우트
│   │   │   └── (auth)/           # 로그인/회원가입
│   │   ├── components/
│   │   │   ├── ui/               # 공통 UI 컴포넌트
│   │   │   ├── catalog/          # ProductCard, ProductTable, CategoryTree
│   │   │   ├── quote/            # QuoteRequestForm, QuoteCompareTable
│   │   │   ├── order/            # OrderStatusStepper, ShippingForm
│   │   │   ├── settlement/       # SettlementTable, DisputeForm
│   │   │   └── admin/            # CompanyApproval, Dashboard
│   │   ├── lib/                  # api.ts (axios), utils.ts
│   │   ├── stores/               # authStore, cartStore
│   │   └── types/                # TypeScript interfaces
│   └── package.json
├── backend/
│   ├── src/main/java/com/tradehub/
│   │   ├── TradeHubApplication.java
│   │   ├── company/
│   │   │   ├── controller/       # CompanyController.java
│   │   │   ├── service/          # CompanyService.java
│   │   │   ├── repository/       # CompanyRepository.java
│   │   │   ├── entity/           # Company.java, User.java
│   │   │   └── dto/              # CompanyDto.java, RegisterRequest.java
│   │   ├── catalog/
│   │   │   ├── controller/       # ProductController.java, CategoryController.java
│   │   │   ├── service/          # ProductService.java, SearchService.java
│   │   │   ├── repository/       # ProductRepository.java
│   │   │   ├── entity/           # Product.java, Category.java
│   │   │   └── dto/              # ProductDto.java, SearchRequest.java
│   │   ├── quote/
│   │   │   ├── controller/       # QuoteController.java
│   │   │   ├── service/          # QuoteService.java
│   │   │   ├── repository/       # QuoteRequestRepository.java
│   │   │   ├── entity/           # QuoteRequest.java, Quote.java
│   │   │   └── dto/              # QuoteRequestDto.java
│   │   ├── order/
│   │   │   ├── controller/       # OrderController.java
│   │   │   ├── service/          # OrderService.java
│   │   │   ├── repository/       # OrderRepository.java
│   │   │   ├── entity/           # Order.java, OrderItem.java
│   │   │   └── dto/              # OrderDto.java
│   │   ├── settlement/
│   │   │   ├── controller/       # SettlementController.java
│   │   │   ├── service/          # SettlementService.java
│   │   │   ├── batch/            # SettlementBatchJob.java
│   │   │   ├── repository/       # SettlementRepository.java
│   │   │   ├── entity/           # Settlement.java, SettlementItem.java
│   │   │   └── dto/              # SettlementDto.java
│   │   ├── partner/
│   │   │   ├── controller/       # PartnerController.java
│   │   │   ├── service/          # PartnerService.java
│   │   │   ├── repository/       # TradePartnershipRepository.java
│   │   │   ├── entity/           # TradePartnership.java
│   │   │   └── dto/              # PartnerDto.java
│   │   ├── admin/
│   │   │   ├── controller/       # AdminController.java
│   │   │   └── service/          # AdminService.java
│   │   └── global/
│   │       ├── config/           # SecurityConfig.java, ElasticsearchConfig.java
│   │       ├── security/         # JwtProvider.java, JwtFilter.java
│   │       ├── exception/        # GlobalExceptionHandler.java, ErrorCode.java
│   │       ├── audit/            # AuditLogInterceptor.java
│   │       └── event/            # OrderEvent.java, ServiceBusPublisher.java
│   ├── src/main/resources/
│   │   ├── application.yml
│   │   └── application-{profile}.yml
│   ├── src/test/java/com/tradehub/
│   └── build.gradle
├── infra/
│   ├── helm/                     # Helm charts
│   ├── terraform/                # Azure 인프라 IaC
│   └── docker-compose.yml        # 로컬 개발 환경
├── Dockerfile
└── .github/workflows/ci.yml
```

## 9. Security Architecture

### 9.1 Authentication & Authorization Flow
1. POST /auth/login → BCrypt 검증 → JWT access (1h) + refresh (14d) 발급
2. 모든 API 요청: Authorization: Bearer {access_token}
3. Spring Security Filter Chain: JWT 검증 → 사용자 정보 추출 → SecurityContext 설정
4. @PreAuthorize("hasRole('SUPPLIER')") — 역할 기반 접근 제어
5. 기업 간 데이터 격리: company_id 기반 필터링 (Row-Level Security 관점)

### 9.2 Role-Based Access Control (RBAC)

| Role | Permissions |
|------|------------|
| BUYER | 상품 검색, 견적 요청, 발주, 수령 확인, 정산 조회 |
| SUPPLIER | 상품 등록, 견적서 작성, 출하 처리, 정산 조회 |
| COMPANY_ADMIN | BUYER/SUPPLIER 전체 + 직원 관리, 거래처 관리, 기업 설정 |
| PLATFORM_ADMIN | 전체 관리 (기업 승인, 분쟁 조정, 수수료 관리, 통계) |

### 9.3 Data Protection
- 비밀번호: BCrypt (strength 12), 평문 저장 절대 금지
- API Key / Secret: Azure Key Vault
- HTTPS 전용, HSTS 헤더, Strict-Transport-Security
- CORS: 프론트엔드 도메인만 허용
- 감사 로그: 정산 변경, 단가 변경, 기업 승인/반려 등 주요 액션 기록

## 10. Infrastructure & DevOps

### 10.1 Environments

| Environment | Purpose | Configuration |
|------------|---------|---------------|
| Local | 개발 | Docker Compose (Spring Boot + PostgreSQL + ES + Redis) |
| Development | 통합 테스트 | AKS (1 node) + Azure DB (Basic) |
| Staging | QA/UAT | AKS (2 nodes) + Azure DB (Standard) |
| Production | 서비스 | AKS (3 nodes, HPA) + Azure DB (High Availability) |

### 10.2 Deployment Strategy
- GitHub Actions: PR → lint + test + SonarQube → Development 자동 배포
- Release branch → Staging 배포 → QA 통과 → Production 배포 (수동 승인)
- ArgoCD: GitOps 기반 Kubernetes 배포 관리
- Rolling Update + Readiness Probe (무중단 배포)

### 10.3 Monitoring
- Azure Monitor: API 지표, 에러율, 응답시간, 컨테이너 리소스
- Application Insights: 분산 트레이싱, 의존성 맵
- Sentry: 에러 추적 + 알림 (Slack 연동)
- Elasticsearch: 검색 품질 모니터링 (검색 성공률, 무결과 쿼리)
- Grafana: PostgreSQL 슬로우 쿼리, Service Bus 대기열 모니터링
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
# Epics & Stories - TradeHub

**Date:** 2026-03-23
**Status:** Complete

---

## Requirements Inventory

### Functional Requirements (from PRD)

| FR ID | Description | Priority | Epic |
|-------|------------|----------|------|
| FR-001~005 | 기업 인증 및 계정 관리 | Must | E-001 |
| FR-010~015 | 상품 카탈로그 | Must | E-002 |
| FR-020~024 | 견적 관리 | Must | E-003 |
| FR-030~033 | 주문 관리 | Must | E-004 |
| FR-040~043 | 정산 | Must | E-005 |
| FR-050~052 | 거래처 관리 | Must | E-006 |
| FR-060~064 | 관리자 백오피스 | Must | E-007 |

## FR Coverage Map

| FR ID | Epic | Story | Status |
|-------|------|-------|--------|
| FR-001 | E-001 | S-001 | Covered |
| FR-002 | E-001 | S-001 | Covered |
| FR-003 | E-001 | S-002 | Covered |
| FR-004 | E-001 | S-002 | Covered |
| FR-005 | E-001 | S-002 | Covered |
| FR-010 | E-002 | S-003 | Covered |
| FR-011 | E-002 | S-003 | Covered |
| FR-012 | E-002 | S-004 | Covered |
| FR-013 | E-002 | S-005 | Covered |
| FR-014 | E-002 | S-003 | Covered |
| FR-015 | E-002 | S-005 | Covered |
| FR-020 | E-003 | S-006 | Covered |
| FR-021 | E-003 | S-007 | Covered |
| FR-022 | E-003 | S-007 | Covered |
| FR-023 | E-003 | S-007 | Covered |
| FR-024 | E-003 | S-006 | Covered |
| FR-030 | E-004 | S-008 | Covered |
| FR-031 | E-004 | S-008 | Covered |
| FR-032 | E-004 | S-009 | Covered |
| FR-033 | E-004 | S-009 | Covered |
| FR-040 | E-005 | S-010 | Covered |
| FR-041 | E-005 | S-010 | Covered |
| FR-042 | E-005 | S-011 | Covered |
| FR-043 | E-005 | S-010 | Covered |
| FR-050 | E-006 | S-012 | Covered |
| FR-051 | E-006 | S-012 | Covered |
| FR-052 | E-006 | S-012 | Covered |
| FR-060 | E-007 | S-013 | Covered |
| FR-061 | E-007 | S-014 | Covered |
| FR-062 | E-007 | S-014 | Covered |
| FR-063 | E-007 | S-013 | Covered |
| FR-064 | E-007 | S-013 | Covered |

---

## Epic 1: 기업 인증 및 계정 관리

**ID:** E-001 | **Priority:** Must | **Phase:** MVP | **Complexity:** M | **Dependencies:** None

### Description
사업자등록번호 기반 기업 회원가입, 관리자 승인, 직원 초대, JWT 인증. 기업별 데이터 격리의 기반.

### Stories

#### Story 1.1: 기업 회원가입 및 인증

**ID:** S-001 | **Points:** 8

**As a** 기업 관리자,
**I want** 사업자등록번호로 기업을 등록하고 인증받고 싶다,
**So that** TradeHub 플랫폼에서 거래를 시작할 수 있다.

**Acceptance Criteria:**

```gherkin
Given 회원가입 페이지에 접속한 상태에서
When 사업자등록번호(10자리)를 입력하면
Then 국세청 API로 유효성을 검증하고 기업명·대표자명이 자동 조회된다

Given 유효한 사업자 정보와 관리자 이메일/비밀번호를 입력하고
When 가입 버튼을 클릭하면
Then 기업 계정이 생성되고 "승인 대기 중" 상태로 등록된다

Given 관리자가 기업 가입을 승인하면
When 기업 관리자에게 승인 알림이 발송되고
Then 해당 기업 계정으로 로그인하여 서비스 이용이 가능하다

Given 이미 등록된 사업자번호로 가입을 시도하면
When 가입 버튼을 클릭하면
Then "이미 등록된 사업자입니다" 에러가 표시된다
```

**Tasks:**
- [ ] Company JPA 엔티티 생성 (id, business_number, name, representative, status, ...)
- [ ] User JPA 엔티티 생성 (id, company_id, email, password_hash, role, ...)
- [ ] POST /api/v1/auth/register 엔드포인트 구현
- [ ] 사업자등록번호 유효성 검증 서비스 (국세청 API 연동 또는 Validation)
- [ ] RegisterRequest/RegisterResponse DTO
- [ ] BCrypt 비밀번호 해싱
- [ ] 프론트엔드 회원가입 폼 (사업자번호 입력 → 자동 조회 → 관리자 정보 입력)
- [ ] 단위 테스트 (중복 사업자번호, 잘못된 형식, 승인 전 로그인 차단)

#### Story 1.2: 로그인/로그아웃 및 직원 관리

**ID:** S-002 | **Points:** 8

**As a** 기업 소속 직원,
**I want** 이메일로 로그인하고 역할에 맞는 기능을 사용하고 싶다,
**So that** 업무에 필요한 기능만 안전하게 접근할 수 있다.

**Acceptance Criteria:**

```gherkin
Given 승인된 기업의 직원 계정으로
When 올바른 이메일과 비밀번호를 입력하면
Then JWT access token(1시간)과 refresh token(14일)이 발급되고 포털로 이동한다

Given 기업 관리자가 직원 초대 페이지에서
When 직원 이메일과 역할(구매/영업)을 입력하고 초대하면
Then 해당 이메일로 초대 링크가 발송되고 가입 시 해당 기업·역할로 자동 연결된다

Given BUYER 역할의 사용자가
When 상품 등록 API에 접근하면
Then 403 Forbidden 에러가 반환된다
```

**Tasks:**
- [ ] Spring Security + JWT 설정 (JwtProvider, JwtFilter)
- [ ] POST /api/v1/auth/login, /api/v1/auth/refresh 구현
- [ ] RBAC 설정 (@PreAuthorize, SecurityConfig)
- [ ] POST /api/v1/companies/{id}/invite 직원 초대 API
- [ ] 이메일 초대 링크 생성 (Redis 기반 토큰)
- [ ] 프론트엔드 로그인 폼 + 역할별 라우팅
- [ ] 직원 관리 페이지 (초대, 역할 변경, 비활성화)

---

## Epic 2: 상품 카탈로그

**ID:** E-002 | **Priority:** Must | **Phase:** MVP | **Complexity:** L | **Dependencies:** E-001

### Description
공급사의 상품 등록·관리, 계층형 카테고리, Elasticsearch 기반 검색, 거래처별 차등 단가.

### Stories

#### Story 2.1: 상품 등록 및 관리

**ID:** S-003 | **Points:** 8

**As a** 공급사 영업 담당자,
**I want** 상품을 등록하고 관리하고 싶다,
**So that** 바이어가 카탈로그에서 우리 상품을 검색하고 주문할 수 있다.

**Acceptance Criteria:**

```gherkin
Given 공급사 포털의 상품 관리 페이지에서
When 상품명, SKU, 카테고리, 기본 단가, 최소 주문 수량, 이미지를 입력하고 등록하면
Then 상품이 DB에 저장되고 Elasticsearch에 인덱싱되어 검색 가능해진다

Given 등록된 상품에서
When 상태를 "판매중"에서 "일시중지"로 변경하면
Then 바이어 검색 결과에서 해당 상품이 제외된다

Given 3단계 카테고리 트리에서
When "산업용품 > 베어링 > 볼베어링"을 선택하면
Then 해당 카테고리로 상품이 분류된다
```

**Tasks:**
- [ ] Product JPA 엔티티 생성
- [ ] Category JPA 엔티티 (self-referencing, parent_id)
- [ ] POST /api/v1/products 상품 등록 API
- [ ] 이미지 업로드 → Azure Blob Storage 저장
- [ ] Elasticsearch 인덱스 생성 (nori analyzer 설정)
- [ ] 상품 저장 시 ES 동기화 (이벤트 기반)
- [ ] GET /api/v1/categories 카테고리 트리 API
- [ ] 프론트엔드 상품 등록 폼 (이미지 드래그 앤 드롭, 카테고리 트리 선택)
- [ ] 상품 목록/상세 페이지 (공급사 포털)

#### Story 2.2: 상품 검색

**ID:** S-004 | **Points:** 8

**As a** 바이어 구매 담당자,
**I want** 키워드와 필터로 상품을 검색하고 싶다,
**So that** 필요한 자재를 빠르게 찾아 견적을 요청할 수 있다.

**Acceptance Criteria:**

```gherkin
Given 상품 검색 페이지에서
When "스테인리스 볼트 M10"을 검색하면
Then Elasticsearch가 한국어 형태소 분석으로 관련 상품을 반환하고 관련도 순 정렬된다

Given 검색 결과에서
When 카테고리 "체결부품", 가격 "1,000원~5,000원" 필터를 적용하면
Then 조건에 맞는 상품만 표시된다

Given 검색 입력창에 "스테인"을 입력하면
When 자동완성 제안이 표시되고
Then "스테인리스 볼트", "스테인리스 너트", "스테인리스 파이프" 등이 표시된다
```

**Tasks:**
- [ ] Elasticsearch SearchService 구현 (multi_match, bool query)
- [ ] nori 한국어 분석기 인덱스 설정
- [ ] 자동완성 API (completion suggester)
- [ ] 카테고리·가격·공급사 필터 (aggregation)
- [ ] GET /api/v1/products 검색 API (ES 기반)
- [ ] 프론트엔드 검색 UI (검색바, 필터 사이드바, 결과 그리드/리스트)

#### Story 2.3: 거래처별 차등 단가 및 대량 등록

**ID:** S-005 | **Points:** 5

**As a** 공급사,
**I want** 거래처별로 다른 단가를 설정하고 대량으로 상품을 등록하고 싶다,
**So that** 거래 관계에 맞는 가격 정책을 적용하고 효율적으로 상품을 관리할 수 있다.

**Acceptance Criteria:**

```gherkin
Given 상품 상세 페이지에서 단가 설정 탭에서
When 거래처 "A제조"에 특별 단가 8,500원(기본가 10,000원)을 지정하면
Then "A제조" 담당자가 해당 상품 조회 시 8,500원이 표시된다

Given Excel 템플릿을 다운로드하고 500개 상품을 작성하여 업로드하면
When 검증 후 등록이 완료되면
Then 500개 상품이 일괄 등록되고 오류 항목은 리포트로 제공된다
```

**Tasks:**
- [ ] ProductPrice 엔티티 (product_id, partner_company_id, special_price)
- [ ] 거래처별 단가 조회 로직 (특별 단가 > 등급별 할인 > 기본 단가)
- [ ] Excel 템플릿 생성/다운로드 API
- [ ] Excel 업로드 → 검증 → 일괄 등록 (Apache POI)
- [ ] 오류 리포트 Excel 생성

---

## Epic 3: 견적 관리

**ID:** E-003 | **Priority:** Must | **Phase:** MVP | **Complexity:** L | **Dependencies:** E-002

### Description
바이어의 견적 요청, 공급사의 견적서 작성, 견적 비교, 유효기간 관리.

### Stories

#### Story 3.1: 견적 요청

**ID:** S-006 | **Points:** 8

**As a** 바이어 구매 담당자,
**I want** 필요한 상품에 대해 공급사에 견적을 요청하고 싶다,
**So that** 최적의 단가와 조건을 비교하여 발주할 수 있다.

**Acceptance Criteria:**

```gherkin
Given 상품 검색 결과에서 3개 상품을 선택하고
When 공급사 A, B에 동시 견적 요청을 생성하면
Then 2개의 견적 요청이 생성되고 각 공급사에 알림이 발송된다

Given 견적 요청에 희망 납기일과 메모를 입력하고
When 견적 요청을 전송하면
Then 공급사의 견적 요청 수신함에 요청이 표시된다

Given 견적 유효기간을 7일로 설정하고
When 7일이 경과하면
Then 해당 견적 요청의 상태가 자동으로 "만료"로 변경된다
```

**Tasks:**
- [ ] QuoteRequest JPA 엔티티 생성
- [ ] POST /api/v1/quotes/requests 견적 요청 API
- [ ] 복수 공급사 동시 견적 요청 로직
- [ ] Service Bus 이벤트 발행 (QUOTE_REQUESTED)
- [ ] 견적 유효기간 스케줄러 (@Scheduled → 만료 처리)
- [ ] 프론트엔드 견적 요청 폼 (상품 선택 → 수량 → 납기 → 공급사 선택)
- [ ] 견적 요청 목록/상세 페이지 (바이어/공급사 양쪽)

#### Story 3.2: 견적서 작성 및 비교

**ID:** S-007 | **Points:** 8

**As a** 공급사 영업 담당자,
**I want** 견적 요청에 대해 견적서를 작성하고 싶다,
**So that** 바이어에게 단가와 조건을 제안할 수 있다.

**As a** 바이어,
**I want** 복수 견적서를 비교하고 싶다,
**So that** 최적의 공급사를 선택하여 발주할 수 있다.

**Acceptance Criteria:**

```gherkin
Given 공급사가 견적 요청을 확인하고
When 품목별 단가, 납기일, 결제조건(월말 정산/선급)을 입력하여 견적서를 작성하면
Then 견적서 PDF가 자동 생성되고 바이어에게 알림이 발송된다

Given 동일 견적 요청에 대해 2개 이상의 견적서가 도착했을 때
When 바이어가 견적 비교 페이지에 접속하면
Then 품목별 단가, 납기, 결제조건이 테이블로 비교 표시된다

Given 바이어가 견적 조건 수정을 요청하면
When 공급사가 수정된 견적서를 재발송하면
Then 견적 협상 이력이 타임라인으로 기록된다
```

**Tasks:**
- [ ] Quote JPA 엔티티 (quote_request_id, items, terms, ...)
- [ ] POST /api/v1/quotes 견적서 작성 API
- [ ] 견적서 PDF 생성 (iText/JasperReports → Azure Blob 저장)
- [ ] GET /api/v1/quotes/compare 견적 비교 API
- [ ] 카운터 오퍼 (견적 수정 요청/재발송) 로직
- [ ] 견적 협상 이력 저장 (QuoteHistory 엔티티)
- [ ] 프론트엔드 견적서 작성 폼, 비교 테이블, 협상 타임라인

---

## Epic 4: 주문 관리

**ID:** E-004 | **Priority:** Must | **Phase:** MVP | **Complexity:** L | **Dependencies:** E-003

### Description
견적 기반 발주 확정, 주문 상태 관리 (상태 머신), 배송 추적, 수령 확인.

### Stories

#### Story 4.1: 발주 확정 및 주문 상태 관리

**ID:** S-008 | **Points:** 8

**As a** 바이어,
**I want** 견적서를 확인하고 발주를 확정하고 싶다,
**So that** 공급사에 정식으로 구매를 요청할 수 있다.

**Acceptance Criteria:**

```gherkin
Given 견적 비교 후 공급사 A의 견적을 선택하고
When "발주 확정" 버튼을 클릭하면
Then 주문번호가 자동 생성(TH-2026-000001)되고 공급사에 발주 확인 알림이 발송된다

Given 발주가 확정된 상태에서
When 공급사가 "주문 확인"을 클릭하면
Then 주문 상태가 "발주접수" → "주문확인"으로 변경되고 바이어에게 알림된다

Given 주문 상태가 "주문확인"인 상태에서
When "배송중"으로 건너뛰고 상태를 변경하려 하면
Then "출하준비 → 출하완료 단계를 먼저 진행하세요" 에러가 표시된다
```

**Tasks:**
- [ ] Order JPA 엔티티 + OrderItem 엔티티
- [ ] 주문 상태 머신 (State Machine) 구현 (Spring Statemachine 또는 Enum 기반)
- [ ] POST /api/v1/orders 발주 확정 API (Quote → Order 변환)
- [ ] PUT /api/v1/orders/{id}/status 상태 변경 API (상태 전이 검증)
- [ ] 주문번호 자동 생성 (TH-YYYY-NNNNNN 형식)
- [ ] Service Bus 이벤트 발행 (ORDER_CONFIRMED, STATUS_CHANGED)
- [ ] 프론트엔드 주문 목록, 주문 상세, 상태 Stepper 컴포넌트

#### Story 4.2: 배송 관리 및 수령 확인

**ID:** S-009 | **Points:** 5

**As a** 공급사,
**I want** 출하 후 배송 정보를 입력하고 싶다,
**So that** 바이어가 배송 상황을 추적할 수 있다.

**As a** 바이어,
**I want** 상품 수령 후 확인 처리를 하고 싶다,
**So that** 정산 프로세스가 진행될 수 있다.

**Acceptance Criteria:**

```gherkin
Given 주문 상태가 "출하완료"인 상태에서
When 공급사가 택배사(CJ대한통운)와 송장번호(123456789)를 입력하면
Then 상태가 "배송중"으로 변경되고 바이어에게 배송 시작 알림이 발송된다

Given 상품이 도착하여 검수가 완료된 상태에서
When 바이어가 "수령 확인" 버튼을 클릭하면
Then 주문 상태가 "수령확인"으로 변경되고 해당 주문이 이번 달 정산 대상에 포함된다

Given 납품된 상품에 불량이 있는 경우
When 바이어가 "반품/교환 요청"을 하면
Then 반품 사유와 이미지가 기록되고 공급사에 알림이 발송된다
```

**Tasks:**
- [ ] PUT /api/v1/orders/{id}/shipping 배송 정보 입력 API
- [ ] 택배사 API 연동 (배송 상태 조회)
- [ ] POST /api/v1/orders/{id}/confirm-receipt 수령 확인 API
- [ ] 수령 확인 시 정산 대상 플래그 설정
- [ ] 반품/교환 요청 로직 (ReturnRequest 엔티티)
- [ ] 프론트엔드 배송 정보 입력 폼, 배송 추적 UI, 수령 확인 버튼

---

## Epic 5: 정산

**ID:** E-005 | **Priority:** Must | **Phase:** MVP | **Complexity:** XL | **Dependencies:** E-004

### Description
월별 자동 정산 (Spring Batch), 정산서 생성, 수수료 계산, 이의 제기 처리.

### Stories

#### Story 5.1: 월별 자동 정산 및 정산서

**ID:** S-010 | **Points:** 13

**As a** 플랫폼 운영팀,
**I want** 매월 자동으로 거래를 정산하고 정산서를 생성하고 싶다,
**So that** 수작업 없이 정확한 정산이 이루어질 수 있다.

**Acceptance Criteria:**

```gherkin
Given 3월에 수령 확인된 주문이 A공급사 50건(총 2,500만 원), B공급사 30건(총 1,200만 원)인 상태에서
When 4월 1일 00:00에 정산 배치가 실행되면
Then A공급사 정산서(총액 2,500만 원, 수수료 50만 원, 정산액 2,450만 원)와 B공급사 정산서가 자동 생성된다

Given 정산서가 생성된 상태에서
When 공급사가 정산 상세 페이지에서 "PDF 다운로드"를 클릭하면
Then 거래 내역이 포함된 정산서 PDF가 다운로드된다

Given 기업 등급이 VIP(수수료 1.5%)인 공급사에 대해
When 정산 금액을 계산하면
Then 기본 수수료(2%) 대신 VIP 수수료(1.5%)가 적용된다
```

**Tasks:**
- [ ] Settlement, SettlementItem JPA 엔티티
- [ ] Spring Batch Job (SettlementBatchJob): 월별 정산 집계
- [ ] 수수료 계산 로직 (기본 2%, 등급별 차등)
- [ ] 정산서 PDF 생성 (거래 내역 포함)
- [ ] GET /api/v1/settlements 정산 목록 API
- [ ] GET /api/v1/settlements/{id} 정산 상세 API
- [ ] 정산 감사 로그 (모든 계산 과정 기록)
- [ ] 정산 이중 검증 (집계 결과 크로스체크)
- [ ] 프론트엔드 정산 목록, 상세, PDF 다운로드

#### Story 5.2: 정산 이의 제기

**ID:** S-011 | **Points:** 5

**As a** 공급사 또는 바이어,
**I want** 정산 내역에 이의를 제기하고 싶다,
**So that** 오류가 있는 정산을 수정받을 수 있다.

**Acceptance Criteria:**

```gherkin
Given 정산 상세 페이지에서 특정 거래 항목을 선택하고
When 이의 사유("단가 불일치, 협의 단가 8,500원이 아닌 10,000원 적용됨")를 작성하여 제출하면
Then 해당 정산 항목이 "분쟁 중" 상태로 변경되고 관리자에게 조정 요청이 전달된다

Given 관리자가 분쟁을 검토하고 조정 결과를 입력하면
When 조정이 확정되면
Then 정산 금액이 수정되고 양측에 조정 결과 알림이 발송된다
```

**Tasks:**
- [ ] POST /api/v1/settlements/{id}/dispute 이의 제기 API
- [ ] SettlementDispute 엔티티 (settlement_id, item_id, reason, status, resolution)
- [ ] 관리자 분쟁 조정 API + UI
- [ ] 정산 금액 재계산 로직
- [ ] 분쟁 이력 감사 로그

---

## Epic 6: 거래처 관리

**ID:** E-006 | **Priority:** Must | **Phase:** MVP | **Complexity:** M | **Dependencies:** E-001

### Description
거래처 등록·승인, 등급 관리, 거래 이력 조회.

### Stories

#### Story 6.1: 거래처 등록 및 관리

**ID:** S-012 | **Points:** 8

**As a** 기업 관리자,
**I want** 거래처를 등록하고 등급·조건을 관리하고 싶다,
**So that** 거래처별 맞춤 가격 정책과 결제 조건을 적용할 수 있다.

**Acceptance Criteria:**

```gherkin
Given 거래처 관리 페이지에서 사업자번호로 거래처를 검색하고
When "거래 관계 요청"을 클릭하면
Then 상대 기업에 거래 관계 요청 알림이 발송되고 승인 시 거래 관계가 수립된다

Given 거래처 상세 페이지에서
When 등급을 "일반"에서 "VIP"로 변경하면
Then 해당 거래처에 VIP 할인율과 결제조건이 자동 적용된다

Given 거래처 이력 탭에서
When 최근 12개월 거래 현황을 조회하면
Then 월별 주문 건수, 거래 금액 추이가 차트로 표시된다
```

**Tasks:**
- [ ] TradePartnership JPA 엔티티
- [ ] POST /api/v1/partners 거래 관계 요청 API
- [ ] 거래 관계 승인/거절 API
- [ ] PUT /api/v1/partners/{id} 등급·조건 변경 API
- [ ] GET /api/v1/partners 거래처 목록 (필터: 등급, 상태)
- [ ] 거래 이력 집계 쿼리 (월별 주문 건수, 금액)
- [ ] 프론트엔드 거래처 관리 (목록, 상세, 등급 변경, 이력 차트)

---

## Epic 7: 관리자 백오피스

**ID:** E-007 | **Priority:** Must | **Phase:** MVP | **Complexity:** M | **Dependencies:** E-001, E-005

### Description
플랫폼 관리자의 기업 승인, 거래 모니터링, 분쟁 조정, 시스템 설정.

### Stories

#### Story 7.1: 기업 승인 및 시스템 설정

**ID:** S-013 | **Points:** 5

**As a** 플랫폼 관리자,
**I want** 가입한 기업을 심사하고 승인/반려하고 싶다,
**So that** 신뢰할 수 있는 기업만 플랫폼에서 거래할 수 있다.

**Acceptance Criteria:**

```gherkin
Given 승인 대기 기업 목록에서 기업 정보를 확인하고
When 사업자등록증과 기업 정보를 심사하여 "승인" 버튼을 클릭하면
Then 해당 기업의 상태가 "활성"으로 변경되고 기업 관리자에게 승인 알림이 발송된다

Given 시스템 설정 페이지에서
When 기본 수수료율을 2.0%에서 1.8%로 변경하면
Then 다음 정산부터 변경된 수수료율이 적용되고 변경 이력이 기록된다
```

**Tasks:**
- [ ] GET /api/v1/admin/companies/pending 승인 대기 목록 API
- [ ] PUT /api/v1/admin/companies/{id}/approve 승인/반려 API
- [ ] 수수료 정책 관리 API (기본률, 기업별, 카테고리별)
- [ ] 카테고리 CRUD API (관리자 전용)
- [ ] 공지사항, 약관 관리 API
- [ ] 프론트엔드 관리자 백오피스 (기업 승인, 시스템 설정)

#### Story 7.2: 거래 모니터링 및 분쟁 조정

**ID:** S-014 | **Points:** 5

**As a** 플랫폼 관리자,
**I want** 전체 거래 현황을 모니터링하고 분쟁을 조정하고 싶다,
**So that** 플랫폼의 건전한 거래 환경을 유지할 수 있다.

**Acceptance Criteria:**

```gherkin
Given 관리자 대시보드에 접속하면
When 페이지가 로드되면
Then 일/주/월 GMV, 거래 건수, 신규 가입 기업 수, 분쟁 건수가 카드로 표시된다

Given 분쟁 목록에서 특정 분쟁을 선택하고
When 양측 의견과 거래 내역을 확인 후 조정 결과를 입력하면
Then 정산에 반영되고 양측에 조정 결과 알림이 발송된다
```

**Tasks:**
- [ ] GET /api/v1/admin/dashboard 대시보드 API (GMV, 거래건수, 가입기업, 분쟁)
- [ ] 일/주/월 통계 집계 쿼리
- [ ] 분쟁 목록/상세/조정 API
- [ ] 프론트엔드 관리자 대시보드 (카드, 차트)
- [ ] 분쟁 조정 UI (타임라인, 조정 입력)

---

## Summary

| Metric | Value |
|--------|-------|
| Total Epics | 7 |
| Total Stories | 14 |
| Total Story Points | 102 |
| Must-Have Points | 102 |
| Sprint 1 Target | E-001 (16pt) |
| Sprint 2 Target | E-002 (21pt) |
| Sprint 3 Target | E-003 + E-006 (24pt) |
| Sprint 4 Target | E-004 (13pt) |
| Sprint 5 Target | E-005 (18pt) |
| Sprint 6 Target | E-007 + 통합 테스트 + 배포 (10pt+) |
""",
    },
    {
        "file_name": "project-context.md",
        "file_path": "planning-artifacts/project-context.md",
        "content": """---
workflowType: 'project-context'
---
# Project Context - TradeHub

## Technology Stack & Versions

| Technology | Version | Purpose |
|-----------|---------|---------|
| Java | 17 (LTS) | 백엔드 런타임 |
| Spring Boot | 3.x | 엔터프라이즈 웹 프레임워크 |
| Spring Data JPA | 3.x | ORM (Hibernate 6) |
| Spring Security | 6.x | 인증·인가 (JWT + RBAC) |
| Spring Batch | 5.x | 정산 배치 처리 |
| Flyway | 10.x | DB 마이그레이션 |
| PostgreSQL | 16.x | 관계형 데이터베이스 |
| Elasticsearch | 8.x | 상품 검색 엔진 (nori 분석기) |
| Redis | 7.x | 캐싱, 세션, 분산 락 |
| Azure Service Bus | — | 이벤트 기반 비동기 메시징 |
| Next.js | 14.x | 프론트엔드 프레임워크 |
| TypeScript | 5.x | 타입 안전성 |
| Tailwind CSS | 3.x | 유틸리티 퍼스트 CSS |
| Ant Design | 5.x | B2B 특화 UI 컴포넌트 |
| Zustand | 4.x | 전역 상태 관리 |
| React Query | 5.x | 서버 상태 캐싱 |
| Docker | latest | 컨테이너화 |
| Azure AKS | — | 컨테이너 오케스트레이션 |
| Azure Database for PostgreSQL | — | 관리형 PostgreSQL |
| Azure Blob Storage | — | 이미지, PDF 파일 저장 |
| Azure Key Vault | — | 시크릿 관리 |

## Critical Implementation Rules

1. **모든 정산 로직은 이중 검증한다** — 배치 집계 결과와 개별 합산 결과를 크로스체크. 불일치 시 정산 생성 중단 + 알림.
2. **주문 상태 변경은 상태 머신으로 제어한다** — 허용되지 않은 상태 전이 시도 시 예외 발생. 상태 이력 기록 필수.
3. **기업 간 데이터 격리를 보장한다** — 모든 쿼리에 company_id 조건 포함. @CompanyScope 커스텀 어노테이션 활용.
4. **비밀번호는 BCrypt (strength 12)로 해싱** — 평문 저장 절대 금지.
5. **환경변수에 시크릿 저장** — Azure Key Vault에서 주입. 코드/로그에 노출 금지.
6. **소프트 삭제를 기본으로** — deleted_at 필드 (NULL이면 활성). @SQLRestriction 활용.
7. **감사 로그 필수** — 정산 변경, 단가 변경, 기업 승인/반려, 주문 상태 변경 시 audit_logs 테이블 기록.
8. **Elasticsearch와 DB 동기화** — 상품 변경 시 이벤트 발행 → ES 인덱스 업데이트. 최종 일관성 허용 (eventual consistency).
9. **API 버전 관리** — URI 기반 /api/v1/. 하위 호환성 보장.
10. **프론트엔드 서버 상태는 React Query** — useState로 API 데이터 관리 금지. 전역 상태는 Zustand (인증 정보, UI 상태만).

## Project Structure

```
tradehub/
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── (auth)/           # 로그인, 회원가입
│   │   │   ├── (buyer)/          # 바이어 포털 (검색, 견적, 주문, 정산)
│   │   │   ├── (supplier)/       # 공급사 포털 (상품, 견적, 주문, 정산)
│   │   │   └── (admin)/          # 관리자 백오피스
│   │   ├── components/
│   │   │   ├── ui/               # 공통 UI (Button, Modal, Table wrapper)
│   │   │   ├── catalog/          # ProductCard, ProductTable, CategoryTree, SearchBar
│   │   │   ├── quote/            # QuoteRequestForm, QuoteCompareTable, QuoteTimeline
│   │   │   ├── order/            # OrderStatusStepper, ShippingForm, ReceiptConfirm
│   │   │   ├── settlement/       # SettlementTable, SettlementDetail, DisputeForm
│   │   │   ├── partner/          # PartnerList, PartnerGradeBadge, TradeHistoryChart
│   │   │   └── admin/            # CompanyApprovalTable, AdminDashboard, CommissionConfig
│   │   ├── lib/                  # api.ts (axios instance), utils.ts, constants.ts
│   │   ├── hooks/                # useAuth, useProducts, useOrders (React Query hooks)
│   │   ├── stores/               # authStore.ts, uiStore.ts
│   │   └── types/                # company.ts, product.ts, order.ts, settlement.ts
│   ├── public/
│   └── package.json
├── backend/
│   ├── src/main/java/com/tradehub/
│   │   ├── TradeHubApplication.java
│   │   ├── company/
│   │   │   ├── controller/       # CompanyController, AuthController
│   │   │   ├── service/          # CompanyService, AuthService
│   │   │   ├── repository/       # CompanyRepository, UserRepository
│   │   │   ├── entity/           # Company, User
│   │   │   └── dto/              # RegisterRequest, LoginRequest, CompanyResponse
│   │   ├── catalog/
│   │   │   ├── controller/       # ProductController, CategoryController
│   │   │   ├── service/          # ProductService, SearchService, CategoryService
│   │   │   ├── repository/       # ProductRepository, CategoryRepository
│   │   │   ├── entity/           # Product, Category, ProductPrice
│   │   │   └── dto/              # ProductCreateRequest, SearchRequest, ProductResponse
│   │   ├── quote/
│   │   │   ├── controller/       # QuoteController
│   │   │   ├── service/          # QuoteService
│   │   │   ├── repository/       # QuoteRequestRepository, QuoteRepository
│   │   │   ├── entity/           # QuoteRequest, Quote, QuoteHistory
│   │   │   └── dto/              # QuoteRequestDto, QuoteDto
│   │   ├── order/
│   │   │   ├── controller/       # OrderController
│   │   │   ├── service/          # OrderService, ShippingService
│   │   │   ├── repository/       # OrderRepository, OrderItemRepository
│   │   │   ├── entity/           # Order, OrderItem, ReturnRequest
│   │   │   ├── dto/              # OrderDto, ShippingDto
│   │   │   └── statemachine/     # OrderStatus, OrderStateMachine
│   │   ├── settlement/
│   │   │   ├── controller/       # SettlementController
│   │   │   ├── service/          # SettlementService
│   │   │   ├── batch/            # SettlementBatchConfig, SettlementItemReader/Writer
│   │   │   ├── repository/       # SettlementRepository, SettlementDisputeRepository
│   │   │   ├── entity/           # Settlement, SettlementItem, SettlementDispute
│   │   │   └── dto/              # SettlementDto, DisputeDto
│   │   ├── partner/
│   │   │   ├── controller/       # PartnerController
│   │   │   ├── service/          # PartnerService
│   │   │   ├── repository/       # TradePartnershipRepository
│   │   │   ├── entity/           # TradePartnership
│   │   │   └── dto/              # PartnerDto
│   │   ├── admin/
│   │   │   ├── controller/       # AdminController
│   │   │   └── service/          # AdminService, DashboardService
│   │   └── global/
│   │       ├── config/           # SecurityConfig, ElasticsearchConfig, ServiceBusConfig, BatchConfig
│   │       ├── security/         # JwtProvider, JwtFilter, CompanyScope
│   │       ├── exception/        # GlobalExceptionHandler, ErrorCode, BusinessException
│   │       ├── audit/            # AuditLogInterceptor, AuditLog entity
│   │       └── event/            # DomainEvent, ServiceBusPublisher, EventSubscriber
│   ├── src/main/resources/
│   │   ├── application.yml
│   │   ├── application-local.yml
│   │   ├── application-dev.yml
│   │   ├── application-staging.yml
│   │   └── application-prod.yml
│   ├── src/test/java/com/tradehub/
│   │   ├── company/              # AuthServiceTest, CompanyServiceTest
│   │   ├── catalog/              # ProductServiceTest, SearchServiceTest
│   │   ├── order/                # OrderServiceTest, OrderStateMachineTest
│   │   ├── settlement/           # SettlementBatchTest, SettlementServiceTest
│   │   └── integration/          # OrderFlowIntegrationTest
│   └── build.gradle
├── infra/
│   ├── helm/                     # Helm charts (values-dev/staging/prod.yaml)
│   ├── terraform/                # Azure 리소스 IaC (AKS, DB, ES, Redis, Service Bus)
│   └── docker-compose.yml        # 로컬 개발 (Spring Boot + PostgreSQL + ES + Redis)
├── Dockerfile
└── .github/workflows/
    ├── ci.yml                    # PR: lint + test + SonarQube
    └── cd.yml                    # Release: build + deploy
```

## Development Conventions

### Naming Conventions
- **Java:** camelCase (변수, 메서드), PascalCase (클래스, DTO, 엔티티)
- **TypeScript:** camelCase (변수, 함수), PascalCase (컴포넌트, 타입/인터페이스)
- **파일명:** PascalCase (Java 클래스), kebab-case (프론트엔드 컴포넌트)
- **API 경로:** kebab-case, 복수형 (/api/v1/products, /api/v1/quote-requests)
- **DB 테이블:** snake_case, 복수형 (companies, products, quote_requests, trade_partnerships)

### Code Style
- Java: Google Java Style (checkstyle), SpotBugs 정적 분석
- TypeScript: ESLint + Prettier (semi: true, singleQuote: false)
- 커밋 메시지: Conventional Commits (feat:, fix:, docs:, refactor:, test:)

### Git Workflow
- `main`: 프로덕션 배포 브랜치 (protected, 직접 push 금지)
- `develop`: 개발 통합 브랜치
- `feature/*`: 기능 브랜치 (develop에서 분기)
- `release/*`: 릴리스 브랜치 (develop → main)
- `hotfix/*`: 긴급 수정 (main에서 분기)
- PR 리뷰 필수 (최소 1명), CI 통과 후 Squash Merge

### Testing Strategy
- 백엔드: JUnit 5 + Mockito (단위) + Testcontainers (통합)
- 프론트엔드: Vitest + React Testing Library
- 커버리지 목표: 80% 이상 (정산 모듈 90% 이상)
- E2E: Playwright (핵심 플로우: 가입 → 상품 등록 → 견적 → 주문 → 정산)

## Environment Setup

### Prerequisites
- Java 17+ (Temurin/Corretto)
- Node.js 20+ (LTS)
- Docker + Docker Compose
- Azure CLI (배포 시)

### Configuration (application-local.yml)
```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/tradehub
    username: tradehub
    password: tradehub_local
  jpa:
    hibernate:
      ddl-auto: validate
  elasticsearch:
    uris: http://localhost:9200
  data:
    redis:
      host: localhost
      port: 6379

jwt:
  secret: local-dev-jwt-secret-key-minimum-256-bits-long
  access-expiry: 3600000   # 1시간
  refresh-expiry: 1209600000  # 14일

azure:
  servicebus:
    connection-string: Endpoint=sb://localhost;SharedAccessKeyName=local;SharedAccessKey=xxx
  blob:
    connection-string: DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;...
```

### Running Locally
```bash
# 인프라 (PostgreSQL + Elasticsearch + Redis)
cd infra
docker-compose up -d

# Backend
cd backend
./gradlew bootRun --args='--spring.profiles.active=local'

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
# Sprint Status - TradeHub

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
  # Epic E-001: 기업 인증 및 계정 관리
  e-001:
    status: backlog
    stories:
      s-001:  # 기업 회원가입 및 인증 (8pt)
        status: ready-for-dev
      s-002:  # 로그인/로그아웃 및 직원 관리 (8pt)
        status: ready-for-dev
    retrospective:
      status: optional

  # Epic E-002: 상품 카탈로그
  e-002:
    status: backlog
    stories:
      s-003:  # 상품 등록 및 관리 (8pt)
        status: ready-for-dev
      s-004:  # 상품 검색 (8pt)
        status: ready-for-dev
      s-005:  # 거래처별 차등 단가 및 대량 등록 (5pt)
        status: backlog
    retrospective:
      status: optional

  # Epic E-003: 견적 관리
  e-003:
    status: backlog
    stories:
      s-006:  # 견적 요청 (8pt)
        status: backlog
      s-007:  # 견적서 작성 및 비교 (8pt)
        status: backlog
    retrospective:
      status: optional

  # Epic E-004: 주문 관리
  e-004:
    status: backlog
    stories:
      s-008:  # 발주 확정 및 주문 상태 관리 (8pt)
        status: backlog
      s-009:  # 배송 관리 및 수령 확인 (5pt)
        status: backlog
    retrospective:
      status: optional

  # Epic E-005: 정산
  e-005:
    status: backlog
    stories:
      s-010:  # 월별 자동 정산 및 정산서 (13pt)
        status: backlog
      s-011:  # 정산 이의 제기 (5pt)
        status: backlog
    retrospective:
      status: optional

  # Epic E-006: 거래처 관리
  e-006:
    status: backlog
    stories:
      s-012:  # 거래처 등록 및 관리 (8pt)
        status: backlog
    retrospective:
      status: optional

  # Epic E-007: 관리자 백오피스
  e-007:
    status: backlog
    stories:
      s-013:  # 기업 승인 및 시스템 설정 (5pt)
        status: backlog
      s-014:  # 거래 모니터링 및 분쟁 조정 (5pt)
        status: backlog
    retrospective:
      status: optional
```

## Sprint Plan

### Sprint 1 (Week 1-2)
**Goal:** 기업 인증 시스템 + 인프라 셋업
**Stories:** S-001 (8pt), S-002 (8pt)
**Total:** 16pt

### Sprint 2 (Week 3-4)
**Goal:** 상품 카탈로그 + Elasticsearch 검색
**Stories:** S-003 (8pt), S-004 (8pt), S-005 (5pt)
**Total:** 21pt

### Sprint 3 (Week 5-6)
**Goal:** 견적 관리 + 거래처 관리
**Stories:** S-006 (8pt), S-007 (8pt), S-012 (8pt)
**Total:** 24pt

### Sprint 4 (Week 7-8)
**Goal:** 주문 관리 (상태 머신 + 배송)
**Stories:** S-008 (8pt), S-009 (5pt)
**Total:** 13pt

### Sprint 5 (Week 9-10)
**Goal:** 정산 시스템 (배치 + 이의 제기)
**Stories:** S-010 (13pt), S-011 (5pt)
**Total:** 18pt

### Sprint 6 (Week 11-12)
**Goal:** 관리자 백오피스 + 통합 테스트 + 배포
**Stories:** S-013 (5pt), S-014 (5pt) + QA + 배포
**Total:** 10pt+

## Sprint Summary

| Metric | Value |
|--------|-------|
| Current Sprint | Sprint 1 |
| Sprint Goal | 기업 인증 시스템 + 인프라 셋업 |
| Total Points | 102 |
| Completed Points | 0 |
| In Progress Points | 0 |
| Remaining Points | 102 |

## Blockers

| Story | Blocker | Status |
|-------|---------|--------|
| - | 없음 | - |
""",
    },
]
