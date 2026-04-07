"use client";

import { useEffect, useMemo } from "react";
import { useParams, useRouter } from "next/navigation";
import { useProjectStore } from "@/stores/projectStore";
import { useChatStore } from "@/stores/chatStore";
import { useContextStore } from "@/stores/contextStore";
import { PhaseIndicator } from "@/components/project/PhaseIndicator";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useI18n } from "@/lib/i18n";

const ARTIFACT_CHECKLIST = [
  { key: "product-brief", label: "Product Brief", file: "product-brief.md", phase: "analysis" },
  { key: "prd", label: "PRD", file: "PRD.md", phase: "planning" },
  { key: "ux-spec", label: "UX Spec", file: "ux-spec.md", phase: "planning" },
  { key: "architecture", label: "Architecture", file: "architecture.md", phase: "solutioning" },
  { key: "epics", label: "Epics & Stories", file: "epics.md", phase: "implementation" },
  { key: "project-context", label: "Project Context", file: "project-context.md", phase: "cross-cutting" },
  { key: "sprint-status", label: "Sprint Status", file: "sprint-status.md", phase: "implementation" },
];

const ARTIFACT_WORKFLOW_MAP: Record<string, { workflow: string; label: string }> = {
  "product-brief": { workflow: "create-brief", label: "Create Project Brief" },
  "prd": { workflow: "create-prd", label: "Create PRD" },
  "ux-spec": { workflow: "create-ux-design", label: "Create UX Design" },
  "architecture": { workflow: "create-architecture", label: "Create Architecture" },
  "epics": { workflow: "create-epics", label: "Create Epics & Stories" },
  "project-context": { workflow: "create-brief", label: "Create Project Context" },
  "sprint-status": { workflow: "sprint-planning", label: "Sprint Planning" },
};

export default function ProjectOverviewPage() {
  const params = useParams();
  const router = useRouter();
  const projectId = Number(params.projectId);
  const { currentProject, files, fetchFiles, members, fetchMembers } = useProjectStore();
  const { sessions, fetchSessions } = useChatStore();
  const { contextFiles, fetchContextFiles: fetchCtx } = useContextStore();
  const { t } = useI18n();

  useEffect(() => {
    fetchFiles(projectId);
    fetchMembers(projectId);
    fetchSessions(projectId);
    fetchCtx(projectId);
  }, [projectId, fetchFiles, fetchMembers, fetchSessions, fetchCtx]);

  // Artifact completion status
  const artifactStatus = useMemo(() => {
    const fileNames = new Set(files.map((f) => f.file_name.toLowerCase()));
    return ARTIFACT_CHECKLIST.map((item) => ({
      ...item,
      completed: fileNames.has(item.file.toLowerCase()),
      fileId: files.find((f) => f.file_name.toLowerCase() === item.file.toLowerCase())?.id,
    }));
  }, [files]);

  const completedCount = artifactStatus.filter((a) => a.completed).length;
  const contextFileCount = contextFiles.length;

  // Next recommended workflow
  const nextRecommendation = useMemo(() => {
    for (const item of artifactStatus) {
      if (!item.completed) {
        const wf = ARTIFACT_WORKFLOW_MAP[item.key];
        if (wf) return { artifact: item, ...wf };
      }
    }
    return null;
  }, [artifactStatus]);

  // Recent sessions (latest 3)
  const recentSessions = useMemo(() => {
    return [...sessions]
      .sort((a, b) => new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime())
      .slice(0, 3);
  }, [sessions]);

  if (!currentProject) return (
    <div className="flex items-center gap-3 text-muted-foreground p-8 justify-center">
      <div className="h-5 w-5 rounded-full border-2 border-primary/30 border-t-primary animate-spin" />
      <span className="text-sm">{t("common.loading")}</span>
    </div>
  );

  return (
    <div className="p-8 space-y-6 max-w-4xl">
      {/* Project header */}
      <div className="flex items-start justify-between gap-4">
        <div>
          <h2 className="text-2xl font-bold tracking-tight">{currentProject.name}</h2>
          <p className="text-muted-foreground/80 mt-1.5 text-sm leading-relaxed">{currentProject.description || t("common.noDescription")}</p>
          <div className="flex items-center gap-3 mt-3 text-xs text-muted-foreground/60">
            <span>
              {t("project.created")}: {new Date(currentProject.created_at).toLocaleString("ko-KR", {
                timeZone: "Asia/Seoul", year: "numeric", month: "short", day: "numeric",
              })}
            </span>
            <span className="h-3 w-px bg-border" />
            <span>
              {t("project.lastModified")}: {new Date(currentProject.updated_at).toLocaleString("ko-KR", {
                timeZone: "Asia/Seoul", month: "short", day: "numeric", hour: "2-digit", minute: "2-digit",
              })}
            </span>
          </div>
        </div>
        <PhaseIndicator phase={currentProject.phase} />
      </div>

      {/* Summary cards */}
      <div className="grid gap-3 md:grid-cols-4">
        {[
          { href: "chat", count: sessions.length, label: t("project.chatSessions"), iconColor: "text-violet-600", bgColor: "bg-violet-50 border-violet-200/50", icon: "M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" },
          { href: "files", count: files.length, label: t("nav.artifacts"), iconColor: "text-green-600", bgColor: "bg-green-50 border-green-200/50", icon: "M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" },
          { href: "context", count: contextFileCount, label: t("nav.context"), iconColor: "text-blue-600", bgColor: "bg-blue-50 border-blue-200/50", icon: "M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4" },
          { href: "members", count: members.length, label: t("project.members"), iconColor: "text-amber-600", bgColor: "bg-amber-50 border-amber-200/50", icon: "M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" },
        ].map((card) => (
          <Card
            key={card.href}
            className="cursor-pointer transition-all duration-200 hover:shadow-md hover:shadow-black/[0.03] border-border/60"
            onClick={() => router.push(`/projects/${projectId}/${card.href}`)}
          >
            <CardContent className="p-4 flex items-center gap-3">
              <div className={`h-10 w-10 rounded-lg ${card.bgColor} border flex items-center justify-center shrink-0`}>
                <svg className={`h-5 w-5 ${card.iconColor}`} fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" d={card.icon} />
                </svg>
              </div>
              <div>
                <p className="text-2xl font-bold tabular-nums">{card.count}</p>
                <p className="text-xs text-muted-foreground/70">{card.label}</p>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* 1. Artifact progress checklist */}
      <Card className="border-border/60">
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between">
            <CardTitle className="text-sm font-semibold">{t("project.artifactProgress")}</CardTitle>
            <span className="text-xs text-muted-foreground/60 tabular-nums">
              {completedCount}/{ARTIFACT_CHECKLIST.length}
            </span>
          </div>
          {/* Progress bar */}
          <div className="flex gap-1 mt-2.5">
            {ARTIFACT_CHECKLIST.map((item) => {
              const status = artifactStatus.find((a) => a.key === item.key);
              return (
                <div
                  key={item.key}
                  className={`h-1 flex-1 rounded-full transition-colors ${status?.completed ? "bg-primary" : "bg-muted"}`}
                  title={item.label}
                />
              );
            })}
          </div>
        </CardHeader>
        <CardContent className="pt-0">
          <div className="grid gap-0.5">
            {artifactStatus.map((item) => (
              <div
                key={item.key}
                className={`flex items-center gap-3 px-3 py-2 rounded-lg transition-colors duration-150 ${
                  item.completed
                    ? "cursor-pointer hover:bg-muted/40"
                    : "opacity-50"
                }`}
                onClick={() => {
                  if (item.completed && item.fileId) {
                    router.push(`/projects/${projectId}/files`);
                  }
                }}
              >
                <div className={`h-[18px] w-[18px] rounded-full flex items-center justify-center shrink-0 ${
                  item.completed ? "bg-primary text-primary-foreground" : "border-[1.5px] border-muted-foreground/25"
                }`}>
                  {item.completed && (
                    <svg className="h-2.5 w-2.5" fill="none" stroke="currentColor" strokeWidth={3} viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                    </svg>
                  )}
                </div>
                <span className={`text-[13px] ${item.completed ? "font-medium text-foreground" : "text-muted-foreground"}`}>
                  {item.label}
                </span>
                <span className="text-[10px] text-muted-foreground/50 ml-auto font-mono">{item.file}</span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* 2. Recent chat sessions */}
      {recentSessions.length > 0 && (
        <Card className="border-border/60">
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <CardTitle className="text-sm font-semibold">{t("project.recentChats")}</CardTitle>
              <Button
                variant="ghost"
                size="sm"
                className="text-xs h-7 text-muted-foreground hover:text-foreground"
                onClick={() => router.push(`/projects/${projectId}/chat`)}
              >
                {t("project.viewAll")} →
              </Button>
            </div>
          </CardHeader>
          <CardContent className="pt-0 space-y-0.5">
            {recentSessions.map((session) => (
              <div
                key={session.id}
                className="flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-muted/40 cursor-pointer transition-colors duration-150"
                onClick={() => router.push(`/projects/${projectId}/chat/${session.id}`)}
              >
                <span className="text-base shrink-0">
                  {session.persona === "analyst" ? "🔍" :
                   session.persona === "pm" ? "📋" :
                   session.persona === "architect" ? "🏗️" :
                   session.persona === "ux-designer" ? "🎨" :
                   session.persona === "scrum-master" ? "📊" :
                   session.persona === "tech-writer" ? "📝" : "💬"}
                </span>
                <div className="flex-1 min-w-0">
                  <p className="text-[13px] font-medium truncate">{session.title || t("chat.untitled")}</p>
                  <p className="text-[11px] text-muted-foreground/60 mt-0.5">
                    {session.message_count || 0} {t("chat.messages")}
                    <span className="mx-1.5 text-border">·</span>
                    {new Date(session.updated_at).toLocaleString("ko-KR", {
                      timeZone: "Asia/Seoul", month: "short", day: "numeric", hour: "2-digit", minute: "2-digit",
                    })}
                  </p>
                </div>
                {session.workflow && (
                  <span className="text-[10px] px-2 py-0.5 rounded-full bg-muted/60 text-muted-foreground/70 border border-border/50 shrink-0">
                    {session.workflow}
                  </span>
                )}
              </div>
            ))}
          </CardContent>
        </Card>
      )}

      {/* 3. Team members */}
      {members.length > 0 && (
        <Card className="border-border/60">
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <CardTitle className="text-sm font-semibold">{t("project.teamMembers")}</CardTitle>
              <Button
                variant="ghost"
                size="sm"
                className="text-xs h-7 text-muted-foreground hover:text-foreground"
                onClick={() => router.push(`/projects/${projectId}/members`)}
              >
                {t("project.manageMembers")} →
              </Button>
            </div>
          </CardHeader>
          <CardContent className="pt-0">
            <div className="flex flex-wrap gap-2">
              {members.map((member) => (
                <div
                  key={member.id}
                  className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-muted/30 border border-border/50 text-sm"
                >
                  <div className="h-6 w-6 rounded-full bg-gradient-to-br from-primary/10 to-primary/5 flex items-center justify-center text-[10px] font-bold text-primary shrink-0">
                    {(member.display_name || member.email || "?").charAt(0).toUpperCase()}
                  </div>
                  <span className="text-[13px] font-medium">{member.display_name || member.email}</span>
                  <span className="text-[10px] text-muted-foreground/60">{member.role}</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* 4. Next recommended action */}
      <Card className="border-primary/15 bg-primary/[0.03]">
        <CardContent className="p-5">
          {nextRecommendation ? (
            <div className="flex items-center justify-between gap-4">
              <div>
                <p className="text-sm font-semibold">{t("project.nextStep")}</p>
                <p className="text-xs text-muted-foreground/70 mt-1">
                  {t("project.nextStepDesc", { artifact: nextRecommendation.artifact.label })}
                </p>
              </div>
              <Button
                size="sm"
                className="rounded-lg shrink-0"
                onClick={() => router.push(`/projects/${projectId}/chat`)}
              >
                {nextRecommendation.label}
              </Button>
            </div>
          ) : (
            <div className="flex items-center justify-between gap-4">
              <div>
                <p className="text-sm font-semibold">{t("project.allComplete")}</p>
                <p className="text-xs text-muted-foreground/70 mt-1">{t("project.allCompleteDesc")}</p>
              </div>
              <Button
                size="sm"
                variant="outline"
                className="rounded-lg shrink-0"
                onClick={() => router.push(`/projects/${projectId}/chat`)}
              >
                {t("project.startChat")}
              </Button>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
