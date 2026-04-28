"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Check, CheckCircle2, EyeOff, ExternalLink, GitBranch } from "lucide-react";
import api from "@/lib/api";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { useI18n, type TranslationKey } from "@/lib/i18n";
import { useProjectStore } from "@/stores/projectStore";
import { IssueDrawer } from "./IssueDrawer";
import { translateRuleMessage, translateRuleSuggestion } from "./ruleI18n";

export interface Issue {
  id: number;
  rule_id: string;
  severity: "error" | "warning" | "info";
  file_id: number | null;
  anchor: string | null;
  related_file_id: number | null;
  related_anchor: string | null;
  message: string;
  suggestion: string | null;
  status: "open" | "acknowledged" | "resolved" | "suppressed";
  confidence: number;
  created_at: string;
}

const SEVERITY_BADGE: Record<Issue["severity"], string> = {
  error: "bg-rose-100 text-rose-700 border-rose-300",
  warning: "bg-amber-100 text-amber-700 border-amber-300",
  info: "bg-sky-100 text-sky-700 border-sky-300",
};

const SEVERITY_LABEL: Record<Issue["severity"], TranslationKey> = {
  error: "valid.severityError",
  warning: "valid.severityWarning",
  info: "valid.severityInfo",
};

type StatusFilter = "open" | "acknowledged" | "resolved" | "suppressed" | "all";

const STATUS_OPTIONS: { value: StatusFilter; key: TranslationKey }[] = [
  { value: "open", key: "valid.statusOpen" },
  { value: "acknowledged", key: "valid.statusAcknowledged" },
  { value: "resolved", key: "valid.statusResolved" },
  { value: "suppressed", key: "valid.statusSuppressed" },
  { value: "all", key: "valid.statusAll" },
];

const STATUS_BADGE: Record<Issue["status"], string> = {
  open: "bg-rose-100 text-rose-700",
  acknowledged: "bg-amber-100 text-amber-700",
  resolved: "bg-emerald-100 text-emerald-700",
  suppressed: "bg-slate-100 text-slate-600",
};

interface IssueListProps {
  projectId: number;
  fileId?: number | null;
  onChanged?: () => void;
}

export function IssueList({ projectId, fileId, onChanged }: IssueListProps) {
  const { t } = useI18n();
  const { files, fetchFiles } = useProjectStore();
  const [issues, setIssues] = useState<Issue[]>([]);
  const [loading, setLoading] = useState(false);
  const [filterSeverity, setFilterSeverity] = useState<Issue["severity"] | "">("");
  const [filterStatus, setFilterStatus] = useState<StatusFilter>("open");
  const [drawerIssueId, setDrawerIssueId] = useState<number | null>(null);

  useEffect(() => {
    if (!files.length) fetchFiles(projectId);
  }, [files.length, fetchFiles, projectId]);

  const fileNameOf = (id: number | null): string | null => {
    if (!id) return null;
    const f = files.find((x) => x.id === id);
    return f?.file_name ?? null;
  };

  const load = async () => {
    setLoading(true);
    try {
      const res = await api.get<Issue[]>(`/projects/${projectId}/validation/issues`, {
        params: {
          status: filterStatus,
          severity: filterSeverity || undefined,
          file_id: fileId ?? undefined,
        },
      });
      setIssues(res.data);
    } catch {
      toast.error(t("valid.loadFailed"));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [projectId, fileId, filterSeverity, filterStatus]);

  const updateStatus = async (id: number, status: Issue["status"]) => {
    try {
      await api.patch(`/projects/${projectId}/validation/issues/${id}`, { status });
      const successKey: TranslationKey =
        status === "acknowledged"
          ? "valid.acked"
          : status === "resolved"
          ? "valid.resolved"
          : status === "suppressed"
          ? "valid.suppressed"
          : "valid.reopened";
      toast.success(t(successKey));
      load();
      onChanged?.();
    } catch {
      toast.error(t("valid.updateFailed"));
    }
  };

  const drawerIssue = issues.find((x) => x.id === drawerIssueId) ?? null;
  const drawerIndex = drawerIssue ? issues.indexOf(drawerIssue) : -1;
  const goPrev = () => {
    if (drawerIndex > 0) setDrawerIssueId(issues[drawerIndex - 1].id);
  };
  const goNext = () => {
    if (drawerIndex >= 0 && drawerIndex < issues.length - 1)
      setDrawerIssueId(issues[drawerIndex + 1].id);
  };

  return (
    <div className="flex flex-col gap-2 text-xs">
      {/* Severity filter */}
      <div className="flex items-center gap-1 flex-wrap">
        <span className="text-[10px] text-muted-foreground">{t("valid.filter")}</span>
        {(["", "error", "warning", "info"] as const).map((s) => (
          <button
            key={s || "all"}
            onClick={() => setFilterSeverity(s)}
            className={cn(
              "text-[10px] px-1.5 py-0.5 rounded border",
              filterSeverity === s ? "bg-foreground text-background" : "hover:bg-muted"
            )}
          >
            {s === "" ? t("valid.severityAll") : t(SEVERITY_LABEL[s])}
          </button>
        ))}
      </div>

      {/* Status filter */}
      <div className="flex items-center gap-1 flex-wrap">
        <span className="text-[10px] text-muted-foreground">{t("valid.statusFilter")}</span>
        {STATUS_OPTIONS.map((opt) => (
          <button
            key={opt.value}
            onClick={() => setFilterStatus(opt.value)}
            className={cn(
              "text-[10px] px-1.5 py-0.5 rounded border",
              filterStatus === opt.value ? "bg-foreground text-background" : "hover:bg-muted"
            )}
          >
            {t(opt.key)}
          </button>
        ))}
        <span className="text-[10px] text-muted-foreground ml-auto">
          {t("valid.resultCount", { count: String(issues.length) })}
        </span>
        <Button size="sm" variant="ghost" className="h-6 text-[10px] px-1" onClick={load} disabled={loading}>
          ↻
        </Button>
      </div>

      {loading ? (
        <p className="text-muted-foreground">{t("valid.loading")}</p>
      ) : issues.length === 0 ? (
        <p className="text-muted-foreground italic">{t("valid.noIssues")}</p>
      ) : (
        <ul className="space-y-1.5">
          {issues.map((i) => {
            const isOpen = i.status === "open";
            return (
              <li
                key={i.id}
                onClick={(e) => {
                  // Avoid stealing clicks from links/buttons inside the card.
                  const target = e.target as HTMLElement;
                  if (target.closest("a, button")) return;
                  setDrawerIssueId(i.id);
                }}
                className={cn(
                  "border rounded p-2 cursor-pointer hover:bg-accent/40 transition-colors",
                  !isOpen && "bg-muted/30 opacity-80",
                  drawerIssueId === i.id && "ring-1 ring-primary/40 bg-accent/30"
                )}
              >
                <div className="flex items-start gap-2">
                  <span
                    className={cn(
                      "text-[10px] font-mono px-1.5 py-0.5 rounded border",
                      SEVERITY_BADGE[i.severity]
                    )}
                  >
                    {t(SEVERITY_LABEL[i.severity])}
                  </span>
                  {!isOpen && (
                    <span
                      className={cn(
                        "text-[10px] font-mono px-1.5 py-0.5 rounded",
                        STATUS_BADGE[i.status]
                      )}
                    >
                      {t(`valid.status${i.status.charAt(0).toUpperCase()}${i.status.slice(1)}` as TranslationKey)}
                    </span>
                  )}
                  <div className="flex-1 min-w-0">
                    <p className="text-xs">{translateRuleMessage(t, i)}</p>
                    <p className="text-[10px] text-muted-foreground mt-0.5 flex flex-wrap items-center gap-x-1">
                      <span>{i.rule_id}</span>
                      {i.anchor && (
                        <>
                          <span>·</span>
                          {i.file_id ? (
                            <Link
                              href={`/projects/${projectId}/files?fileId=${i.file_id}`}
                              className="text-sky-700 hover:underline inline-flex items-center gap-0.5"
                              title={fileNameOf(i.file_id) ?? ""}
                            >
                              {fileNameOf(i.file_id) ?? t("valid.openFile")} #{i.anchor}
                              <ExternalLink className="h-2.5 w-2.5" />
                            </Link>
                          ) : (
                            <span>{i.anchor}</span>
                          )}
                        </>
                      )}
                      {i.related_anchor && (
                        <>
                          <span>↔</span>
                          {i.related_file_id ? (
                            <Link
                              href={`/projects/${projectId}/files?fileId=${i.related_file_id}`}
                              className="text-sky-700 hover:underline inline-flex items-center gap-0.5"
                              title={fileNameOf(i.related_file_id) ?? ""}
                            >
                              {fileNameOf(i.related_file_id) ?? t("valid.openFile")} #{i.related_anchor}
                              <ExternalLink className="h-2.5 w-2.5" />
                            </Link>
                          ) : (
                            <span>{i.related_anchor}</span>
                          )}
                        </>
                      )}
                    </p>
                    {i.suggestion && (
                      <p className="text-[10px] text-muted-foreground italic mt-1">💡 {translateRuleSuggestion(t, i)}</p>
                    )}
                  </div>
                  <div className="flex flex-col items-stretch gap-1 ml-2 shrink-0">
                    {i.file_id && (
                      <Link
                        href={`/projects/${projectId}/files?fileId=${i.file_id}`}
                        className="inline-flex items-center gap-1 text-[10px] px-2 py-1 rounded border bg-sky-50 text-sky-800 hover:bg-sky-100"
                      >
                        <ExternalLink className="h-3 w-3" />
                        {t("valid.openInArtifacts")}
                      </Link>
                    )}
                    {i.anchor && (
                      <Link
                        href={`/projects/${projectId}/traceability?focus=${encodeURIComponent(i.anchor)}`}
                        className="inline-flex items-center gap-1 text-[10px] px-2 py-1 rounded border bg-violet-50 text-violet-800 hover:bg-violet-100"
                      >
                        <GitBranch className="h-3 w-3" />
                        {t("valid.openInTrace")}
                      </Link>
                    )}
                  </div>
                </div>
                <div className="flex gap-1.5 mt-2">
                  {isOpen ? (
                    <>
                      <button
                        type="button"
                        onClick={() => updateStatus(i.id, "acknowledged")}
                        className="inline-flex items-center gap-1 text-[10.5px] px-2 py-1 rounded border border-amber-300 bg-amber-50 text-amber-800 hover:bg-amber-100 hover:border-amber-400 active:scale-95 transition shadow-sm"
                      >
                        <Check className="h-3 w-3" />
                        {t("valid.ack")}
                      </button>
                      <button
                        type="button"
                        onClick={() => updateStatus(i.id, "resolved")}
                        className="inline-flex items-center gap-1 text-[10.5px] px-2 py-1 rounded border border-emerald-300 bg-emerald-50 text-emerald-800 hover:bg-emerald-100 hover:border-emerald-400 active:scale-95 transition shadow-sm"
                      >
                        <CheckCircle2 className="h-3 w-3" />
                        {t("valid.resolve")}
                      </button>
                      <button
                        type="button"
                        onClick={() => updateStatus(i.id, "suppressed")}
                        className="inline-flex items-center gap-1 text-[10.5px] px-2 py-1 rounded border border-slate-300 bg-slate-50 text-slate-700 hover:bg-slate-100 hover:border-slate-400 active:scale-95 transition shadow-sm"
                      >
                        <EyeOff className="h-3 w-3" />
                        {t("valid.suppress")}
                      </button>
                    </>
                  ) : (
                    <button
                      type="button"
                      onClick={() => updateStatus(i.id, "open")}
                      className="inline-flex items-center gap-1 text-[10.5px] px-2 py-1 rounded border border-slate-300 bg-white hover:bg-slate-50 active:scale-95 transition shadow-sm"
                    >
                      {t("valid.reopen")}
                    </button>
                  )}
                </div>
              </li>
            );
          })}
        </ul>
      )}
      <IssueDrawer
        projectId={projectId}
        issue={drawerIssue}
        fileName={drawerIssue ? fileNameOf(drawerIssue.file_id) : null}
        open={drawerIssueId !== null}
        onOpenChange={(o) => !o && setDrawerIssueId(null)}
        onUpdateStatus={updateStatus}
        onPrev={goPrev}
        onNext={goNext}
      />
    </div>
  );
}
