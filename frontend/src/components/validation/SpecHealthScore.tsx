"use client";

import { cn } from "@/lib/utils";
import { useI18n } from "@/lib/i18n";

interface SpecHealthScoreProps {
  score: number;
  issuesOpen: number;
  size?: "sm" | "md" | "lg";
}

function colorFor(score: number): string {
  if (score >= 90) return "text-emerald-600 border-emerald-300";
  if (score >= 70) return "text-amber-600 border-amber-300";
  if (score >= 50) return "text-orange-600 border-orange-300";
  return "text-rose-600 border-rose-300";
}

export function SpecHealthScore({ score, issuesOpen, size = "md" }: SpecHealthScoreProps) {
  const { t } = useI18n();
  const sizeClass =
    size === "sm"
      ? "h-14 w-14"
      : size === "lg"
      ? "h-28 w-28"
      : "h-20 w-20";
  const numClass =
    size === "sm" ? "text-base" : size === "lg" ? "text-3xl" : "text-xl";
  const denomClass =
    size === "sm" ? "text-[9px]" : size === "lg" ? "text-xs" : "text-[10px]";
  return (
    <div className="flex items-center gap-2">
      <div
        className={cn(
          "rounded-full border-2 flex flex-col items-center justify-center font-bold leading-none",
          sizeClass,
          colorFor(score)
        )}
        title={t("valid.specHealth")}
      >
        <span className={numClass}>{Math.round(score)}</span>
        <span className={cn("opacity-60 mt-0.5", denomClass)}>/ 100</span>
      </div>
      <div className="text-xs text-muted-foreground leading-tight">
        <p className="font-semibold">{t("valid.specHealth")}</p>
        <p>{t("valid.openIssues", { count: String(issuesOpen) })}</p>
      </div>
    </div>
  );
}
