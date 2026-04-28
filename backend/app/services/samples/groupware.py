GROUPWARE_FILES = [
    {
        "file_name": "product-brief.md",
        "file_path": "planning-artifacts/product-brief.md",
        "content": """---
stepsCompleted: [1,2,3,4,5]
inputDocuments: []
workflowType: 'brief'
---
# Product Brief - SmartWork 기업용 그룹웨어

**Author:** BMad Sample
**Date:** 2026-03-21
**Status:** Complete

---

## Executive Summary

SmartWork는 중소·중견기업을 위한 통합 그룹웨어 시스템으로, 포털 대시보드, 전자결재, 게시판, 조직관리 기능을 하나의 플랫폼에서 제공합니다. 기존 그룹웨어의 복잡한 설정과 높은 도입 비용 문제를 해결하여, 50~500인 규모 기업이 즉시 도입할 수 있는 클라우드 기반 업무 협업 환경을 구축합니다.

## The Problem

중소·중견기업은 업무 처리를 위해 이메일, 메신저, 종이 결재, 엑셀 인사관리 등 파편화된 도구를 사용하고 있습니다. 결재 문서가 담당자 부재 시 며칠씩 지연되고, 공지사항이 제대로 전달되지 않으며, 조직도 변경 시 각 시스템을 개별 수정해야 합니다. 대기업용 그룹웨어(e-HR, SAP 등)는 도입 비용이 수천만 원에 달하고 커스터마이징에 수개월이 소요되어, 중소기업은 사실상 체계적인 업무 시스템 없이 운영되고 있습니다.

### Current Alternatives

- **이메일 + 메신저:** 결재 이력 관리 불가, 문서 버전 혼란, 보안 취약
- **종이 결재:** 물리적 이동 필요, 분실 위험, 원격근무 시 불가능
- **대기업용 그룹웨어 (더존, 한컴오피스 등):** 높은 도입비용, 긴 구축기간, 과도한 기능
- **Google Workspace / MS 365:** 결재 기능 없음, 한국 기업 문화에 부적합
- **엑셀 기반 인사관리:** 데이터 무결성 불보장, 조직 변경 시 수동 업데이트

## The Solution

웹 브라우저에서 즉시 사용 가능한 클라우드 그룹웨어. 포털 대시보드에서 오늘의 결재 대기·공지·일정을 한눈에 확인하고, 전자결재로 휴가·지출·기안을 온라인으로 처리하며, 게시판으로 부서별 소통하고, 조직관리로 인사 정보를 체계적으로 관리합니다.

### Core Capabilities

- **포털 대시보드:** 결재 대기 건수, 최신 공지, 오늘 일정, 부서 공유 사항을 위젯 형태로 통합 표시
- **전자결재:** 기안·휴가·지출 결재를 온라인으로 신청·승인·반려. 결재선 자동 생성, 대결·후결 지원
- **게시판:** 전사 공지, 부서별 게시판, 자유게시판. 파일 첨부, 댓글, 공지 고정 기능
- **조직관리:** 부서·직급·사원 정보 관리, 조직도 시각화, 인사발령 이력 관리

## What Makes This Different

**한국 기업 문화 최적화** — 결재선(순차/병렬/합의), 직급 체계, 부서 기반 권한 등 한국 기업의 업무 관행을 기본 내장. 별도 커스터마이징 없이 즉시 사용 가능. SaaS 모델로 초기 비용 없이 월정액으로 도입.

## Who This Serves

### Primary Users

**중소기업 임직원 (50~500인 규모):** IT 전담 인력이 부족한 기업의 일반 사무직 직원. 매일 결재 처리, 공지 확인, 조직 정보 조회가 필요하며, 복잡한 시스템보다 직관적인 UI를 선호하는 사용자.

### Secondary Users

**중소기업 경영진/관리자:** 결재 승인, 조직 현황 파악, 전사 공지 등록이 주 업무. 모바일에서도 결재 승인이 가능해야 하는 의사결정권자.
**IT/인사 관리자:** 조직도 관리, 사원 등록/퇴직 처리, 권한 설정을 담당하는 관리자. 엑셀 대비 효율적인 인사 관리 도구 필요.

## Success Criteria

| Criteria | Target | Measurement |
|----------|--------|-------------|
| 도입 기업 수 | 50개사 (출시 6개월) | CRM 시스템 |
| 일일 활성 사용자 (DAU) | 도입 기업 임직원의 80% | Analytics |
| 결재 처리 시간 단축 | 기존 대비 60% 감소 | 결재 완료 시간 로그 |
| 사용자 만족도 (NPS) | 40 이상 | 분기별 설문 |
| 시스템 가용성 | 99.9% | Azure Monitor |

## Scope

### In Scope (MVP)

- Azure AD 연동 SSO + 자체 인증 (이메일/비밀번호)
- 포털 대시보드 (결재 대기, 최신 공지, 오늘 일정 위젯)
- 전자결재 (기안·휴가·지출 양식, 순차 결재선, 승인/반려/보류)
- 게시판 (전사 공지, 부서별, 자유게시판, 파일 첨부, 댓글)
- 조직관리 (부서 CRUD, 사원 CRUD, 조직도 시각화, 직급 관리)
- 반응형 웹 (데스크톱 + 태블릿 + 모바일)

### Out of Scope

- 메신저/채팅 기능
- 전자메일 시스템
- 프로젝트 관리 / 일정 캘린더 (별도 모듈)
- 근태관리 (출퇴근 체크)
- 모바일 네이티브 앱
- ERP/회계 연동

## Vision

**1년:** 중소기업 50개사 도입, 핵심 4대 기능 안정화. 모바일 앱 출시. 월 매출 5,000만 원.
**3년:** 200개사 도입. 메신저, 캘린더, 근태관리, 전자계약 모듈 추가. API 마켓플레이스로 3rd party 연동 생태계 구축. 월 매출 3억 원. 해외(일본·동남아) 진출 시작.
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
# Product Requirements Document - SmartWork 기업용 그룹웨어

**Author:** BMad Sample
**Date:** 2026-03-21
**Version:** 1.0
**Status:** Complete

---

## 1. Executive Summary

SmartWork는 중소·중견기업을 위한 클라우드 기반 통합 그룹웨어 시스템입니다. 포털 대시보드, 전자결재, 게시판, 조직관리 4대 핵심 모듈을 제공하여 파편화된 업무 환경을 하나의 플랫폼으로 통합합니다.

Java 17 / Spring Boot 3.x 백엔드, React + TypeScript + Ant Design 프론트엔드, PostgreSQL 16 데이터베이스를 기반으로 Azure 클라우드에 배포됩니다. Spring Security와 Azure AD 연동으로 엔터프라이즈급 보안을 제공합니다.

## 2. Project Classification

| Attribute | Value |
|-----------|-------|
| Project Type | Enterprise Web Application (SPA + REST API) |
| Domain | 기업 협업 / 그룹웨어 (Enterprise Collaboration) |
| Complexity | High |
| Greenfield/Brownfield | Greenfield (신규 개발) |

## 3. Product Vision

### 1-Year Vision
중소기업 50개사 도입. 결재·게시판·조직관리 핵심 기능 안정화. 모바일 반응형 완성. NPS 40 이상 달성.

### 3-Year Vision
200개사 도입. 메신저, 캘린더, 근태, 전자계약 모듈 확장. API 마켓플레이스 구축. 해외 진출 시작.

### Key Differentiator
한국 기업 문화(결재선, 직급 체계, 부서 권한)를 기본 내장한 클라우드 SaaS. 별도 커스터마이징 없이 즉시 도입 가능.

## 4. Success Criteria

### User Success

| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| 결재 처리 시간 | 평균 2시간 이내 완료 | 결재 로그 타임스탬프 분석 |
| 일일 포털 접속률 | 도입 기업 임직원 80% | DAU / 전체 등록 사용자 |
| 게시판 활용률 | 주 1회 이상 글 작성 (부서당) | 게시글 생성 로그 |

### Business Success

| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| 도입 기업 수 | 50개사 (6개월) | CRM |
| 월 반복 매출 (MRR) | 5,000만 원 | 결제 시스템 |
| 계약 유지율 | 90% 이상 (연간) | 이탈 분석 |

### Technical Success

| Metric | Target | Measurement Method |
|--------|--------|--------------------|
| API p95 응답시간 | < 300ms | Azure Monitor |
| 시스템 가용성 | 99.9% | Uptime 모니터링 |
| 보안 취약점 | Critical 0건 | SonarQube + OWASP ZAP |

## 5. User Journeys

### UJ-001: 일반 직원 김대리 (마케팅팀, 29세)

**Discovery:** 회사에서 SmartWork 도입 공지. 기존에는 결재를 종이로 올리고, 공지는 이메일로 받았지만 자주 놓침.

**Onboarding:** Azure AD SSO로 회사 계정 그대로 로그인. 첫 화면에 결재 대기 0건, 오늘 공지 3건, 부서 게시글 2건이 위젯으로 표시. 별도 설정 없이 즉시 업무 시작.

**Core Usage:** 아침 출근 후 포털 대시보드 확인 → 결재 대기 건 클릭하여 승인 → 전사 공지 확인 → 휴가 신청서 기안 → 부서 게시판에 주간 보고 작성. 모든 업무가 한 화면에서 처리됨.

**Edge Cases:** 결재선의 팀장이 출장 중 → 대결자(파트장)에게 자동 이관. 첨부 파일이 10MB 초과 → 업로드 전 용량 안내 후 압축 권고.

**Return Usage:** 매일 아침 대시보드 확인이 습관화. 결재 알림으로 처리 지연 없음. 월말에 부서 게시판에서 지난 공유 자료 검색.

### UJ-002: 인사팀장 박과장 (인사총무팀, 38세)

**Discovery:** 기존 엑셀 인사관리의 한계 체감. 조직 개편 시 30개 부서 정보를 수동 수정해야 하는 고충.

**Core Usage:** 신입사원 입사 → 조직관리에서 사원 등록 + 부서 배정 → 자동으로 조직도 반영 + 결재선에 포함. 인사발령 시 부서 이동 처리 → 이력 자동 기록. 전사 공지 게시판에 인사 관련 공지 등록.

### UJ-003: 대표이사 이사장 (경영진, 52세)

**Core Usage:** 모바일에서 결재 대기 건 확인 → 지출 결의서 금액 확인 후 승인/반려. 전사 공지 작성. 조직도에서 부서별 인원 현황 확인.

## 6. Domain Requirements

### 전자결재 규정

- 결재선은 기안자 → 팀장 → 부서장 순서로 자동 생성 (조직도 기반)
- 결재권자 부재 시 대결자 지정 가능
- 결재 완료 문서는 수정 불가 (감사 추적용)
- 문서번호는 연도-부서코드-일련번호 형식 (예: 2026-MKT-00123)
- 결재 이력(시간, IP, 의견)은 영구 보관

### 개인정보 보호

- 사원 개인정보(주민번호, 연락처 등)는 AES-256 암호화 저장
- 접근 권한: 본인 + 인사팀 + 시스템 관리자만 열람
- 개인정보 조회 시 감사 로그 기록

## 7. Scoping & Roadmap

### MVP (Phase 1) — Must-Have

- SSO (Azure AD) + 자체 인증 (이메일/비밀번호)
- 포털 대시보드 (결재 대기, 최신 공지, 오늘 일정 위젯)
- 전자결재 (기안/휴가/지출 양식, 순차 결재선, 승인/반려/보류)
- 게시판 (전사 공지, 부서별 게시판, 파일 첨부, 댓글)
- 조직관리 (부서/사원 CRUD, 조직도, 직급 관리)
- 반응형 웹 디자인

### Growth (Phase 2) — Should-Have

- 병렬/합의 결재선 지원
- 결재 양식 빌더 (관리자 커스텀 양식 생성)
- 게시판 카테고리 관리, 익명 게시판
- 알림 센터 (웹 푸시 + 이메일 알림)
- 결재 통계 대시보드 (월별 처리량, 평균 처리시간)
- 사원 프로필 사진 / 직인 이미지 관리

### Vision (Phase 3) — Could-Have

- 메신저/채팅 모듈
- 캘린더/일정 관리 모듈
- 근태관리 (출퇴근 체크, 연차 관리)
- 전자계약 모듈
- 모바일 네이티브 앱 (React Native)
- API 마켓플레이스 (3rd party 연동)

### Won't-Have (Explicitly Excluded)

- ERP/회계 시스템
- 급여 관리
- 화상 회의
- 문서 공동 편집 (Google Docs 스타일)
- AI 기반 자동화 (1차 범위 외)

### Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Azure AD 연동 복잡도 | 중 | 높 | MSAL 라이브러리 활용, POC 선행 |
| 결재선 로직 복잡도 | 높 | 높 | 순차 결재만 MVP, 병렬은 Phase 2 |
| 기업별 커스터마이징 요구 | 높 | 중 | 설정 기반 유연성 확보, 양식 빌더 제공 |
| 개인정보 보안 사고 | 낮 | 최고 | 암호화, 접근제어, 감사로그, 정기 보안점검 |
| 레거시 데이터 마이그레이션 | 중 | 중 | 엑셀 임포트 기능, 마이그레이션 가이드 |

## 8. Functional Requirements

### 8.1 사용자 인증 및 권한

| ID | Requirement | Priority | Acceptance Criteria |
|----|------------|----------|---------------------|
| FR-001 | Azure AD SSO 로그인 | Must | MSAL 토큰으로 자동 로그인, 사원 정보 동기화 |
| FR-002 | 자체 이메일/비밀번호 로그인 | Must | JWT access token (1시간) + refresh token (14일) 발급 |
| FR-003 | 역할 기반 접근제어 (RBAC) | Must | ADMIN, HR_MANAGER, MANAGER, USER 4개 역할, API별 권한 검증 |
| FR-004 | 로그인 이력 관리 | Should | 로그인 시각, IP, 브라우저 정보 기록 |

### 8.2 포털 대시보드

| ID | Requirement | Priority | Acceptance Criteria |
|----|------------|----------|---------------------|
| FR-010 | 결재 대기 위젯 | Must | 내가 승인해야 할 문서 건수 + 최근 3건 제목 표시 |
| FR-011 | 최신 공지 위젯 | Must | 전사 공지 최신 5건 표시, 클릭 시 상세 이동 |
| FR-012 | 오늘 일정 위젯 | Must | 오늘 결재 예정, 부서 일정 표시 |
| FR-013 | 내 결재 현황 요약 | Must | 기안 중/승인 대기/완료/반려 건수 카드 |

### 8.3 전자결재

| ID | Requirement | Priority | Acceptance Criteria |
|----|------------|----------|---------------------|
| FR-020 | 결재 문서 기안 | Must | 양식 선택(기안/휴가/지출) → 내용 작성 → 결재선 설정 → 제출 |
| FR-021 | 결재선 자동 생성 | Must | 기안자의 조직도 기반 상위 결재선 자동 구성 (팀장→부서장) |
| FR-022 | 결재 승인/반려/보류 | Must | 결재권자가 의견 작성 후 승인·반려·보류 처리 |
| FR-023 | 결재 문서 목록 조회 | Must | 기안함/결재대기함/결재완료함/반려함 탭 분류, 페이지네이션 |
| FR-024 | 결재 상태 추적 | Must | 결재선 각 단계별 처리 상태 시각화 (대기/승인/반려) |
| FR-025 | 대결 처리 | Should | 결재권자 부재 시 지정된 대결자가 대신 승인 |
| FR-026 | 문서번호 자동 발번 | Must | 연도-부서코드-일련번호 형식 자동 생성 |
| FR-027 | 결재 문서 PDF 출력 | Should | 완료된 결재 문서를 PDF로 다운로드 |

### 8.4 게시판

| ID | Requirement | Priority | Acceptance Criteria |
|----|------------|----------|---------------------|
| FR-030 | 게시판 분류 관리 | Must | 전사 공지, 부서별, 자유게시판 카테고리 생성·수정·삭제 |
| FR-031 | 게시글 CRUD | Must | 제목, 본문(에디터), 첨부파일과 함께 게시글 생성·수정·삭제 |
| FR-032 | 공지 고정 기능 | Must | 관리자가 특정 게시글을 상단 고정 (최대 5건) |
| FR-033 | 댓글 기능 | Must | 게시글에 댓글 작성·수정·삭제, 대댓글 1단계 |
| FR-034 | 파일 첨부 | Must | 게시글당 최대 5개 파일, 파일당 10MB, 총 30MB 제한 |
| FR-035 | 게시글 검색 | Should | 제목+본문 전문 검색, 작성자·기간 필터 |

### 8.5 조직관리

| ID | Requirement | Priority | Acceptance Criteria |
|----|------------|----------|---------------------|
| FR-040 | 부서 CRUD | Must | 부서명, 부서코드, 상위부서, 부서장 설정 |
| FR-041 | 사원 CRUD | Must | 이름, 사번, 직급, 부서, 입사일, 연락처, 이메일 관리 |
| FR-042 | 조직도 시각화 | Must | 트리 구조 조직도 표시, 부서 클릭 시 소속 사원 목록 |
| FR-043 | 직급 체계 관리 | Must | 직급(사원→대리→과장→차장→부장→이사→대표) 정의 및 순서 관리 |
| FR-044 | 인사발령 처리 | Should | 부서 이동, 직급 변경 시 이력 자동 기록, 발령일 기준 적용 |
| FR-045 | 사원 검색 | Must | 이름, 부서명, 직급으로 사원 검색 |

## 9. Non-Functional Requirements

### 9.1 Performance — NFR-001

| Metric | Target |
|--------|--------|
| 페이지 초기 로드 (FCP) | < 2.0초 |
| API 응답 시간 (p95) | < 300ms |
| 결재 문서 PDF 생성 | < 5초 |
| 동시 사용자 | 1,000명 |
| 파일 업로드 (10MB) | < 10초 |

### 9.2 Security — NFR-002

- 비밀번호: BCrypt (strength 12), 평문 저장 금지
- 인증: JWT RS256, Spring Security 필터 체인
- SSO: Azure AD MSAL, OAuth 2.0 / OIDC
- 통신: HTTPS 전용 (TLS 1.3)
- 개인정보: AES-256 암호화 (주민번호, 연락처)
- SQL Injection: JPA/Hibernate 사용, native query 최소화
- XSS: React 기본 이스케이프 + CSP 헤더
- CSRF: Spring Security CSRF 토큰
- 파일 업로드: 확장자 화이트리스트, 바이러스 스캔

### 9.3 Scalability — NFR-003

- 수평 확장: Azure App Service 오토스케일링 (CPU 70% 기준)
- DB: Azure Database for PostgreSQL Read Replica
- 파일 스토리지: Azure Blob Storage (CDN 연동)
- 세션: Redis (Azure Cache for Redis)

### 9.4 Reliability — NFR-004

- 가용성: 99.9% (월간 다운타임 < 44분)
- 백업: Azure 자동 백업 (30일 보존, 지역 간 복제)
- 에러 추적: Application Insights + Sentry
- DR: Azure paired region 재해복구

### 9.5 Accessibility — NFR-005

- WCAG 2.1 AA 준수
- 키보드 네비게이션 지원 (결재 승인 등 주요 액션)
- 스크린 리더: aria-label, role 적용 (Ant Design 기본 지원)
- 색상 대비: 4.5:1 이상

## 10. Appendix

### Glossary

| Term | Definition |
|------|-----------|
| 기안 | 결재 문서를 최초 작성하여 상신하는 행위 |
| 결재선 | 문서가 승인되어야 하는 결재권자의 순서 |
| 대결 | 결재권자 부재 시 지정된 대리인이 결재하는 것 |
| 후결 | 긴급 시 상위 결재 없이 처리 후 사후 승인받는 것 |
| SSO | Single Sign-On, 한 번의 로그인으로 여러 시스템 접근 |
| RBAC | Role-Based Access Control, 역할 기반 접근제어 |
| MSAL | Microsoft Authentication Library, Azure AD 인증 라이브러리 |

### References

- Spring Boot Documentation: https://docs.spring.io/spring-boot/docs/current/reference/html/
- Ant Design: https://ant.design/
- Azure AD (Microsoft Entra ID): https://learn.microsoft.com/en-us/azure/active-directory/
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
# Architecture Decision Document - SmartWork 기업용 그룹웨어

**Author:** BMad Sample
**Date:** 2026-03-21
**Version:** 1.0
**Status:** Complete

---

## 1. Overview

### 1.1 Purpose
SmartWork 그룹웨어 시스템의 기술 아키텍처를 정의합니다. 포털 대시보드, 전자결재, 게시판, 조직관리 4대 모듈을 지원하는 엔터프라이즈급 웹 애플리케이션 구조를 설계합니다.

### 1.2 Scope
MVP 기능 전체 (인증/SSO, 포털, 전자결재, 게시판, 조직관리). 메신저, 캘린더, 근태관리는 범위 외.

### 1.3 Context
5인 개발팀 (백엔드 2, 프론트엔드 2, DevOps 1), 6개월 MVP 목표. Azure 클라우드 기반, 기업 고객 대상.

## 2. Architecture Drivers

### 2.1 Key Requirements

| ID | Requirement | Impact Level |
|----|------------|-------------|
| FR-001 | Azure AD SSO 연동 | High — 인증 아키텍처 결정 |
| FR-020~027 | 전자결재 워크플로우 | High — 상태 머신 + 트랜잭션 설계 |
| FR-040~045 | 조직관리 + 결재선 연동 | High — 데이터 모델 + 권한 체계 |
| NFR-Security | 개인정보 암호화 + RBAC | High — 보안 아키텍처 |
| NFR-Performance | API p95 < 300ms, 1000 동시 | High — 캐싱, 인덱스 전략 |

### 2.2 Quality Attributes

| Attribute | Priority | Target |
|-----------|----------|--------|
| Security | Critical | 개인정보 암호화, RBAC, 감사 로그 |
| Performance | High | API < 300ms, 1000 동시 사용자 |
| Reliability | High | 99.9% 가용성, 자동 백업 |
| Maintainability | High | 모듈 분리, 테스트 커버리지 80% |
| Scalability | Medium | 수평 확장, Read Replica |

### 2.3 Constraints

- 5인 개발팀 → 적절한 모듈 분리, 마이크로서비스 지양
- 기업 고객 → 보안·감사 요구사항 엄격
- Azure 클라우드 → Azure 네이티브 서비스 활용
- 한국 기업 문화 → 결재선, 직급, 부서 체계 내장

## 3. Architecture Decisions (ADRs)

### ADR-001: Architecture Style — 모듈러 모놀리스 + SPA

- **Context:** 4개 도메인 모듈이 밀접하게 연동 (결재선 ↔ 조직도, 대시보드 ↔ 전체)
- **Decision:** 모듈러 모놀리스 (Spring Boot) + SPA (React)
- **Rationale:** 모듈 간 트랜잭션 관리 용이, 5인 팀에 마이크로서비스는 운영 부담 과다. 패키지 경계로 모듈 분리하여 향후 서비스 분리 가능
- **Consequences:** 단일 배포 단위로 운영 단순. 향후 트래픽 증가 시 결재 모듈만 분리 가능
- **Alternatives:** 마이크로서비스 (운영 복잡도 과다), Serverless (결재 워크플로우에 부적합)

### ADR-002: Backend Framework — Spring Boot 3.x + Java 17

- **Context:** 기업용 시스템, 트랜잭션 관리, 보안, 장기 유지보수 중요
- **Decision:** Spring Boot 3.x + Java 17 (LTS)
- **Rationale:** Spring Security (RBAC, SSO), Spring Data JPA (ORM), 풍부한 엔터프라이즈 생태계, Java 개발자 채용 용이
- **Consequences:** 안정적 엔터프라이즈 생태계, 풍부한 보안 라이브러리
- **Alternatives:** FastAPI/Python (엔터프라이즈 생태계 부족), .NET (Azure 네이티브이나 인력 수급 어려움)

### ADR-003: Database — PostgreSQL 16 (Azure Database)

- **Context:** 조직도 트리 구조, 결재 워크플로우, 감사 로그, 전문 검색
- **Decision:** Azure Database for PostgreSQL 16
- **Rationale:** CTE (재귀 쿼리)로 조직도 트리 처리, JSONB로 결재 양식 메타데이터, tsvector로 게시판 검색, 트랜잭션 무결성
- **Consequences:** 단일 DB로 모든 도메인 처리, Azure 관리형으로 운영 부담 최소
- **Alternatives:** MySQL (CTE 지원 약함), MongoDB (트랜잭션 제약), SQL Server (라이선스 비용)

### ADR-004: Frontend — React + TypeScript + Ant Design

- **Context:** 기업용 관리 화면, 폼/테이블/트리 컴포넌트 다수, 일관된 UI
- **Decision:** React 18 + TypeScript + Ant Design 5.x
- **Rationale:** Ant Design은 테이블, 폼, 트리, 모달 등 기업용 컴포넌트 풍부. 기업 관리 시스템에 최적화된 디자인 시스템
- **Consequences:** 빠른 UI 개발, 일관된 디자인. 번들 사이즈 관리 필요 (tree-shaking)
- **Alternatives:** MUI (Material Design은 기업용에 덜 적합), Tailwind (컴포넌트 직접 구현 필요)

### ADR-005: File Storage — Azure Blob Storage

- **Context:** 게시판 첨부파일, 결재 문서 PDF, 사원 프로필 사진 저장
- **Decision:** Azure Blob Storage + Azure CDN
- **Rationale:** 무제한 확장, 접근 제어 (SAS 토큰), CDN으로 빠른 배포, 비용 효율
- **Consequences:** 파일은 DB에 메타데이터만, 실제 파일은 Blob Storage에 저장
- **Alternatives:** 로컬 파일시스템 (확장 불가), S3 (Azure 환경에서 추가 비용)

### ADR-006: Caching — Redis (Azure Cache)

- **Context:** 조직도, 코드 테이블 등 변경 빈도 낮은 데이터 캐싱
- **Decision:** Azure Cache for Redis
- **Rationale:** 조직도 트리, 직급 목록, 부서 목록 캐싱으로 API 성능 향상. Spring Cache 추상화로 간편 적용
- **Consequences:** 조직 변경 시 캐시 무효화 로직 필요
- **Alternatives:** Ehcache (분산 환경 제약), Caffeine (로컬 전용)

## 4. Technology Stack

| Layer | Technology | Version | Justification |
|-------|-----------|---------|---------------|
| Frontend | React + TypeScript | 18.x / 5.x | SPA, 타입 안전성 |
| UI Framework | Ant Design | 5.x | 기업용 컴포넌트 풍부 (테이블, 폼, 트리) |
| State Mgmt | Zustand | 4.x | 경량, 직관적, React 친화적 |
| HTTP Client | Axios | 1.x | 인터셉터, 토큰 자동 갱신 |
| Charts | Apache ECharts | 5.x | 대시보드 차트 (기업용 고성능) |
| Backend | Spring Boot + Java | 3.x / 17 | 엔터프라이즈 표준, 보안, 트랜잭션 |
| Security | Spring Security | 6.x | RBAC, JWT, OAuth2/OIDC |
| ORM | Spring Data JPA + Hibernate | 3.x / 6.x | 타입 안전, 자동 감사 |
| Migration | Flyway | 10.x | 버전 관리형 DB 마이그레이션 |
| Database | PostgreSQL | 16.x | CTE, JSONB, tsvector |
| Cache | Redis (Azure Cache) | 7.x | 조직도, 코드 테이블 캐싱 |
| File Storage | Azure Blob Storage | — | 첨부파일, PDF |
| Auth (SSO) | MSAL (Azure AD) | 4.x | 기업 SSO, OAuth2/OIDC |
| Hosting | Azure App Service | — | Java 앱 호스팅, 오토스케일링 |
| DB Hosting | Azure Database for PostgreSQL | — | 관리형 PostgreSQL |
| CI/CD | GitHub Actions | — | PR 기반, 자동 테스트 + Azure 배포 |
| Monitoring | Azure Monitor + Application Insights | — | APM, 로그, 알림 |

## 5. System Architecture

### 5.1 Component Diagram

```
┌──────────────┐     HTTPS      ┌──────────────────────────────┐
│   Browser    │ ←───────────→  │  React SPA (Azure Static)    │
└──────────────┘                └──────────┬───────────────────┘
                                           │ REST API (JSON)
                                           ▼
                                ┌──────────────────────────────┐
                                │    Spring Boot Backend        │
                                │   (Azure App Service)         │
                                ├──────────┬───────────────────┤
                                │ Auth     │ Portal Module     │
                                │ Module   ├───────────────────┤
                                │ (SSO+JWT)│ Approval Module   │
                                │          ├───────────────────┤
                                │          │ Board Module      │
                                │          ├───────────────────┤
                                │          │ Org Mgmt Module   │
                                └────┬─────┴─────┬─────┬───────┘
                                     │           │     │
                              ┌──────▼──┐  ┌─────▼──┐  │
                              │PostgreSQL│  │ Redis  │  │
                              │(Azure DB)│  │(Cache) │  │
                              └─────────┘  └────────┘  │
                                                       │
                                              ┌────────▼────────┐
                                              │  Azure Blob     │
                                              │  Storage (Files)│
                                              └─────────────────┘
```

### 5.2 Data Flow (결재 기안 → 승인)

1. 기안자가 결재 양식 선택 → 내용 작성 → 결재선 확인 → 제출
2. Frontend → POST /api/approvals { formType, content, approvalLine }
3. Backend Approval Module: 문서번호 발번 → 결재선 생성 → 상태 DRAFT → PENDING
4. 1차 결재권자에게 알림 발송 (웹 푸시)
5. 1차 결재권자: GET /api/approvals/{id} → 문서 확인 → PUT /api/approvals/{id}/approve
6. Approval Module: 1차 APPROVED → 2차 결재권자에게 알림 → PENDING
7. 2차 결재권자: approve → 최종 APPROVED → 기안자에게 완료 알림
8. 결재 완료 문서: 수정 불가, 이력 영구 보존

## 6. Data Architecture

### 6.1 Entity Relationship

```
Organization (부서)
├── id: BIGSERIAL PK
├── name: VARCHAR(100)
├── code: VARCHAR(20) UNIQUE — 부서코드
├── parent_id: FK → organizations.id (nullable, 트리 구조)
├── leader_id: FK → employees.id (nullable)
├── sort_order: INTEGER
├── is_active: BOOLEAN
├── created_at: TIMESTAMPTZ
└── updated_at: TIMESTAMPTZ

Employee (사원)
├── id: BIGSERIAL PK
├── employee_number: VARCHAR(20) UNIQUE — 사번
├── name: VARCHAR(50)
├── email: VARCHAR(255) UNIQUE
├── password_hash: VARCHAR(255) (nullable, SSO 사용 시)
├── position_id: FK → positions.id — 직급
├── organization_id: FK → organizations.id — 소속 부서
├── role: VARCHAR(20) — ADMIN/HR_MANAGER/MANAGER/USER
├── phone: VARCHAR(20) (AES-256 암호화)
├── hire_date: DATE
├── resign_date: DATE (nullable)
├── azure_ad_oid: VARCHAR(255) (nullable) — Azure AD Object ID
├── is_active: BOOLEAN
├── created_at: TIMESTAMPTZ
└── updated_at: TIMESTAMPTZ

Position (직급)
├── id: SERIAL PK
├── name: VARCHAR(50) — 사원/대리/과장/차장/부장/이사/대표
├── level: INTEGER — 정렬 순서 (1=사원, 7=대표)
└── is_active: BOOLEAN

ApprovalDocument (결재 문서)
├── id: BIGSERIAL PK
├── document_number: VARCHAR(30) UNIQUE — 2026-MKT-00123
├── form_type: VARCHAR(20) — DRAFT/LEAVE/EXPENSE
├── title: VARCHAR(200)
├── content: JSONB — 양식별 구조화된 내용
├── status: VARCHAR(20) — DRAFT/PENDING/APPROVED/REJECTED/ON_HOLD
├── drafter_id: FK → employees.id
├── organization_id: FK → organizations.id — 기안 부서
├── created_at: TIMESTAMPTZ
└── updated_at: TIMESTAMPTZ

ApprovalLine (결재선)
├── id: BIGSERIAL PK
├── document_id: FK → approval_documents.id
├── approver_id: FK → employees.id — 결재권자
├── delegate_id: FK → employees.id (nullable) — 대결자
├── step_order: INTEGER — 결재 순서
├── status: VARCHAR(20) — PENDING/APPROVED/REJECTED/ON_HOLD
├── comment: TEXT (nullable)
├── acted_at: TIMESTAMPTZ (nullable)
├── acted_ip: VARCHAR(45) (nullable)
└── created_at: TIMESTAMPTZ

Board (게시판)
├── id: SERIAL PK
├── name: VARCHAR(100) — 게시판명
├── type: VARCHAR(20) — NOTICE/DEPARTMENT/FREE
├── organization_id: FK → organizations.id (nullable, 부서 게시판)
├── is_active: BOOLEAN
└── created_at: TIMESTAMPTZ

Post (게시글)
├── id: BIGSERIAL PK
├── board_id: FK → boards.id
├── author_id: FK → employees.id
├── title: VARCHAR(200)
├── content: TEXT
├── is_pinned: BOOLEAN — 공지 고정
├── view_count: INTEGER DEFAULT 0
├── is_deleted: BOOLEAN
├── created_at: TIMESTAMPTZ
└── updated_at: TIMESTAMPTZ

PostComment (댓글)
├── id: BIGSERIAL PK
├── post_id: FK → posts.id
├── author_id: FK → employees.id
├── parent_id: FK → post_comments.id (nullable, 대댓글)
├── content: TEXT
├── is_deleted: BOOLEAN
├── created_at: TIMESTAMPTZ
└── updated_at: TIMESTAMPTZ

Attachment (첨부파일)
├── id: BIGSERIAL PK
├── post_id: FK → posts.id (nullable)
├── document_id: FK → approval_documents.id (nullable)
├── original_name: VARCHAR(255)
├── stored_path: VARCHAR(500) — Blob Storage 경로
├── file_size: BIGINT
├── content_type: VARCHAR(100)
├── created_at: TIMESTAMPTZ
└── uploaded_by: FK → employees.id

PersonnelHistory (인사발령 이력)
├── id: BIGSERIAL PK
├── employee_id: FK → employees.id
├── change_type: VARCHAR(20) — HIRE/TRANSFER/PROMOTE/RESIGN
├── from_org_id: FK → organizations.id (nullable)
├── to_org_id: FK → organizations.id (nullable)
├── from_position_id: FK → positions.id (nullable)
├── to_position_id: FK → positions.id (nullable)
├── effective_date: DATE
├── description: TEXT
└── created_at: TIMESTAMPTZ
```

### 6.2 Indexing Strategy

- `idx_employees_org_id`: (organization_id) — 부서별 사원 조회
- `idx_employees_name`: (name) — 사원 검색
- `idx_approval_docs_drafter`: (drafter_id, status) — 내 기안 문서
- `idx_approval_line_approver`: (approver_id, status) — 결재 대기함
- `idx_posts_board_created`: (board_id, created_at DESC) — 게시글 목록
- `idx_posts_search`: GIN(to_tsvector('korean', title || ' ' || content)) — 전문 검색
- `idx_orgs_parent`: (parent_id) — 조직도 트리 조회

## 7. API Design

### 7.1 API Style
RESTful JSON API. 모든 요청/응답은 DTO 클래스로 검증. Spring Validation 활용.

### 7.2 Endpoint Structure

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | /api/auth/login | 자체 로그인 → JWT 발급 | Public |
| POST | /api/auth/sso/callback | Azure AD SSO 콜백 | Public |
| POST | /api/auth/refresh | 토큰 갱신 | Refresh Token |
| GET | /api/portal/dashboard | 대시보드 위젯 데이터 | USER |
| GET | /api/approvals | 결재 문서 목록 (탭별 필터) | USER |
| POST | /api/approvals | 결재 문서 기안 | USER |
| GET | /api/approvals/{id} | 결재 문서 상세 | USER |
| PUT | /api/approvals/{id}/approve | 결재 승인 | MANAGER+ |
| PUT | /api/approvals/{id}/reject | 결재 반려 | MANAGER+ |
| PUT | /api/approvals/{id}/hold | 결재 보류 | MANAGER+ |
| GET | /api/boards | 게시판 목록 | USER |
| GET | /api/boards/{id}/posts | 게시글 목록 | USER |
| POST | /api/boards/{id}/posts | 게시글 작성 | USER |
| GET | /api/posts/{id} | 게시글 상세 | USER |
| PUT | /api/posts/{id} | 게시글 수정 | AUTHOR |
| DELETE | /api/posts/{id} | 게시글 삭제 (소프트) | AUTHOR/ADMIN |
| POST | /api/posts/{id}/comments | 댓글 작성 | USER |
| GET | /api/organizations | 조직 목록 (트리) | USER |
| POST | /api/organizations | 부서 생성 | HR_MANAGER+ |
| PUT | /api/organizations/{id} | 부서 수정 | HR_MANAGER+ |
| GET | /api/employees | 사원 목록 (검색) | USER |
| POST | /api/employees | 사원 등록 | HR_MANAGER+ |
| PUT | /api/employees/{id} | 사원 정보 수정 | HR_MANAGER+ |
| GET | /api/employees/{id} | 사원 상세 | USER (본인+HR) |
| POST | /api/files/upload | 파일 업로드 | USER |

### 7.3 Error Handling

```json
{
  "timestamp": "2026-03-21T10:30:00Z",
  "status": 404,
  "error": "Not Found",
  "code": "APPROVAL_NOT_FOUND",
  "message": "결재 문서를 찾을 수 없습니다.",
  "path": "/api/approvals/999"
}
```
표준 HTTP 상태 코드 + 커스텀 에러 코드 + 한국어 메시지.

## 8. Project Structure

```
smartwork/
├── frontend/
│   ├── src/
│   │   ├── pages/              # 페이지 컴포넌트
│   │   │   ├── portal/         # Dashboard
│   │   │   ├── approval/       # 전자결재
│   │   │   ├── board/          # 게시판
│   │   │   └── organization/   # 조직관리
│   │   ├── components/
│   │   │   ├── common/         # Layout, Header, Sidebar
│   │   │   ├── approval/       # ApprovalForm, ApprovalLine, StatusBadge
│   │   │   ├── board/          # PostList, PostEditor, CommentList
│   │   │   └── organization/   # OrgTree, EmployeeTable, PositionSelect
│   │   ├── api/                # Axios API 클라이언트
│   │   ├── stores/             # Zustand stores (auth, approval, board, org)
│   │   ├── types/              # TypeScript 인터페이스
│   │   └── utils/              # 유틸리티 함수
│   ├── public/
│   └── package.json
├── backend/
│   ├── src/main/java/com/smartwork/
│   │   ├── SmartWorkApplication.java
│   │   ├── config/             # SecurityConfig, CorsConfig, RedisConfig
│   │   ├── auth/               # AuthController, JwtProvider, SsoService
│   │   ├── portal/             # PortalController, DashboardService
│   │   ├── approval/           # ApprovalController, ApprovalService, ApprovalLineService
│   │   │   ├── dto/            # ApprovalRequest, ApprovalResponse
│   │   │   ├── entity/         # ApprovalDocument, ApprovalLine
│   │   │   └── repository/     # ApprovalRepository
│   │   ├── board/              # BoardController, PostService, CommentService
│   │   │   ├── dto/
│   │   │   ├── entity/         # Board, Post, PostComment
│   │   │   └── repository/
│   │   ├── organization/       # OrgController, EmployeeService, PositionService
│   │   │   ├── dto/
│   │   │   ├── entity/         # Organization, Employee, Position, PersonnelHistory
│   │   │   └── repository/
│   │   ├── file/               # FileController, FileService (Blob Storage)
│   │   └── common/             # BaseEntity, ApiResponse, GlobalExceptionHandler
│   ├── src/main/resources/
│   │   ├── application.yml
│   │   └── db/migration/       # Flyway SQL 파일
│   ├── src/test/java/
│   │   ├── approval/           # ApprovalServiceTest, ApprovalIntegrationTest
│   │   ├── board/              # PostServiceTest
│   │   └── organization/       # OrgServiceTest
│   └── build.gradle
├── docker-compose.yml
├── Dockerfile
└── .github/workflows/ci.yml
```

## 9. Security Architecture

### 9.1 Authentication Flow

#### 자체 로그인
1. POST /auth/login → BCrypt 검증 → JWT access (1h) + refresh (14d) 발급
2. 모든 API: Authorization: Bearer {access_token}
3. Access 만료 → POST /auth/refresh → 새 토큰 쌍 발급
4. Refresh 만료 → 재로그인

#### Azure AD SSO
1. 프론트엔드: MSAL.js → Azure AD 로그인 → ID Token 획득
2. POST /auth/sso/callback { idToken } → 백엔드 검증 → 사원 매칭 (azure_ad_oid)
3. 사원 존재 시 JWT 발급, 미존재 시 자동 등록 또는 에러

### 9.2 Authorization (RBAC)

| Role | Permissions |
|------|------------|
| ADMIN | 전체 시스템 관리, 게시판 관리, 모든 데이터 접근 |
| HR_MANAGER | 조직관리, 사원 CRUD, 인사발령 |
| MANAGER | 결재 승인/반려, 부서 게시판 관리 |
| USER | 기안, 게시글 CRUD (본인), 조회 |

### 9.3 Data Protection
- 비밀번호: BCrypt (strength 12), 평문 저장 절대 금지
- 개인정보 (전화번호): AES-256-GCM 암호화, 키는 Azure Key Vault
- API Key / Secret: Azure Key Vault, 코드/로그 노출 금지
- HTTPS 전용, HSTS 헤더
- CORS: 프론트엔드 도메인만 허용
- 결재 문서 감사: 모든 결재 액션의 시간, IP, 사용자 기록

## 10. Infrastructure & DevOps

### 10.1 Environments

| Environment | Purpose | Configuration |
|------------|---------|---------------|
| Local | 개발 | Docker Compose (Spring Boot + PostgreSQL + Redis) |
| Staging | QA/테스트 | Azure App Service (B1) + Azure DB (Basic) |
| Production | 서비스 | Azure App Service (S1, Auto Scale) + Azure DB (GP, Read Replica) |

### 10.2 Deployment Strategy
- GitHub Actions: PR → lint + test → staging 자동 배포
- main merge → production 배포 (수동 승인 게이트)
- Blue-Green 배포 (Azure App Service Deployment Slots)
- Flyway 마이그레이션 자동 실행

### 10.3 Monitoring
- Azure Monitor + Application Insights: API 지표, 에러율, 응답시간, 사용자 흐름
- Sentry: 에러 추적 + 슬랙 알림
- PostgreSQL: slow query log (300ms 이상)
- Azure Alerts: CPU > 80%, 에러율 > 1%, 응답시간 > 500ms
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
# Epics & Stories - SmartWork 기업용 그룹웨어

**Date:** 2026-03-21
**Status:** Complete

---

## Requirements Inventory

### Functional Requirements (from PRD)

| FR ID | Description | Priority | Epic |
|-------|------------|----------|------|
| FR-001~004 | 인증/SSO/RBAC/로그인이력 | Must | E-001 |
| FR-010~013 | 포털 대시보드 위젯 | Must | E-002 |
| FR-020~027 | 전자결재 (기안/결재선/승인/반려/보류/대결/문서번호/PDF) | Must | E-003 |
| FR-030~035 | 게시판 (분류/CRUD/고정/댓글/첨부/검색) | Must | E-004 |
| FR-040~045 | 조직관리 (부서/사원/조직도/직급/인사발령/검색) | Must | E-005 |

## FR Coverage Map

| FR ID | Epic | Story | Status |
|-------|------|-------|--------|
| FR-001 | E-001 | S-001 | Covered |
| FR-002 | E-001 | S-001 | Covered |
| FR-003 | E-001 | S-002 | Covered |
| FR-004 | E-001 | S-002 | Covered |
| FR-010 | E-002 | S-003 | Covered |
| FR-011 | E-002 | S-003 | Covered |
| FR-012 | E-002 | S-003 | Covered |
| FR-013 | E-002 | S-003 | Covered |
| FR-020 | E-003 | S-004 | Covered |
| FR-021 | E-003 | S-004 | Covered |
| FR-022 | E-003 | S-005 | Covered |
| FR-023 | E-003 | S-005 | Covered |
| FR-024 | E-003 | S-005 | Covered |
| FR-025 | E-003 | S-006 | Covered |
| FR-026 | E-003 | S-004 | Covered |
| FR-027 | E-003 | S-006 | Covered |
| FR-030 | E-004 | S-007 | Covered |
| FR-031 | E-004 | S-007 | Covered |
| FR-032 | E-004 | S-007 | Covered |
| FR-033 | E-004 | S-008 | Covered |
| FR-034 | E-004 | S-008 | Covered |
| FR-035 | E-004 | S-008 | Covered |
| FR-040 | E-005 | S-009 | Covered |
| FR-041 | E-005 | S-010 | Covered |
| FR-042 | E-005 | S-009 | Covered |
| FR-043 | E-005 | S-009 | Covered |
| FR-044 | E-005 | S-011 | Covered |
| FR-045 | E-005 | S-010 | Covered |

---

## Epic 1: 사용자 인증 및 권한

**ID:** E-001 | **Priority:** Must | **Phase:** MVP | **Complexity:** M | **Dependencies:** None

### Description
Azure AD SSO 연동 + 자체 로그인, JWT 기반 인증, RBAC 역할 기반 접근제어.

### Stories

#### Story 1.1: 로그인 (자체 + SSO) 및 토큰 관리

**ID:** S-001 | **Points:** 8

**As a** 기업 임직원,
**I want** 회사 Azure AD 계정 또는 이메일/비밀번호로 로그인하고 싶다,
**So that** SmartWork 그룹웨어에 안전하게 접근할 수 있다.

**Acceptance Criteria:**

```gherkin
Given 로그인 페이지에 접속한 상태에서
When Azure AD SSO 버튼을 클릭하면
Then Microsoft 로그인 화면이 표시되고 인증 후 JWT가 발급되어 대시보드로 이동한다

Given 로그인 페이지에서
When 유효한 이메일과 비밀번호를 입력하고 로그인 버튼을 클릭하면
Then JWT access token(1시간)과 refresh token(14일)이 발급되고 대시보드로 이동한다

Given 잘못된 비밀번호를 입력한 상태에서
When 로그인을 시도하면
Then "이메일 또는 비밀번호가 올바르지 않습니다" 에러가 표시된다

Given access token이 만료된 상태에서
When API 요청을 보내면
Then refresh token으로 자동 갱신 후 원래 요청이 재시도된다
```

**Tasks:**
- [ ] Spring Security 설정 (SecurityConfig, JWT 필터)
- [ ] JwtProvider 구현 (토큰 생성, 검증, 갱신)
- [ ] MSAL 연동 SsoService 구현
- [ ] Employee 엔티티 + 리포지토리
- [ ] 로그인 API 엔드포인트 (POST /auth/login, /auth/sso/callback, /auth/refresh)
- [ ] 프론트엔드 로그인 페이지 + MSAL.js 연동
- [ ] Axios 인터셉터 (토큰 자동 갱신)
- [ ] 단위 테스트 (JWT 검증, 로그인 실패 케이스)

#### Story 1.2: RBAC 권한 관리 및 로그인 이력

**ID:** S-002 | **Points:** 5

**As a** 시스템 관리자,
**I want** 사용자 역할에 따라 접근 권한을 제어하고 싶다,
**So that** 민감한 기능에 대한 보안을 유지할 수 있다.

**Acceptance Criteria:**

```gherkin
Given USER 역할의 사용자가
When 조직관리의 부서 생성 API를 호출하면
Then 403 Forbidden 에러가 반환된다

Given HR_MANAGER 역할의 사용자가
When 사원 등록 API를 호출하면
Then 정상적으로 사원이 등록된다

Given 사용자가 로그인에 성공하면
When 로그인 이력이
Then 로그인 시각, IP 주소, 브라우저 정보가 기록된다
```

---

## Epic 2: 포털 대시보드

**ID:** E-002 | **Priority:** Must | **Phase:** MVP | **Complexity:** S | **Dependencies:** E-001, E-003, E-004

### Description
로그인 후 첫 화면. 결재 대기, 최신 공지, 오늘 일정, 결재 현황을 위젯으로 통합 표시.

### Stories

#### Story 2.1: 대시보드 위젯 구성

**ID:** S-003 | **Points:** 8

**As a** 로그인된 임직원,
**I want** 대시보드에서 오늘의 주요 업무 현황을 한눈에 보고 싶다,
**So that** 중요한 결재나 공지를 놓치지 않을 수 있다.

**Acceptance Criteria:**

```gherkin
Given 대시보드에 접속한 상태에서
When 페이지가 로드되면
Then 결재 대기 건수와 최근 3건의 제목이 위젯에 표시된다

Given 전사 공지가 등록된 상태에서
When 대시보드를 확인하면
Then 최신 공지 5건이 제목과 날짜와 함께 표시되고 클릭 시 상세 페이지로 이동한다

Given 기안한 결재 문서가 있는 상태에서
When 대시보드의 결재 현황 카드를 확인하면
Then 기안중/승인대기/완료/반려 건수가 각각 표시된다

Given 결재 대기 위젯에서
When 문서 제목을 클릭하면
Then 해당 결재 문서 상세 페이지로 이동한다
```

**Tasks:**
- [ ] PortalController + DashboardService 구현
- [ ] 결재 대기 건수 집계 쿼리 (ApprovalLine 기반)
- [ ] 최신 공지 조회 API
- [ ] 내 결재 현황 집계 API
- [ ] 프론트엔드 Dashboard 페이지 + 위젯 컴포넌트 (Ant Design Card, Statistic)
- [ ] API 응답 캐싱 (Redis, 5분 TTL)

---

## Epic 3: 전자결재

**ID:** E-003 | **Priority:** Must | **Phase:** MVP | **Complexity:** L | **Dependencies:** E-001, E-005

### Description
결재 문서 기안, 결재선 자동 생성, 순차 승인/반려/보류, 상태 추적, 문서번호 발번.

### Stories

#### Story 3.1: 결재 문서 기안 및 결재선 생성

**ID:** S-004 | **Points:** 13

**As a** 임직원,
**I want** 기안서/휴가신청서/지출결의서를 작성하고 결재를 요청하고 싶다,
**So that** 종이 없이 온라인으로 결재를 처리할 수 있다.

**Acceptance Criteria:**

```gherkin
Given 전자결재 메뉴에서 "새 결재"를 클릭하고
When 양식(기안/휴가/지출)을 선택하면
Then 해당 양식에 맞는 입력 폼이 표시된다

Given 기안서 양식에서 내용을 작성하고
When "결재 요청" 버튼을 클릭하면
Then 문서번호(2026-MKT-00001)가 자동 발번되고 결재선이 조직도 기반으로 자동 생성된다

Given 결재선이 자동 생성된 상태에서
When 결재선 미리보기를 확인하면
Then 기안자 → 팀장 → 부서장 순서로 결재선이 표시된다

Given 필수 입력 항목을 비운 상태에서
When 결재 요청을 시도하면
Then 해당 필드에 유효성 검증 에러가 표시된다
```

**Tasks:**
- [ ] ApprovalDocument, ApprovalLine 엔티티 구현
- [ ] 결재선 자동 생성 로직 (조직도 트리 탐색)
- [ ] 문서번호 발번 서비스 (연도-부서코드-일련번호)
- [ ] ApprovalController + ApprovalService (기안 API)
- [ ] 프론트엔드: 양식 선택 → 폼 입력 → 결재선 미리보기 → 제출
- [ ] Ant Design Form + 유효성 검증
- [ ] 단위 테스트 (결재선 생성, 문서번호 발번)

#### Story 3.2: 결재 승인/반려/보류 및 상태 추적

**ID:** S-005 | **Points:** 13

**As a** 결재권자 (팀장/부서장),
**I want** 대기 중인 결재 문서를 확인하고 승인하거나 반려하고 싶다,
**So that** 업무 의사결정을 신속하게 처리할 수 있다.

**Acceptance Criteria:**

```gherkin
Given 결재 대기함에 문서가 있는 상태에서
When 문서를 클릭하면
Then 문서 내용과 결재선 현황이 표시된다

Given 결재 문서 상세에서
When "승인" 버튼을 클릭하고 의견을 입력한 후 확인하면
Then 해당 단계가 APPROVED로 변경되고 다음 결재자에게 알림이 발송된다

Given 최종 결재자가 승인하면
When 결재선의 모든 단계가 APPROVED이면
Then 문서 상태가 APPROVED로 변경되고 기안자에게 완료 알림이 발송된다

Given 결재 문서 상세에서
When "반려" 버튼을 클릭하고 반려 사유를 입력하면
Then 문서 상태가 REJECTED로 변경되고 기안자에게 반려 알림이 발송된다

Given 결재 문서 목록에서
When 기안함/결재대기함/결재완료함/반려함 탭을 클릭하면
Then 해당 상태의 문서만 필터링되어 페이지네이션과 함께 표시된다
```

**Tasks:**
- [ ] 결재 승인/반려/보류 API 구현 (상태 머신)
- [ ] 알림 서비스 (웹 소켓 또는 폴링)
- [ ] 결재 문서 목록 API (상태별 필터, 페이지네이션)
- [ ] 결재 이력 기록 (시간, IP, 의견)
- [ ] 프론트엔드: 결재 상세 + 결재선 시각화 (Ant Design Steps)
- [ ] 프론트엔드: 결재함 탭 (Ant Design Tabs + Table)
- [ ] 통합 테스트 (결재 흐름: 기안 → 1차 승인 → 최종 승인)

#### Story 3.3: 대결 처리 및 PDF 출력

**ID:** S-006 | **Points:** 5

**As a** 결재권자,
**I want** 출장 시 대결자를 지정하여 결재가 지연되지 않게 하고 싶다,
**So that** 부재 중에도 업무가 원활하게 진행된다.

**Acceptance Criteria:**

```gherkin
Given 결재권자가 대결자를 지정한 상태에서
When 결재 문서가 해당 단계에 도달하면
Then 대결자에게도 결재 대기 알림이 발송된다

Given 완료된 결재 문서에서
When "PDF 다운로드" 버튼을 클릭하면
Then 문서 내용과 결재선 이력이 포함된 PDF 파일이 다운로드된다
```

---

## Epic 4: 게시판

**ID:** E-004 | **Priority:** Must | **Phase:** MVP | **Complexity:** M | **Dependencies:** E-001

### Description
전사 공지, 부서별 게시판, 자유게시판. 게시글 CRUD, 공지 고정, 댓글, 파일 첨부.

### Stories

#### Story 4.1: 게시판 및 게시글 관리

**ID:** S-007 | **Points:** 8

**As a** 임직원,
**I want** 게시판에 글을 작성하고 전사 공지를 확인하고 싶다,
**So that** 회사 소식을 파악하고 부서 내 정보를 공유할 수 있다.

**Acceptance Criteria:**

```gherkin
Given 게시판 목록에 접속한 상태에서
When 전사 공지/부서 게시판/자유게시판을 선택하면
Then 해당 게시판의 게시글이 최신순으로 페이지네이션되어 표시된다

Given 게시판에서 "글쓰기" 버튼을 클릭하고
When 제목과 본문을 입력하고 등록 버튼을 클릭하면
Then 게시글이 저장되고 목록에 즉시 표시된다

Given 관리자가 공지 고정을 설정하면
When 게시판 목록을 조회할 때
Then 고정된 게시글이 상단에 최대 5건 표시된다

Given 게시글 작성자가
When 자신의 게시글을 수정하거나 삭제하면
Then 내용이 업데이트되거나 소프트 삭제되어 목록에서 제거된다
```

**Tasks:**
- [ ] Board, Post 엔티티 구현
- [ ] BoardController + PostService 구현
- [ ] 게시글 CRUD API (페이지네이션, 공지 고정)
- [ ] 프론트엔드: 게시판 목록 + 게시글 목록 (Ant Design Table)
- [ ] 프론트엔드: 에디터 (React Quill 또는 TinyMCE)
- [ ] 권한 검증 (작성자 본인 또는 ADMIN만 수정/삭제)

#### Story 4.2: 댓글, 파일 첨부, 검색

**ID:** S-008 | **Points:** 8

**As a** 임직원,
**I want** 게시글에 댓글을 달고 파일을 첨부하고 검색하고 싶다,
**So that** 동료와 소통하고 필요한 자료를 빠르게 찾을 수 있다.

**Acceptance Criteria:**

```gherkin
Given 게시글 상세에서
When 댓글 입력창에 내용을 작성하고 등록하면
Then 댓글이 게시글 하단에 표시되고 대댓글도 1단계까지 가능하다

Given 게시글 작성 시
When 파일 첨부 영역에 파일을 드래그하면
Then 최대 5개, 파일당 10MB까지 업로드되고 첨부 목록에 표시된다

Given 10MB를 초과하는 파일을 첨부하면
When 업로드를 시도하면
Then "파일 크기는 10MB 이하여야 합니다" 에러가 표시된다

Given 게시판 검색창에 키워드를 입력하면
When 검색 버튼을 클릭하면
Then 제목과 본문에서 키워드가 포함된 게시글이 검색 결과로 표시된다
```

**Tasks:**
- [ ] PostComment 엔티티 + 댓글 API (대댓글 포함)
- [ ] Attachment 엔티티 + FileService (Azure Blob Storage 연동)
- [ ] 파일 업로드 API (용량 검증, 확장자 화이트리스트)
- [ ] PostgreSQL tsvector 기반 전문 검색
- [ ] 프론트엔드: 댓글 컴포넌트 (Ant Design Comment)
- [ ] 프론트엔드: 파일 업로드 (Ant Design Upload, Drag & Drop)
- [ ] 프론트엔드: 검색 (Ant Design Input.Search)

---

## Epic 5: 조직관리

**ID:** E-005 | **Priority:** Must | **Phase:** MVP | **Complexity:** M | **Dependencies:** E-001

### Description
부서·직급·사원 관리, 조직도 시각화, 인사발령 이력 관리.

### Stories

#### Story 5.1: 부서 관리 및 조직도

**ID:** S-009 | **Points:** 8

**As a** 인사팀 관리자,
**I want** 부서를 등록/수정/삭제하고 조직도를 확인하고 싶다,
**So that** 회사 조직 구조를 체계적으로 관리할 수 있다.

**Acceptance Criteria:**

```gherkin
Given 조직관리 메뉴에서
When 부서 등록 폼에 부서명, 부서코드, 상위부서를 입력하고 저장하면
Then 부서가 생성되고 조직도 트리에 반영된다

Given 조직도 페이지에 접속하면
When 페이지가 로드되면
Then 전체 조직 트리가 계층 구조로 시각화되어 표시된다

Given 조직도에서 특정 부서를 클릭하면
When 부서 상세가 표시되면
Then 부서장, 소속 사원 목록, 하위 부서가 함께 표시된다

Given 직급 관리에서
When 사원→대리→과장→차장→부장→이사→대표 직급을 설정하면
Then 각 직급에 레벨이 부여되어 결재선 자동 생성에 활용된다
```

**Tasks:**
- [ ] Organization, Position 엔티티 구현 (트리 구조)
- [ ] 부서 CRUD API (재귀 CTE 쿼리로 트리 조회)
- [ ] 직급 CRUD API
- [ ] 프론트엔드: 조직도 트리 (Ant Design Tree)
- [ ] 프론트엔드: 부서/직급 관리 폼 (Ant Design Form + TreeSelect)
- [ ] Redis 캐싱 (조직도 트리, 직급 목록)

#### Story 5.2: 사원 관리 및 검색

**ID:** S-010 | **Points:** 8

**As a** 인사팀 관리자,
**I want** 사원을 등록하고 정보를 관리하고 검색하고 싶다,
**So that** 인사 정보를 체계적으로 관리하고 필요한 사원을 빠르게 찾을 수 있다.

**Acceptance Criteria:**

```gherkin
Given 사원 관리 페이지에서
When 이름, 사번, 직급, 부서, 입사일, 연락처, 이메일을 입력하고 저장하면
Then 사원이 등록되고 해당 부서 소속으로 조직도에 반영된다

Given 사원 목록에서
When 이름 또는 부서명으로 검색하면
Then 해당 조건에 맞는 사원이 검색 결과에 표시된다

Given 사원 상세 페이지에서
When 연락처 필드를 확인하면
Then 개인정보(전화번호)는 AES-256으로 암호화되어 권한 있는 사용자에게만 복호화되어 표시된다

Given USER 역할의 사용자가
When 다른 사원의 연락처를 조회하면
Then 마스킹 처리되어 표시된다 (010-****-1234)
```

**Tasks:**
- [ ] Employee 엔티티 확장 (개인정보 암호화 컬럼)
- [ ] 사원 CRUD API (EmployeeService)
- [ ] AES-256 암호화/복호화 유틸리티
- [ ] 사원 검색 API (이름, 부서, 직급 필터)
- [ ] 프론트엔드: 사원 테이블 (Ant Design Table + 검색)
- [ ] 프론트엔드: 사원 등록/수정 폼
- [ ] 개인정보 마스킹 로직 (역할별 분기)

#### Story 5.3: 인사발령 관리

**ID:** S-011 | **Points:** 5

**As a** 인사팀 관리자,
**I want** 부서 이동이나 직급 변경 시 발령 처리하고 이력을 관리하고 싶다,
**So that** 인사 변동 사항을 체계적으로 추적할 수 있다.

**Acceptance Criteria:**

```gherkin
Given 사원 상세에서 "인사발령" 버튼을 클릭하고
When 이동할 부서와 발령일을 입력하고 저장하면
Then 사원의 소속 부서가 변경되고 인사발령 이력이 자동 기록된다

Given 사원의 인사발령 이력 탭을 클릭하면
When 이력 목록이 표시되면
Then 변경 유형(입사/이동/승진/퇴사), 이전·이후 부서/직급, 발령일이 시간순으로 표시된다
```

---

## Summary

| Metric | Value |
|--------|-------|
| Total Epics | 5 |
| Total Stories | 11 |
| Total Story Points | 89 |
| Must-Have Points | 89 |
| Sprint 1 Target | E-001 + E-005 (29pt) |
| Sprint 2 Target | E-003 (31pt) |
| Sprint 3 Target | E-004 (16pt) |
| Sprint 4 Target | E-002 + 통합 테스트 + 배포 (8pt+) |
""",
    },
    {
        "file_name": "project-context.md",
        "file_path": "planning-artifacts/project-context.md",
        "content": """---
workflowType: 'project-context'
---
# Project Context - SmartWork 기업용 그룹웨어

## Technology Stack & Versions

| Technology | Version | Purpose |
|-----------|---------|---------|
| Java | 17 (LTS) | 백엔드 런타임 |
| Spring Boot | 3.x | 웹 프레임워크 |
| Spring Security | 6.x | 인증/인가 (JWT, OAuth2, RBAC) |
| Spring Data JPA | 3.x | ORM + 리포지토리 |
| Hibernate | 6.x | JPA 구현체 |
| Flyway | 10.x | DB 마이그레이션 |
| PostgreSQL | 16.x | 데이터베이스 |
| Redis | 7.x | 캐싱 (Azure Cache for Redis) |
| React | 18.x | 프론트엔드 SPA |
| TypeScript | 5.x | 타입 안전성 |
| Ant Design | 5.x | UI 컴포넌트 프레임워크 |
| Zustand | 4.x | 상태 관리 |
| Axios | 1.x | HTTP 클라이언트 |
| Apache ECharts | 5.x | 차트 라이브러리 |
| MSAL.js | 2.x | Azure AD SSO (프론트엔드) |
| Azure App Service | — | Java 앱 호스팅 |
| Azure Database for PostgreSQL | — | 관리형 DB |
| Azure Blob Storage | — | 파일 스토리지 |
| Azure Cache for Redis | — | 관리형 Redis |
| Azure Key Vault | — | 시크릿 관리 |
| Docker | latest | 컨테이너화 |
| GitHub Actions | — | CI/CD |

## Critical Implementation Rules

1. **모든 API 응답은 DTO 클래스로 반환한다** — Entity를 직접 반환하지 않음. 순환 참조 방지 + 응답 형식 제어.
2. **결재 상태 변경은 상태 머신 패턴을 따른다** — DRAFT→PENDING→APPROVED/REJECTED. 잘못된 전이 방지.
3. **결재 완료 문서는 수정 불가** — APPROVED/REJECTED 상태의 문서는 UPDATE API 호출 시 403 반환.
4. **개인정보는 AES-256-GCM으로 암호화 저장** — 전화번호 등. 키는 Azure Key Vault에서 로드.
5. **조직도 변경 시 Redis 캐시 무효화** — 부서/사원 CRUD 후 관련 캐시 @CacheEvict.
6. **파일 업로드는 Azure Blob Storage에만 저장** — 로컬 파일시스템 사용 금지. SAS 토큰으로 접근 제어.
7. **Native Query 최소화** — Spring Data JPA + QueryDSL 사용. 불가피한 경우 @Query(nativeQuery=true)에 파라미터 바인딩.
8. **모든 엔티티는 BaseEntity 상속** — createdAt, updatedAt, createdBy, updatedBy 자동 기록 (@EntityListeners).
9. **비밀번호는 BCrypt(strength 12)로 해싱** — PasswordEncoder 빈 사용. 평문 비교 금지.
10. **결재 액션(승인/반려)마다 감사 로그 기록** — 시각, IP, 사용자, 의견을 ApprovalLine에 기록.

## Project Structure

```
smartwork/
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── portal/         # DashboardPage
│   │   │   ├── approval/       # ApprovalListPage, ApprovalDetailPage, ApprovalFormPage
│   │   │   ├── board/          # BoardListPage, PostListPage, PostDetailPage, PostEditorPage
│   │   │   └── organization/   # OrgTreePage, EmployeeListPage, EmployeeDetailPage
│   │   ├── components/
│   │   │   ├── common/         # AppLayout, Header, Sidebar, ProtectedRoute
│   │   │   ├── approval/       # ApprovalForm, ApprovalLineView, StatusBadge, ApprovalTabs
│   │   │   ├── board/          # PostTable, PostEditor, CommentList, FileUploader
│   │   │   └── organization/   # OrgTree, EmployeeTable, PositionSelect, PersonnelHistoryTable
│   │   ├── api/                # authApi.ts, approvalApi.ts, boardApi.ts, orgApi.ts, fileApi.ts
│   │   ├── stores/             # authStore.ts, approvalStore.ts, boardStore.ts, orgStore.ts
│   │   ├── types/              # auth.ts, approval.ts, board.ts, organization.ts, common.ts
│   │   ├── hooks/              # useAuth.ts, usePagination.ts
│   │   └── utils/              # dateUtils.ts, formatUtils.ts, permissionUtils.ts
│   ├── public/
│   └── package.json
├── backend/
│   ├── src/main/java/com/smartwork/
│   │   ├── SmartWorkApplication.java
│   │   ├── config/
│   │   │   ├── SecurityConfig.java
│   │   │   ├── CorsConfig.java
│   │   │   ├── RedisConfig.java
│   │   │   └── AuditConfig.java    # JPA Auditing
│   │   ├── auth/
│   │   │   ├── AuthController.java
│   │   │   ├── AuthService.java
│   │   │   ├── JwtProvider.java
│   │   │   ├── JwtAuthenticationFilter.java
│   │   │   ├── SsoService.java
│   │   │   └── dto/ (LoginRequest, TokenResponse)
│   │   ├── portal/
│   │   │   ├── PortalController.java
│   │   │   ├── DashboardService.java
│   │   │   └── dto/ (DashboardResponse)
│   │   ├── approval/
│   │   │   ├── ApprovalController.java
│   │   │   ├── ApprovalService.java
│   │   │   ├── ApprovalLineService.java
│   │   │   ├── DocumentNumberService.java
│   │   │   ├── entity/ (ApprovalDocument, ApprovalLine)
│   │   │   ├── repository/ (ApprovalDocumentRepository, ApprovalLineRepository)
│   │   │   └── dto/ (ApprovalRequest, ApprovalResponse, ApprovalLineResponse)
│   │   ├── board/
│   │   │   ├── BoardController.java
│   │   │   ├── PostController.java
│   │   │   ├── PostService.java
│   │   │   ├── CommentService.java
│   │   │   ├── entity/ (Board, Post, PostComment)
│   │   │   ├── repository/ (BoardRepository, PostRepository, CommentRepository)
│   │   │   └── dto/ (PostRequest, PostResponse, CommentRequest, CommentResponse)
│   │   ├── organization/
│   │   │   ├── OrgController.java
│   │   │   ├── EmployeeController.java
│   │   │   ├── OrgService.java
│   │   │   ├── EmployeeService.java
│   │   │   ├── PositionService.java
│   │   │   ├── PersonnelService.java
│   │   │   ├── entity/ (Organization, Employee, Position, PersonnelHistory)
│   │   │   ├── repository/ (OrgRepository, EmployeeRepository, PositionRepository)
│   │   │   └── dto/ (OrgRequest, OrgResponse, EmployeeRequest, EmployeeResponse)
│   │   ├── file/
│   │   │   ├── FileController.java
│   │   │   ├── FileService.java
│   │   │   ├── entity/ (Attachment)
│   │   │   └── repository/ (AttachmentRepository)
│   │   └── common/
│   │       ├── entity/ (BaseEntity)
│   │       ├── dto/ (ApiResponse, PageResponse)
│   │       ├── exception/ (GlobalExceptionHandler, BusinessException, ErrorCode)
│   │       └── util/ (CryptoUtils, DateUtils)
│   ├── src/main/resources/
│   │   ├── application.yml
│   │   ├── application-local.yml
│   │   ├── application-staging.yml
│   │   ├── application-prod.yml
│   │   └── db/migration/
│   │       ├── V1__create_organizations.sql
│   │       ├── V2__create_employees.sql
│   │       ├── V3__create_positions.sql
│   │       ├── V4__create_approval_documents.sql
│   │       ├── V5__create_boards_posts.sql
│   │       └── V6__create_attachments.sql
│   ├── src/test/java/com/smartwork/
│   │   ├── auth/ (AuthServiceTest, JwtProviderTest)
│   │   ├── approval/ (ApprovalServiceTest, ApprovalIntegrationTest)
│   │   ├── board/ (PostServiceTest)
│   │   └── organization/ (OrgServiceTest, EmployeeServiceTest)
│   └── build.gradle
├── docker-compose.yml          # PostgreSQL + Redis (로컬 개발)
├── Dockerfile
└── .github/workflows/
    ├── ci.yml                  # PR → build + test
    └── deploy.yml              # main → Azure 배포
```

## Development Conventions

### Naming Conventions
- **Java:** camelCase (변수, 메서드), PascalCase (클래스, 인터페이스, DTO)
- **TypeScript:** camelCase (변수, 함수), PascalCase (컴포넌트, 타입/인터페이스)
- **파일명:** PascalCase (Java 클래스), kebab-case (React 컴포넌트 파일)
- **패키지:** 도메인 기반 (com.smartwork.approval, com.smartwork.board)
- **API 경로:** kebab-case, 복수형 (/api/approvals, /api/boards/{id}/posts)
- **DB 테이블:** snake_case, 복수형 (employees, approval_documents, post_comments)
- **DB 컬럼:** snake_case (employee_number, created_at, organization_id)

### Code Style
- Java: Google Java Format, Checkstyle (line length 120)
- TypeScript: ESLint + Prettier (semi: true, singleQuote: false)
- 커밋 메시지: Conventional Commits (feat:, fix:, docs:, refactor:, test:)

### Git Workflow
- `main`: 프로덕션 배포 브랜치 (protected)
- `develop`: 개발 통합 브랜치
- `feature/*`: 기능 브랜치 (develop에서 분기)
- PR 리뷰 필수 (최소 1인), CI 통과 후 Squash Merge

### Testing Strategy
- 백엔드: JUnit 5 + Mockito (단위) + @SpringBootTest + Testcontainers (통합)
- 프론트엔드: Vitest + React Testing Library
- 커버리지 목표: 80% 이상
- E2E: Playwright (주요 결재 흐름)

## Environment Setup

### Prerequisites
- Java 17+ (Adoptium Temurin)
- Node.js 20+ (LTS)
- PostgreSQL 16+ (또는 Docker)
- Redis 7+ (또는 Docker)
- Azure CLI (배포 시)

### Configuration (application-local.yml)
```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/smartwork
    username: smartwork
    password: smartwork
  jpa:
    hibernate:
      ddl-auto: validate
  redis:
    host: localhost
    port: 6379

jwt:
  secret: your-256-bit-secret-key
  access-expiration: 3600000      # 1시간
  refresh-expiration: 1209600000  # 14일

azure:
  ad:
    client-id: your-azure-ad-client-id
    tenant-id: your-azure-ad-tenant-id
  blob:
    connection-string: DefaultEndpointsProtocol=https;AccountName=...
    container-name: smartwork-files
  keyvault:
    uri: https://smartwork-vault.vault.azure.net/

crypto:
  aes-key: ${CRYPTO_AES_KEY}     # Azure Key Vault에서 로드
```

### Running Locally
```bash
# Docker로 PostgreSQL + Redis 실행
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
# Sprint Status - SmartWork 기업용 그룹웨어

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
  # Epic E-001: 사용자 인증 및 권한
  e-001:
    status: backlog
    stories:
      s-001:  # 로그인 (자체 + SSO) 및 토큰 관리 (8pt)
        status: ready-for-dev
      s-002:  # RBAC 권한 관리 및 로그인 이력 (5pt)
        status: ready-for-dev
    retrospective:
      status: optional

  # Epic E-002: 포털 대시보드
  e-002:
    status: backlog
    stories:
      s-003:  # 대시보드 위젯 구성 (8pt)
        status: backlog
    retrospective:
      status: optional

  # Epic E-003: 전자결재
  e-003:
    status: backlog
    stories:
      s-004:  # 결재 문서 기안 및 결재선 생성 (13pt)
        status: backlog
      s-005:  # 결재 승인/반려/보류 및 상태 추적 (13pt)
        status: backlog
      s-006:  # 대결 처리 및 PDF 출력 (5pt)
        status: backlog
    retrospective:
      status: optional

  # Epic E-004: 게시판
  e-004:
    status: backlog
    stories:
      s-007:  # 게시판 및 게시글 관리 (8pt)
        status: backlog
      s-008:  # 댓글, 파일 첨부, 검색 (8pt)
        status: backlog
    retrospective:
      status: optional

  # Epic E-005: 조직관리
  e-005:
    status: backlog
    stories:
      s-009:  # 부서 관리 및 조직도 (8pt)
        status: ready-for-dev
      s-010:  # 사원 관리 및 검색 (8pt)
        status: ready-for-dev
      s-011:  # 인사발령 관리 (5pt)
        status: ready-for-dev
    retrospective:
      status: optional
```

## Sprint Plan

### Sprint 1 (Week 1-3)
**Goal:** 인증 시스템 + 조직관리 기반 구축
**Stories:** S-001 (8pt), S-002 (5pt), S-009 (8pt), S-010 (8pt)
**Total:** 29pt

### Sprint 2 (Week 4-6)
**Goal:** 전자결재 전체 기능
**Stories:** S-004 (13pt), S-005 (13pt), S-006 (5pt)
**Total:** 31pt

### Sprint 3 (Week 7-9)
**Goal:** 게시판 전체 기능
**Stories:** S-007 (8pt), S-008 (8pt)
**Total:** 16pt

### Sprint 4 (Week 10-12)
**Goal:** 포털 대시보드 + 인사발령 + 통합 테스트 + 배포
**Stories:** S-003 (8pt), S-011 (5pt) + QA + 배포
**Total:** 13pt+

## Sprint Summary

| Metric | Value |
|--------|-------|
| Current Sprint | Sprint 1 |
| Sprint Goal | 인증 시스템 + 조직관리 기반 구축 |
| Total Points | 89 |
| Completed Points | 0 |
| In Progress Points | 0 |
| Remaining Points | 89 |

## Blockers

| Story | Blocker | Status |
|-------|---------|--------|
| S-001 | Azure AD 테넌트 설정 및 앱 등록 필요 | 대기 중 |
| - | 없음 | - |
""",
    },
]
