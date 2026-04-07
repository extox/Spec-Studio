"use client";

import { useEffect, useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { PhaseIndicator } from "@/components/project/PhaseIndicator";
import { toast } from "sonner";
import api from "@/lib/api";
import { useI18n } from "@/lib/i18n";

interface ProjectItem {
  id: number;
  name: string;
  description: string | null;
  phase: string;
  created_by: number;
  created_at: string;
  updated_at: string;
  owner_name: string;
  member_count: number;
  is_member: boolean;
}

interface ProjectListResponse {
  projects: ProjectItem[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}

type SortField = "updated_at" | "created_at" | "name";

export default function ProjectsPage() {
  const router = useRouter();
  const { t } = useI18n();
  const [data, setData] = useState<ProjectListResponse | null>(null);
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");
  const [searchInput, setSearchInput] = useState("");
  const [sort, setSort] = useState<SortField>("updated_at");
  const [order, setOrder] = useState<"asc" | "desc">("desc");
  const [filter, setFilter] = useState<"all" | "member" | "owned">("all");
  const [isLoading, setIsLoading] = useState(true);

  const fetchProjects = useCallback(async () => {
    setIsLoading(true);
    try {
      const res = await api.get<ProjectListResponse>("/projects/all", {
        params: { page, per_page: 12, search, sort, order, filter },
      });
      setData(res.data);
    } catch {
      toast.error(t("projects.loadFailed"));
    } finally {
      setIsLoading(false);
    }
  }, [page, search, sort, order, filter, t]);

  useEffect(() => {
    fetchProjects();
  }, [fetchProjects]);

  const handleSearch = () => {
    setPage(1);
    setSearch(searchInput);
  };

  const handleSort = (field: SortField) => {
    if (sort === field) {
      setOrder(order === "desc" ? "asc" : "desc");
    } else {
      setSort(field);
      setOrder("desc");
    }
    setPage(1);
  };

  const handleProjectClick = (project: ProjectItem) => {
    if (project.is_member) {
      router.push(`/projects/${project.id}`);
    } else {
      toast.error(t("projects.noAccess", { owner: project.owner_name }));
    }
  };

  return (
    <div className="p-8 max-w-[1200px] mx-auto">
      <div className="mb-8 flex items-center justify-between">
        <h2 className="text-2xl font-bold tracking-tight">{t("projects.title")}</h2>
        <Button onClick={() => router.push("/projects/new")} size="sm" className="rounded-lg h-8 px-4 text-[13px]">
          {t("projects.new")}
        </Button>
      </div>

      {/* Filter tabs */}
      <div className="flex gap-0.5 border-b border-border/60 mb-5">
        {(["all", "member", "owned"] as const).map((f) => (
          <button
            key={f}
            onClick={() => { setFilter(f); setPage(1); }}
            className={`px-4 py-2.5 text-[13px] font-medium border-b-2 transition-colors -mb-px ${
              filter === f
                ? "border-primary text-foreground"
                : "border-transparent text-muted-foreground hover:text-foreground"
            }`}
          >
            {t(`projects.filter_${f}`)}
          </button>
        ))}
      </div>

      {/* Search bar */}
      <div className="flex items-center gap-2 mb-4">
        <div className="relative flex-1">
          <svg className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground/40" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input
            type="text"
            value={searchInput}
            onChange={(e) => setSearchInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSearch()}
            placeholder={t("projects.searchPlaceholder")}
            className="w-full rounded-lg border border-border/60 px-3 py-2 pl-9 text-sm bg-transparent focus:outline-none focus:ring-2 focus:ring-ring/30 focus:border-primary/30 transition-all"
          />
          {search && (
            <button
              onClick={() => { setSearchInput(""); setSearch(""); setPage(1); }}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground/50 hover:text-foreground transition-colors"
            >
              <svg className="h-4 w-4" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          )}
        </div>
      </div>

      {/* Sort + results info */}
      <div className="flex items-center justify-between mb-4">
        {data && (
          <p className="text-xs text-muted-foreground/70">
            {t("projects.totalCount", { count: String(data.total) })}
            {search && ` · "${search}" ${t("projects.searchResult")}`}
          </p>
        )}
        <div className="flex items-center rounded-lg border border-border/60 bg-muted/20 text-xs overflow-hidden">
          {(["updated_at", "name", "created_at"] as SortField[]).map((field) => (
            <button
              key={field}
              onClick={() => handleSort(field)}
              className={`px-3 py-1.5 transition-all ${
                sort === field
                  ? "bg-foreground text-background font-medium"
                  : "text-muted-foreground hover:text-foreground"
              }`}
            >
              {t(`projects.sort${field === "updated_at" ? "Date" : field === "name" ? "Name" : "Created"}`)}
              {sort === field && (
                <span className="ml-0.5">{order === "desc" ? "↓" : "↑"}</span>
              )}
            </button>
          ))}
        </div>
      </div>

      {/* Project grid */}
      {isLoading ? (
        <div className="flex items-center gap-3 text-muted-foreground py-16 justify-center">
          <div className="h-5 w-5 rounded-full border-2 border-primary/30 border-t-primary animate-spin" />
          <span className="text-sm">{t("common.loading")}</span>
        </div>
      ) : data && data.projects.length === 0 ? (
        <div className="py-24 text-center text-muted-foreground text-sm">
          {search ? t("projects.noSearchResults") : t("projects.noProjects")}
        </div>
      ) : data && (
        <>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {data.projects.map((project) => (
              <Card
                key={project.id}
                className={`group transition-all duration-300 cursor-pointer hover:shadow-lg hover:shadow-black/[0.04] hover:-translate-y-0.5 ${
                  project.is_member
                    ? "border-border/60 bg-card hover:border-primary/25"
                    : "border-dashed border-border/40 bg-muted/10 opacity-70 hover:opacity-100"
                }`}
                onClick={() => handleProjectClick(project)}
              >
                <CardHeader className="pb-2">
                  <div className="flex items-start justify-between gap-3">
                    <CardTitle className="text-[15px] font-semibold group-hover:text-primary transition-colors duration-200 truncate leading-snug" title={project.name}>
                      {project.name}
                    </CardTitle>
                    <div className="flex items-center gap-1.5 shrink-0">
                      {!project.is_member && (
                        <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-muted text-muted-foreground/70 border border-border/50">
                          {t("projects.notMember")}
                        </span>
                      )}
                      <PhaseIndicator phase={project.phase} />
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground/80 line-clamp-2 mb-5 leading-relaxed">
                    {project.description || t("common.noDescription")}
                  </p>
                  <div className="flex items-center gap-3 text-xs text-muted-foreground/70">
                    {project.owner_name && (
                      <>
                        <span className="flex items-center gap-1.5">
                          <svg className="h-3.5 w-3.5" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                          </svg>
                          <span className="font-medium text-muted-foreground">{project.owner_name}</span>
                        </span>
                        <span className="h-3 w-px bg-border" />
                      </>
                    )}
                    <span className="flex items-center gap-1.5">
                      <svg className="h-3.5 w-3.5" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
                      </svg>
                      {project.member_count}
                    </span>
                    <span className="h-3 w-px bg-border" />
                    <span>
                      {new Date(project.updated_at).toLocaleDateString("ko-KR")}
                    </span>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* Pagination */}
          {data.total_pages > 1 && (
            <div className="flex items-center justify-center gap-3 mt-8">
              <Button
                size="sm"
                variant="outline"
                disabled={page <= 1}
                onClick={() => setPage(page - 1)}
                className="h-8 px-3 text-xs rounded-lg"
              >
                {t("projects.prev")}
              </Button>
              <span className="text-xs text-muted-foreground tabular-nums">
                {page} / {data.total_pages}
              </span>
              <Button
                size="sm"
                variant="outline"
                disabled={page >= data.total_pages}
                onClick={() => setPage(page + 1)}
                className="h-8 px-3 text-xs rounded-lg"
              >
                {t("projects.next")}
              </Button>
            </div>
          )}
        </>
      )}
    </div>
  );
}
