"use client";

import { useEffect } from "react";
import { useParams } from "next/navigation";
import { useProjectStore } from "@/stores/projectStore";
import { ProjectSidebar } from "@/components/layout/ProjectSidebar";

export default function ProjectLayout({ children }: { children: React.ReactNode }) {
  const params = useParams();
  const projectId = params.projectId as string;
  const { currentProject, fetchProject } = useProjectStore();

  useEffect(() => {
    fetchProject(Number(projectId));
  }, [projectId, fetchProject]);

  return (
    <div className="flex h-full">
      <ProjectSidebar
        projectId={projectId}
        projectName={currentProject?.name}
      />
      <div className="flex-1 overflow-auto">{children}</div>
    </div>
  );
}
