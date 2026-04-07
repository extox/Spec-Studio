"use client";

import { useCallback, useState, useEffect, useRef } from "react";
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  Panel,
  useNodesState,
  useEdgesState,
  addEdge,
  useReactFlow,
  type Node,
  type Edge,
  type Connection,
  type NodeChange,
  type EdgeChange,
  type NodeProps,
  type EdgeProps,
  Handle,
  Position,
  MarkerType,
  BaseEdge,
  EdgeLabelRenderer,
  getBezierPath,
  ReactFlowProvider,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import yaml from "js-yaml";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { useI18n } from "@/lib/i18n";
import { ARCHITECTURE_SAMPLES, type ArchitectureSample } from "./sampleArchitectures";

// ─── Data types ───
type SystemInfoNodeData = { systemName: string; systemType: string; description: string };
type InfraNodeData = { label: string; infraType: string; technology: string; introduced_year: number | null; notes: string };
type BoundaryNodeData = { label: string; boundaryType: string; color: string; description: string };
type InfraEdgeData = { protocol: string; port: number | null; label: string; direction: "forward" | "backward" | "bidirectional" };

type SystemInfoNode = Node<SystemInfoNodeData, "systemInfo">;
type InfraNode = Node<InfraNodeData, "infra">;
type BoundaryNode = Node<BoundaryNodeData, "boundary">;
type CanvasNode = InfraNode | SystemInfoNode | BoundaryNode;
type InfraEdge = Edge<InfraEdgeData>;

// ─── Node configs ───
const NODE_TYPES_CONFIG = [
  { type: "server", color: "#3b82f6", icon: "🖥️", group: "infra" },
  { type: "database", color: "#6366f1", icon: "🗄️", group: "infra" },
  { type: "storage", color: "#8b5cf6", icon: "💾", group: "infra" },
  { type: "cache", color: "#ec4899", icon: "⚡", group: "infra" },
  { type: "container", color: "#06b6d4", icon: "📦", group: "infra" },
  { type: "load-balancer", color: "#10b981", icon: "⚖️", group: "network" },
  { type: "switch", color: "#f59e0b", icon: "🔀", group: "network" },
  { type: "firewall", color: "#ef4444", icon: "🛡️", group: "network" },
  { type: "gateway", color: "#f97316", icon: "🚪", group: "network" },
  { type: "service", color: "#8b5cf6", icon: "⚙️", group: "service" },
  { type: "queue", color: "#14b8a6", icon: "📨", group: "service" },
  { type: "client", color: "#64748b", icon: "👤", group: "service" },
];
const NODE_TYPE_MAP = Object.fromEntries(NODE_TYPES_CONFIG.map((n) => [n.type, n]));

const BOUNDARY_PRESETS = [
  { type: "vpc", label: "VPC", color: "#3b82f6", icon: "☁️" },
  { type: "dmz", label: "DMZ", color: "#f59e0b", icon: "🛡️" },
  { type: "internal", label: "Internal Network", color: "#10b981", icon: "🔒" },
  { type: "external", label: "External Network", color: "#64748b", icon: "🌐" },
  { type: "subnet", label: "Subnet", color: "#8b5cf6", icon: "📡" },
  { type: "cluster", label: "Cluster", color: "#06b6d4", icon: "🔗" },
];

const BOUNDARY_COLORS = ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#06b6d4", "#64748b", "#ec4899"];

const SYSTEM_TYPE_OPTIONS = [
  { value: "monolith", label: "Monolith" }, { value: "microservice", label: "Microservice" },
  { value: "saas", label: "SaaS" }, { value: "package", label: "Package" },
  { value: "legacy", label: "Legacy" }, { value: "serverless", label: "Serverless" },
  { value: "event-driven", label: "Event-Driven" }, { value: "layered", label: "Layered" },
];

// ─── YAML interfaces ───
interface InfraConnection { target: string; protocol?: string; port?: number | null; label?: string; direction?: "forward" | "backward" | "bidirectional" }
interface InfraObject { id: string; type: string; name: string; technology?: string; introduced_year?: number | null; connections?: InfraConnection[]; notes?: string; _position?: { x: number; y: number }; _boundary?: string }
interface BoundaryObject { id: string; type: string; name: string; color: string; description?: string; children?: string[]; _position?: { x: number; y: number }; _size?: { width: number; height: number } }
interface YamlData { [key: string]: unknown; infrastructure?: InfraObject[]; components?: InfraObject[]; boundaries?: BoundaryObject[]; _system_info_position?: { x: number; y: number } }

const SYSTEM_INFO_NODE_ID = "__system-info__";

// ─── System Info Node ───
function SystemInfoNodeComponent({ data, selected }: NodeProps<SystemInfoNode>) {
  const { t } = useI18n();
  return (
    <div className={cn("px-4 py-3 rounded-xl border-2 shadow-sm min-w-[260px] max-w-[360px] bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800 transition-shadow", selected ? "shadow-lg ring-2 ring-primary/50 border-primary" : "border-slate-400")}>
      <div className="flex items-center gap-2 mb-1"><span className="text-base">📋</span><span className="text-[10px] font-medium text-muted-foreground uppercase tracking-wider">System Info</span></div>
      <div className="text-sm font-bold leading-tight">{data.systemName || t("canvas.systemNameEmpty")}</div>
      <div className="flex items-center gap-2 mt-1"><span className="text-[10px] px-1.5 py-0.5 rounded bg-primary/10 text-primary font-medium">{data.systemType || "monolith"}</span></div>
      {data.description && <div className="text-[10px] text-muted-foreground mt-1.5 leading-relaxed line-clamp-3">{data.description}</div>}
    </div>
  );
}

// ─── Boundary Node ───
function BoundaryNodeComponent({ data, selected }: NodeProps<BoundaryNode>) {
  const borderColor = data.color || "#3b82f6";
  return (
    <div
      className={cn("rounded-xl border-2 border-dashed transition-shadow relative", selected ? "shadow-lg ring-2 ring-primary/30" : "")}
      style={{ borderColor, minWidth: 300, minHeight: 200, backgroundColor: `${borderColor}08` }}
    >
      {/* Handles on boundary for external connections */}
      <Handle type="target" position={Position.Top} className={cn("!w-3 !h-3 transition-opacity", selected ? "!bg-muted-foreground/60 opacity-100" : "!bg-transparent opacity-0")} />
      <Handle type="source" position={Position.Bottom} className={cn("!w-3 !h-3 transition-opacity", selected ? "!bg-muted-foreground/60 opacity-100" : "!bg-transparent opacity-0")} />
      <Handle type="target" position={Position.Left} className={cn("!w-3 !h-3 transition-opacity", selected ? "!bg-muted-foreground/60 opacity-100" : "!bg-transparent opacity-0")} id="left-target" />
      <Handle type="source" position={Position.Right} className={cn("!w-3 !h-3 transition-opacity", selected ? "!bg-muted-foreground/60 opacity-100" : "!bg-transparent opacity-0")} id="right-source" />
      <div className="absolute top-0 left-3 -translate-y-1/2 px-2 py-0.5 rounded text-[10px] font-semibold bg-background border" style={{ borderColor, color: borderColor }}>
        {data.boundaryType === "dmz" ? "🛡️" : data.boundaryType === "external" ? "🌐" : data.boundaryType === "vpc" ? "☁️" : "🔒"}{" "}
        {data.label || data.boundaryType}
      </div>
      {data.description && (
        <div className="absolute bottom-1 left-3 text-[9px] text-muted-foreground">{data.description}</div>
      )}
    </div>
  );
}

// ─── Infra Node ───
function InfraNodeComponent({ data, selected }: NodeProps<InfraNode>) {
  const config = NODE_TYPE_MAP[data.infraType] || { color: "#64748b", icon: "📦" };
  return (
    <div className={cn("px-3 py-2 rounded-lg border-2 shadow-sm min-w-[120px] bg-background transition-shadow", selected ? "shadow-lg ring-2 ring-primary/50" : "")} style={{ borderColor: config.color }}>
      <Handle type="target" position={Position.Top} className={cn("!w-2.5 !h-2.5 transition-opacity", selected ? "!bg-muted-foreground/60 opacity-100" : "!bg-transparent opacity-0")} />
      <Handle type="source" position={Position.Bottom} className={cn("!w-2.5 !h-2.5 transition-opacity", selected ? "!bg-muted-foreground/60 opacity-100" : "!bg-transparent opacity-0")} />
      <Handle type="target" position={Position.Left} className={cn("!w-2.5 !h-2.5 transition-opacity", selected ? "!bg-muted-foreground/60 opacity-100" : "!bg-transparent opacity-0")} id="left-target" />
      <Handle type="source" position={Position.Right} className={cn("!w-2.5 !h-2.5 transition-opacity", selected ? "!bg-muted-foreground/60 opacity-100" : "!bg-transparent opacity-0")} id="right-source" />
      <div className="flex items-center gap-2">
        <span className="text-base">{config.icon}</span>
        <div>
          <div className="text-xs font-semibold leading-tight truncate max-w-[140px]">{data.label || data.infraType}</div>
          {data.technology && <div className="text-[9px] text-muted-foreground leading-tight truncate max-w-[140px]">{data.technology}</div>}
        </div>
      </div>
    </div>
  );
}

// ─── Custom Edge ───
function LabeledEdge({ id, sourceX, sourceY, targetX, targetY, sourcePosition, targetPosition, data, markerEnd, markerStart, selected }: EdgeProps<InfraEdge>) {
  const [path, labelX, labelY] = getBezierPath({ sourceX, sourceY, targetX, targetY, sourcePosition, targetPosition });
  const edgeLabel = data?.label || data?.protocol || "";
  return (
    <>
      <BaseEdge id={id} path={path} markerEnd={markerEnd} markerStart={markerStart} style={{ strokeWidth: selected ? 2.5 : 1.5, stroke: selected ? "hsl(var(--primary))" : undefined }} />
      {edgeLabel && (
        <EdgeLabelRenderer>
          <div style={{ position: "absolute", transform: `translate(-50%, -50%) translate(${labelX}px,${labelY}px)`, pointerEvents: "all" }}
            className={cn("px-1.5 py-0.5 rounded text-[9px] font-medium border bg-background shadow-sm", selected ? "border-primary text-primary" : "border-border text-muted-foreground")}>
            {edgeLabel}
          </div>
        </EdgeLabelRenderer>
      )}
    </>
  );
}

const nodeTypes = { infra: InfraNodeComponent, systemInfo: SystemInfoNodeComponent, boundary: BoundaryNodeComponent };
const edgeTypes = { labeled: LabeledEdge };

// ─── YAML ↔ Flow ───
function yamlToFlow(yamlContent: string): { nodes: CanvasNode[]; edges: InfraEdge[] } {
  let parsed: YamlData;
  try { parsed = yaml.load(yamlContent) as YamlData; } catch { return { nodes: [], edges: [] }; }
  if (!parsed || typeof parsed !== "object") return { nodes: [], edges: [] };

  const nodes: CanvasNode[] = [];
  const edges: InfraEdge[] = [];

  // System info
  const sysPos = parsed._system_info_position || { x: 20, y: 20 };
  nodes.push({ id: SYSTEM_INFO_NODE_ID, type: "systemInfo", position: sysPos, draggable: true, data: { systemName: (parsed.system_name as string) || "", systemType: (parsed.system_type as string) || "monolith", description: (parsed.description as string) || "" } });

  // Boundaries
  const boundaries = (parsed.boundaries || []) as BoundaryObject[];
  const boundaryChildMap: Record<string, string> = {}; // childId -> boundaryId
  boundaries.forEach((b) => {
    const pos = b._position || { x: 100, y: 200 };
    const size = b._size || { width: 400, height: 300 };
    nodes.push({
      id: b.id,
      type: "boundary",
      position: pos,
      style: { width: size.width, height: size.height },
      data: { label: b.name || b.type, boundaryType: b.type || "internal", color: b.color || "#3b82f6", description: b.description || "" },
    } as BoundaryNode);
    (b.children || []).forEach((childId) => { boundaryChildMap[childId] = b.id; });
  });

  // Infra nodes
  const items = (parsed.infrastructure || parsed.components || []) as InfraObject[];
  const COLS = 4, X_GAP = 220, Y_GAP = 140, Y_OFFSET = 160;
  if (Array.isArray(items)) {
    items.forEach((item, i) => {
      const defaultPos = { x: (i % COLS) * X_GAP + 50, y: Math.floor(i / COLS) * Y_GAP + Y_OFFSET };
      const pos = item._position || defaultPos;
      const parentBoundary = item._boundary || boundaryChildMap[item.id];
      const node: Record<string, unknown> = {
        id: item.id || `node-${i}`,
        type: "infra",
        position: pos,
        data: { label: item.name || item.id, infraType: item.type || "service", technology: item.technology || "", introduced_year: item.introduced_year || null, notes: item.notes || "" },
      };
      if (parentBoundary) {
        node.parentId = parentBoundary;
        node.extent = "parent";
      }
      nodes.push(node as InfraNode);

      if (item.connections) {
        item.connections.forEach((conn, ci) => {
          if (!conn.target) return;
          const dir = conn.direction || "forward";
          edges.push({
            id: `${item.id}-${conn.target}-${ci}`, source: item.id || `node-${i}`, target: conn.target, type: "labeled",
            markerEnd: dir !== "backward" ? { type: MarkerType.ArrowClosed, width: 15, height: 15 } : undefined,
            markerStart: dir === "backward" || dir === "bidirectional" ? { type: MarkerType.ArrowClosed, width: 15, height: 15 } : undefined,
            style: { strokeWidth: 1.5 },
            data: { protocol: conn.protocol || "", port: conn.port || null, label: conn.label || conn.protocol || "", direction: dir },
          });
        });
      }
    });
  }
  return { nodes, edges };
}

function flowToYaml(nodes: CanvasNode[], edges: InfraEdge[], originalYaml: string): string {
  let parsed: YamlData;
  try { parsed = (yaml.load(originalYaml) as YamlData) || {}; } catch { parsed = {}; }

  const sysNode = nodes.find((n) => n.id === SYSTEM_INFO_NODE_ID);
  if (sysNode) {
    const d = sysNode.data as SystemInfoNodeData;
    parsed.system_name = d.systemName || "";
    parsed.system_type = d.systemType || "monolith";
    parsed.description = d.description || "";
    parsed._system_info_position = { x: Math.round(sysNode.position.x), y: Math.round(sysNode.position.y) };
  }

  // Boundaries
  const boundaryNodes = nodes.filter((n) => n.type === "boundary") as BoundaryNode[];
  if (boundaryNodes.length > 0) {
    parsed.boundaries = boundaryNodes.map((bn) => {
      const children = nodes.filter((n) => (n as any).parentId === bn.id).map((n) => n.id);
      const b: BoundaryObject = {
        id: bn.id, type: bn.data.boundaryType, name: bn.data.label || bn.data.boundaryType,
        color: bn.data.color || "#3b82f6",
      };
      if (bn.data.description) b.description = bn.data.description;
      if (children.length > 0) b.children = children;
      b._position = { x: Math.round(bn.position.x), y: Math.round(bn.position.y) };
      const style = bn.style as Record<string, unknown> | undefined;
      b._size = { width: Number(style?.width) || 400, height: Number(style?.height) || 300 };
      return b;
    });
  } else {
    delete parsed.boundaries;
  }

  // Infra nodes
  const key = parsed.components ? "components" : "infrastructure";
  const infraNodes = nodes.filter((n) => n.type === "infra") as InfraNode[];
  const items: InfraObject[] = infraNodes.map((node) => {
    const connections: InfraConnection[] = edges.filter((e) => e.source === node.id).map((e) => {
      const c: InfraConnection = { target: e.target };
      if (e.data?.protocol) c.protocol = e.data.protocol;
      if (e.data?.port) c.port = e.data.port;
      if (e.data?.label) c.label = e.data.label;
      if (e.data?.direction && e.data.direction !== "forward") c.direction = e.data.direction;
      return c;
    });
    const item: InfraObject = { id: node.id, type: node.data.infraType, name: node.data.label || node.id };
    if (node.data.technology) item.technology = node.data.technology;
    if (node.data.introduced_year) item.introduced_year = node.data.introduced_year;
    if (node.data.notes) item.notes = node.data.notes;
    if (connections.length > 0) item.connections = connections;
    item._position = { x: Math.round(node.position.x), y: Math.round(node.position.y) };
    if ((node as any).parentId) item._boundary = (node as any).parentId;
    return item;
  });
  parsed[key] = items;
  return yaml.dump(parsed, { lineWidth: -1, noRefs: true, sortKeys: false });
}

// ─── Edge Properties ───
function EdgePropertiesPanel({ edge, onUpdate, onDelete }: { edge: InfraEdge; onUpdate: (id: string, data: InfraEdgeData) => void; onDelete: (id: string) => void }) {
  const { t } = useI18n();
  const d = edge.data || { protocol: "", port: null, label: "", direction: "forward" as const };
  return (
    <div className="p-3 space-y-3 text-xs">
      <div className="flex items-center gap-2"><span>🔗</span><span className="font-semibold">{t("canvas.edgeProperties")}</span></div>
      <div className="text-[10px] text-muted-foreground">{edge.source} → {edge.target}</div>
      <div>
        <label className="text-[10px] text-muted-foreground block mb-0.5">{t("canvas.edgeLabel")}</label>
        <input type="text" value={d.label || ""} onChange={(e) => onUpdate(edge.id, { ...d, label: e.target.value })} className="w-full px-2 py-1 border rounded text-xs bg-background" placeholder={t("canvas.edgeLabelPlaceholder")} />
      </div>
      <div>
        <label className="text-[10px] text-muted-foreground block mb-0.5">{t("canvas.edgeProtocol")}</label>
        <input type="text" value={d.protocol || ""} onChange={(e) => onUpdate(edge.id, { ...d, protocol: e.target.value })} className="w-full px-2 py-1 border rounded text-xs bg-background" placeholder={t("canvas.edgeProtocolPlaceholder")} />
      </div>
      <div>
        <label className="text-[10px] text-muted-foreground block mb-0.5">{t("canvas.edgePort")}</label>
        <input type="number" value={d.port || ""} onChange={(e) => onUpdate(edge.id, { ...d, port: e.target.value ? Number(e.target.value) : null })} className="w-full px-2 py-1 border rounded text-xs bg-background" placeholder="8080" />
      </div>
      <div>
        <label className="text-[10px] text-muted-foreground block mb-0.5">{t("canvas.edgeDirection")}</label>
        <div className="flex gap-1">
          {([{ value: "forward", label: t("canvas.dirForward") }, { value: "backward", label: t("canvas.dirBackward") }, { value: "bidirectional", label: t("canvas.dirBidirectional") }] as const).map((opt) => (
            <button key={opt.value} onClick={() => onUpdate(edge.id, { ...d, direction: opt.value })}
              className={cn("flex-1 px-1.5 py-1 rounded border text-[10px] transition-colors", d.direction === opt.value ? "bg-primary text-primary-foreground border-primary" : "hover:bg-muted")}>
              {opt.label}
            </button>
          ))}
        </div>
      </div>
      <Button size="sm" variant="destructive" className="w-full text-xs h-7 mt-2" onClick={() => onDelete(edge.id)}>{t("canvas.deleteEdge")}</Button>
    </div>
  );
}

// ─── Node Properties ───
function NodePropertiesPanel({ node, nodes, edges, onUpdateNode, onUpdateSystemInfo, onUpdateBoundary, onDeleteNode, onMoveToParent }:
  { node: CanvasNode; nodes: CanvasNode[]; edges: InfraEdge[];
    onUpdateNode: (id: string, data: InfraNodeData) => void; onUpdateSystemInfo: (data: SystemInfoNodeData) => void;
    onUpdateBoundary: (id: string, data: BoundaryNodeData, style?: Record<string, unknown>) => void; onDeleteNode: (id: string) => void;
    onMoveToParent: (nodeId: string, parentId: string | null) => void }) {
  const { t } = useI18n();

  // System Info
  if (node.id === SYSTEM_INFO_NODE_ID) {
    const d = node.data as SystemInfoNodeData;
    return (
      <div className="p-3 space-y-3 text-xs">
        <div className="flex items-center gap-2"><span>📋</span><span className="font-semibold">{t("canvas.systemInfoLabel")}</span></div>
        <div><label className="text-[10px] text-muted-foreground block mb-0.5">{t("canvas.propName")}</label>
          <input type="text" value={d.systemName || ""} onChange={(e) => onUpdateSystemInfo({ ...d, systemName: e.target.value })} className="w-full px-2 py-1 border rounded text-xs bg-background" placeholder="e.g., Order ERP" /></div>
        <div><label className="text-[10px] text-muted-foreground block mb-0.5">{t("canvas.propType")}</label>
          <select value={d.systemType || "monolith"} onChange={(e) => onUpdateSystemInfo({ ...d, systemType: e.target.value })} className="w-full px-2 py-1 border rounded text-xs bg-background">
            {SYSTEM_TYPE_OPTIONS.map((opt) => <option key={opt.value} value={opt.value}>{opt.label}</option>)}</select></div>
        <div><label className="text-[10px] text-muted-foreground block mb-0.5">{t("canvas.propNotes")}</label>
          <textarea value={d.description || ""} onChange={(e) => onUpdateSystemInfo({ ...d, description: e.target.value })} className="w-full px-2 py-1 border rounded text-xs bg-background resize-none" rows={4} /></div>
      </div>
    );
  }

  // Boundary
  if (node.type === "boundary") {
    const d = node.data as BoundaryNodeData;
    const children = nodes.filter((n) => (n as any).parentId === node.id);
    const style = (node.style || {}) as Record<string, unknown>;
    return (
      <div className="p-3 space-y-3 text-xs">
        <div className="flex items-center gap-2"><span>🔲</span><span className="font-semibold">{t("canvas.boundaryProperties")}</span></div>
        <div><label className="text-[10px] text-muted-foreground block mb-0.5">{t("canvas.propName")}</label>
          <input type="text" value={d.label || ""} onChange={(e) => onUpdateBoundary(node.id, { ...d, label: e.target.value })} className="w-full px-2 py-1 border rounded text-xs bg-background" /></div>
        <div><label className="text-[10px] text-muted-foreground block mb-0.5">{t("canvas.propType")}</label>
          <select value={d.boundaryType || "internal"} onChange={(e) => { const preset = BOUNDARY_PRESETS.find((p) => p.type === e.target.value); onUpdateBoundary(node.id, { ...d, boundaryType: e.target.value, color: preset?.color || d.color }); }}
            className="w-full px-2 py-1 border rounded text-xs bg-background">
            {BOUNDARY_PRESETS.map((p) => <option key={p.type} value={p.type}>{p.icon} {p.label}</option>)}</select></div>
        <div><label className="text-[10px] text-muted-foreground block mb-0.5">{t("canvas.propColor")}</label>
          <div className="flex gap-1 flex-wrap">
            {BOUNDARY_COLORS.map((c) => (
              <button key={c} onClick={() => onUpdateBoundary(node.id, { ...d, color: c })}
                className={cn("w-5 h-5 rounded-full border-2 transition-transform", d.color === c ? "scale-125 border-foreground" : "border-transparent hover:scale-110")} style={{ backgroundColor: c }} />
            ))}
          </div>
        </div>
        <div><label className="text-[10px] text-muted-foreground block mb-0.5">{t("canvas.boundarySize")}</label>
          <div className="flex gap-1">
            <input type="number" value={Number(style.width) || 400} onChange={(e) => onUpdateBoundary(node.id, d, { ...style, width: Number(e.target.value) })} className="w-full px-2 py-1 border rounded text-xs bg-background" />
            <span className="text-muted-foreground self-center">×</span>
            <input type="number" value={Number(style.height) || 300} onChange={(e) => onUpdateBoundary(node.id, d, { ...style, height: Number(e.target.value) })} className="w-full px-2 py-1 border rounded text-xs bg-background" />
          </div>
        </div>
        <div><label className="text-[10px] text-muted-foreground block mb-0.5">{t("canvas.propNotes")}</label>
          <textarea value={d.description || ""} onChange={(e) => onUpdateBoundary(node.id, { ...d, description: e.target.value })} className="w-full px-2 py-1 border rounded text-xs bg-background resize-none" rows={2} /></div>
        {children.length > 0 && (
          <div><label className="text-[10px] text-muted-foreground block mb-0.5">{t("canvas.boundaryChildren")} ({children.length})</label>
            {children.map((c) => <div key={c.id} className="text-[10px] text-muted-foreground pl-2">• {(c.data as InfraNodeData).label || c.id}</div>)}</div>
        )}
        <Button size="sm" variant="destructive" className="w-full text-xs h-7 mt-2" onClick={() => onDeleteNode(node.id)}>{t("canvas.deleteSelected")}</Button>
      </div>
    );
  }

  // Infra node
  const infraNode = node as InfraNode;
  const config = NODE_TYPE_MAP[infraNode.data.infraType] || { color: "#64748b", icon: "📦" };
  const nodeEdges = edges.filter((e) => e.source === node.id || e.target === node.id);
  const boundaryNodes = nodes.filter((n) => n.type === "boundary");
  const currentParent = (node as any).parentId || null;

  return (
    <div className="p-3 space-y-3 text-xs">
      <div className="flex items-center gap-2"><span>{config.icon}</span><span className="font-semibold">{t("canvas.properties")}</span></div>
      <div><label className="text-[10px] text-muted-foreground block mb-0.5">{t("canvas.propName")}</label>
        <input type="text" value={infraNode.data.label || ""} onChange={(e) => onUpdateNode(node.id, { ...infraNode.data, label: e.target.value })} className="w-full px-2 py-1 border rounded text-xs bg-background" /></div>
      <div><label className="text-[10px] text-muted-foreground block mb-0.5">{t("canvas.propType")}</label>
        <select value={infraNode.data.infraType || "server"} onChange={(e) => onUpdateNode(node.id, { ...infraNode.data, infraType: e.target.value })} className="w-full px-2 py-1 border rounded text-xs bg-background">
          {NODE_TYPES_CONFIG.map((nt) => <option key={nt.type} value={nt.type}>{nt.icon} {nt.type}</option>)}</select></div>
      <div><label className="text-[10px] text-muted-foreground block mb-0.5">{t("canvas.propTechnology")}</label>
        <input type="text" value={infraNode.data.technology || ""} onChange={(e) => onUpdateNode(node.id, { ...infraNode.data, technology: e.target.value })} className="w-full px-2 py-1 border rounded text-xs bg-background" placeholder="e.g., Apache Tomcat 9" /></div>
      <div><label className="text-[10px] text-muted-foreground block mb-0.5">{t("canvas.propYear")}</label>
        <input type="number" value={infraNode.data.introduced_year || ""} onChange={(e) => onUpdateNode(node.id, { ...infraNode.data, introduced_year: e.target.value ? Number(e.target.value) : null })} className="w-full px-2 py-1 border rounded text-xs bg-background" placeholder="2020" /></div>
      {boundaryNodes.length > 0 && (
        <div><label className="text-[10px] text-muted-foreground block mb-0.5">{t("canvas.parentBoundary")}</label>
          <select value={currentParent || ""} onChange={(e) => onMoveToParent(node.id, e.target.value || null)} className="w-full px-2 py-1 border rounded text-xs bg-background">
            <option value="">{t("canvas.parentNone")}</option>
            {boundaryNodes.map((b) => <option key={b.id} value={b.id}>{(b.data as BoundaryNodeData).label || b.id}</option>)}
          </select></div>
      )}
      <div><label className="text-[10px] text-muted-foreground block mb-0.5">{t("canvas.propNotes")}</label>
        <textarea value={infraNode.data.notes || ""} onChange={(e) => onUpdateNode(node.id, { ...infraNode.data, notes: e.target.value })} className="w-full px-2 py-1 border rounded text-xs bg-background resize-none" rows={2} /></div>
      {nodeEdges.length > 0 && (
        <div><label className="text-[10px] text-muted-foreground block mb-0.5">{t("canvas.connections")} ({nodeEdges.length})</label>
          {nodeEdges.map((e) => <div key={e.id} className="text-[10px] text-muted-foreground">{e.source === node.id ? `→ ${e.target}` : `← ${e.source}`}{e.data?.label ? ` (${e.data.label})` : ""}</div>)}</div>
      )}
      <Button size="sm" variant="destructive" className="w-full text-xs h-7 mt-2" onClick={() => onDeleteNode(node.id)}>{t("canvas.deleteSelected")}</Button>
    </div>
  );
}

// ─── Object Palette ───
function ObjectPalette({ onAdd, onAddBoundary, onLoadSample, collapsed, onToggle }: { onAdd: (type: string) => void; onAddBoundary: (preset: typeof BOUNDARY_PRESETS[0]) => void; onLoadSample: () => void; collapsed: boolean; onToggle: () => void }) {
  const { t } = useI18n();
  const groups = NODE_TYPES_CONFIG.reduce<Record<string, typeof NODE_TYPES_CONFIG>>((acc, n) => { (acc[n.group] ||= []).push(n); return acc; }, {});
  const groupLabels: Record<string, string> = { infra: t("canvas.groupInfra"), network: t("canvas.groupNetwork"), service: t("canvas.groupService") };

  if (collapsed) {
    return (
      <div className="w-10 border-r flex flex-col items-center py-2 gap-0.5 bg-muted/20 overflow-auto">
        <button onClick={onLoadSample} title={t("canvas.loadSample")} className="w-8 h-8 flex items-center justify-center rounded hover:bg-blue-50 hover:text-blue-600 transition-colors text-sm mb-0.5">📥</button>
        <div className="w-6 border-t my-0.5" />
        {BOUNDARY_PRESETS.slice(0, 3).map((bp) => (
          <button key={bp.type} onClick={() => onAddBoundary(bp)} title={bp.label} className="w-8 h-8 flex items-center justify-center rounded hover:bg-muted transition-colors text-sm">{bp.icon}</button>
        ))}
        <div className="w-6 border-t my-0.5" />
        {NODE_TYPES_CONFIG.map((nt) => (
          <button key={nt.type} onClick={() => onAdd(nt.type)} title={nt.type} className="w-8 h-8 flex items-center justify-center rounded hover:bg-muted transition-colors text-sm">{nt.icon}</button>
        ))}
        <button onClick={onToggle} className="mt-auto w-8 h-8 flex items-center justify-center text-muted-foreground hover:text-foreground">
          <svg className="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 5l7 7-7 7M5 5l7 7-7 7" /></svg>
        </button>
      </div>
    );
  }

  return (
    <div className="w-44 border-r flex flex-col bg-muted/20 overflow-auto">
      <div className="flex items-center justify-between px-2 py-1.5 border-b">
        <span className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider">{t("canvas.palette")}</span>
        <button onClick={onToggle} className="text-muted-foreground hover:text-foreground">
          <svg className="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 19l-7-7 7-7M18 19l-7-7 7-7" /></svg>
        </button>
      </div>
      {/* Sample load */}
      <button onClick={onLoadSample} className="mx-2 my-1.5 flex items-center gap-1.5 px-2 py-1.5 rounded border border-dashed border-blue-300 hover:bg-blue-50 hover:border-blue-400 text-xs text-blue-600 transition-colors">
        <span>📥</span><span>{t("canvas.loadSample")}</span>
      </button>
      <div className="mx-2 border-t" />
      {/* Boundaries */}
      <div className="px-1 py-1">
        <div className="text-[9px] text-muted-foreground font-medium uppercase tracking-wider px-1 mb-0.5">{t("canvas.groupBoundary")}</div>
        {BOUNDARY_PRESETS.map((bp) => (
          <button key={bp.type} onClick={() => onAddBoundary(bp)} className="w-full flex items-center gap-1.5 px-2 py-1.5 rounded hover:bg-muted text-xs transition-colors text-left">
            <span>{bp.icon}</span><span className="truncate">{bp.label}</span>
          </button>
        ))}
      </div>
      <div className="mx-2 border-t" />
      {Object.entries(groups).map(([group, items]) => (
        <div key={group} className="px-1 py-1">
          <div className="text-[9px] text-muted-foreground font-medium uppercase tracking-wider px-1 mb-0.5">{groupLabels[group] || group}</div>
          {items.map((nt) => (
            <button key={nt.type} onClick={() => onAdd(nt.type)} className="w-full flex items-center gap-1.5 px-2 py-1.5 rounded hover:bg-muted text-xs transition-colors text-left">
              <span>{nt.icon}</span><span className="truncate">{nt.type}</span>
            </button>
          ))}
        </div>
      ))}
    </div>
  );
}

// ─── Main (inner, needs ReactFlowProvider) ───
// ─── Custom Controls ───
function CanvasControls({ infraCount, boundaryCount, edgeCount }: { infraCount: number; boundaryCount: number; edgeCount: number }) {
  const { zoomIn, zoomOut, fitView } = useReactFlow();
  return (
    <Panel position="bottom-left">
      <div className="flex items-center gap-1">
        <div className="flex flex-col border rounded-md overflow-hidden bg-background shadow-sm">
          <button onClick={() => zoomIn()} className="px-2 py-1.5 hover:bg-muted transition-colors text-sm font-medium border-b" title="Zoom In">+</button>
          <button onClick={() => zoomOut()} className="px-2 py-1.5 hover:bg-muted transition-colors text-sm font-medium border-b" title="Zoom Out">−</button>
          <button onClick={() => fitView({ padding: 0.15, duration: 300 })} className="px-2 py-1.5 hover:bg-muted transition-colors" title="Fit View">
            <svg className="h-3.5 w-3.5 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" /></svg>
          </button>
        </div>
        <div className="text-[10px] text-muted-foreground bg-background/80 px-2 py-1 rounded border shadow-sm">
          {infraCount} objects · {boundaryCount} boundaries · {edgeCount} connections
        </div>
      </div>
    </Panel>
  );
}

function CanvasInner({ yamlContent, onYamlChange }: { yamlContent: string; onYamlChange: (yaml: string) => void }) {
  const { t } = useI18n();
  const [nodes, setNodes, onNodesChange] = useNodesState<CanvasNode>([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState<InfraEdge>([]);
  const [selectedNode, setSelectedNode] = useState<CanvasNode | null>(null);
  const [selectedEdge, setSelectedEdge] = useState<InfraEdge | null>(null);
  const [paletteCollapsed, setPaletteCollapsed] = useState(false);
  const [showSampleDialog, setShowSampleDialog] = useState(false);
  const syncRef = useRef(false);
  const yamlRef = useRef(yamlContent);

  useEffect(() => {
    yamlRef.current = yamlContent;
    if (!syncRef.current) { const { nodes: n, edges: e } = yamlToFlow(yamlContent); setNodes(n); setEdges(e); }
    syncRef.current = false;
  }, [yamlContent, setNodes, setEdges]);

  const syncToYaml = useCallback(() => {
    syncRef.current = true;
    const newYaml = flowToYaml(nodes, edges, yamlRef.current);
    yamlRef.current = newYaml;
    onYamlChange(newYaml);
  }, [nodes, edges, onYamlChange]);

  const timerRef = useRef<NodeJS.Timeout>();
  const debouncedSync = useCallback(() => { clearTimeout(timerRef.current); timerRef.current = setTimeout(syncToYaml, 500); }, [syncToYaml]);

  const handleNodesChange = useCallback((changes: NodeChange<CanvasNode>[]) => {
    onNodesChange(changes);
    if (changes.some((c) => (c.type === "position" && (c as unknown as Record<string, unknown>).dragging === false) || c.type === "remove" || c.type === "dimensions")) debouncedSync();
  }, [onNodesChange, debouncedSync]);

  const handleEdgesChange = useCallback((changes: EdgeChange<InfraEdge>[]) => {
    onEdgesChange(changes);
    if (changes.some((c) => c.type === "remove")) { setSelectedEdge(null); debouncedSync(); }
  }, [onEdgesChange, debouncedSync]);

  const onConnect = useCallback((connection: Connection) => {
    setEdges((eds) => addEdge({ ...connection, type: "labeled", markerEnd: { type: MarkerType.ArrowClosed, width: 15, height: 15 }, style: { strokeWidth: 1.5 }, data: { protocol: "", port: null, label: "", direction: "forward" as const } }, eds));
    setTimeout(debouncedSync, 100);
  }, [setEdges, debouncedSync]);

  const onNodeClick = useCallback((_: React.MouseEvent, node: CanvasNode) => { setSelectedNode(node); setSelectedEdge(null); }, []);
  const onEdgeClick = useCallback((_: React.MouseEvent, edge: InfraEdge) => { setSelectedEdge(edge); setSelectedNode(null); }, []);
  const onPaneClick = useCallback(() => { setSelectedNode(null); setSelectedEdge(null); }, []);

  const handleUpdateNode = useCallback((id: string, data: InfraNodeData) => {
    setNodes((nds) => nds.map((n) => (n.id === id ? { ...n, data } as CanvasNode : n)));
    setSelectedNode((prev) => (prev?.id === id ? { ...prev, data } as CanvasNode : prev));
    debouncedSync();
  }, [setNodes, debouncedSync]);

  const handleUpdateSystemInfo = useCallback((data: SystemInfoNodeData) => {
    setNodes((nds) => nds.map((n) => (n.id === SYSTEM_INFO_NODE_ID ? { ...n, data } as CanvasNode : n)));
    setSelectedNode((prev) => (prev?.id === SYSTEM_INFO_NODE_ID ? { ...prev, data } as CanvasNode : prev));
    debouncedSync();
  }, [setNodes, debouncedSync]);

  const handleUpdateBoundary = useCallback((id: string, data: BoundaryNodeData, style?: Record<string, unknown>) => {
    setNodes((nds) => nds.map((n) => {
      if (n.id !== id) return n;
      const updated = { ...n, data } as CanvasNode;
      if (style) (updated as any).style = { ...(n.style || {}), ...style };
      return updated;
    }));
    setSelectedNode((prev) => {
      if (prev?.id !== id) return prev;
      const updated = { ...prev, data } as CanvasNode;
      if (style) (updated as any).style = { ...((prev as any).style || {}), ...style };
      return updated;
    });
    debouncedSync();
  }, [setNodes, debouncedSync]);

  const handleMoveToParent = useCallback((nodeId: string, parentId: string | null) => {
    setNodes((nds) => nds.map((n) => {
      if (n.id !== nodeId) return n;
      const updated = { ...n } as any;
      if (parentId) { updated.parentId = parentId; updated.extent = "parent"; updated.position = { x: 40, y: 40 }; }
      else { delete updated.parentId; delete updated.extent; }
      return updated as CanvasNode;
    }));
    debouncedSync();
  }, [setNodes, debouncedSync]);

  const handleUpdateEdge = useCallback((id: string, data: InfraEdgeData) => {
    const dir = data.direction || "forward";
    const markerEnd = dir !== "backward" ? { type: MarkerType.ArrowClosed, width: 15, height: 15 } : undefined;
    const markerStart = dir === "backward" || dir === "bidirectional" ? { type: MarkerType.ArrowClosed, width: 15, height: 15 } : undefined;
    setEdges((eds) => eds.map((e) => (e.id === id ? { ...e, data, markerEnd, markerStart } : e)));
    setSelectedEdge((prev) => (prev?.id === id ? { ...prev, data, markerEnd, markerStart } as InfraEdge : prev));
    debouncedSync();
  }, [setEdges, debouncedSync]);

  const handleDeleteNode = useCallback((id: string) => {
    if (id === SYSTEM_INFO_NODE_ID) return;
    // If deleting boundary, release children
    setNodes((nds) => {
      const released = nds.map((n) => {
        if ((n as any).parentId === id) { const u = { ...n } as any; delete u.parentId; delete u.extent; return u as CanvasNode; }
        return n;
      });
      return released.filter((n) => n.id !== id);
    });
    setEdges((eds) => eds.filter((e) => e.source !== id && e.target !== id));
    setSelectedNode(null);
    debouncedSync();
  }, [setNodes, setEdges, debouncedSync]);

  const handleDeleteEdge = useCallback((id: string) => { setEdges((eds) => eds.filter((e) => e.id !== id)); setSelectedEdge(null); debouncedSync(); }, [setEdges, debouncedSync]);

  const addNode = useCallback((type: string) => {
    const id = `${type}-${Date.now()}`;
    const newNode: InfraNode = { id, type: "infra", position: { x: 200 + Math.random() * 300, y: 200 + Math.random() * 200 }, data: { label: type, infraType: type, technology: "", introduced_year: null, notes: "" } };
    setNodes((nds) => [...nds, newNode]);
    setSelectedNode(newNode); setSelectedEdge(null);
    debouncedSync();
  }, [setNodes, debouncedSync]);

  const addBoundary = useCallback((preset: typeof BOUNDARY_PRESETS[0]) => {
    const id = `boundary-${preset.type}-${Date.now()}`;
    const newNode: BoundaryNode = {
      id, type: "boundary",
      position: { x: 100 + Math.random() * 200, y: 150 + Math.random() * 100 },
      style: { width: 400, height: 300 },
      data: { label: preset.label, boundaryType: preset.type, color: preset.color, description: "" },
    };
    setNodes((nds) => {
      // Boundaries must come before their children in the array for rendering order
      const sysInfo = nds.filter((n) => n.id === SYSTEM_INFO_NODE_ID);
      const otherBoundaries = nds.filter((n) => n.type === "boundary");
      const rest = nds.filter((n) => n.id !== SYSTEM_INFO_NODE_ID && n.type !== "boundary");
      return [...sysInfo, ...otherBoundaries, newNode, ...rest];
    });
    setSelectedNode(newNode); setSelectedEdge(null);
    debouncedSync();
  }, [setNodes, debouncedSync]);

  const infraCount = nodes.filter((n) => n.type === "infra").length;
  const boundaryCount = nodes.filter((n) => n.type === "boundary").length;
  const hasSelection = selectedNode || selectedEdge;

  return (
    <div className="flex h-full">
      <ObjectPalette onAdd={addNode} onAddBoundary={addBoundary} onLoadSample={() => setShowSampleDialog(true)} collapsed={paletteCollapsed} onToggle={() => setPaletteCollapsed(!paletteCollapsed)} />

      <div className="flex-1 relative">
        <ReactFlow
          nodes={nodes} edges={edges}
          onNodesChange={handleNodesChange} onEdgesChange={handleEdgesChange} onConnect={onConnect}
          onNodeClick={onNodeClick} onEdgeClick={onEdgeClick} onPaneClick={onPaneClick}
          nodeTypes={nodeTypes} edgeTypes={edgeTypes} defaultEdgeOptions={{ type: "labeled" }}
          snapToGrid snapGrid={[20, 20]} deleteKeyCode={["Backspace", "Delete"]}
          proOptions={{ hideAttribution: true }}
        >
          <Background gap={20} />
          <MiniMap nodeStrokeWidth={3} pannable zoomable style={{ height: 80, width: 120 }} />
          <CanvasControls infraCount={infraCount} boundaryCount={boundaryCount} edgeCount={edges.length} />
        </ReactFlow>
      </div>

      {hasSelection && (
        <div className="w-56 border-l overflow-auto bg-background animate-in slide-in-from-right-2 duration-150">
          <div className="flex items-center justify-between px-3 py-1.5 border-b">
            <span className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider">{t("canvas.properties")}</span>
            <button onClick={onPaneClick} className="text-muted-foreground hover:text-foreground">
              <svg className="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>
            </button>
          </div>
          {selectedEdge ? (
            <EdgePropertiesPanel edge={selectedEdge} onUpdate={handleUpdateEdge} onDelete={handleDeleteEdge} />
          ) : selectedNode ? (
            <NodePropertiesPanel node={selectedNode} nodes={nodes} edges={edges} onUpdateNode={handleUpdateNode}
              onUpdateSystemInfo={handleUpdateSystemInfo} onUpdateBoundary={handleUpdateBoundary}
              onDeleteNode={handleDeleteNode} onMoveToParent={handleMoveToParent} />
          ) : null}
        </div>
      )}

      {/* Sample dialog */}
      {showSampleDialog && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50" onClick={() => setShowSampleDialog(false)}>
          <div className="bg-background rounded-lg shadow-lg w-full max-w-xl p-6" onClick={(e) => e.stopPropagation()}>
            <h3 className="text-lg font-semibold mb-1">{t("canvas.sampleDialogTitle")}</h3>
            <p className="text-xs text-muted-foreground mb-4">{t("canvas.sampleDialogDesc")}</p>
            <div className="grid gap-3">
              {ARCHITECTURE_SAMPLES.map((sample) => (
                <button
                  key={sample.id}
                  onClick={() => {
                    if (nodes.length > 1 && !confirm(t("canvas.sampleConfirm"))) return;
                    onYamlChange(sample.yaml);
                    setShowSampleDialog(false);
                    setTimeout(() => { try { (document.querySelector(".react-flow__controls button:last-child") as HTMLElement)?.click(); } catch {} }, 300);
                  }}
                  className="flex items-start gap-3 p-4 rounded-lg border border-border hover:border-primary/40 hover:bg-primary/5 transition-colors text-left"
                >
                  <span className="text-2xl mt-0.5">{sample.icon}</span>
                  <div>
                    <div className="text-sm font-semibold">{sample.name}</div>
                    <div className="text-xs text-muted-foreground mt-0.5">{sample.description}</div>
                  </div>
                </button>
              ))}
            </div>
            <div className="flex justify-end mt-4">
              <Button variant="outline" size="sm" onClick={() => setShowSampleDialog(false)}>{t("common.close")}</Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// ─── Exported wrapper with ReactFlowProvider ───
export default function SystemDrawingCanvas(props: { yamlContent: string; onYamlChange: (yaml: string) => void }) {
  return (
    <ReactFlowProvider>
      <CanvasInner {...props} />
    </ReactFlowProvider>
  );
}
