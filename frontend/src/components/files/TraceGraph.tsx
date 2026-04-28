"use client";

import { useEffect, useMemo } from "react";
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
  MarkerType,
  Position,
  type Node,
  type Edge,
  ReactFlowProvider,
  useReactFlow,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import { useI18n } from "@/lib/i18n";

export type TraceNode = {
  id: string;
  anchor: string;
  file_id: number;
  file_name: string | null;
  file_path: string | null;
  prefix: string | null;
};

export type TraceEdge = {
  id: number;
  source: string;
  target: string;
  relation: string;
  origin: string;
  confidence: number;
  rationale: string | null;
};

export type TraceGraphData = {
  nodes: TraceNode[];
  edges: TraceEdge[];
};

const PREFIX_COLORS: Record<string, string> = {
  PRD: "#2563eb",
  BRIEF: "#0ea5e9",
  ARCH: "#16a34a",
  UX: "#a855f7",
  EPIC: "#f59e0b",
  STORY: "#ef4444",
  SPRINT: "#64748b",
};

const ORIGIN_STYLE: Record<string, { stroke: string; dash?: string }> = {
  explicit: { stroke: "#0f172a" },
  suggested: { stroke: "#94a3b8", dash: "4 3" },
  manual: { stroke: "#7c3aed" },
};

export type LayoutDirection = "horizontal" | "vertical";

interface TraceGraphProps {
  data: TraceGraphData | null;
  loading?: boolean;
  selectedNodeId?: string | null;
  enabledPrefixes?: Set<string>;
  focusDepth?: number;
  /**
   * Optional set of node ids matched by an external search query. When
   * provided, only these ids are drawn (AND with prefix filter).
   * `null`/undefined means no search is active.
   */
  searchNodeIds?: Set<string> | null;
  /** "horizontal" = PRD→STORY left-to-right; "vertical" = top-to-bottom. */
  layoutDirection?: LayoutDirection;
  /**
   * When false (default), nodes that don't appear in any edge are hidden so the
   * graph stays focused on the connected backbone. Toggle on to inspect them.
   */
  showOrphans?: boolean;
  onNodeClick?: (node: TraceNode) => void;
  onPaneClick?: () => void;
}

/**
 * BFS over the graph from the seed node. Returns the set of node ids reachable
 * within `depth` hops in either direction (both upstream and downstream).
 */
function computeNeighborhood(
  data: TraceGraphData,
  seed: string,
  depth: number,
): { nodeIds: Set<string>; edgeIds: Set<number> } {
  // BFS adjacency uses raw data direction (independent of visual swap in buildEdges).
  const adj: Map<string, Array<{ neighbor: string; edgeId: number }>> = new Map();
  for (const e of data.edges) {
    if (!adj.has(e.source)) adj.set(e.source, []);
    if (!adj.has(e.target)) adj.set(e.target, []);
    adj.get(e.source)!.push({ neighbor: e.target, edgeId: e.id });
    adj.get(e.target)!.push({ neighbor: e.source, edgeId: e.id });
  }

  const nodeIds = new Set<string>([seed]);
  const edgeIds = new Set<number>();
  let frontier = [seed];
  for (let d = 0; d < depth; d++) {
    const next: string[] = [];
    for (const n of frontier) {
      for (const { neighbor, edgeId } of adj.get(n) || []) {
        edgeIds.add(edgeId);
        if (!nodeIds.has(neighbor)) {
          nodeIds.add(neighbor);
          next.push(neighbor);
        }
      }
    }
    frontier = next;
    if (frontier.length === 0) break;
  }
  return { nodeIds, edgeIds };
}

function layoutNodes(
  nodes: TraceNode[],
  visibleIds: Set<string>,
  highlightedIds: Set<string> | null,
  direction: LayoutDirection,
  selectedId: string | null,
): Node[] {
  const layerOrder = ["BRIEF", "PRD", "UX", "ARCH", "EPIC", "STORY", "SPRINT"];
  const buckets = new Map<string, TraceNode[]>();
  for (const n of nodes) {
    if (!visibleIds.has(n.id)) continue;
    const layer = n.prefix || "OTHER";
    if (!buckets.has(layer)) buckets.set(layer, []);
    buckets.get(layer)!.push(n);
  }
  // Horizontal: layers are columns (x advances), items stack vertically (y).
  // Vertical:   layers are rows    (y advances), items spread horizontally (x).
  const HORIZONTAL_COL_WIDTH = 260;
  const HORIZONTAL_ROW_HEIGHT = 70;
  const VERTICAL_ROW_HEIGHT = 130;
  const VERTICAL_COL_WIDTH = 200;
  const sourcePosition = direction === "horizontal" ? Position.Right : Position.Bottom;
  const targetPosition = direction === "horizontal" ? Position.Left : Position.Top;
  const result: Node[] = [];
  let layerIndex = 0;
  for (const layer of [...layerOrder, "OTHER"]) {
    const items = buckets.get(layer);
    if (!items || items.length === 0) continue;
    items.forEach((n, i) => {
      const dimmed = highlightedIds !== null && !highlightedIds.has(n.id);
      const isHighlighted = highlightedIds !== null && highlightedIds.has(n.id);
      const color = PREFIX_COLORS[n.prefix || ""] || "#64748b";
      const isSelected = selectedId === n.id;
      const isConnected = isHighlighted && !isSelected;
      const position =
        direction === "horizontal"
          ? { x: layerIndex * HORIZONTAL_COL_WIDTH, y: i * HORIZONTAL_ROW_HEIGHT }
          : { x: i * VERTICAL_COL_WIDTH, y: layerIndex * VERTICAL_ROW_HEIGHT };
      result.push({
        id: n.id,
        type: "default",
        position,
        sourcePosition,
        targetPosition,
        // Surface prefix on node.data so MiniMap nodeColor can read it.
        data: {
          prefix: n.prefix,
          label: (
            <div className="text-left">
              <div
                className="text-[10px] font-bold uppercase"
                style={{ color }}
              >
                {n.prefix || "OTHER"}
              </div>
              <div className={isSelected ? "text-sm font-bold" : "text-xs font-medium"}>
                {n.anchor}
              </div>
              <div className="text-[10px] text-muted-foreground truncate max-w-[200px]">
                {n.file_name}
              </div>
            </div>
          ),
        },
        zIndex: isSelected ? 1000 : isConnected ? 500 : undefined,
        style: {
          background: isSelected ? "#fff7ed" : isConnected ? "#fffbeb" : "#fff",
          border: isSelected
            ? `3px solid #f97316`
            : isConnected
              ? `3px solid #fbbf24`
              : `2px solid ${color}`,
          borderRadius: 8,
          padding: 8,
          minWidth: 180,
          opacity: dimmed ? 0.35 : 1,
          boxShadow: isSelected
            ? "0 0 0 4px rgba(249,115,22,0.35), 0 8px 24px -4px rgba(249,115,22,0.45)"
            : isConnected
              ? "0 0 0 2px rgba(251,191,36,0.3)"
              : undefined,
        },
      });
    });
    layerIndex += 1;
  }
  return result;
}

function buildEdges(
  edges: TraceEdge[],
  visibleNodeIds: Set<string>,
  highlightedEdgeIds: Set<number> | null,
): Edge[] {
  return edges
    .filter((e) => visibleNodeIds.has(e.source) && visibleNodeIds.has(e.target))
    .map((e) => {
      const style = ORIGIN_STYLE[e.origin] || ORIGIN_STYLE.explicit;
      const dimmed = highlightedEdgeIds !== null && !highlightedEdgeIds.has(e.id);
      // Visual direction is REVERSED from the data direction.
      // Data:  ARCH#C-1 ──derived_from──▶ PRD#FR-001  (downstream → upstream)
      // Visual: PRD#FR-001 ─────────────▶ ARCH#C-1   (upstream "flows to" downstream)
      // This matches the reading order of the column layout.
      //
      // Using default (bezier) edges rather than smoothstep: multiple edges
      // leaving the same node fan out as unique curves instead of stacking on
      // top of each other along the same right-angle path.
      return {
        id: String(e.id),
        source: e.target,   // PRD-side anchor (left column)
        target: e.source,   // implementation anchor (right column)
        type: "default",
        label: e.origin === "suggested" ? `~${Math.round(e.confidence * 100)}%` : undefined,
        animated: !dimmed && e.origin === "suggested",
        style: {
          stroke: style.stroke,
          strokeWidth: dimmed ? 1 : 2.5,
          strokeDasharray: style.dash,
          opacity: dimmed ? 0.2 : 1,
        },
        markerEnd: { type: MarkerType.ArrowClosed, color: style.stroke },
      };
    });
}

export function TraceGraph({
  data,
  loading,
  selectedNodeId,
  enabledPrefixes,
  focusDepth = 1,
  searchNodeIds,
  layoutDirection = "horizontal",
  showOrphans = false,
  onNodeClick,
  onPaneClick,
}: TraceGraphProps) {
  const { t } = useI18n();

  // Set of node ids that participate in at least one edge.
  const connectedNodeIds = useMemo(() => {
    if (!data) return new Set<string>();
    const s = new Set<string>();
    for (const e of data.edges) {
      s.add(e.source);
      s.add(e.target);
    }
    return s;
  }, [data]);

  const visibleNodeIds = useMemo(() => {
    if (!data) return new Set<string>();
    let pool = enabledPrefixes
      ? data.nodes.filter((n) => enabledPrefixes.has(n.prefix || "OTHER"))
      : data.nodes;
    if (searchNodeIds) {
      pool = pool.filter((n) => searchNodeIds.has(n.id));
    }
    if (!showOrphans) {
      pool = pool.filter((n) => connectedNodeIds.has(n.id));
    }
    return new Set(pool.map((n) => n.id));
  }, [data, enabledPrefixes, searchNodeIds, showOrphans, connectedNodeIds]);

  const highlight = useMemo(() => {
    if (!data || !selectedNodeId) return null;
    const edgeIds = new Set<number>();
    const nodeIds = new Set<string>([selectedNodeId]);
    let frontier = [selectedNodeId];
    for (let d = 0; d < Math.max(1, focusDepth); d++) {
      const next: string[] = [];
      for (const e of data.edges) {
        if (frontier.includes(e.source) || frontier.includes(e.target)) {
          edgeIds.add(e.id);
          const other = frontier.includes(e.source) ? e.target : e.source;
          if (!nodeIds.has(other)) {
            nodeIds.add(other);
            next.push(other);
          }
        }
      }
      frontier = next;
      if (!frontier.length) break;
    }
    return { nodeIds, edgeIds };
  }, [data, selectedNodeId, focusDepth]);

  const initialNodes = useMemo(
    () =>
      data
        ? layoutNodes(data.nodes, visibleNodeIds, highlight?.nodeIds ?? null, layoutDirection, selectedNodeId ?? null)
        : [],
    [data, visibleNodeIds, highlight, layoutDirection, selectedNodeId],
  );
  const initialEdges = useMemo(
    () => (data ? buildEdges(data.edges, visibleNodeIds, highlight?.edgeIds ?? null) : []),
    [data, visibleNodeIds, highlight],
  );

  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  useEffect(() => {
    setNodes(initialNodes);
  }, [initialNodes, setNodes]);

  useEffect(() => {
    setEdges(initialEdges);
  }, [initialEdges, setEdges]);

  if (loading) {
    return (
      <div className="flex h-full items-center justify-center text-muted-foreground text-sm">
        {t("trace.loading")}
      </div>
    );
  }

  if (!data || data.nodes.length === 0) {
    return (
      <div className="flex h-full flex-col items-center justify-center text-sm text-muted-foreground gap-2">
        <p>{t("trace.empty")}</p>
        <p className="text-xs opacity-70">{t("trace.emptyHint")}</p>
      </div>
    );
  }

  return (
    <ReactFlowProvider>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onNodeClick={(_, node) => {
          const found = data.nodes.find((n) => n.id === node.id);
          if (found && onNodeClick) onNodeClick(found);
        }}
        onPaneClick={() => onPaneClick?.()}
        fitView
        fitViewOptions={{ padding: 0.2, maxZoom: 1.2 }}
        minZoom={0.05}
        maxZoom={2}
        proOptions={{ hideAttribution: true }}
      >
        <Background gap={16} />
        <Controls showInteractive={false} />
        <MiniMap
          zoomable
          pannable
          nodeColor={(n) => {
            const prefix = (n.data as { prefix?: string | null } | undefined)?.prefix;
            return PREFIX_COLORS[prefix || ""] || "#94a3b8";
          }}
          nodeStrokeColor={(n) => {
            const prefix = (n.data as { prefix?: string | null } | undefined)?.prefix;
            return PREFIX_COLORS[prefix || ""] || "#64748b";
          }}
          nodeStrokeWidth={2}
        />
        <FitViewButton label={t("trace.fitAll")} />
      </ReactFlow>
    </ReactFlowProvider>
  );
}

/**
 * Floating "Fit All" button — fits the entire graph into the viewport in one
 * click. Useful when the canvas has many nodes and the user is lost.
 */
function FitViewButton({ label }: { label: string }) {
  const { fitView } = useReactFlow();
  return (
    <button
      type="button"
      onClick={() => fitView({ padding: 0.2, duration: 400 })}
      title={label}
      className="absolute top-2 right-2 z-10 inline-flex items-center gap-1 rounded-md border bg-background px-2.5 py-1 text-[11px] font-medium shadow-sm hover:bg-muted text-foreground transition-colors"
    >
      <svg className="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 8V4m0 0h4M4 4l5 5m11-5h-4m4 0v4m0-4l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5v-4m0 4h-4m4 0l-5-5" />
      </svg>
      {label}
    </button>
  );
}

