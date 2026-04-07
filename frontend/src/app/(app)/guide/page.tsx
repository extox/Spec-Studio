"use client";

import { useState, useEffect } from "react";
import dynamic from "next/dynamic";
import { useI18n } from "@/lib/i18n";
import { cn } from "@/lib/utils";
import api from "@/lib/api";
import "@uiw/react-md-editor/markdown-editor.css";
import "@uiw/react-markdown-preview/markdown.css";

const MDEditor = dynamic(() => import("@uiw/react-md-editor"), { ssr: false });

interface DBGuidePage {
  id: number;
  slug: string;
  title: string;
  title_en?: string;
  group_name: string;
  group_name_en?: string;
  content_ko?: string;
  content_en?: string;
}

type Section =
  | "overview" | "getting-started" | "dashboard" | "project-overview"
  | "workflow" | "persona" | "artifact" | "aprc" | "collaboration" | "admin-settings" | "bmad"
  | string;

const DEFAULT_SECTIONS_KO: { id: string; label: string; group?: string }[] = [
  { id: "overview", label: "서비스 개요", group: "기본" },
  { id: "getting-started", label: "시작하기" },
  { id: "dashboard", label: "대시보드" },
  { id: "project-overview", label: "프로젝트 개요" },
  { id: "workflow", label: "워크플로우 실행", group: "핵심 기능" },
  { id: "persona", label: "AI 페르소나" },
  { id: "aprc", label: "A/P/R/C 메뉴" },
  { id: "artifact", label: "아티팩트 관리" },
  { id: "collaboration", label: "다중 사용자 협업", group: "협업" },
  { id: "admin-settings", label: "설정 및 프로필" },
  { id: "bmad", label: "BMad Method 철학", group: "철학" },
];

const DEFAULT_SECTIONS_EN: { id: string; label: string; group?: string }[] = [
  { id: "overview", label: "Overview", group: "Basics" },
  { id: "getting-started", label: "Getting Started" },
  { id: "dashboard", label: "Dashboard" },
  { id: "project-overview", label: "Project Overview" },
  { id: "workflow", label: "Workflows", group: "Core Features" },
  { id: "persona", label: "AI Personas" },
  { id: "aprc", label: "A/P/R/C Menu" },
  { id: "artifact", label: "Artifacts" },
  { id: "collaboration", label: "Collaboration", group: "Team" },
  { id: "admin-settings", label: "Settings & Profile" },
  { id: "bmad", label: "BMad Philosophy", group: "Philosophy" },
];

export default function GuidePage() {
  const { t, locale } = useI18n();
  const [section, setSection] = useState<string>("overview");
  const [dbPages, setDbPages] = useState<DBGuidePage[]>([]);
  const [dbContent, setDbContent] = useState<string | null>(null);

  // Load DB pages
  useEffect(() => {
    api.get("/guide/pages").then((r) => setDbPages(r.data)).catch(() => {});
  }, []);

  // Load DB content when section changes
  useEffect(() => {
    const dbPage = dbPages.find((p) => p.slug === section);
    if (dbPage) {
      api.get(`/guide/pages/${section}`).then((r) => {
        const content = locale === "ko"
          ? (r.data.content_ko || null)
          : (r.data.content_en || r.data.content_ko || null);
        setDbContent(content);
      }).catch(() => setDbContent(null));
    } else {
      setDbContent(null);
    }
  }, [section, dbPages, locale]);

  const DEFAULT_SECTIONS = locale === "ko" ? DEFAULT_SECTIONS_KO : DEFAULT_SECTIONS_EN;

  // Merge DB pages with defaults: DB pages replace matching slugs, extras appended
  const sections = (() => {
    if (dbPages.length === 0) return DEFAULT_SECTIONS;

    const merged: { id: string; label: string; group?: string }[] = [];

    // Add defaults
    for (const s of DEFAULT_SECTIONS) {
      merged.push(s);
    }

    // Add DB-only pages (not in defaults)
    for (const p of dbPages) {
      if (!DEFAULT_SECTIONS.some((d) => d.id === p.slug)) {
        const label = locale === "en" ? (p.title_en || p.title) : p.title;
        const group = locale === "en" ? (p.group_name_en || p.group_name) : p.group_name;
        merged.push({ id: p.slug, label, group: group || undefined });
      }
    }

    return merged;
  })();

  const exportToPdf = (currentSection: string, allSections: { id: string; label: string }[]) => {
    const contentEl = document.getElementById("guide-content");
    if (!contentEl) return;

    const title = allSections.find((s) => s.id === currentSection)?.label || "Guide";
    const html = contentEl.innerHTML;

    const printWindow = window.open("", "_blank", "width=900,height=700");
    if (!printWindow) return;

    printWindow.document.write(`<!DOCTYPE html><html><head>
<meta charset="utf-8">
<title>Dev.AI Spec Studio - ${title}</title>
<style>
@media print {
  @page { margin: 20mm 15mm; size: A4; }
  body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
}
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans KR', sans-serif; max-width: 700px; margin: 0 auto; padding: 40px 0; color: #1a1a2e; line-height: 1.7; font-size: 13px; }
h1 { font-size: 22px; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; margin-top: 0; }
h2 { font-size: 17px; margin-top: 24px; color: #334155; }
h3 { font-size: 14px; margin-top: 16px; }
table { border-collapse: collapse; width: 100%; border: 1px solid #cbd5e1; margin: 12px 0; }
thead { background: #f1f5f9; }
th, td { border: 1px solid #cbd5e1; padding: 6px 10px; text-align: left; font-size: 12px; }
tbody tr:nth-child(even) { background: #f8fafc; }
ul, ol { padding-left: 20px; }
li { margin: 3px 0; }
a { color: #6366f1; text-decoration: none; }
blockquote { border-left: 4px solid #6366f1; margin: 12px 0; padding: 8px 16px; background: #f5f3ff; }
img { max-width: 100%; border: 1px solid #e2e8f0; border-radius: 4px; margin: 8px 0; }
code { background: #f1f5f9; padding: 2px 4px; border-radius: 3px; font-size: 11px; }
.header-bar { text-align: center; font-size: 11px; color: #94a3b8; margin-bottom: 24px; border-bottom: 1px solid #e2e8f0; padding-bottom: 12px; }
.footer-bar { text-align: center; font-size: 10px; color: #94a3b8; margin-top: 32px; border-top: 1px solid #e2e8f0; padding-top: 12px; }
</style>
</head><body>
<div class="header-bar">Dev.AI Spec Studio — 사용자 가이드</div>
${html}
<div class="footer-bar">Dev.AI Spec Studio &copy; ${new Date().getFullYear()}</div>
</body></html>`);

    printWindow.document.close();
    setTimeout(() => {
      printWindow.print();
    }, 500);
  };

  let lastGroup = "";

  return (
    <div className="flex h-full">
      <div className="w-52 border-r bg-muted/20 p-3 overflow-auto shrink-0">
        <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-3 px-2">
          {t("guide.title")}
        </p>
        {sections.map((s) => {
          const showGroup = s.group && s.group !== lastGroup;
          if (s.group) lastGroup = s.group;
          return (
            <div key={s.id}>
              {showGroup && (
                <p className="text-[10px] font-semibold text-muted-foreground/60 uppercase tracking-wider mt-4 mb-1 px-2">
                  {s.group}
                </p>
              )}
              <button
                onClick={() => setSection(s.id)}
                className={cn(
                  "w-full text-left text-sm px-3 py-1.5 rounded-md transition-colors",
                  section === s.id
                    ? "bg-primary/10 text-primary font-medium"
                    : "text-muted-foreground hover:bg-muted hover:text-foreground"
                )}
              >
                {s.label}
              </button>
            </div>
          );
        })}
      </div>

      <div className="flex-1 overflow-auto p-8 max-w-4xl">
        <div className="flex justify-end mb-4">
          <button
            onClick={() => exportToPdf(section, sections)}
            className="flex items-center gap-1.5 px-3 py-1.5 text-xs text-muted-foreground hover:text-foreground border rounded-md hover:bg-muted transition-colors"
          >
            <svg className="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            PDF {t("files.download")}
          </button>
        </div>
        <div id="guide-content">
          {dbContent ? (
            dbContent.trim().startsWith("<") ? (
              // Legacy HTML content
              <article className="prose prose-sm max-w-none" dangerouslySetInnerHTML={{ __html: dbContent }} />
            ) : (
              // Markdown content
              <div data-color-mode="light">
                <MDEditor
                  value={dbContent}
                  preview="preview"
                  hideToolbar
                  height="auto"
                  visibleDragbar={false}
                />
              </div>
            )
          ) : (
            <GuideContent section={section} locale={locale} />
          )}
        </div>
      </div>
    </div>
  );
}

function ScreenshotPlaceholder({ label }: { label: string }) {
  return (
    <div className="my-4 rounded-lg border-2 border-dashed border-muted-foreground/20 bg-muted/10 p-6 text-center">
      <svg className="h-8 w-8 mx-auto text-muted-foreground/30 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
      </svg>
      <p className="text-xs text-muted-foreground/50">{label}</p>
    </div>
  );
}

function Tip({ children }: { children: React.ReactNode }) {
  return (
    <div className="my-3 rounded-lg bg-primary/5 border border-primary/10 px-4 py-3 text-sm">
      <span className="font-semibold text-primary mr-1">TIP:</span>
      {children}
    </div>
  );
}

function GuideContent({ section, locale }: { section: Section; locale: string }) {
  // All content in Korean (primary), English abbreviated
  switch (section) {
    case "overview": return (
      <article className="prose prose-sm max-w-none">
        <h1>서비스 개요</h1>
        <p>
          <strong>Dev.AI Spec Studio</strong>는 AI-Driven Development(AIDD) 실행을 위한 웹기반 Spec lifecycle 관리 협업 서비스입니다.
          소프트웨어 개발의 기획부터 구현 준비까지, 6명의 AI 전문가 페르소나와 체계적으로 산출물을 만들어갑니다.
        </p>

        <ScreenshotPlaceholder label="대시보드 화면" />

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
        <div className="not-prose my-4">
          <div className="flex items-center gap-2 text-sm">
            {["회원가입", "LLM 설정", "프로젝트 생성", "워크플로우 실행", "아티팩트 생성", "다음 단계"].map((step, i) => (
              <div key={i} className="flex items-center gap-2">
                {i > 0 && <span className="text-muted-foreground">→</span>}
                <span className="px-3 py-1 rounded-lg bg-primary/10 text-primary text-xs font-medium">{step}</span>
              </div>
            ))}
          </div>
        </div>

        <h2>화면 구성</h2>
        <table>
          <thead><tr><th>영역</th><th>위치</th><th>기능</th></tr></thead>
          <tbody>
            <tr><td>상단 헤더</td><td>최상단 고정</td><td>로고, 언어 전환(KO/EN), 사용자 메뉴(프로필/설정/관리자/로그아웃)</td></tr>
            <tr><td>좌측 사이드바</td><td>좌측 고정</td><td>대시보드, 프로젝트, 설정, 사용자 가이드 (접기/펼치기 가능)</td></tr>
            <tr><td>프로젝트 사이드바</td><td>프로젝트 내부 좌측</td><td>개요, 실행, 아티팩트, 멤버, 설정 (접기/펼치기 가능)</td></tr>
            <tr><td>메인 콘텐츠</td><td>중앙</td><td>선택한 메뉴의 내용 표시</td></tr>
          </tbody>
        </table>
      </article>
    );

    case "getting-started": return (
      <article className="prose prose-sm max-w-none">
        <h1>시작하기</h1>

        <h2>Step 1: 회원가입</h2>
        <ol>
          <li>서비스 접속 후 <strong>회원가입</strong> 클릭</li>
          <li>이름, 이메일, 비밀번호(8자 이상) 입력</li>
          <li>가입 완료 시 자동 로그인되어 대시보드로 이동</li>
        </ol>
        <Tip>첫 번째 가입자에게 시스템 관리자 권한이 자동 부여됩니다.</Tip>
        <ScreenshotPlaceholder label="회원가입 화면" />

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
        <Tip>LLM 설정 없이 워크플로우를 시작하면 "No default LLM configuration" 에러가 발생합니다.</Tip>
        <ScreenshotPlaceholder label="LLM API 설정 화면" />

        <h2>Step 3: 프로젝트 생성</h2>
        <ol>
          <li>대시보드 → <strong>새 프로젝트</strong> 클릭</li>
          <li><strong>프로젝트 이름</strong> 입력 (예: "AI 기반 할일 관리 서비스")</li>
          <li><strong>설명</strong> 입력 — 페르소나가 프로젝트를 이해하는 컨텍스트로 사용되므로 가능한 구체적으로 작성</li>
          <li><strong>생성</strong> 클릭 → 프로젝트 개요 페이지로 이동</li>
        </ol>
        <Tip>프로젝트 설명 예시: "Python/FastAPI 기반의 AI 스마트 할일 관리 웹 앱. 자연어 입력으로 할일을 추가하면 AI가 자동으로 분류하고 우선순위를 지정합니다."</Tip>
        <ScreenshotPlaceholder label="프로젝트 생성 화면" />

        <h2>Step 4: 첫 워크플로우 실행</h2>
        <ol>
          <li>프로젝트 → <strong>실행</strong> 메뉴 → <strong>새 실행</strong> 클릭</li>
          <li><strong>워크플로우 실행</strong> 탭에서 "Create Project Brief" 선택 (첫 시작 추천)</li>
          <li>페르소나(Analyst Mary)가 자동으로 인사하고 Step 1을 안내합니다</li>
          <li>페르소나의 질문에 답하며 진행하거나, <strong>[R] Propose</strong>를 눌러 AI가 대신 작성하게 합니다</li>
          <li><strong>[C] Continue</strong>로 다음 단계로 넘어갑니다</li>
        </ol>
        <ScreenshotPlaceholder label="워크플로우 실행 화면" />
      </article>
    );

    case "dashboard": return (
      <article className="prose prose-sm max-w-none">
        <h1>대시보드</h1>
        <p>로그인 후 첫 화면입니다. 시간대별 인사와 함께 내가 참여한 프로젝트와 최근 활동을 한눈에 확인합니다.</p>
        <ScreenshotPlaceholder label="대시보드 전체 화면" />

        <h2>구성 요소</h2>
        <h3>히어로 영역</h3>
        <p>시간대별 인사(좋은 아침/오후/저녁) + 사용자 이름 + 서비스 소개 문구</p>

        <h3>참여 중인 프로젝트</h3>
        <ul>
          <li>내가 멤버로 참여한 프로젝트 카드 목록</li>
          <li>각 카드: 프로젝트명, 설명, 오너 이름, 멤버 수, 마지막 수정일, 단계(Phase) 뱃지</li>
          <li>프로젝트가 6개 미만이면 빈 placeholder 영역 표시</li>
          <li>카드 클릭 시 프로젝트 개요 페이지로 이동</li>
        </ul>

        <h3>최근 활동</h3>
        <p>참여 프로젝트들의 활동 내역 (최대 10개):</p>
        <ul>
          <li>📄 아티팩트 생성/수정 — 누가, 어떤 파일을, 언제</li>
          <li>💬 실행 세션 참여 — 누가, 어떤 세션에서</li>
          <li>👤 멤버 추가</li>
          <li>➕ 프로젝트 생성</li>
          <li>✏️ 프로젝트 정보 수정, 🔄 단계 변경, 🗑️ 프로젝트 삭제</li>
        </ul>
        <p>각 항목 클릭 시 해당 위치로 이동합니다. 시간은 한국 시간 기준입니다.</p>
      </article>
    );

    case "project-overview": return (
      <article className="prose prose-sm max-w-none">
        <h1>프로젝트 개요</h1>
        <p>프로젝트에 들어가면 첫 화면으로 표시됩니다. 프로젝트의 전체 현황을 파악합니다.</p>
        <ScreenshotPlaceholder label="프로젝트 개요 화면" />

        <h2>프로젝트 헤더</h2>
        <p>프로젝트명, 설명, 생성일, 마지막 수정일, 현재 단계(Phase) 뱃지</p>

        <h2>요약 카드 (3개)</h2>
        <table>
          <thead><tr><th>카드</th><th>표시 내용</th><th>클릭 시</th></tr></thead>
          <tbody>
            <tr><td>실행 세션</td><td>총 세션 수</td><td>실행 메뉴로 이동</td></tr>
            <tr><td>아티팩트</td><td>총 파일 수</td><td>아티팩트 메뉴로 이동</td></tr>
            <tr><td>멤버</td><td>총 멤버 수</td><td>멤버 관리로 이동</td></tr>
          </tbody>
        </table>

        <h2>아티팩트 진행 체크리스트</h2>
        <p>7개 BMad 핵심 아티팩트의 완성 여부를 시각적으로 표시합니다:</p>
        <ul>
          <li>✅ 완성된 아티팩트 — primary 체크 표시, 클릭 시 아티팩트 페이지로 이동</li>
          <li>⬜ 미작성 아티팩트 — 빈 원</li>
          <li>상단에 진행률 바 표시 (예: 3/7)</li>
        </ul>

        <h2>최근 실행 세션</h2>
        <p>최근 3개 세션이 표시됩니다. 페르소나 아이콘, 세션 제목, 메시지 수, 마지막 활동 시간, 워크플로우 뱃지를 포함합니다.</p>

        <h2>팀 멤버</h2>
        <p>참여 멤버의 이니셜 아바타 + 이름 + 역할(Owner/Member)이 pill 형태로 나열됩니다.</p>

        <h2>다음 단계 추천</h2>
        <p>미작성된 첫 아티팩트에 해당하는 워크플로우를 자동으로 추천합니다. 모든 아티팩트가 완성되면 "모든 핵심 아티팩트가 완성되었습니다" 메시지가 표시됩니다.</p>
      </article>
    );

    case "workflow": return (
      <article className="prose prose-sm max-w-none">
        <h1>워크플로우 실행</h1>
        <p>프로젝트 → <strong>실행</strong> 메뉴에서 워크플로우를 선택하거나 페르소나와 자유 대화를 시작합니다.</p>
        <ScreenshotPlaceholder label="워크플로우/페르소나 선택 화면" />

        <h2>새 실행 시작</h2>
        <p><strong>새 실행</strong> 버튼을 클릭하면 2개 탭이 표시됩니다:</p>

        <h3>워크플로우 실행 탭 (기본)</h3>
        <p>BMad 단계(분석→기획→설계→구현)별로 그룹핑된 워크플로우 카드가 표시됩니다.</p>
        <table>
          <thead><tr><th>단계</th><th>워크플로우</th><th>산출물</th><th>단계 수</th></tr></thead>
          <tbody>
            <tr><td>분석</td><td>Create Project Brief</td><td>product-brief.md</td><td>5</td></tr>
            <tr><td rowSpan={3}>기획</td><td>Create PRD</td><td>PRD.md</td><td>12</td></tr>
            <tr><td>Validate PRD</td><td>—</td><td>13</td></tr>
            <tr><td>Create UX Design</td><td>ux-spec.md</td><td>14</td></tr>
            <tr><td>설계</td><td>Create Architecture</td><td>architecture.md</td><td>8</td></tr>
            <tr><td rowSpan={3}>구현</td><td>Create Epics & Stories</td><td>epics.md</td><td>4</td></tr>
            <tr><td>Sprint Planning</td><td>sprint-status.md</td><td>5</td></tr>
            <tr><td>Create Story</td><td>story.md</td><td>6</td></tr>
          </tbody>
        </table>
        <p>카드를 클릭하면 추천 페르소나가 자동 배정되어 세션이 시작됩니다.</p>

        <h3>페르소나 실행 탭</h3>
        <p>워크플로우 없이 특정 페르소나와 자유롭게 대화합니다. 질문, 리뷰, 브레인스토밍에 활용하세요.</p>

        <h2>워크플로우 진행 화면</h2>
        <ScreenshotPlaceholder label="워크플로우 진행 중 화면 (상단 진행바 + 채팅)" />
        <h3>상단 워크플로우 패널</h3>
        <ul>
          <li>워크플로우 이름 + 현재 단계/전체 단계 뱃지 (예: Step 3/12)</li>
          <li>진행률 바 — 완료 단계는 primary, 현재 단계는 펄스 애니메이션, 미진행은 회색</li>
          <li>현재 단계 이름과 설명</li>
          <li>A/P/R/C 메뉴 버튼 (마지막 단계에서는 숨김)</li>
        </ul>

        <h3>채팅 영역</h3>
        <ul>
          <li>현재 페르소나 표시 + <strong>페르소나 전환</strong> 버튼</li>
          <li>메시지: 페르소나 아바타, 이름, 작성 시간 표시</li>
          <li>페르소나의 <strong>Bold 텍스트</strong>를 클릭하면 입력창에 자동 입력됩니다 (A/P/R/C 텍스트 제외)</li>
          <li>메시지에 마우스 오버 시: 복사 버튼, 아티팩트로 저장 버튼</li>
          <li>하단: 입력창 (Shift+Enter로 줄바꿈, 최대 5줄 자동 확장) + 전송/중지 버튼</li>
        </ul>

        <h3>문서 패널 (우측)</h3>
        <p><strong>Show Documents</strong> 버튼 또는 아티팩트 자동 생성 시 우측에 문서 패널이 열립니다.</p>
        <ul>
          <li>프로젝트의 모든 아티팩트 파일을 탭으로 전환</li>
          <li>Markdown 프리뷰 + 편집 모드 전환</li>
          <li>문서 패널에서 파일을 수정하면 채팅에 "파일이 수정되었습니다" 알림 표시 → 다음 대화에 반영</li>
        </ul>

        <h2>권장 실행 순서</h2>
        <p>이전 아티팩트를 컨텍스트로 참조하므로 다음 순서를 권장합니다:</p>
        <ol>
          <li>Product Brief (프로젝트 개요 정리)</li>
          <li>PRD (상세 요구사항 작성)</li>
          <li>UX Spec (사용자 경험 설계)</li>
          <li>Architecture (기술 아키텍처 결정)</li>
          <li>Epics & Stories (구현 작업 분해)</li>
          <li>Sprint Planning (스프린트 계획)</li>
          <li>Story (개별 스토리 상세화)</li>
        </ol>
      </article>
    );

    case "persona": return (
      <article className="prose prose-sm max-w-none">
        <h1>AI 페르소나</h1>
        <p>6명의 전문가 AI가 각자의 고유한 성격과 전문성으로 프로젝트에 참여합니다.</p>
        <ScreenshotPlaceholder label="페르소나 선택 화면" />

        <h2>페르소나 상세</h2>

        <h3>🔍 Analyst — Mary</h3>
        <ul>
          <li><strong>역할:</strong> 비즈니스 분석가</li>
          <li><strong>전문:</strong> 시장 조사, 경쟁 분석, 요구사항 도출, 전략 기획</li>
          <li><strong>성격:</strong> 호기심 많고 열정적. 데이터에서 패턴을 발견하면 흥분하는 탐험가 타입</li>
          <li><strong>워크플로우:</strong> Create Project Brief</li>
          <li><strong>주요 능력:</strong> 브레인스토밍(BP), 시장 조사(MR), 도메인 리서치(DR), 기술 리서치(TR)</li>
        </ul>

        <h3>📋 PM — John</h3>
        <ul>
          <li><strong>역할:</strong> 프로덕트 매니저 (8년 경력)</li>
          <li><strong>전문:</strong> PRD 작성, 요구사항 관리, 로드맵, 이해관계자 관리</li>
          <li><strong>성격:</strong> 직설적이고 데이터 중심. 불필요한 것을 외과적으로 제거. "왜?"를 끈질기게 묻는 타입</li>
          <li><strong>워크플로우:</strong> Create PRD, Validate PRD</li>
          <li><strong>주요 능력:</strong> PRD 작성(CP), PRD 검증(VP), PRD 편집(EP)</li>
        </ul>

        <h3>🏗️ Architect — Winston</h3>
        <ul>
          <li><strong>역할:</strong> 시스템 아키텍트</li>
          <li><strong>전문:</strong> 분산 시스템, 클라우드, API 설계, 확장 가능한 패턴</li>
          <li><strong>성격:</strong> 차분하고 실용적. 트레이드오프를 중시하며, 유행 기술 대신 검증된 기술을 선호</li>
          <li><strong>워크플로우:</strong> Create Architecture</li>
          <li><strong>주요 능력:</strong> 아키텍처 설계(CA), 구현 준비 검증(IR)</li>
        </ul>

        <h3>🎨 UX Designer — Sally</h3>
        <ul>
          <li><strong>역할:</strong> UX 디자이너 (7년 경력)</li>
          <li><strong>전문:</strong> 사용자 리서치, 정보 구조, 와이어프레임, 인터랙션 패턴</li>
          <li><strong>성격:</strong> 공감적이고 사용자 중심. 인터페이스를 말로 생생하게 묘사하는 스토리텔러</li>
          <li><strong>워크플로우:</strong> Create UX Design</li>
        </ul>

        <h3>📊 Scrum Master — Bob</h3>
        <ul>
          <li><strong>역할:</strong> 스크럼 마스터 (기술 배경 보유)</li>
          <li><strong>전문:</strong> 에픽/스토리 분해, 스프린트 계획, BDD 인수 기준</li>
          <li><strong>성격:</strong> 체계적이고 체크리스트 중심. 모호함에 대한 불관용. 개발자가 질문 없이 구현할 수 있을 만큼 상세하게 작성</li>
          <li><strong>워크플로우:</strong> Create Epics, Sprint Planning, Create Story</li>
        </ul>

        <h3>📝 Tech Writer — Paige</h3>
        <ul>
          <li><strong>역할:</strong> 기술 문서가</li>
          <li><strong>전문:</strong> CommonMark, DITA, OpenAPI, 기술 문서 작성</li>
          <li><strong>성격:</strong> 인내심 있고 교육적. 친구에게 설명하듯 복잡한 개념을 쉽게 풀어냄</li>
          <li><strong>워크플로우:</strong> (모든 단계에서 활용 가능)</li>
        </ul>

        <h2>대화 중 페르소나 전환</h2>
        <p>채팅 상단의 <strong>페르소나 전환</strong>을 클릭하면 6명의 페르소나 목록이 표시됩니다. 원하는 페르소나를 선택하면 즉시 전환되며, 대화 맥락은 유지됩니다.</p>
        <Tip>PRD를 작성하다가 기술적 판단이 필요하면 Architect로 전환하여 의견을 구한 뒤 다시 PM으로 돌아올 수 있습니다.</Tip>
      </article>
    );

    case "aprc": return (
      <article className="prose prose-sm max-w-none">
        <h1>A/P/R/C 메뉴</h1>
        <p>워크플로우의 각 단계에서 4가지 액션을 선택할 수 있습니다. 워크플로우 패널의 버튼 또는 채팅 메시지의 퀵 액션 버튼으로 실행합니다.</p>
        <ScreenshotPlaceholder label="A/P/R/C 메뉴 버튼 영역" />

        <h2>[A] Advanced Elicitation — 심층 분석</h2>
        <p>현재 단계의 내용을 4가지 관점에서 깊이 검토합니다:</p>
        <table>
          <thead><tr><th>기법</th><th>방법</th><th>효과</th></tr></thead>
          <tbody>
            <tr><td>소크라틱 질문</td><td>모든 가정에 "왜?"로 도전</td><td>숨겨진 전제 발견</td></tr>
            <tr><td>퍼스트 프린시플</td><td>근본 원리로 분해</td><td>불필요한 복잡성 제거</td></tr>
            <tr><td>프리모텀 분석</td><td>실패를 상상하고 역추적</td><td>리스크 사전 발견</td></tr>
            <tr><td>레드팀 리뷰</td><td>적대적 관점에서 비판</td><td>약점 식별</td></tr>
          </tbody>
        </table>
        <Tip>중요한 의사결정(기술 스택 선택, 핵심 기능 범위 등) 전에 사용하면 효과적입니다.</Tip>

        <h2>[P] Party Mode — 멀티 페르소나 토론</h2>
        <p>관련 분야 페르소나 2명이 참여하여 <strong>3단계 토론</strong>을 진행합니다:</p>
        <ol>
          <li><strong>Round 1 — 초기 관점:</strong> 각 게스트 페르소나가 현재 토론에 대한 전문가 관점 제시</li>
          <li><strong>Round 2 — 상호 토론:</strong> 서로의 Round 1 의견에 동의/반박/보완</li>
          <li><strong>합의 정리:</strong> 리드 페르소나가 합의 사항, 논쟁 포인트, 액션 아이템을 종합</li>
        </ol>
        <p><strong>참여 페르소나 매핑 예시:</strong></p>
        <ul>
          <li>Create PRD → Architect + UX Designer 참여</li>
          <li>Create Architecture → PM + Scrum Master 참여</li>
          <li>Create UX Design → PM + Analyst 참여</li>
        </ul>
        <Tip>다양한 관점이 필요한 단계(요구사항 정의, 아키텍처 결정 등)에서 활용하면 편향을 방지할 수 있습니다.</Tip>
        <ScreenshotPlaceholder label="Party Mode 실행 중 (멀티 페르소나 토론)" />

        <h2>[R] Propose Mode — AI 자동 초안</h2>
        <p>페르소나가 질문 대신 <strong>현재 단계의 내용을 직접 작성하여 제안</strong>합니다.</p>
        <h3>동작 방식</h3>
        <ol>
          <li>프로젝트명, 설명, 기존 아티팩트를 분석</li>
          <li>현재 단계에 필요한 내용을 AI가 추론하여 완성된 초안 작성</li>
          <li>"이 제안을 검토해주세요"와 함께 결과 제시</li>
          <li>사용자는 "좋습니다" 또는 수정 요청만 하면 됩니다</li>
        </ol>
        <Tip>모든 질문에 일일이 답하기 부담스러울 때 사용하세요. 사용자의 입력 부담을 최소화합니다.</Tip>

        <h2>[C] Continue — 다음 단계</h2>
        <p>현재 단계를 완료하고 다음 단계로 이동합니다.</p>
        <ul>
          <li>페르소나가 자동으로 다음 단계를 안내합니다</li>
          <li>마지막 단계에서 Continue를 누르면 BMad 템플릿에 맞춰 아티팩트가 자동 생성됩니다</li>
          <li>마지막 단계에서는 A/P/R/C 메뉴가 숨겨집니다</li>
        </ul>

        <h2>퀵 액션 버튼</h2>
        <p>페르소나의 응답에서 A/P/R/C가 감지되면 메시지 하단에 클릭 가능한 버튼이 자동 표시됩니다. 직접 타이핑하지 않아도 됩니다.</p>
      </article>
    );

    case "artifact": return (
      <article className="prose prose-sm max-w-none">
        <h1>아티팩트 관리</h1>
        <p>프로젝트 → <strong>아티팩트</strong> 메뉴에서 산출물 파일을 관리합니다.</p>
        <ScreenshotPlaceholder label="아티팩트 관리 화면 (파일 트리 + 뷰어)" />

        <h2>화면 구성</h2>
        <table>
          <thead><tr><th>영역</th><th>기능</th></tr></thead>
          <tbody>
            <tr><td>좌측 파일 트리</td><td>폴더/파일 목록, 정렬(이름/수정일/크기), 버전·수정자 표시</td></tr>
            <tr><td>우측 뷰어</td><td>Markdown 프리뷰/편집, 버전 히스토리, Diff 비교</td></tr>
            <tr><td>하단 도구</td><td>새 파일, 업로드, 전체 다운로드</td></tr>
          </tbody>
        </table>

        <h2>파일 생성</h2>
        <h3>직접 생성</h3>
        <ol>
          <li>하단 <strong>새 파일</strong> 클릭</li>
          <li><strong>템플릿</strong> 선택 (BMad 아티팩트 템플릿 또는 빈 파일)</li>
          <li>파일명, 경로 입력</li>
          <li>Markdown 에디터에서 내용 작성 → 저장</li>
        </ol>

        <h3>채팅에서 자동 저장</h3>
        <p>페르소나에게 "이 내용을 PRD로 저장해줘"라고 요청하면 BMad 템플릿에 맞춰 정리 후 자동 저장됩니다.</p>

        <h3>샘플 아티팩트 로드</h3>
        <p>아티팩트가 없을 때 3종의 샘플 프로젝트를 선택하여 로드할 수 있습니다:</p>
        <ul>
          <li>TaskFlow — Python/FastAPI/PostgreSQL/AWS</li>
          <li>SmartWork — Java/Spring/PostgreSQL/Azure (그룹웨어)</li>
          <li>TradeHub — Java/Spring/PostgreSQL/Azure (B2B 이커머스)</li>
        </ul>

        <h2>파일 편집</h2>
        <ol>
          <li>파일 트리에서 파일 클릭 → Markdown 프리뷰 표시</li>
          <li><strong>편집</strong> 버튼 → Markdown 에디터 모드</li>
          <li>수정 후 <strong>저장</strong> → 자동으로 새 버전 생성</li>
        </ol>

        <h2>버전 관리</h2>
        <ul>
          <li>버전 라벨: YYMMDD_HHMMSS (한국 시간 기준)</li>
          <li><strong>버전</strong> 버튼 → 우측에 버전 히스토리 패널 표시</li>
          <li>과거 버전 클릭 → 현재 버전과 <strong>Diff 비교</strong> (추가: 초록, 삭제: 빨강)</li>
          <li><strong>복구</strong> 버튼 → 해당 버전으로 복원 (현재 시각 기준 새 버전 생성)</li>
        </ul>
        <ScreenshotPlaceholder label="버전 Diff 비교 화면" />

        <h2>파일 관리 기능</h2>
        <table>
          <thead><tr><th>기능</th><th>방법</th></tr></thead>
          <tbody>
            <tr><td>이름 변경</td><td>파일/폴더 호버 → 연필 아이콘 → 인라인 편집</td></tr>
            <tr><td>파일 이동</td><td>드래그 앤 드롭으로 다른 폴더에 놓기</td></tr>
            <tr><td>삭제</td><td>호버 → 휴지통 아이콘 → 한 번 더 클릭으로 확인</td></tr>
            <tr><td>폴더 삭제</td><td>폴더 호버 → 휴지통 → 폴더 내 모든 파일 일괄 삭제</td></tr>
            <tr><td>다운로드</td><td>개별: 뷰어 헤더의 다운로드 아이콘 / 전체: 하단 "전체 다운로드"</td></tr>
            <tr><td>정렬</td><td>파일 트리 상단 정렬 버튼 (이름순 → 수정일순 → 크기순)</td></tr>
          </tbody>
        </table>

        <h2>파일 목록 접기</h2>
        <p>뷰어 영역을 넓게 사용하려면 파일 목록 패널을 접을 수 있습니다. 접힌 상태에서도 파일명이 축약되어 표시되며, 클릭하면 해당 파일로 이동합니다.</p>
      </article>
    );

    case "collaboration": return (
      <article className="prose prose-sm max-w-none">
        <h1>다중 사용자 협업</h1>
        <p>Dev.AI Spec Studio는 팀 단위 실시간 협업을 지원합니다.</p>

        <h2>프로젝트 멤버 관리</h2>
        <ul>
          <li>프로젝트 → <strong>멤버</strong> 메뉴에서 이메일로 팀원 초대</li>
          <li>역할: <strong>Owner</strong> (프로젝트 설정 수정 권한) / <strong>Member</strong> (실행, 아티팩트 편집 권한)</li>
          <li>프로젝트 설정(이름, 설명, 단계, 삭제)은 Owner만 가능</li>
        </ul>

        <h2>실시간 채팅 협업</h2>
        <ul>
          <li>같은 실행 세션에 여러 사용자가 동시 접속 가능</li>
          <li>한 사용자가 메시지를 보내면 다른 사용자에게 실시간 표시</li>
          <li>페르소나 응답 중 중지 버튼은 해당 메시지를 보낸 사용자에게만 표시</li>
          <li>다른 사용자가 페르소나 응답을 트리거한 경우, 나의 채팅 입력은 비활성화되지 않습니다</li>
        </ul>

        <h2>아티팩트 협업</h2>
        <ul>
          <li>모든 멤버가 아티팩트 파일을 생성, 편집, 삭제할 수 있습니다</li>
          <li>파일 수정 시 수정자 이름과 버전이 자동 기록됩니다</li>
          <li>채팅 내 문서 패널에서 수정하면 채팅에 "파일이 수정되었습니다" 알림이 표시됩니다</li>
        </ul>

        <h2>프로젝트 탐색</h2>
        <p>좌측 메뉴 → <strong>프로젝트</strong>에서 전체 프로젝트를 볼 수 있습니다:</p>
        <ul>
          <li><strong>전체 프로젝트</strong> — 모든 사용자의 프로젝트 (미참여 프로젝트는 점선 테두리, "미참여" 뱃지)</li>
          <li><strong>참여 중</strong> — 내가 멤버인 프로젝트만</li>
          <li><strong>내가 만든</strong> — 내가 오너인 프로젝트만</li>
        </ul>
        <p>미참여 프로젝트 클릭 시 "프로젝트 오너에게 초대를 요청해주세요" 메시지가 표시됩니다.</p>
      </article>
    );

    case "admin-settings": return (
      <article className="prose prose-sm max-w-none">
        <h1>설정 및 프로필</h1>

        <h2>LLM API 설정</h2>
        <p>좌측 메뉴 → <strong>설정</strong>에서 LLM 프로바이더를 관리합니다.</p>
        <ul>
          <li>여러 프로바이더/모델을 등록할 수 있습니다</li>
          <li>하나를 <strong>기본값</strong>으로 설정해야 페르소나가 동작합니다</li>
          <li>API Key는 암호화되어 저장됩니다</li>
        </ul>
        <ScreenshotPlaceholder label="LLM 설정 화면" />

        <h2>프로필 관리</h2>
        <p>우측 상단 아바타 → <strong>프로필</strong>에서:</p>
        <ul>
          <li><strong>이름 변경</strong> — 표시 이름을 수정합니다</li>
          <li><strong>비밀번호 변경</strong> — 새 비밀번호(8자 이상) + 확인 입력</li>
          <li>이메일은 변경할 수 없습니다</li>
        </ul>

        <h2>프로젝트 설정 (Owner 전용)</h2>
        <p>프로젝트 → <strong>설정</strong>에서:</p>
        <ul>
          <li>프로젝트 이름, 설명 수정</li>
          <li>개발 단계(Phase) 변경: 분석 → 기획 → 설계 → 구현</li>
          <li>프로젝트 삭제 (위험 구역)</li>
        </ul>
        <Tip>프로젝트 설정은 Owner만 수정 가능합니다. 멤버가 시도하면 "프로젝트 오너만 수정 가능합니다" 메시지가 표시됩니다.</Tip>

        <h2>언어 전환</h2>
        <p>상단 헤더의 <strong>KO/EN</strong> 스위치로 한국어/영어를 전환합니다. 전환 시 즉시 반영됩니다.</p>
      </article>
    );

    case "bmad": return (
      <article className="prose prose-sm max-w-none">
        <h1>BMad Method 철학</h1>

        <h2>AI-Driven Development (AIDD)란?</h2>
        <p>
          AI-Driven Development는 소프트웨어 개발의 전 과정에서 AI를 <strong>핵심 협업 파트너</strong>로 활용하는 방법론입니다.
          단순히 코드 생성에 AI를 사용하는 것이 아니라, <strong>기획 → 설계 → 구현 준비</strong>의 모든 단계에서
          AI 전문가 에이전트가 인간과 함께 사고하고, 검토하고, 제안합니다.
        </p>
        <p>
          기존의 AI 활용이 "코드를 생성해줘"에 머물렀다면,
          AIDD는 "무엇을 만들어야 하는지, 왜 만들어야 하는지, 어떻게 만들어야 하는지"부터 AI와 함께 정의합니다.
        </p>

        <h2>BMad Method V6의 5가지 핵심 원칙</h2>

        <h3>1. 페르소나 기반 전문성</h3>
        <p>
          하나의 범용 AI 대신, 각 전문 분야별 <strong>독립된 페르소나</strong>를 사용합니다.
          PM은 PM처럼, Architect는 Architect처럼 사고합니다.
          각 페르소나는 고유한 성격, 커뮤니케이션 스타일, 전문 지식, 판단 기준을 가지고 있습니다.
        </p>
        <blockquote>
          범용 AI에게 "PRD를 작성해줘"라고 하면 평범한 문서가 나옵니다.
          PM John에게 같은 요청을 하면, "왜 이 기능이 필요한가?"부터 묻고,
          데이터 기반으로 우선순위를 매기며, 불필요한 기능을 적극적으로 제거합니다.
        </blockquote>

        <h3>2. 단계별 워크플로우</h3>
        <p>
          복잡한 산출물을 한 번에 만들지 않습니다.
          워크플로우의 각 단계에서 <strong>하나의 관점에 집중</strong>하여 점진적으로 완성해갑니다.
        </p>
        <p>예: PRD는 12단계를 거쳐 완성됩니다:</p>
        <ol>
          <li>입력 문서 탐색 → 2. 프로젝트 분류 → 3. 비전 발견 → 4. 요약 작성 → 5. 성공 기준 → 6. 사용자 저니 → 7. 도메인 요구사항 → 8. 혁신 패턴 → 9. 범위 & 로드맵 → 10. 기능 요구사항 → 11. 비기능 요구사항 → 12. 최종 검토</li>
        </ol>

        <h3>3. 컨텍스트 체인</h3>
        <p>
          각 아티팩트는 이전 단계의 산출물을 <strong>자동으로 참조</strong>합니다.
        </p>
        <table>
          <thead><tr><th>워크플로우</th><th>참조하는 아티팩트</th></tr></thead>
          <tbody>
            <tr><td>Create PRD</td><td>Product Brief</td></tr>
            <tr><td>Create Architecture</td><td>PRD, Product Brief, UX Spec</td></tr>
            <tr><td>Create UX Design</td><td>PRD, Product Brief</td></tr>
            <tr><td>Create Epics</td><td>PRD, Architecture, UX Spec</td></tr>
            <tr><td>Create Story</td><td>Epics, Sprint Status, PRD, Architecture, UX Spec</td></tr>
          </tbody>
        </table>
        <p>이를 통해 산출물 간 일관성이 자연스럽게 유지됩니다.</p>

        <h3>4. 인간 중심 의사결정</h3>
        <p>
          AI는 제안하고 초안을 작성하지만, <strong>최종 의사결정은 인간</strong>이 합니다.
          A/P/R/C 메뉴를 통해 사용자가 깊이와 진행 속도를 조절합니다.
        </p>
        <ul>
          <li>꼼꼼하게 진행하고 싶으면 → 각 단계에서 질문에 답하며 진행</li>
          <li>빠르게 진행하고 싶으면 → <strong>[R] Propose Mode</strong>로 AI가 대신 작성하게 하고 검토만</li>
          <li>다양한 관점이 필요하면 → <strong>[P] Party Mode</strong>로 멀티 페르소나 토론</li>
          <li>깊이 있는 검토가 필요하면 → <strong>[A] Advanced</strong>로 소크라틱 질문, 프리모텀 분석</li>
        </ul>

        <h3>5. 다자 협업 토론 (Party Mode)</h3>
        <p>
          단일 AI의 관점에는 편향이 있을 수 있습니다.
          Party Mode에서 여러 페르소나가 서로의 의견에 반응하며 토론합니다.
        </p>
        <blockquote>
          PM이 "이 기능은 MVP에 필수"라고 하면,
          Architect가 "기술적으로 3주 추가 소요"라고 반박하고,
          UX Designer가 "사용자 테스트 결과 이 기능 없이도 핵심 가치 전달 가능"이라고 보완합니다.
          리드 페르소나가 최종 합의를 정리합니다.
        </blockquote>

        <h2>산출물 체계</h2>
        <table>
          <thead><tr><th>산출물</th><th>목적</th><th>주요 내용</th></tr></thead>
          <tbody>
            <tr><td><strong>Product Brief</strong></td><td>프로젝트 개요</td><td>문제 정의, 솔루션, 대상 사용자, 성공 기준, MVP 범위, 비전</td></tr>
            <tr><td><strong>PRD</strong></td><td>제품 요구사항</td><td>FR 20-50개 (ID+우선순위+인수기준), NFR, 사용자 저니, 로드맵, 리스크</td></tr>
            <tr><td><strong>UX Spec</strong></td><td>사용자 경험</td><td>페르소나, 정보 구조, 사용자 흐름, 와이어프레임, 접근성</td></tr>
            <tr><td><strong>Architecture</strong></td><td>기술 아키텍처</td><td>ADR (결정 기록), 기술 스택, 시스템 구조, 데이터 모델, API 설계</td></tr>
            <tr><td><strong>Epics & Stories</strong></td><td>구현 계획</td><td>에픽 분해, BDD 인수 기준(Gherkin), 스토리 포인트, FR 커버리지 맵</td></tr>
            <tr><td><strong>Project Context</strong></td><td>구현 규칙</td><td>기술 스택 버전, 코딩 컨벤션, 프로젝트 구조, 핵심 구현 규칙</td></tr>
            <tr><td><strong>Sprint Status</strong></td><td>스프린트 추적</td><td>에픽/스토리 상태(YAML), 스프린트 목표, 블로커</td></tr>
          </tbody>
        </table>

        <h2>왜 BMad Method인가?</h2>
        <ul>
          <li><strong>전문가 없는 팀도</strong> 높은 품질의 기획 문서를 만들 수 있습니다</li>
          <li>AI가 <strong>놓치기 쉬운 부분</strong>(보안, 접근성, 엣지 케이스)을 체크합니다</li>
          <li><strong>일관된 템플릿</strong>으로 표준화된 산출물을 생성합니다</li>
          <li>Propose Mode로 <strong>사용자 부담을 최소화</strong>합니다</li>
          <li>Party Mode로 <strong>다양한 관점</strong>을 반영합니다</li>
          <li>산출물 간 <strong>자동 컨텍스트 참조</strong>로 일관성을 유지합니다</li>
        </ul>

        <h2>참고 자료</h2>
        <ul>
          <li><a href="https://github.com/bmadcode/bmad-method" target="_blank" rel="noopener noreferrer">BMad Method V6 GitHub Repository</a></li>
          <li><a href="https://www.youtube.com/@BMadCode" target="_blank" rel="noopener noreferrer">BMad Code YouTube Channel</a></li>
        </ul>
      </article>
    );

    default: return <p>Content not found.</p>;
  }
}
