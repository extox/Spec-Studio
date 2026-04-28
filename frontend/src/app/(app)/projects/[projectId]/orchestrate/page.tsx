"use client";

import { useParams } from "next/navigation";
import { OrchestratePanel } from "@/components/orchestrate/OrchestratePanel";

export default function OrchestratePage() {
  const params = useParams();
  const projectId = Number(params.projectId);

  return (
    <div className="h-full overflow-auto">
      <OrchestratePanel projectId={projectId} />
    </div>
  );
}
