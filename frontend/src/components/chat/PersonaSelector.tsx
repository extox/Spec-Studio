"use client";

import { useEffect, useState } from "react";
import { useChatStore } from "@/stores/chatStore";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import type { Persona, Workflow } from "@/types";
import { useI18n } from "@/lib/i18n";
import { cn } from "@/lib/utils";

interface PersonaSelectorProps {
  onSelect: (persona: Persona, workflow?: Workflow) => void;
}

type Tab = "persona" | "workflow" | "context";

const phaseColors: Record<string, string> = {
  analysis: "bg-blue-100 text-blue-700",
  planning: "bg-violet-100 text-violet-700",
  solutioning: "bg-emerald-100 text-emerald-700",
  implementation: "bg-amber-100 text-amber-700",
  "cross-cutting": "bg-slate-100 text-slate-600",
};

export function PersonaSelector({ onSelect }: PersonaSelectorProps) {
  const { personas, workflows, fetchPersonas, fetchWorkflows } = useChatStore();
  const { t } = useI18n();
  const [tab, setTab] = useState<Tab>("workflow");

  useEffect(() => {
    fetchPersonas();
    fetchWorkflows();
  }, [fetchPersonas, fetchWorkflows]);

  return (
    <div className="space-y-4">
      {/* Tab switcher */}
      <div className="flex gap-1 border-b">
        <button
          onClick={() => setTab("workflow")}
          className={cn(
            "px-4 py-2 text-sm font-medium border-b-2 transition-colors -mb-px",
            tab === "workflow"
              ? "border-primary text-primary"
              : "border-transparent text-muted-foreground hover:text-foreground"
          )}
        >
          {t("persona.workflowTab")}
        </button>
        <button
          onClick={() => setTab("persona")}
          className={cn(
            "px-4 py-2 text-sm font-medium border-b-2 transition-colors -mb-px",
            tab === "persona"
              ? "border-primary text-primary"
              : "border-transparent text-muted-foreground hover:text-foreground"
          )}
        >
          {t("persona.freeChat")}
        </button>
      </div>

      {tab === "workflow" ? (
        <WorkflowList
          workflows={workflows}
          personas={personas}
          onSelect={onSelect}
          t={t}
        />
      ) : (
        <PersonaList
          personas={personas}
          onSelect={onSelect}
          t={t}
        />
      )}
    </div>
  );
}

function WorkflowList({
  workflows, personas, onSelect, t,
}: {
  workflows: Workflow[];
  personas: Persona[];
  onSelect: (persona: Persona, workflow: Workflow) => void;
  t: (key: string) => string;
}) {
  // Group workflows by phase
  const phases = ["analysis", "planning", "solutioning", "implementation"];
  const grouped: Record<string, Workflow[]> = {};
  for (const wf of workflows) {
    const persona = personas.find((p) => p.id === wf.persona);
    const phase = persona?.phase || "cross-cutting";
    if (!grouped[phase]) grouped[phase] = [];
    grouped[phase].push(wf);
  }

  const phaseLabels: Record<string, string> = {
    analysis: t("phase.analysis"),
    planning: t("phase.planning"),
    solutioning: t("phase.solutioning"),
    implementation: t("phase.implementation"),
    "cross-cutting": "Cross-cutting",
  };

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-bold tracking-tight">{t("persona.selectWorkflow")}</h3>
        <p className="text-sm text-muted-foreground">{t("persona.selectWorkflowDesc")}</p>
      </div>
      {phases.map((phase) => {
        const phaseWorkflows = grouped[phase];
        if (!phaseWorkflows || phaseWorkflows.length === 0) return null;
        return (
          <div key={phase}>
            <div className="flex items-center gap-2 mb-3">
              <Badge className={`text-[10px] px-2 py-0.5 border-0 ${phaseColors[phase] || "bg-muted"}`}>
                {phaseLabels[phase]}
              </Badge>
            </div>
            <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
              {phaseWorkflows.map((wf) => {
                const persona = personas.find((p) => p.id === wf.persona);
                if (!persona) return null;
                return (
                  <Card
                    key={wf.id}
                    className="group cursor-pointer transition-all duration-200 hover:shadow-lg hover:shadow-primary/5 hover:-translate-y-0.5 border-transparent hover:border-primary/20"
                    onClick={() => onSelect(persona, wf)}
                  >
                    <CardContent className="p-4">
                      <div className="flex items-center gap-2 mb-2">
                        <span className="text-lg">{persona.avatar}</span>
                        <div>
                          <p className="font-semibold text-sm group-hover:text-primary transition-colors">{wf.name}</p>
                          <p className="text-[10px] text-muted-foreground">{persona.name}</p>
                        </div>
                      </div>
                      <p className="text-xs text-muted-foreground leading-relaxed mb-2">{wf.description}</p>
                      <div className="flex items-center justify-between text-[10px] text-muted-foreground">
                        {wf.steps && (
                          <span>{wf.steps.length} {t("persona.steps")}</span>
                        )}
                        {wf.template && (
                          <span className="text-primary">→ {wf.template}.md</span>
                        )}
                      </div>
                    </CardContent>
                  </Card>
                );
              })}
            </div>
          </div>
        );
      })}
    </div>
  );
}

function PersonaList({
  personas, onSelect, t,
}: {
  personas: Persona[];
  onSelect: (persona: Persona) => void;
  t: (key: string) => string;
}) {
  return (
    <div className="space-y-4">
      <div>
        <h3 className="text-lg font-bold tracking-tight">{t("persona.selectTitle")}</h3>
        <p className="text-sm text-muted-foreground">{t("persona.freeChatDesc")}</p>
      </div>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {personas.map((persona) => (
          <Card
            key={persona.id}
            className="group cursor-pointer transition-all duration-200 hover:shadow-lg hover:shadow-primary/5 hover:-translate-y-0.5 border-transparent hover:border-primary/20"
            onClick={() => onSelect(persona)}
          >
            <CardContent className="p-5">
              <div className="flex items-start gap-3 mb-3">
                <div className="h-10 w-10 rounded-xl bg-accent flex items-center justify-center text-xl shrink-0">
                  {persona.avatar}
                </div>
                <div className="min-w-0">
                  <p className="font-semibold text-sm group-hover:text-primary transition-colors">{persona.name}</p>
                  <Badge className={`text-[10px] px-1.5 py-0 mt-0.5 border-0 ${phaseColors[persona.phase] || "bg-muted"}`}>
                    {persona.phase}
                  </Badge>
                </div>
              </div>
              <p className="text-xs text-muted-foreground mb-3 leading-relaxed">{persona.description}</p>
              {persona.capabilities && persona.capabilities.length > 0 && (
                <div className="flex flex-wrap gap-1">
                  {persona.capabilities.map((cap) => (
                    <span
                      key={cap.code}
                      className="inline-flex items-center rounded-md bg-secondary px-1.5 py-0.5 text-[10px] font-medium text-secondary-foreground"
                      title={cap.description}
                    >
                      {cap.code}
                    </span>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
