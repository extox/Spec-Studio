"""Default guide pages content for seeding into DB."""

DEFAULT_GUIDE_PAGES = [
    {
        "slug": "overview",
        "title": "서비스 개요",
        "group_name": "기본",
        "sort_order": 0,
        "content_ko": """<h1>서비스 개요</h1>
<p><strong>Dev.AI Spec Studio</strong>는 AI-Driven Development(AIDD) 실행을 위한 웹기반 Spec lifecycle 관리 협업 서비스입니다. 소프트웨어 개발의 기획부터 구현 준비까지, 6명의 AI 전문가 페르소나와 체계적으로 산출물을 만들어갑니다.</p>

<h2>핵심 개념 용어</h2>
<table>
<thead><tr><th>개념</th><th>설명</th><th>예시</th></tr></thead>
<tbody>
<tr><td><strong>프로젝트</strong></td><td>하나의 소프트웨어 개발 단위</td><td>"TaskFlow - AI 할일 관리 서비스"</td></tr>
<tr><td><strong>워크플로우</strong></td><td>단계별 진행 프로세스</td><td>Create PRD (12단계)</td></tr>
<tr><td><strong>페르소나</strong></td><td>전문 분야 AI 에이전트</td><td>PM (John), Architect (Winston)</td></tr>
<tr><td><strong>아티팩트</strong></td><td>생성된 문서 산출물</td><td>PRD.md, architecture.md</td></tr>
<tr><td><strong>실행 세션</strong></td><td>페르소나와의 대화 세션</td><td>"PM (John) - Create PRD"</td></tr>
<tr><td><strong>A/P/R/C</strong></td><td>워크플로우 단계별 액션 메뉴</td><td>Advanced, Party, Propose, Continue</td></tr>
</tbody>
</table>

<h2>전체 이용 흐름</h2>
<ol>
<li><strong>회원가입</strong> — 이메일/비밀번호로 가입 (첫 사용자 = 관리자)</li>
<li><strong>LLM 설정</strong> — 설정 메뉴에서 LLM 프로바이더 및 API 키 등록</li>
<li><strong>프로젝트 생성</strong> — 프로젝트명과 설명 입력</li>
<li><strong>워크플로우 실행</strong> — BMad 워크플로우 선택, 페르소나가 단계별 안내</li>
<li><strong>아티팩트 생성</strong> — 대화를 통해 산출물이 자동 생성/저장</li>
<li><strong>다음 단계</strong> — 이전 아티팩트를 컨텍스트로 활용하여 다음 워크플로우 진행</li>
</ol>

<h2>화면 구성</h2>
<table>
<thead><tr><th>영역</th><th>위치</th><th>기능</th></tr></thead>
<tbody>
<tr><td>상단 헤더</td><td>최상단 고정</td><td>로고, 언어 전환(KO/EN), 사용자 메뉴</td></tr>
<tr><td>좌측 사이드바</td><td>좌측 고정</td><td>대시보드, 프로젝트, 설정, 사용자 가이드</td></tr>
<tr><td>프로젝트 사이드바</td><td>프로젝트 내부 좌측</td><td>개요, 실행, 아티팩트, 멤버, 설정</td></tr>
<tr><td>메인 콘텐츠</td><td>중앙</td><td>선택한 메뉴의 내용 표시</td></tr>
</tbody>
</table>""",
        "content_en": "<h1>Service Overview</h1><p><strong>Dev.AI Spec Studio</strong> is a web-based Spec lifecycle management collaboration service for AI-Driven Development.</p>",
    },
    {
        "slug": "getting-started",
        "title": "시작하기",
        "group_name": "기본",
        "sort_order": 1,
        "content_ko": """<h1>시작하기</h1>

<h2>Step 1: 회원가입</h2>
<ol>
<li>서비스 접속 후 <strong>회원가입</strong> 클릭</li>
<li>이름, 이메일, 비밀번호(8자 이상) 입력</li>
<li>가입 완료 시 자동 로그인되어 대시보드로 이동</li>
</ol>
<div style="background:#f0f7ff;border:1px solid #bfdbfe;border-radius:8px;padding:12px;margin:12px 0;font-size:13px;"><strong>TIP:</strong> 첫 번째 가입자에게 시스템 관리자 권한이 자동 부여됩니다.</div>

<h2>Step 2: LLM API 설정 (필수)</h2>
<p>페르소나와 대화하려면 LLM 프로바이더를 먼저 등록해야 합니다.</p>
<ol>
<li>좌측 메뉴 → <strong>설정</strong> 클릭</li>
<li><strong>프로바이더</strong> 선택 (OpenAI, Anthropic, Google, Ollama 등)</li>
<li><strong>모델</strong> 선택 (예: gpt-4o-mini, claude-sonnet-4-20250514)</li>
<li>Dify 등 자체 호스팅 프로바이더는 <strong>Base URL</strong> 입력 필요</li>
<li><strong>API Key</strong> 입력 (암호화되어 저장됨)</li>
<li><strong>"기본값으로 설정"</strong> 체크 → <strong>설정 추가</strong> 클릭</li>
</ol>
<div style="background:#f0f7ff;border:1px solid #bfdbfe;border-radius:8px;padding:12px;margin:12px 0;font-size:13px;"><strong>TIP:</strong> LLM 설정 없이 워크플로우를 시작하면 "No default LLM configuration" 에러가 발생합니다.</div>

<h2>Step 3: 프로젝트 생성</h2>
<ol>
<li>대시보드 → <strong>새 프로젝트</strong> 클릭</li>
<li><strong>프로젝트 이름</strong> 입력</li>
<li><strong>설명</strong> 입력 — 페르소나가 프로젝트를 이해하는 컨텍스트로 사용</li>
<li><strong>생성</strong> 클릭 → 프로젝트 개요 페이지로 이동</li>
</ol>

<h2>Step 4: 첫 워크플로우 실행</h2>
<ol>
<li>프로젝트 → <strong>실행</strong> 메뉴 → <strong>새 실행</strong> 클릭</li>
<li><strong>워크플로우 실행</strong> 탭에서 "Create Project Brief" 선택</li>
<li>페르소나가 자동으로 인사하고 Step 1을 안내합니다</li>
<li>페르소나의 질문에 답하거나, <strong>[R] Propose</strong>를 눌러 AI가 대신 작성</li>
<li><strong>[C] Continue</strong>로 다음 단계로 넘어갑니다</li>
</ol>""",
        "content_en": "<h1>Getting Started</h1><p>1. Sign up. 2. Configure LLM API. 3. Create a project. 4. Start a workflow.</p>",
    },
    {
        "slug": "dashboard",
        "title": "대시보드",
        "group_name": "기본",
        "sort_order": 2,
        "content_ko": """<h1>대시보드</h1>
<p>로그인 후 첫 화면입니다. 참여 중인 프로젝트와 최근 활동을 확인합니다.</p>

<h2>구성 요소</h2>
<h3>히어로 영역</h3>
<p>시간대별 인사(좋은 아침/오후/저녁) + 사용자 이름 + 서비스 소개</p>

<h3>참여 중인 프로젝트</h3>
<ul>
<li>내가 멤버로 참여한 프로젝트 카드 목록</li>
<li>각 카드: 프로젝트명, 설명, 오너 이름, 멤버 수, 수정일, 단계 뱃지</li>
<li>카드 클릭 시 프로젝트 개요 페이지로 이동</li>
</ul>

<h3>최근 활동 (최대 10개)</h3>
<ul>
<li>📄 아티팩트 생성/수정</li>
<li>💬 실행 세션 참여</li>
<li>👤 멤버 추가</li>
<li>➕ 프로젝트 생성</li>
<li>✏️ 프로젝트 정보 수정, 🔄 단계 변경</li>
</ul>
<p>각 항목 클릭 시 해당 위치로 이동. 시간은 한국 시간 기준.</p>""",
        "content_en": "<h1>Dashboard</h1><p>First screen after login. View projects and recent activities.</p>",
    },
    {
        "slug": "project-overview",
        "title": "프로젝트 개요",
        "group_name": "기본",
        "sort_order": 3,
        "content_ko": """<h1>프로젝트 개요</h1>
<p>프로젝트에 들어가면 첫 화면입니다.</p>

<h2>구성</h2>
<ul>
<li><strong>프로젝트 헤더</strong> — 이름, 설명, 생성일, 수정일, 단계 뱃지</li>
<li><strong>요약 카드 3개</strong> — 실행 세션 수, 아티팩트 수, 멤버 수 (클릭 시 이동)</li>
<li><strong>아티팩트 진행 체크리스트</strong> — 7개 BMad 아티팩트 완성 여부 (✅/⬜) + 진행률 바</li>
<li><strong>최근 실행 세션</strong> — 최근 3개 세션 미리보기</li>
<li><strong>팀 멤버</strong> — 이니셜 아바타 + 이름 + 역할</li>
<li><strong>다음 단계 추천</strong> — 미작성 아티팩트에 맞는 워크플로우 추천</li>
</ul>""",
        "content_en": "<h1>Project Overview</h1><p>Summary cards, artifact checklist, recent sessions, team members, next step recommendation.</p>",
    },
    {
        "slug": "workflow",
        "title": "워크플로우 실행",
        "group_name": "핵심 기능",
        "sort_order": 4,
        "content_ko": """<h1>워크플로우 실행</h1>
<p>프로젝트 → <strong>실행</strong> → <strong>새 실행</strong>에서 시작합니다.</p>

<h2>워크플로우 목록</h2>
<table>
<thead><tr><th>단계</th><th>워크플로우</th><th>산출물</th><th>단계 수</th></tr></thead>
<tbody>
<tr><td>분석</td><td>Create Project Brief</td><td>product-brief.md</td><td>5</td></tr>
<tr><td>기획</td><td>Create PRD</td><td>PRD.md</td><td>12</td></tr>
<tr><td>기획</td><td>Validate PRD</td><td>—</td><td>13</td></tr>
<tr><td>기획</td><td>Create UX Design</td><td>ux-spec.md</td><td>14</td></tr>
<tr><td>설계</td><td>Create Architecture</td><td>architecture.md</td><td>8</td></tr>
<tr><td>구현</td><td>Create Epics & Stories</td><td>epics.md</td><td>4</td></tr>
<tr><td>구현</td><td>Sprint Planning</td><td>sprint-status.md</td><td>5</td></tr>
<tr><td>구현</td><td>Create Story</td><td>story.md</td><td>6</td></tr>
</tbody>
</table>

<h2>진행 방법</h2>
<ol>
<li>워크플로우 선택 → 페르소나가 자동 배정, Step 1 안내</li>
<li>페르소나 질문에 답하거나 <strong>[R] Propose</strong>로 AI 자동 작성</li>
<li><strong>[C] Continue</strong>로 다음 단계 진행</li>
<li>마지막 단계에서 아티팩트 자동 생성</li>
</ol>

<h2>권장 순서</h2>
<p>Product Brief → PRD → UX Spec → Architecture → Epics → Sprint Planning → Story</p>

<h2>워크플로우 진행 화면</h2>
<ul>
<li><strong>상단 패널</strong> — 워크플로우명 + 단계 카운터 + 진행률 바 + A/P/R/C 메뉴</li>
<li><strong>채팅 영역</strong> — 페르소나 표시, 메시지, Bold 클릭 입력, 복사/저장 버튼</li>
<li><strong>문서 패널</strong> — 우측에 아티팩트 파일 프리뷰/편집</li>
</ul>""",
        "content_en": "<h1>Workflows</h1><p>BMad workflows: Brief → PRD → UX → Architecture → Epics → Sprint → Story.</p>",
    },
    {
        "slug": "persona",
        "title": "AI 페르소나",
        "group_name": "핵심 기능",
        "sort_order": 5,
        "content_ko": """<h1>AI 페르소나</h1>
<table>
<thead><tr><th>페르소나</th><th>역할</th><th>전문 분야</th><th>성격</th></tr></thead>
<tbody>
<tr><td>🔍 Analyst (Mary)</td><td>비즈니스 분석가</td><td>시장 조사, 요구사항 도출</td><td>호기심 많고 열정적</td></tr>
<tr><td>📋 PM (John)</td><td>프로덕트 매니저</td><td>PRD, 요구사항 관리</td><td>직설적, 데이터 중심</td></tr>
<tr><td>🏗️ Architect (Winston)</td><td>시스템 아키텍트</td><td>시스템 설계, API</td><td>차분하고 실용적</td></tr>
<tr><td>🎨 UX Designer (Sally)</td><td>UX 디자이너</td><td>사용자 리서치, 와이어프레임</td><td>공감적, 스토리텔러</td></tr>
<tr><td>📊 Scrum Master (Bob)</td><td>스크럼 마스터</td><td>에픽/스토리, BDD</td><td>체계적, 모호함 불허</td></tr>
<tr><td>📝 Tech Writer (Paige)</td><td>기술 문서가</td><td>문서 작성, 다이어그램</td><td>인내심, 교육적</td></tr>
</tbody>
</table>

<h2>페르소나 전환</h2>
<p>채팅 상단 <strong>페르소나 전환</strong>을 클릭하면 대화 중 언제든 다른 페르소나로 전환 가능합니다. 대화 맥락은 유지됩니다.</p>

<div style="background:#f0f7ff;border:1px solid #bfdbfe;border-radius:8px;padding:12px;margin:12px 0;font-size:13px;"><strong>TIP:</strong> PRD 작성 중 기술 판단이 필요하면 Architect로 전환하여 의견을 구한 뒤 PM으로 돌아올 수 있습니다.</div>""",
        "content_en": "<h1>AI Personas</h1><p>6 expert personas: Analyst, PM, Architect, UX Designer, Scrum Master, Tech Writer.</p>",
    },
    {
        "slug": "aprc",
        "title": "A/P/R/C 메뉴",
        "group_name": "핵심 기능",
        "sort_order": 6,
        "content_ko": """<h1>A/P/R/C 메뉴</h1>
<p>워크플로우 각 단계에서 4가지 액션을 선택합니다.</p>

<h2>[A] Advanced Elicitation — 심층 분석</h2>
<table>
<thead><tr><th>기법</th><th>방법</th><th>효과</th></tr></thead>
<tbody>
<tr><td>소크라틱 질문</td><td>모든 가정에 "왜?"로 도전</td><td>숨겨진 전제 발견</td></tr>
<tr><td>퍼스트 프린시플</td><td>근본 원리로 분해</td><td>불필요한 복잡성 제거</td></tr>
<tr><td>프리모텀 분석</td><td>실패 상상 후 역추적</td><td>리스크 사전 발견</td></tr>
<tr><td>레드팀 리뷰</td><td>적대적 관점 비판</td><td>약점 식별</td></tr>
</tbody>
</table>

<h2>[P] Party Mode — 멀티 페르소나 토론</h2>
<ol>
<li><strong>Round 1</strong> — 게스트 페르소나 2명이 전문가 관점 제시</li>
<li><strong>Round 2</strong> — 서로의 의견에 동의/반박/보완</li>
<li><strong>합의 정리</strong> — 리드 페르소나가 합의·논쟁·액션아이템 종합</li>
</ol>

<h2>[R] Propose Mode — AI 자동 초안</h2>
<p>페르소나가 질문 대신 <strong>현재 단계 내용을 직접 작성하여 제안</strong>합니다. 사용자는 "좋습니다" 또는 수정 요청만 하면 됩니다.</p>

<h2>[C] Continue — 다음 단계</h2>
<p>현재 단계 완료 → 다음 단계로 이동. 마지막 단계에서는 아티팩트 자동 생성.</p>""",
        "content_en": "<h1>A/P/R/C Menu</h1><p>[A] Advanced, [P] Party, [R] Propose, [C] Continue.</p>",
    },
    {
        "slug": "artifact",
        "title": "아티팩트 관리",
        "group_name": "핵심 기능",
        "sort_order": 7,
        "content_ko": """<h1>아티팩트 관리</h1>
<p>프로젝트 → <strong>아티팩트</strong> 메뉴</p>

<h2>파일 관리 기능</h2>
<table>
<thead><tr><th>기능</th><th>방법</th></tr></thead>
<tbody>
<tr><td>파일 생성</td><td>하단 <strong>새 파일</strong> → 템플릿 선택 또는 빈 파일</td></tr>
<tr><td>편집</td><td>파일 선택 → <strong>편집</strong> 버튼 → Markdown 에디터</td></tr>
<tr><td>이름 변경</td><td>호버 → 연필 아이콘 → 인라인 편집</td></tr>
<tr><td>파일 이동</td><td>드래그 앤 드롭</td></tr>
<tr><td>삭제</td><td>호버 → 휴지통 → 확인 클릭</td></tr>
<tr><td>다운로드</td><td>개별: 뷰어 다운로드 아이콘 / 전체: "전체 다운로드"</td></tr>
<tr><td>정렬</td><td>이름순 → 수정일순 → 크기순 순환</td></tr>
</tbody>
</table>

<h2>버전 관리</h2>
<ul>
<li>수정마다 자동 버전 생성 (YYMMDD_HHMMSS 한국 시간)</li>
<li><strong>버전</strong> 버튼 → 히스토리 패널 → 과거 버전 클릭 → <strong>Diff 비교</strong></li>
<li><strong>복구</strong> 버튼 → 현재 시각 기준 새 버전으로 복원</li>
</ul>

<h2>채팅 연동</h2>
<ul>
<li>"이 내용을 PRD로 저장해줘" → AI가 BMad 템플릿에 맞춰 자동 저장</li>
<li>메시지 호버 → <strong>아티팩트로 저장</strong> → 파일명 입력 → 수동 저장</li>
<li>아티팩트 파일은 모든 대화에서 자동으로 컨텍스트로 로드</li>
</ul>

<h2>샘플 아티팩트</h2>
<p>아티팩트가 없을 때 3종 샘플 프로젝트 로드 가능: TaskFlow, SmartWork, TradeHub</p>""",
        "content_en": "<h1>Artifact Management</h1><p>Markdown files with version control, diff, drag-and-drop, and auto context loading.</p>",
    },
    {
        "slug": "collaboration",
        "title": "다중 사용자 협업",
        "group_name": "협업",
        "sort_order": 8,
        "content_ko": """<h1>다중 사용자 협업</h1>

<h2>멤버 관리</h2>
<ul>
<li>프로젝트 → <strong>멤버</strong>에서 이메일로 초대</li>
<li>역할: <strong>Owner</strong> (설정 수정 권한) / <strong>Member</strong> (실행, 편집 권한)</li>
</ul>

<h2>실시간 채팅</h2>
<ul>
<li>같은 세션에 여러 사용자 동시 접속</li>
<li>메시지 실시간 표시, 중지 버튼은 발신자에게만 표시</li>
<li>다른 사용자의 스트리밍 중에도 내 입력은 비활성화되지 않음</li>
</ul>

<h2>프로젝트 탐색</h2>
<ul>
<li><strong>전체 프로젝트</strong> — 미참여 프로젝트도 표시 (점선 테두리, "미참여" 뱃지)</li>
<li><strong>참여 중</strong> — 내가 멤버인 프로젝트</li>
<li><strong>내가 만든</strong> — 내가 오너인 프로젝트</li>
</ul>""",
        "content_en": "<h1>Multi-user Collaboration</h1><p>Real-time chat, member management, project exploration.</p>",
    },
    {
        "slug": "admin-settings",
        "title": "설정 및 프로필",
        "group_name": "협업",
        "sort_order": 9,
        "content_ko": """<h1>설정 및 프로필</h1>

<h2>LLM API 설정</h2>
<p>좌측 → <strong>설정</strong>에서 프로바이더 등록. 여러 개 등록 가능, 하나를 기본값으로 설정.</p>

<h2>프로필 관리</h2>
<p>우측 아바타 → <strong>프로필</strong>에서 이름 변경, 비밀번호 변경 가능. 이메일은 변경 불가.</p>

<h2>프로젝트 설정 (Owner 전용)</h2>
<p>프로젝트 → <strong>설정</strong>에서 이름/설명 수정, 단계 변경, 삭제.</p>
<div style="background:#f0f7ff;border:1px solid #bfdbfe;border-radius:8px;padding:12px;margin:12px 0;font-size:13px;"><strong>TIP:</strong> 프로젝트 설정은 Owner만 수정 가능합니다.</div>

<h2>언어 전환</h2>
<p>상단 <strong>KO/EN</strong> 스위치로 즉시 전환.</p>""",
        "content_en": "<h1>Settings & Profile</h1><p>LLM API config, profile management, project settings.</p>",
    },
    {
        "slug": "bmad",
        "title": "BMad Method 철학",
        "group_name": "철학",
        "sort_order": 10,
        "content_ko": """<h1>BMad Method 철학</h1>

<h2>AI-Driven Development (AIDD)란?</h2>
<p>소프트웨어 개발의 전 과정에서 AI를 <strong>핵심 협업 파트너</strong>로 활용하는 방법론입니다. 기획 → 설계 → 구현 준비의 모든 단계에서 AI 전문가 에이전트가 인간과 함께 사고하고, 검토하고, 제안합니다.</p>

<h2>5가지 핵심 원칙</h2>

<h3>1. 페르소나 기반 전문성</h3>
<p>범용 AI 대신 분야별 독립 페르소나. PM은 PM처럼, Architect는 Architect처럼 사고합니다.</p>

<h3>2. 단계별 워크플로우</h3>
<p>복잡한 산출물을 한 번에 만들지 않고 각 단계에서 하나의 관점에 집중하여 점진적으로 완성합니다.</p>

<h3>3. 컨텍스트 체인</h3>
<p>각 아티팩트는 이전 단계를 자동 참조합니다. Architecture는 PRD를 읽고, Epics는 PRD+Architecture를 읽습니다.</p>

<h3>4. 인간 중심 의사결정</h3>
<p>AI는 제안하고, 최종 결정은 인간이 합니다. A/P/R/C로 깊이와 속도를 조절합니다.</p>

<h3>5. 다자 협업 토론</h3>
<p>Party Mode에서 여러 페르소나가 토론하여 단일 관점의 편향을 방지합니다.</p>

<h2>산출물 체계</h2>
<table>
<thead><tr><th>산출물</th><th>목적</th><th>주요 내용</th></tr></thead>
<tbody>
<tr><td>Product Brief</td><td>프로젝트 개요</td><td>문제, 솔루션, 사용자, 범위, 비전</td></tr>
<tr><td>PRD</td><td>제품 요구사항</td><td>FR 20-50개, NFR, 사용자 저니, 로드맵</td></tr>
<tr><td>UX Spec</td><td>UX 설계</td><td>페르소나, IA, 사용자 흐름, 와이어프레임</td></tr>
<tr><td>Architecture</td><td>기술 아키텍처</td><td>ADR, 기술 스택, 시스템 구조, 데이터 모델</td></tr>
<tr><td>Epics & Stories</td><td>구현 계획</td><td>에픽, BDD 인수 기준, 스토리 포인트</td></tr>
<tr><td>Project Context</td><td>구현 규칙</td><td>기술 버전, 컨벤션, 프로젝트 구조</td></tr>
<tr><td>Sprint Status</td><td>스프린트 추적</td><td>상태 YAML, 스프린트 목표, 블로커</td></tr>
</tbody>
</table>

<h2>참고 자료</h2>
<ul>
<li><a href="https://github.com/bmadcode/bmad-method" target="_blank">BMad Method V6 GitHub</a></li>
<li><a href="https://www.youtube.com/@BMadCode" target="_blank">BMad Code YouTube</a></li>
</ul>""",
        "content_en": "<h1>BMad Method Philosophy</h1><p>AI-Driven Development with persona-based expertise, workflows, context chaining, and human-centered decisions.</p>",
    },
]
