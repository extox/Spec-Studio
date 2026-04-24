"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { useProjectStore } from "@/stores/projectStore";
import { useAuthStore } from "@/stores/authStore";
import { ProjectCard } from "@/components/project/ProjectCard";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { useI18n } from "@/lib/i18n";
import api from "@/lib/api";
import type { Project } from "@/types";

interface Activity {
  type: string;
  project_id: number;
  project_name: string;
  user_name: string;
  detail: string;
  detail_path: string;
  timestamp: string;
}

export default function DashboardPage() {
  const router = useRouter();
  const { projects, fetchProjects, isLoading } = useProjectStore();
  const { user } = useAuthStore();
  const { t } = useI18n();

  const [activities, setActivities] = useState<Activity[]>([]);

  useEffect(() => {
    fetchProjects();
    api.get<Activity[]>("/activity/recent?limit=10").then((res) => setActivities(res.data)).catch(() => {});
  }, [fetchProjects]);

  const stats = useMemo(() => {
    const total = projects.length;
    const phaseCount: Record<string, number> = {};
    let recentProject: typeof projects[0] | null = null;

    for (const p of projects) {
      phaseCount[p.phase] = (phaseCount[p.phase] || 0) + 1;
      if (!recentProject || new Date(p.updated_at) > new Date(recentProject.updated_at)) {
        recentProject = p;
      }
    }

    return { total, phaseCount, recentProject };
  }, [projects]);

  const greeting = useMemo(() => {
    const hour = new Date().getHours();
    if (hour < 6) return t("dashboard.goodNight");
    if (hour < 12) return t("dashboard.goodMorning");
    if (hour < 18) return t("dashboard.goodAfternoon");
    return t("dashboard.goodEvening");
  }, [t]);

  return (
    <div className="p-6 lg:p-8 max-w-[1100px] mx-auto">
      {/* Header section */}
      <div className="mb-8 pb-6 border-b border-border">
        <div className="flex items-center gap-2 mb-1">
          <span className="text-[11px] font-medium text-muted-foreground uppercase tracking-widest">{greeting}</span>
        </div>
        <h2 className="text-2xl font-bold tracking-tight text-foreground">
          {user?.display_name || ""}
        </h2>
        <p className="text-muted-foreground text-sm mt-1">
          {t("dashboard.subtitle")}
        </p>
      </div>

      {isLoading ? (
        <div className="flex items-center gap-3 text-muted-foreground py-12 justify-center">
          <div className="h-4 w-4 rounded-full border-2 border-primary/30 border-t-primary animate-spin" />
          <span className="text-sm">{t("dashboard.loadingProjects")}</span>
        </div>
      ) : projects.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-20 text-center rounded-lg border border-dashed border-border bg-muted/30">
          <div className="h-12 w-12 rounded-lg bg-muted flex items-center justify-center mb-4">
            <svg className="h-5 w-5 text-muted-foreground" fill="none" stroke="currentColor" strokeWidth={1.75} viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
          </div>
          <p className="text-base font-semibold mb-1">{t("dashboard.noProjects")}</p>
          <p className="text-sm text-muted-foreground mb-6 max-w-sm">{t("dashboard.startFirst")}</p>
          <Button onClick={() => router.push("/projects/new")} size="default" className="px-5">
            {t("dashboard.createProject")}
          </Button>
        </div>
      ) : (
        <>
          {/* Projects */}
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-[11px] font-semibold text-muted-foreground uppercase tracking-widest">
              {t("dashboard.allProjects")} <span className="text-muted-foreground/50 ml-0.5">({stats.total})</span>
            </h3>
            <Button onClick={() => router.push("/projects/new")} size="sm" variant="outline" className="h-7 px-3 text-[12px]">
              <svg className="h-3 w-3 mr-1" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              {t("dashboard.newProject")}
            </Button>
          </div>
          <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-3 mb-8">
            {projects.map((project) => (
              <ProjectCard key={project.id} project={project} />
            ))}
          </div>

          {/* Activity feed */}
          {activities.length > 0 && (
            <div>
              <h3 className="text-[11px] font-semibold text-muted-foreground uppercase tracking-widest mb-3">
                {t("dashboard.recentActivity")}
              </h3>
              <Card className="border-border overflow-hidden">
                <CardContent className="p-0 divide-y divide-border">
                  {activities.slice(0, 10).map((act, i) => (
                    <ActivityRow key={i} activity={act} router={router} t={t} />
                  ))}
                </CardContent>
              </Card>
            </div>
          )}
        </>
      )}
    </div>
  );
}

const ACTIVITY_CONFIG: Record<string, { icon: string; labelKey: string; color: string }> = {
  artifact_created: {
    icon: "M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z",
    labelKey: "dashboard.actArtifactCreated",
    color: "text-emerald-600 bg-emerald-50",
  },
  artifact_updated: {
    icon: "M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z",
    labelKey: "dashboard.actArtifactUpdated",
    color: "text-blue-600 bg-blue-50",
  },
  chat_activity: {
    icon: "M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z",
    labelKey: "dashboard.actChatActivity",
    color: "text-slate-600 bg-slate-100",
  },
  member_added: {
    icon: "M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z",
    labelKey: "dashboard.actMemberAdded",
    color: "text-amber-600 bg-amber-50",
  },
  project_created: {
    icon: "M12 6v6m0 0v6m0-6h6m-6 0H6",
    labelKey: "dashboard.actProjectCreated",
    color: "text-primary bg-primary/5",
  },
  project_updated: {
    icon: "M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z",
    labelKey: "dashboard.actProjectUpdated",
    color: "text-blue-600 bg-blue-50",
  },
  project_deleted: {
    icon: "M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16",
    labelKey: "dashboard.actProjectDeleted",
    color: "text-red-600 bg-red-50",
  },
  phase_changed: {
    icon: "M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15",
    labelKey: "dashboard.actPhaseChanged",
    color: "text-teal-600 bg-teal-50",
  },
};

function ActivityRow({
  activity,
  router,
  t,
}: {
  activity: Activity;
  router: ReturnType<typeof useRouter>;
  t: (key: string) => string;
}) {
  const config = ACTIVITY_CONFIG[activity.type] || ACTIVITY_CONFIG.chat_activity;

  const handleClick = () => {
    if (activity.detail_path) {
      router.push(activity.detail_path);
    } else {
      router.push(`/projects/${activity.project_id}`);
    }
  };

  return (
    <div
      className="flex items-center gap-3 px-4 py-3 hover:bg-muted/50 cursor-pointer transition-colors duration-100"
      onClick={handleClick}
    >
      <div className={`h-7 w-7 rounded-md flex items-center justify-center shrink-0 ${config.color}`}>
        <svg className="h-3.5 w-3.5" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" d={config.icon} />
        </svg>
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-[13px] leading-snug">
          <span className="font-medium text-foreground">{activity.user_name || t("chat.assistant")}</span>
          <span className="text-muted-foreground">{" "}{t(config.labelKey)}{" "}</span>
          <span className="font-medium text-foreground">{activity.detail}</span>
        </p>
        <p className="text-[11px] text-muted-foreground/70 mt-0.5">
          {activity.project_name}
          <span className="mx-1 text-border">·</span>
          {new Date(activity.timestamp).toLocaleString("ko-KR", {
            timeZone: "Asia/Seoul",
            month: "short", day: "numeric",
            hour: "2-digit", minute: "2-digit",
          })}
        </p>
      </div>
    </div>
  );
}
