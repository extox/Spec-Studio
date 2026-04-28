"use client";

import { useEffect, useState } from "react";
import api from "@/lib/api";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import { useI18n } from "@/lib/i18n";

interface TraceLink {
  id: number;
  source_file_id: number;
  source_anchor: string;
  target_file_id: number;
  target_anchor: string;
  relation: string;
  origin: string;
  confidence: number;
  rationale: string | null;
}

interface TraceAnchor {
  file_id: number;
  file_name: string;
  file_path: string;
  prefix: string;
  anchor: string;
}

interface TracePanelProps {
  projectId: number;
  fileId: number | null;
}

export function TracePanel({ projectId, fileId }: TracePanelProps) {
  const { t } = useI18n();
  const [links, setLinks] = useState<TraceLink[]>([]);
  const [anchors, setAnchors] = useState<TraceAnchor[]>([]);
  const [loading, setLoading] = useState(false);
  const [suggesting, setSuggesting] = useState(false);

  const load = async () => {
    if (!fileId) {
      setLinks([]);
      setAnchors([]);
      return;
    }
    setLoading(true);
    try {
      const [linksRes, anchorsRes] = await Promise.all([
        api.get(`/projects/${projectId}/traceability/links`, { params: { file_id: fileId } }),
        api.get(`/projects/${projectId}/traceability/anchors`),
      ]);
      setLinks(linksRes.data);
      setAnchors(anchorsRes.data.filter((a: TraceAnchor) => a.file_id === fileId));
    } catch {
      toast.error(t("trace.loadFailed"));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [fileId, projectId]);

  const onRebuild = async () => {
    if (!fileId) return;
    try {
      const res = await api.post(`/projects/${projectId}/traceability/rebuild`, null, {
        params: { file_id: fileId },
      });
      toast.success(t("trace.rebuildOk", { count: String(res.data.links_inserted) }));
      load();
    } catch {
      toast.error(t("trace.rebuildFail"));
    }
  };

  const onSuggest = async () => {
    if (!fileId) return;
    setSuggesting(true);
    try {
      const res = await api.post(`/projects/${projectId}/traceability/suggest`, null, {
        params: { file_id: fileId, min_confidence: 0.5 },
      });
      toast.success(t("trace.suggestOk", { count: String(res.data.links_inserted) }));
      load();
    } catch {
      toast.error(t("trace.suggestFail"));
    } finally {
      setSuggesting(false);
    }
  };

  const onDelete = async (linkId: number) => {
    try {
      await api.delete(`/projects/${projectId}/traceability/links/${linkId}`);
      load();
    } catch {
      toast.error(t("trace.deleteFail"));
    }
  };

  if (!fileId) {
    return (
      <div className="text-xs text-muted-foreground p-3">
        {t("trace.selectFileHint")}
      </div>
    );
  }

  const upstream = links.filter((l) => l.source_file_id === fileId);
  const downstream = links.filter((l) => l.target_file_id === fileId);

  return (
    <div className="flex flex-col gap-3 text-xs p-3">
      <div className="flex gap-2">
        <Button size="sm" variant="outline" onClick={onRebuild} disabled={loading}>
          {t("trace.rebuild")}
        </Button>
        <Button size="sm" variant="outline" onClick={onSuggest} disabled={suggesting || loading}>
          {suggesting ? t("trace.suggesting") : t("trace.suggest")}
        </Button>
      </div>

      <div>
        <p className="font-semibold mb-1">{t("trace.anchorsInFile", { count: String(anchors.length) })}</p>
        {anchors.length === 0 ? (
          <p className="text-muted-foreground italic">{t("trace.noAnchors")}</p>
        ) : (
          <div className="flex flex-wrap gap-1">
            {anchors.map((a, i) => (
              <span
                key={`${a.anchor}-${i}`}
                className="inline-flex items-center rounded-md border px-1.5 py-0.5 text-[10px] font-mono"
              >
                {a.anchor}
              </span>
            ))}
          </div>
        )}
      </div>

      <div>
        <p className="font-semibold mb-1">{t("trace.derivesFrom", { count: String(upstream.length) })}</p>
        {upstream.length === 0 ? (
          <p className="text-muted-foreground italic">{t("trace.noUpstream")}</p>
        ) : (
          <ul className="space-y-1">
            {upstream.map((l) => (
              <li key={l.id} className="border rounded p-2 flex items-start justify-between gap-2">
                <div>
                  <div className="font-mono">
                    <span className="opacity-60">{l.source_anchor}</span>
                    <span className="mx-1">→</span>
                    <span className="font-semibold">{l.target_anchor}</span>
                  </div>
                  <div className="text-[10px] text-muted-foreground mt-0.5">
                    {l.origin}
                    {l.origin === "suggested" && ` · ${Math.round(l.confidence * 100)}%`}
                    {l.rationale && ` · ${l.rationale}`}
                  </div>
                </div>
                {l.origin !== "explicit" && (
                  <button
                    onClick={() => onDelete(l.id)}
                    className="text-muted-foreground hover:text-destructive"
                    title={t("trace.deleteLink")}
                  >
                    ×
                  </button>
                )}
              </li>
            ))}
          </ul>
        )}
      </div>

      <div>
        <p className="font-semibold mb-1">{t("trace.referencedBy", { count: String(downstream.length) })}</p>
        {downstream.length === 0 ? (
          <p className="text-muted-foreground italic">{t("trace.noDownstream")}</p>
        ) : (
          <ul className="space-y-1">
            {downstream.map((l) => (
              <li key={l.id} className="border rounded p-2">
                <div className="font-mono">
                  <span className="font-semibold">{l.target_anchor}</span>
                  <span className="mx-1">←</span>
                  <span className="opacity-60">{l.source_anchor}</span>
                </div>
                <div className="text-[10px] text-muted-foreground mt-0.5">
                  {l.origin}
                  {l.rationale && ` · ${l.rationale}`}
                </div>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
