"use client";

import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { Project } from "@/types";
import { PhaseIndicator } from "./PhaseIndicator";

interface ProjectCardProps {
  project: Project;
}

export function ProjectCard({ project }: ProjectCardProps) {
  return (
    <Link href={`/projects/${project.id}`}>
      <Card className="group relative transition-all duration-200 hover:shadow-md cursor-pointer border-border hover:border-primary/20 bg-card">
        <CardHeader className="pb-2">
          <div className="flex items-start justify-between gap-3">
            <CardTitle className="text-sm font-semibold group-hover:text-primary transition-colors duration-150 truncate leading-snug" title={project.name}>{project.name}</CardTitle>
            <PhaseIndicator phase={project.phase} />
          </div>
        </CardHeader>
        <CardContent>
          <p className="text-[13px] text-muted-foreground line-clamp-2 mb-4 leading-relaxed">
            {project.description || "No description"}
          </p>
          <div className="flex items-center gap-2.5 text-xs text-muted-foreground">
            {project.owner_name && (
              <>
                <span className="flex items-center gap-1">
                  <svg className="h-3 w-3" fill="none" stroke="currentColor" strokeWidth={1.75} viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                  <span className="font-medium text-foreground/70">{project.owner_name}</span>
                </span>
                <span className="h-3 w-px bg-border" />
              </>
            )}
            <span className="flex items-center gap-1">
              <svg className="h-3 w-3" fill="none" stroke="currentColor" strokeWidth={1.75} viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
              {project.member_count || 1}
            </span>
            <span className="h-3 w-px bg-border" />
            <span className="text-muted-foreground/70">{new Date(project.updated_at).toLocaleDateString("ko-KR")}</span>
          </div>
        </CardContent>
      </Card>
    </Link>
  );
}
