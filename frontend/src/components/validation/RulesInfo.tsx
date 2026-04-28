"use client";

import { useEffect, useState } from "react";
import { ChevronDown, Info } from "lucide-react";
import api from "@/lib/api";
import { useI18n, type TranslationKey } from "@/lib/i18n";
import { cn } from "@/lib/utils";

interface RuleInfo {
  id: string;
  severity: "error" | "warning" | "info";
  description: string;
  is_llm: boolean;
  tags: string[];
  enabled: boolean;
}

const SEVERITY_BADGE: Record<RuleInfo["severity"], string> = {
  error: "bg-rose-100 text-rose-700 border-rose-300",
  warning: "bg-amber-100 text-amber-700 border-amber-300",
  info: "bg-sky-100 text-sky-700 border-sky-300",
};

interface RulesInfoProps {
  projectId: number;
}

export function RulesInfo({ projectId }: RulesInfoProps) {
  const { t } = useI18n();
  const [rules, setRules] = useState<RuleInfo[]>([]);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    if (!open || rules.length) return;
    api
      .get<RuleInfo[]>(`/projects/${projectId}/validation/rules`)
      .then((res) => setRules(res.data))
      .catch(() => {
        // silent — non-critical
      });
  }, [open, projectId, rules.length]);

  return (
    <div className="relative">
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        className="inline-flex items-center gap-1 text-[11px] text-sky-700 hover:underline"
      >
        <Info className="h-3 w-3" />
        {t("valid.rulesInfo")}
        <ChevronDown
          className={cn(
            "h-3 w-3 transition-transform",
            open && "rotate-180"
          )}
        />
      </button>
      {open && (
        <div className="absolute left-0 top-full z-30 mt-1 w-[28rem] rounded-md border bg-background p-3 text-xs shadow-lg">
          <p className="font-semibold mb-2">{t("valid.rulesListTitle")}</p>
          {rules.length === 0 ? (
            <p className="text-muted-foreground italic">{t("valid.loading")}</p>
          ) : (
            <ul className="space-y-2">
              {rules.map((r) => {
                const nameKey = `valid.rule.${r.id}.name` as TranslationKey;
                const descKey = `valid.rule.${r.id}.desc` as TranslationKey;
                const name = t(nameKey);
                const desc = t(descKey);
                return (
                  <li
                    key={r.id}
                    className="flex gap-2 border-b border-dashed pb-2 last:border-b-0 last:pb-0"
                  >
                    <span
                      className={cn(
                        "shrink-0 h-fit text-[10px] font-mono px-1.5 py-0.5 rounded border",
                        SEVERITY_BADGE[r.severity]
                      )}
                    >
                      {t(`valid.severity${r.severity.charAt(0).toUpperCase()}${r.severity.slice(1)}` as TranslationKey)}
                    </span>
                    <div className="flex-1 min-w-0">
                      <p className="font-medium">
                        {name === nameKey ? r.id : name}
                        {r.is_llm && (
                          <span className="ml-1 text-[10px] rounded bg-violet-100 text-violet-700 px-1">
                            LLM
                          </span>
                        )}
                      </p>
                      <p className="text-[11px] text-muted-foreground mt-0.5">
                        {desc === descKey ? r.description : desc}
                      </p>
                      <p className="text-[10px] text-muted-foreground/70 mt-0.5 font-mono">
                        {r.id}
                      </p>
                    </div>
                  </li>
                );
              })}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}
