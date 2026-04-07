"use client";

import { useI18n } from "@/lib/i18n";

const phaseStyles: Record<string, { bg: string; text: string; dot: string }> = {
  analysis: { bg: "bg-blue-50 border-blue-200/80", text: "text-blue-700", dot: "bg-blue-500" },
  planning: { bg: "bg-slate-100 border-slate-300/80", text: "text-slate-700", dot: "bg-slate-500" },
  solutioning: { bg: "bg-teal-50 border-teal-200/80", text: "text-teal-700", dot: "bg-teal-500" },
  implementation: { bg: "bg-amber-50 border-amber-200/80", text: "text-amber-700", dot: "bg-amber-500" },
};

export function PhaseIndicator({ phase }: { phase: string }) {
  const { t } = useI18n();

  const labelMap: Record<string, string> = {
    analysis: t("phase.analysis"),
    planning: t("phase.planning"),
    solutioning: t("phase.solutioning"),
    implementation: t("phase.implementation"),
  };

  const label = labelMap[phase] || phase;
  const style = phaseStyles[phase] || { bg: "bg-muted border-border", text: "text-muted-foreground", dot: "bg-muted-foreground" };

  return (
    <span className={`inline-flex items-center gap-1.5 rounded-md px-2 py-0.5 text-[10px] font-semibold border ${style.bg} ${style.text} uppercase tracking-wide`}>
      <span className={`h-1.5 w-1.5 rounded-full ${style.dot}`} />
      {label}
    </span>
  );
}
