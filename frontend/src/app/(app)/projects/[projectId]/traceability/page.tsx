"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useParams, useSearchParams } from "next/navigation";
import api from "@/lib/api";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { useI18n } from "@/lib/i18n";
import { cn } from "@/lib/utils";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { TraceGraph, type TraceGraphData, type TraceNode, type LayoutDirection } from "@/components/files/TraceGraph";
import { TracePanel } from "@/components/files/TracePanel";
import { MarkdownPreview } from "@/components/editor/MarkdownPreview";

interface OrphanAnchor {
  file_id: number;
  anchor: string;
  prefix: string;
}

interface AnchorSnippet {
  file_id: number;
  file_name: string;
  file_path: string;
  prefix: string | null;
  anchor: string;
  kind: "heading" | "table" | "text" | "none";
  heading: string | null;
  snippet: string;
}

const PREFIX_ORDER = ["BRIEF", "PRD", "UX", "ARCH", "EPIC", "STORY", "SPRINT"] as const;
const PREFIX_COLORS: Record<string, string> = {
  PRD: "bg-blue-100 text-blue-700 border-blue-300",
  BRIEF: "bg-sky-100 text-sky-700 border-sky-300",
  ARCH: "bg-emerald-100 text-emerald-700 border-emerald-300",
  UX: "bg-purple-100 text-purple-700 border-purple-300",
  EPIC: "bg-amber-100 text-amber-700 border-amber-300",
  STORY: "bg-rose-100 text-rose-700 border-rose-300",
  SPRINT: "bg-slate-100 text-slate-700 border-slate-300",
};

export default function TraceabilityPage() {
  const params = useParams();
  const searchParamsHook = useSearchParams();
  const projectId = Number(params.projectId);
  const { t } = useI18n();

  const [graph, setGraph] = useState<TraceGraphData | null>(null);
  const [orphans, setOrphans] = useState<OrphanAnchor[]>([]);
  const [loading, setLoading] = useState(false);
  const [rebuilding, setRebuilding] = useState(false);

  const [selectedNode, setSelectedNode] = useState<TraceNode | null>(null);
  const [snippet, setSnippet] = useState<AnchorSnippet | null>(null);
  const [snippetLoading, setSnippetLoading] = useState(false);
  const selectedOrphanRef = useRef<HTMLDivElement | null>(null);

  const [enabledPrefixes, setEnabledPrefixes] = useState<Set<string>>(
    new Set([...PREFIX_ORDER, "OTHER"])
  );
  const [focusDepth, setFocusDepth] = useState(2);
  const [searchQuery, setSearchQuery] = useState("");

  // Deep link from validation issues: ?focus=FR-001 → select the node, but
  // do NOT seed the search filter — the filter would hide every other node
  // and prevent the user from seeing how this anchor connects to the rest of
  // the graph. Selection alone is enough; the search box stays empty so the
  // full graph remains visible around the focused node.

  const focusAppliedRef = useRef<string | null>(null);

  const [layoutDirection, setLayoutDirection] = useState<LayoutDirection>(() => {
    if (typeof window === "undefined") return "horizontal";
    const saved = localStorage.getItem("trace-layout-direction");
    return saved === "vertical" ? "vertical" : "horizontal";
  });

  const changeLayoutDirection = (dir: LayoutDirection) => {
    setLayoutDirection(dir);
    if (typeof window !== "undefined") {
      localStorage.setItem("trace-layout-direction", dir);
    }
  };

  const [showOrphans, setShowOrphans] = useState<boolean>(() => {
    if (typeof window === "undefined") return false;
    const saved = localStorage.getItem("trace-show-orphans");
    return saved === "true";
  });

  const toggleShowOrphans = () => {
    setShowOrphans((prev) => {
      const next = !prev;
      if (typeof window !== "undefined") {
        localStorage.setItem("trace-show-orphans", String(next));
      }
      return next;
    });
  };
  // Persistent collapse state for the three right-side sections.
  const usePersistentCollapsed = (key: string, defaultCollapsed: boolean) => {
    const [collapsed, setCollapsed] = useState<boolean>(() => {
      if (typeof window === "undefined") return defaultCollapsed;
      const saved = localStorage.getItem(key);
      return saved === null ? defaultCollapsed : saved === "true";
    });
    const toggle = () => {
      setCollapsed((prev) => {
        const next = !prev;
        if (typeof window !== "undefined") {
          localStorage.setItem(key, String(next));
        }
        return next;
      });
    };
    const set = (value: boolean) => {
      setCollapsed(value);
      if (typeof window !== "undefined") {
        localStorage.setItem(key, String(value));
      }
    };
    return [collapsed, toggle, set] as const;
  };

  const [anchorContentCollapsed, toggleAnchorContent, setAnchorContentCollapsed] = usePersistentCollapsed(
    "trace-anchor-content-collapsed",
    false,
  );
  const [fileDetailsCollapsed, toggleFileDetails] = usePersistentCollapsed(
    "trace-file-details-collapsed",
    false,
  );
  const [orphanCollapsed, toggleOrphanCollapsed] = usePersistentCollapsed(
    "trace-orphan-collapsed",
    true,
  );

  // Whole right-side panel collapse (independent of inner section collapses).
  const [sidePanelCollapsed, , setSidePanelCollapsed] = usePersistentCollapsed(
    "trace-side-panel-collapsed",
    false,
  );

  // Auto-expand the side panel whenever a node is selected.
  useEffect(() => {
    if (selectedNode) setSidePanelCollapsed(false);
  }, [selectedNode, setSidePanelCollapsed]);

  // Once the graph is loaded, auto-select the node matching ?focus= so the
  // right-side "Anchor content" panel shows immediately rather than requiring
  // the user to click the node themselves.
  useEffect(() => {
    const focus = searchParamsHook.get("focus");
    if (!focus || !graph) return;
    if (focusAppliedRef.current === focus) return;
    const target = focus.toLowerCase();
    const match = graph.nodes.find((n) => n.anchor.toLowerCase() === target);
    if (match) {
      setSelectedNode(match);
      setAnchorContentCollapsed(false);
      focusAppliedRef.current = focus;
    }
  }, [graph, searchParamsHook, setAnchorContentCollapsed]);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const [graphRes, orphansRes] = await Promise.all([
        api.get(`/projects/${projectId}/traceability/graph`),
        api.get(`/projects/${projectId}/traceability/orphans`),
      ]);
      setGraph(graphRes.data);
      setOrphans(orphansRes.data);
    } catch {
      toast.error(t("trace.loadFailed"));
    } finally {
      setLoading(false);
    }
  }, [projectId, t]);

  useEffect(() => {
    load();
  }, [load]);

  // Discovered prefixes from current data — only show filter chips for prefixes
  // that actually exist in the project.
  const presentPrefixes = useMemo(() => {
    if (!graph) return new Set<string>();
    const s = new Set<string>();
    for (const n of graph.nodes) s.add(n.prefix || "OTHER");
    return s;
  }, [graph]);

  // Per-prefix anchor counts (denominator of the validation health score).
  const prefixCounts = useMemo(() => {
    const counts = new Map<string, number>();
    if (!graph) return counts;
    for (const n of graph.nodes) {
      const k = n.prefix || "OTHER";
      counts.set(k, (counts.get(k) ?? 0) + 1);
    }
    return counts;
  }, [graph]);

  const totalAnchorCount = useMemo(() => {
    return Array.from(prefixCounts.values()).reduce((a, b) => a + b, 0);
  }, [prefixCounts]);

  const searchMatchCount = useMemo(() => {
    const q = searchQuery.trim().toLowerCase();
    if (!q || !graph) return 0;
    return graph.nodes.filter(
      (n) =>
        enabledPrefixes.has(n.prefix || "OTHER") &&
        (n.anchor.toLowerCase().includes(q) ||
          (n.file_name || "").toLowerCase().includes(q))
    ).length;
  }, [searchQuery, graph, enabledPrefixes]);

  const visibleNodeIdsForSearch = useMemo(() => {
    if (!graph) return null;
    const q = searchQuery.trim().toLowerCase();
    if (!q) return null;
    return new Set(
      graph.nodes
        .filter(
          (n) =>
            enabledPrefixes.has(n.prefix || "OTHER") &&
            (n.anchor.toLowerCase().includes(q) ||
              (n.file_name || "").toLowerCase().includes(q))
        )
        .map((n) => n.id)
    );
  }, [graph, searchQuery, enabledPrefixes]);

  // Auto-scroll the selected orphan into view (when one is selected and the
  // orphan section is expanded).
  useEffect(() => {
    if (!selectedNode || orphanCollapsed) return;
    selectedOrphanRef.current?.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }, [selectedNode, orphanCollapsed]);

  // Fetch snippet whenever the selection changes.
  useEffect(() => {
    if (!selectedNode) {
      setSnippet(null);
      return;
    }
    let cancelled = false;
    setSnippetLoading(true);
    api
      .get<AnchorSnippet>(`/projects/${projectId}/traceability/anchor-content`, {
        params: { file_id: selectedNode.file_id, anchor: selectedNode.anchor },
      })
      .then((res) => {
        if (!cancelled) setSnippet(res.data);
      })
      .catch(() => {
        if (!cancelled) setSnippet(null);
      })
      .finally(() => {
        if (!cancelled) setSnippetLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, [selectedNode, projectId]);

  const onRebuildAll = async () => {
    setRebuilding(true);
    try {
      const res = await api.post(`/projects/${projectId}/traceability/rebuild`);
      toast.success(t("trace.rebuildAllOk", { count: String(res.data.links_inserted) }));
      load();
    } catch {
      toast.error(t("trace.rebuildFail"));
    } finally {
      setRebuilding(false);
    }
  };

  const togglePrefix = (prefix: string) => {
    setEnabledPrefixes((prev) => {
      const next = new Set(prev);
      if (next.has(prefix)) next.delete(prefix);
      else next.add(prefix);
      return next;
    });
  };

  const onNodeClick = (node: TraceNode) => setSelectedNode(node);
  const onPaneClick = () => setSelectedNode(null);

  const DEFAULT_PREFIXES = new Set<string>([...PREFIX_ORDER, "OTHER"]);
  const allPrefixesEnabled =
    enabledPrefixes.size === DEFAULT_PREFIXES.size &&
    [...DEFAULT_PREFIXES].every((p) => enabledPrefixes.has(p));
  const filtersActive =
    !allPrefixesEnabled ||
    focusDepth !== 2 ||
    searchQuery.trim() !== "" ||
    showOrphans;

  const onResetFilters = () => {
    setEnabledPrefixes(new Set([...PREFIX_ORDER, "OTHER"]));
    setFocusDepth(2);
    setSearchQuery("");
    setShowOrphans(false);
    if (typeof window !== "undefined") {
      localStorage.setItem("trace-show-orphans", "false");
    }
  };

  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center justify-between border-b px-4 py-2">
        <div>
          <h1 className="text-base font-semibold">{t("trace.title")}</h1>
          <p className="text-[11px] text-muted-foreground">{t("trace.subtitle")}</p>
        </div>
        <div className="flex items-center gap-2">
          <Button size="sm" variant="outline" onClick={onRebuildAll} disabled={rebuilding || loading}>
            {rebuilding ? t("trace.rebuilding") : t("trace.rebuildAll")}
          </Button>
          <Button size="sm" variant="outline" onClick={load} disabled={loading}>
            {t("trace.reload")}
          </Button>
        </div>
      </div>

      {/* Filter / focus toolbar */}
      <div className="flex items-center gap-3 border-b px-4 py-2 text-xs flex-wrap">
        <span
          className="font-mono text-[10px] px-2 py-0.5 rounded-full bg-slate-900 text-slate-100"
          title={t("trace.totalAnchorsHint")}
        >
          Σ {totalAnchorCount}
        </span>
        <span className="text-muted-foreground">{t("trace.filter")}</span>
        {[...PREFIX_ORDER, "OTHER"]
          .filter((p) => presentPrefixes.has(p))
          .map((p) => {
            const active = enabledPrefixes.has(p);
            const count = prefixCounts.get(p) ?? 0;
            return (
              <button
                key={p}
                onClick={() => togglePrefix(p)}
                className={cn(
                  "px-2 py-0.5 rounded-full border font-mono text-[10px] transition-colors inline-flex items-center gap-1",
                  active ? PREFIX_COLORS[p] || "bg-muted border-muted-foreground/30" : "opacity-40 hover:opacity-70 border-muted-foreground/30"
                )}
              >
                <span>{p}</span>
                <span className="opacity-70">{count}</span>
              </button>
            );
          })}

        <div className="ml-4 flex items-center gap-1">
          <span className="text-muted-foreground">{t("trace.focusDepth", { n: String(focusDepth) })}</span>
          <input
            type="range"
            min={1}
            max={3}
            step={1}
            value={focusDepth}
            onChange={(e) => setFocusDepth(Number(e.target.value))}
            className="w-16"
          />
        </div>

        {/* Show orphans toggle */}
        <button
          onClick={toggleShowOrphans}
          title={t("trace.showOrphansHint")}
          className={cn(
            "ml-4 flex items-center gap-1 h-6 px-2 text-[11px] rounded border transition-colors",
            showOrphans
              ? "bg-foreground text-background border-foreground"
              : "bg-background text-muted-foreground border-muted-foreground/40 hover:border-foreground hover:text-foreground"
          )}
        >
          <svg className="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            {showOrphans ? (
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            ) : (
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            )}
          </svg>
          {t("trace.showOrphansToggle")}
        </button>

        {/* Layout direction toggle (horizontal / vertical) */}
        <div className="ml-4 flex items-center gap-1">
          <span className="text-muted-foreground">{t("trace.layoutLabel")}</span>
          <div className="inline-flex rounded border overflow-hidden">
            <button
              onClick={() => changeLayoutDirection("horizontal")}
              className={cn(
                "px-2 py-0.5 text-[10px] flex items-center gap-1 transition-colors",
                layoutDirection === "horizontal"
                  ? "bg-foreground text-background"
                  : "bg-background text-muted-foreground hover:bg-muted"
              )}
              title={t("trace.layoutHorizontal")}
            >
              <svg className="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 12h14M13 6l6 6-6 6" />
              </svg>
              {t("trace.layoutHorizontal")}
            </button>
            <button
              onClick={() => changeLayoutDirection("vertical")}
              className={cn(
                "px-2 py-0.5 text-[10px] flex items-center gap-1 transition-colors border-l",
                layoutDirection === "vertical"
                  ? "bg-foreground text-background"
                  : "bg-background text-muted-foreground hover:bg-muted"
              )}
              title={t("trace.layoutVertical")}
            >
              <svg className="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 5v14M6 13l6 6 6-6" />
              </svg>
              {t("trace.layoutVertical")}
            </button>
          </div>
        </div>

        {/* Anchor search */}
        <div className="ml-4 flex items-center gap-1 relative">
          <svg className="h-3 w-3 text-muted-foreground" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-4.35-4.35M17 10a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder={t("trace.searchPlaceholder")}
            className="h-6 px-2 text-[11px] border rounded bg-background w-44 focus:w-56 transition-all focus:outline-none focus:ring-1 focus:ring-primary/30"
          />
          {searchQuery && (
            <>
              <button
                onClick={onResetFilters}
                className="text-[10px] text-muted-foreground hover:text-destructive px-1"
                title={t("trace.resetFiltersHint")}
              >
                ×
              </button>
              <span className="text-[10px] text-muted-foreground">
                {t("trace.searchMatches", { count: String(searchMatchCount) })}
              </span>
            </>
          )}
        </div>

        {/* Reset all filters (only visible when any filter deviates from defaults) */}
        {filtersActive && (
          <button
            onClick={onResetFilters}
            title={t("trace.resetFiltersHint")}
            className="ml-2 flex items-center gap-1 h-6 px-2 text-[11px] rounded border border-dashed border-muted-foreground/50 text-muted-foreground hover:border-primary hover:text-primary transition-colors"
          >
            <svg className="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            {t("trace.resetFilters")}
          </button>
        )}

        {selectedNode && (
          <div className="ml-auto flex items-center gap-2">
            <span className="text-muted-foreground">{t("trace.focusOn")}</span>
            <span className="font-mono px-1.5 py-0.5 rounded border bg-muted">
              {selectedNode.prefix}#{selectedNode.anchor}
            </span>
            <button
              onClick={() => setSelectedNode(null)}
              className="text-[10px] text-primary hover:underline"
            >
              {t("trace.clearFocus")}
            </button>
          </div>
        )}
      </div>

      <div className="relative flex flex-1 overflow-hidden">
        <div className={cn("flex-1", sidePanelCollapsed ? "" : "border-r")}>
          <TraceGraph
            data={graph}
            loading={loading}
            selectedNodeId={selectedNode?.id ?? null}
            enabledPrefixes={enabledPrefixes}
            focusDepth={focusDepth}
            searchNodeIds={visibleNodeIdsForSearch}
            layoutDirection={layoutDirection}
            showOrphans={showOrphans}
            onNodeClick={onNodeClick}
            onPaneClick={onPaneClick}
          />
        </div>
        {/* Floating toggle handle on the panel boundary */}
        <button
          type="button"
          onClick={() => setSidePanelCollapsed(!sidePanelCollapsed)}
          title={sidePanelCollapsed ? t("trace.expandSidePanel") : t("trace.collapseSidePanel")}
          aria-label={sidePanelCollapsed ? t("trace.expandSidePanel") : t("trace.collapseSidePanel")}
          className={cn(
            "absolute top-1/2 z-10 -translate-y-1/2 flex h-12 w-5 items-center justify-center",
            "rounded-l-md border border-r-0 bg-background shadow-sm",
            "text-muted-foreground hover:text-foreground hover:bg-muted transition-colors"
          )}
          style={{ right: sidePanelCollapsed ? 0 : 360 }}
        >
          {sidePanelCollapsed ? (
            <ChevronLeft className="h-4 w-4" />
          ) : (
            <ChevronRight className="h-4 w-4" />
          )}
        </button>

        {!sidePanelCollapsed && (
        <div className="w-[360px] flex flex-col overflow-hidden">
          {/* Selected anchor content preview (collapsible) */}
          <button
            type="button"
            onClick={toggleAnchorContent}
            className="border-b px-3 py-2 text-xs font-semibold shrink-0 flex items-center justify-between hover:bg-muted/50 transition-colors text-left"
            title={anchorContentCollapsed ? t("trace.expand") : t("trace.collapse")}
          >
            <span className="flex items-center gap-1.5">
              <svg
                className={cn(
                  "h-3 w-3 transition-transform text-muted-foreground",
                  anchorContentCollapsed ? "" : "rotate-90"
                )}
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
              {t("trace.anchorContent")}
            </span>
            {selectedNode && (
              <span className="font-mono text-[10px] text-muted-foreground">
                {selectedNode.prefix}#{selectedNode.anchor}
              </span>
            )}
          </button>
          {!anchorContentCollapsed && (
            <div
              className={cn(
                "overflow-auto px-3 py-2 text-xs",
                (fileDetailsCollapsed || !selectedNode) && orphanCollapsed
                  ? "flex-1 min-h-0"
                  : "shrink-0 max-h-[35%]"
              )}
            >
              {!selectedNode ? (
                <p className="text-muted-foreground italic">{t("trace.selectFileHint")}</p>
              ) : snippetLoading ? (
                <p className="text-muted-foreground">{t("trace.anchorContentLoading")}</p>
              ) : !snippet || snippet.kind === "none" ? (
                <p className="text-muted-foreground italic">{t("trace.anchorContentEmpty")}</p>
              ) : (
                <div className="space-y-1.5">
                  <div className="flex items-center gap-1.5 text-[10px] text-muted-foreground">
                    <span className="font-mono">{snippet.file_name}</span>
                    <span>·</span>
                    <span>{t(`trace.kind${snippet.kind.charAt(0).toUpperCase()}${snippet.kind.slice(1)}` as never)}</span>
                  </div>
                  {snippet.heading && (
                    <p className="text-xs font-semibold">{snippet.heading}</p>
                  )}
                  <div className="trace-snippet-md bg-muted/30 rounded p-2 overflow-x-auto">
                    <MarkdownPreview content={snippet.snippet} />
                  </div>
                </div>
              )}
            </div>
          )}

          {/* File-level traceability details (collapsible, disabled when no selection) */}
          <button
            type="button"
            onClick={selectedNode ? toggleFileDetails : undefined}
            disabled={!selectedNode}
            className={cn(
              "border-t px-3 py-2 text-xs font-semibold shrink-0 flex items-center justify-between text-left transition-colors",
              selectedNode
                ? "hover:bg-muted/50 cursor-pointer"
                : "cursor-not-allowed opacity-60"
            )}
            title={
              !selectedNode
                ? t("trace.selectFileHint")
                : fileDetailsCollapsed
                ? t("trace.expand")
                : t("trace.collapse")
            }
          >
            <span className="flex items-center gap-1.5 min-w-0">
              <svg
                className={cn(
                  "h-3 w-3 transition-transform shrink-0 text-muted-foreground",
                  selectedNode && !fileDetailsCollapsed ? "rotate-90" : ""
                )}
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
              <span className="truncate">
                {t("trace.fileDetails")}
                {selectedNode?.file_name && (
                  <span className="ml-1 font-normal text-muted-foreground">
                    ({selectedNode.file_name})
                  </span>
                )}
              </span>
            </span>
          </button>
          {selectedNode && !fileDetailsCollapsed && (
            <div className="flex-1 min-h-0 overflow-auto">
              <TracePanel projectId={projectId} fileId={selectedNode.file_id} />
            </div>
          )}

          {/* Orphan anchors (collapsible) */}
          <button
            type="button"
            onClick={toggleOrphanCollapsed}
            className="border-t px-3 py-2 text-xs font-semibold shrink-0 flex items-center justify-between hover:bg-muted/50 transition-colors text-left"
            title={orphanCollapsed ? t("trace.expand") : t("trace.collapse")}
          >
            <span className="flex items-center gap-1.5">
              <svg
                className={cn(
                  "h-3 w-3 transition-transform text-muted-foreground",
                  orphanCollapsed ? "" : "rotate-90"
                )}
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
              {t("trace.orphanAnchors", { count: String(orphans.length) })}
            </span>
            <span
              className="text-[10px] text-muted-foreground hover:text-foreground"
              title={t("trace.orphanHint")}
            >
              ⓘ
            </span>
          </button>
          {!orphanCollapsed && (
            <div
              className={cn(
                "overflow-auto px-3 py-2 text-xs space-y-1",
                anchorContentCollapsed && (fileDetailsCollapsed || !selectedNode)
                  ? "flex-1 min-h-0"
                  : "shrink-0 max-h-[35%]"
              )}
            >
              <p className="text-[10px] text-muted-foreground italic mb-1.5">
                {t("trace.orphanHint")}
              </p>
              {(() => {
                const q = searchQuery.trim().toLowerCase();
                const filteredOrphans = q
                  ? orphans.filter(
                      (o) =>
                        o.anchor.toLowerCase().includes(q) ||
                        o.prefix.toLowerCase().includes(q)
                    )
                  : orphans;
                if (filteredOrphans.length === 0) {
                  return (
                    <p className="text-muted-foreground italic">{t("trace.noOrphans")}</p>
                  );
                }
                return filteredOrphans.map((o, i) => {
                  const isSelected =
                    selectedNode?.file_id === o.file_id && selectedNode?.anchor === o.anchor;
                  return (
                    <div
                      key={`${o.file_id}-${o.anchor}-${i}`}
                      ref={isSelected ? selectedOrphanRef : null}
                      className={cn(
                        "flex items-center justify-between border rounded px-2 py-1 transition-colors",
                        isSelected
                          ? "bg-primary/10 border-primary text-primary font-semibold"
                          : "hover:bg-muted/40"
                      )}
                    >
                      <span className="font-mono flex items-center gap-1">
                        {isSelected && <span className="text-primary">▸</span>}
                        {o.prefix}#{o.anchor}
                      </span>
                      <button
                        className={cn(
                          "text-[10px] hover:underline",
                          isSelected ? "text-primary font-semibold" : "text-primary"
                        )}
                        onClick={() => {
                          const node = graph?.nodes.find(
                            (n) => n.file_id === o.file_id && n.anchor === o.anchor
                          );
                          if (node) setSelectedNode(node);
                        }}
                      >
                        {isSelected ? "✓" : t("trace.inspect")}
                      </button>
                    </div>
                  );
                });
              })()}
            </div>
          )}
        </div>
        )}
      </div>
    </div>
  );
}
