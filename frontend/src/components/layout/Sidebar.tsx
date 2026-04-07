"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { useI18n } from "@/lib/i18n";

const iconMap: Record<string, React.ReactNode> = {
  grid: (
    <svg className="h-4 w-4 shrink-0" fill="none" stroke="currentColor" strokeWidth={1.75} viewBox="0 0 24 24">
      <rect x="3" y="3" width="7" height="7" rx="1.5" /><rect x="14" y="3" width="7" height="7" rx="1.5" />
      <rect x="3" y="14" width="7" height="7" rx="1.5" /><rect x="14" y="14" width="7" height="7" rx="1.5" />
    </svg>
  ),
  folder: (
    <svg className="h-4 w-4 shrink-0" fill="none" stroke="currentColor" strokeWidth={1.75} viewBox="0 0 24 24">
      <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z" />
    </svg>
  ),
  settings: (
    <svg className="h-4 w-4 shrink-0" fill="none" stroke="currentColor" strokeWidth={1.75} viewBox="0 0 24 24">
      <circle cx="12" cy="12" r="3" /><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42" />
    </svg>
  ),
  guide: (
    <svg className="h-4 w-4 shrink-0" fill="none" stroke="currentColor" strokeWidth={1.75} viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
    </svg>
  ),
};

export function Sidebar() {
  const pathname = usePathname();
  const [collapsed, setCollapsed] = useState(() => {
    if (typeof window !== "undefined") {
      return localStorage.getItem("sidebar-collapsed") === "true";
    }
    return false;
  });

  const toggleCollapsed = () => {
    setCollapsed((prev) => {
      const next = !prev;
      localStorage.setItem("sidebar-collapsed", String(next));
      return next;
    });
  };
  const { t } = useI18n();

  const navItems = [
    { href: "/dashboard", label: t("nav.dashboard"), icon: "grid" },
    { href: "/projects", label: t("nav.projects"), icon: "folder" },
    { href: "/settings", label: t("nav.settings"), icon: "settings" },
  ];

  return (
    <aside
      className={cn(
        "flex flex-col border-r border-border bg-sidebar transition-all duration-200 ease-in-out",
        collapsed ? "w-12" : "w-52"
      )}
    >
      <nav className="flex-1 space-y-0.5 p-1.5 pt-3">
        {navItems.map((item) => {
          const isActive = pathname === item.href || pathname.startsWith(item.href + "/");
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
      <div className="border-t border-border p-1.5">
        <Link
          href="/guide"
          className={cn(
            "relative group flex items-center gap-2.5 rounded-md py-1.5 text-[13px] font-medium transition-colors duration-100",
            collapsed ? "justify-center px-2" : "px-2.5",
            pathname === "/guide" || pathname.startsWith("/guide/")
              ? "bg-primary/6 text-primary font-semibold"
              : "text-muted-foreground hover:bg-muted hover:text-foreground"
          )}
        >
          <span className={cn(
            "transition-colors",
            pathname === "/guide" || pathname.startsWith("/guide/")
              ? "text-primary"
              : "text-muted-foreground group-hover:text-foreground"
          )}>
            {iconMap.guide}
          </span>
          {!collapsed && <span>{t("nav.guide")}</span>}
          {(pathname === "/guide" || pathname.startsWith("/guide/")) && (
            <span className="absolute left-0 top-1/2 -translate-y-1/2 w-[2px] h-4 rounded-r-full bg-primary" />
          )}
          {collapsed && (
            <span className="absolute left-full ml-2 px-2 py-1 rounded-md bg-foreground text-background text-[11px] font-medium shadow-lg whitespace-nowrap opacity-0 pointer-events-none group-hover:opacity-100 transition-opacity z-50">
              {t("nav.guide")}
            </span>
          )}
        </Link>
      </div>
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
