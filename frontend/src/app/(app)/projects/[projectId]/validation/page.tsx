"use client";

import { useCallback, useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { ChevronDown, ChevronRight } from "lucide-react";
import api from "@/lib/api";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { useI18n } from "@/lib/i18n";
import { SpecHealthScore } from "@/components/validation/SpecHealthScore";
import { IssueList } from "@/components/validation/IssueList";
import { RulesInfo } from "@/components/validation/RulesInfo";

interface ValidationRun {
  id: number;
  health_score: number;
  issues_open: number;
  issues_resolved: number;
  rules_executed: number;
  duration_ms: number;
  total_anchors: number | null;
  created_at: string;
  triggered_by: string;
}

interface IssueCounts {
  open: number;
  acknowledged: number;
  resolved: number;
  suppressed: number;
}

export default function ValidationPage() {
  const params = useParams();
  const projectId = Number(params.projectId);
  const { t } = useI18n();

  const [run, setRun] = useState<ValidationRun | null>(null);
  const [counts, setCounts] = useState<IssueCounts | null>(null);
  const [running, setRunning] = useState(false);
  const [includeLlm, setIncludeLlm] = useState(true);
  const [showFormula, setShowFormula] = useState(false);

  const loadRun = useCallback(async () => {
    try {
      const [runRes, countsRes] = await Promise.all([
        api.get(`/projects/${projectId}/validation/runs/latest`),
        api.get(`/projects/${projectId}/validation/issues/counts`),
      ]);
      setRun(runRes.data);
      setCounts(countsRes.data);
    } catch {
      // no-op
    }
  }, [projectId]);

  useEffect(() => {
    loadRun();
  }, [loadRun]);

  const onRun = async () => {
    setRunning(true);
    try {
      const res = await api.post(`/projects/${projectId}/validation`, null, {
        params: { scope: "all", include_llm: includeLlm },
      });
      setRun(res.data);
      toast.success(
        t("valid.runOk", { open: String(res.data.issues_open), resolved: String(res.data.issues_resolved) })
      );
    } catch {
      toast.error(t("valid.runFail"));
    } finally {
      setRunning(false);
    }
  };

  return (
    <div className="flex h-full flex-col">
      <div className="flex flex-wrap items-center justify-between gap-3 border-b px-4 py-2">
        {/* Engine result — compact: score + inline meta */}
        <div className="flex items-center gap-3">
          {run ? (
            <>
              <SpecHealthScore score={run.health_score} issuesOpen={run.issues_open} size="sm" />
              <div className="flex flex-col gap-0.5 text-[11px] text-muted-foreground leading-tight">
                <div className="flex items-center gap-2">
                  <span>{t("valid.runMeta", { rules: String(run.rules_executed), ms: String(run.duration_ms) })}</span>
                  <RulesInfo projectId={projectId} />
                </div>
                <div className="flex items-center gap-2 flex-wrap">
                  {run.total_anchors !== null && run.total_anchors !== undefined && (
                    <Link
                      href={`/projects/${projectId}/traceability`}
                      className="text-sky-700 hover:underline inline-flex items-center gap-0.5"
                    >
                      {t("valid.anchorsTotal", { total: String(run.total_anchors) })}
                      <span aria-hidden="true">↗</span>
                    </Link>
                  )}
                  <button
                    type="button"
                    onClick={() => setShowFormula((v) => !v)}
                    className="inline-flex items-center gap-0.5 hover:text-slate-700"
                    aria-expanded={showFormula}
                  >
                    {showFormula ? <ChevronDown className="h-3 w-3" /> : <ChevronRight className="h-3 w-3" />}
                    {t("valid.scoreFormulaToggle")}
                  </button>
                </div>
              </div>
            </>
          ) : (
            <div className="text-sm text-muted-foreground">{t("valid.noRunYet")}</div>
          )}
        </div>

        {/* User label chips — inline, no separate block */}
        {counts && (
          <div
            className="flex items-center gap-2 text-[11px]"
            title={t("valid.labelHint")}
          >
            <span className="font-semibold text-slate-600">{t("valid.labelSection")}</span>
            <span className="rounded bg-amber-100 px-1.5 py-0.5 text-amber-800">
              {t("valid.labelAck", { count: String(counts.acknowledged) })}
            </span>
            <span className="rounded bg-emerald-100 px-1.5 py-0.5 text-emerald-800">
              {t("valid.labelResolved", { count: String(counts.resolved) })}
            </span>
            <span className="rounded bg-slate-200 px-1.5 py-0.5 text-slate-700">
              {t("valid.labelSuppressed", { count: String(counts.suppressed) })}
            </span>
          </div>
        )}

        <div className="flex items-center gap-2">
          <label className="flex items-center gap-1 text-[11px] text-muted-foreground">
            <input
              type="checkbox"
              checked={includeLlm}
              onChange={(e) => setIncludeLlm(e.target.checked)}
            />
            {t("valid.includeLlm")}
          </label>
          <Button size="sm" variant="outline" onClick={onRun} disabled={running}>
            {running ? t("valid.running") : t("valid.runValidation")}
          </Button>
        </div>
      </div>

      {/* Collapsible formula explanation */}
      {showFormula && run && (
        <div className="border-b bg-slate-50 px-4 py-2 text-[11px] text-muted-foreground">
          <p className="italic">{t("valid.scoreNote")}</p>
          <p className="mt-1">
            {t("valid.triggered", { by: run.triggered_by, when: new Date(run.created_at).toLocaleString() })}
          </p>
        </div>
      )}

      <div className="flex-1 overflow-auto p-4">
        <IssueList projectId={projectId} onChanged={loadRun} />
      </div>
    </div>
  );
}
