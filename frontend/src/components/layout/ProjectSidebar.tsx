"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { useI18n } from "@/lib/i18n";

interface ProjectSidebarProps {
  projectId: string;
  projectName?: string;
}

const iconMap: Record<string, React.ReactNode> = {
  Overview: (
    <svg className="h-4 w-4 shrink-0" fill="none" stroke="currentColor" strokeWidth={1.75} viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-4 0a1 1 0 01-1-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 01-1 1h-2z" />
    </svg>
  ),
  Chat: (
    <svg className="h-4 w-4 shrink-0" fill="none" stroke="currentColor" strokeWidth={1.75} viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
    </svg>
  ),
  Files: (
    <svg className="h-4 w-4 shrink-0" fill="none" stroke="currentColor" strokeWidth={1.75} viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
    </svg>
  ),
  Context: (
    <svg className="h-4 w-4 shrink-0" fill="none" stroke="currentColor" strokeWidth={1.75} viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4" />
    </svg>
  ),
  Members: (
    <svg className="h-4 w-4 shrink-0" fill="none" stroke="currentColor" strokeWidth={1.75} viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
    </svg>
  ),
  Settings: (
    <svg className="h-4 w-4 shrink-0" fill="none" stroke="currentColor" strokeWidth={1.75} viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.573 1.066c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.066-2.573c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
      <circle cx="12" cy="12" r="3" />
    </svg>
  ),
  Traceability: (
    <svg className="h-4 w-4 shrink-0" fill="none" stroke="currentColor" strokeWidth={1.75} viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" d="M4 6h6m4 0h6M4 12h16M4 18h6m4 0h6" />
      <circle cx="10" cy="6" r="1.5" />
      <circle cx="14" cy="18" r="1.5" />
    </svg>
  ),
  Board: (
    <svg className="h-4 w-4 shrink-0" fill="none" stroke="currentColor" strokeWidth={1.75} viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" d="M13 2L4 14h7l-1 8 9-12h-7l1-8z" />
    </svg>
  ),
  Orchestrate: (
    <svg className="h-4 w-4 shrink-0" fill="none" stroke="currentColor" strokeWidth={1.75} viewBox="0 0 24 24">
      <circle cx="6" cy="6" r="2" />
      <circle cx="18" cy="6" r="2" />
      <circle cx="6" cy="18" r="2" />
      <circle cx="18" cy="18" r="2" />
      <circle cx="12" cy="12" r="2.5" />
      <path strokeLinecap="round" d="M8 7l3 3M16 7l-3 3M8 17l3-3M16 17l-3-3" />
    </svg>
  ),
  Validation: (
    <svg className="h-4 w-4 shrink-0" fill="none" stroke="currentColor" strokeWidth={1.75} viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m5 2a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  ),
};

export function ProjectSidebar({ projectId, projectName }: ProjectSidebarProps) {
  const pathname = usePathname();
  const [collapsed, setCollapsed] = useState(() => {
    if (typeof window !== "undefined") {
      return localStorage.getItem("project-sidebar-collapsed") === "true";
    }
    return false;
  });

  const toggleCollapsed = () => {
    setCollapsed((prev) => {
      const next = !prev;
      localStorage.setItem("project-sidebar-collapsed", String(next));
      return next;
    });
  };
  const { t } = useI18n();
  const base = `/projects/${projectId}`;

  const items = [
    { href: base, label: t("nav.overview"), icon: "Overview", exact: true },
    { href: `${base}/chat`, label: t("nav.chat"), icon: "Chat" },
    { href: `${base}/files`, label: t("nav.artifacts"), icon: "Files" },
    { href: `${base}/traceability`, label: t("nav.traceability"), icon: "Traceability" },
    { href: `${base}/validation`, label: t("nav.validation"), icon: "Validation" },
    { href: `${base}/story-board`, label: t("nav.board"), icon: "Board" },
    { href: `${base}/orchestrate`, label: t("nav.orchestrate"), icon: "Orchestrate" },
    { href: `${base}/context`, label: t("nav.context"), icon: "Context" },
    { href: `${base}/members`, label: t("nav.members"), icon: "Members" },
    { href: `${base}/settings`, label: t("nav.settings"), icon: "Settings" },
  ];

  return (
    <aside
      className={cn(
        "flex flex-col border-r border-border bg-sidebar transition-all duration-200 ease-in-out",
        collapsed ? "w-12" : "w-48"
      )}
    >
      {collapsed && (
        <Link
          href={base}
          className="block border-b border-border px-1.5 py-2 hover:bg-muted transition-colors text-center"
          title={projectName || t("projects.title")}
        >
          <span className="text-[10px] font-semibold text-primary leading-tight break-words line-clamp-3">
            {projectName || t("projects.title")}
          </span>
        </Link>
      )}

      {!collapsed && (
        <div className="flex items-center border-b border-border h-10 px-3">
          <Link href={base} className="flex-1 text-[13px] font-semibold truncate text-foreground" title={projectName || t("projects.title")}>
            {projectName || t("projects.title")}
          </Link>
        </div>
      )}

      <nav className="flex-1 space-y-0.5 p-1.5 pt-2">
        {items.map((item) => {
          const isActive = item.exact
            ? pathname === item.href
            : pathname.startsWith(item.href);
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "relative group flex items-center gap-2.5 rounded-md py-1.5 text-[13px] font-medium transition-colors duration-100",
                collapsed ? "justify-center px-2" : "px-2.5",
                isActive
                  ? "bg-primary/6 text-primary font-semibold"
                  : "text-muted-foreground hover:bg-muted hover:text-foreground"
              )}
            >
              <span className={cn(
                "transition-colors",
                isActive ? "text-primary" : "text-muted-foreground group-hover:text-foreground"
              )}>
                {iconMap[item.icon]}
              </span>
              {!collapsed && <span>{item.label}</span>}
              {isActive && (
                <span className="absolute left-0 top-1/2 -translate-y-1/2 w-[2px] h-4 rounded-r-full bg-primary" />
              )}
              {collapsed && (
                <span className="absolute left-full ml-2 px-2 py-1 rounded-md bg-foreground text-background text-[11px] font-medium shadow-lg whitespace-nowrap opacity-0 pointer-events-none group-hover:opacity-100 transition-opacity z-50">
                  {item.label}
                </span>
              )}
            </Link>
          );
        })}
      </nav>
      <button
        onClick={toggleCollapsed}
        className="flex items-center justify-center h-8 border-t border-border hover:bg-muted transition-colors text-muted-foreground/50 hover:text-muted-foreground"
        title={collapsed ? t("nav.expand") : t("nav.collapse")}
      >
        <svg
          className={cn("h-3 w-3 transition-transform duration-200", collapsed && "rotate-180")}
          fill="none"
          stroke="currentColor"
          strokeWidth={2}
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" d="M11 19l-7-7 7-7M18 19l-7-7 7-7" />
        </svg>
      </button>
    </aside>
  );
}
