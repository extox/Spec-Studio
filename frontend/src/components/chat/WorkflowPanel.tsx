"use client";

import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import type { Workflow } from "@/types";
import { useI18n } from "@/lib/i18n";

interface WorkflowPanelProps {
  workflow: Workflow | null;
  currentStep: number;
  onAction: (action: string) => void;
  onAPCAction?: (action: "advanced" | "party" | "propose" | "continue") => void;
  disabled?: boolean;
}

export function WorkflowPanel({
  workflow,
  currentStep,
  onAction,
  onAPCAction,
  disabled = false,
}: WorkflowPanelProps) {
  const { t } = useI18n();

  if (!workflow) return null;

  const totalSteps = workflow.steps.length;
  const currentStepInfo = currentStep > 0 && currentStep <= totalSteps
    ? workflow.steps[currentStep - 1]
    : null;
  const supportsAPC = workflow.supports_apc;

  return (
    <div className="border-b px-4 py-2 bg-muted/30">
      {/* Header: workflow name, step counter */}
      <div className="flex items-center gap-2">
        <span className="text-xs font-medium">{workflow.name}</span>
        <Badge variant="secondary" className="text-[10px] px-1.5 py-0">
          {t("workflow.step")} {currentStep}/{totalSteps}
        </Badge>
      </div>

      {/* Progress bar */}
      <div className="mt-1.5 flex gap-0.5">
        {workflow.steps.map((step) => (
          <div
            key={step.step}
            className={`h-1.5 flex-1 rounded-full transition-colors ${
              step.step < currentStep
                ? "bg-primary"
                : step.step === currentStep
                ? "bg-primary/70 animate-pulse"
                : "bg-muted"
            }`}
            title={`Step ${step.step}: ${step.name}`}
          />
        ))}
      </div>

      {/* Current step info */}
      {currentStepInfo && (
        <div className="mt-1.5">
          <p className="text-xs font-medium text-foreground">
            {currentStepInfo.name}
          </p>
          <p className="text-[11px] text-muted-foreground leading-tight">
            {currentStepInfo.description}
          </p>
        </div>
      )}

      {/* A/P/C Menu */}
      {supportsAPC && onAPCAction && currentStep > 0 && currentStep < totalSteps && (
        <>
          <Separator className="my-1.5" />
          <div className="flex items-center gap-1.5">
            <span className="text-[10px] text-muted-foreground font-medium mr-1">{t("workflow.aprc")}</span>
            <Button
              size="sm"
              variant="outline"
              onClick={() => onAPCAction("advanced")}
              className="h-5 text-[10px] px-2 gap-1"
              disabled={disabled}
              title={t("workflow.advancedTitle")}
            >
              {t("workflow.advanced")}
            </Button>
            <Button
              size="sm"
              variant="outline"
              onClick={() => onAPCAction("party")}
              className="h-5 text-[10px] px-2 gap-1"
              disabled={disabled}
              title={t("workflow.partyTitle")}
            >
              {t("workflow.party")}
            </Button>
            <Button
              size="sm"
              variant="outline"
              onClick={() => onAPCAction("propose")}
              className="h-5 text-[10px] px-2 gap-1 border-emerald-300 text-emerald-700 hover:bg-emerald-50"
              disabled={disabled}
              title={t("workflow.proposeTitle")}
            >
              {t("workflow.propose")}
            </Button>
            <Button
              size="sm"
              variant="default"
              onClick={() => onAPCAction("continue")}
              className="h-5 text-[10px] px-2 gap-1"
              disabled={disabled}
              title={t("workflow.continueTitle")}
            >
              {t("workflow.continue")}
            </Button>
          </div>
        </>
      )}
    </div>
  );
}
