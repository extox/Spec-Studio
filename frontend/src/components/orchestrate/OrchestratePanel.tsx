"use client";

import { useState } from "react";
import api from "@/lib/api";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { useI18n, type TranslationKey } from "@/lib/i18n";

interface SubAgentResult {
  name: string;
  output: string;
  error: string | null;
  duration_seconds: number;
}

interface ScenarioResult {
  scenario: string;
  synthesis: string;
  subagents: SubAgentResult[];
}

interface OrchestratePanelProps {
  projectId: number;
}

const SCENARIOS: { id: string; labelKey: TranslationKey; descKey: TranslationKey }[] = [
  {
    id: "review-prd",
    labelKey: "orch.scenario.review-prd.label",
    descKey: "orch.scenario.review-prd.desc",
  },
];

export function OrchestratePanel({ projectId }: OrchestratePanelProps) {
  const { t } = useI18n();
  const [running, setRunning] = useState<string | null>(null);
  const [result, setResult] = useState<ScenarioResult | null>(null);

  const onRun = async (scenarioId: string) => {
    setRunning(scenarioId);
    setResult(null);
    try {
      const res = await api.post<ScenarioResult>(
        `/projects/${projectId}/orchestrate/${scenarioId}`
      );
      setResult(res.data);
      toast.success(t("orch.runOk", { id: scenarioId }));
    } catch (e: unknown) {
      const msg = (e as { response?: { data?: { detail?: string } } })?.response?.data?.detail || t("orch.runFail");
      toast.error(msg);
    } finally {
      setRunning(null);
    }
  };

  return (
    <div className="flex flex-col gap-4 p-4">
      <div>
        <h2 className="text-base font-semibold">{t("orch.title")}</h2>
        <p className="text-xs text-muted-foreground mt-1">{t("orch.subtitle")}</p>
      </div>

      <div className="grid gap-2">
        {SCENARIOS.map((s) => (
          <div key={s.id} className="border rounded-md p-3 flex items-start justify-between gap-3">
            <div className="flex-1">
              <p className="text-sm font-medium">{t(s.labelKey)}</p>
              <p className="text-[11px] text-muted-foreground mt-0.5">{t(s.descKey)}</p>
            </div>
            <Button
              size="sm"
              variant="outline"
              onClick={() => onRun(s.id)}
              disabled={running !== null}
            >
              {running === s.id ? t("orch.running") : t("orch.run")}
            </Button>
          </div>
        ))}
      </div>

      {result && (
        <div className="border rounded-md p-3 space-y-3">
          <div>
            <p className="text-xs font-semibold uppercase text-muted-foreground">{t("orch.synthesis")}</p>
            <pre className="text-xs whitespace-pre-wrap mt-1">{result.synthesis}</pre>
          </div>
          <details className="text-xs">
            <summary className="cursor-pointer text-muted-foreground hover:text-foreground">
              {t("orch.subagentResults", { count: String(result.subagents.length) })}
            </summary>
            <div className="mt-2 space-y-2">
              {result.subagents.map((s) => (
                <div key={s.name} className="border rounded p-2">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-semibold">{s.name}</span>
                    <span className="text-[10px] text-muted-foreground">{s.duration_seconds}s</span>
                  </div>
                  {s.error ? (
                    <p className="text-[11px] text-destructive italic mt-1">{s.error}</p>
                  ) : (
                    <pre className="text-[11px] whitespace-pre-wrap mt-1">{s.output}</pre>
                  )}
                </div>
              ))}
            </div>
          </details>
        </div>
      )}
    </div>
  );
}
