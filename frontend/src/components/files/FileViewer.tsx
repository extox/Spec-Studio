"use client";

import { useState, useEffect } from "react";
import api from "@/lib/api";
import { Button } from "@/components/ui/button";
import type { ProjectFile, FileVersion } from "@/types";
import { MarkdownPreview } from "@/components/editor/MarkdownPreview";
import { MarkdownEditor } from "@/components/editor/MarkdownEditor";
import { DiffView } from "@/components/files/DiffView";
import { toast } from "sonner";
import { useI18n } from "@/lib/i18n";
import { cn } from "@/lib/utils";

interface FileViewerProps {
  projectId: number;
  fileId: number;
  onSaved?: (fileName: string) => void;
}

export function FileViewer({ projectId, fileId, onSaved }: FileViewerProps) {
  const { t } = useI18n();
  const [file, setFile] = useState<ProjectFile | null>(null);
  const [isEditing, setIsEditing] = useState(false);
  const [editContent, setEditContent] = useState("");
  const [versions, setVersions] = useState<FileVersion[]>([]);
  const [showVersions, setShowVersions] = useState(false);
  const [restoringId, setRestoringId] = useState<number | null>(null);

  // Diff compare state
  const [compareVersionId, setCompareVersionId] = useState<number | null>(null);
  const [compareContent, setCompareContent] = useState<string | null>(null);
  const [compareLabel, setCompareLabel] = useState("");
  const [loadingCompare, setLoadingCompare] = useState(false);

  useEffect(() => {
    setIsEditing(false);
    setShowVersions(false);
    setCompareVersionId(null);
    setCompareContent(null);
    api.get<ProjectFile>(`/projects/${projectId}/files/${fileId}`).then((res) => {
      setFile(res.data);
      setEditContent(res.data.content || "");
    });
  }, [projectId, fileId]);

  const fetchVersions = async () => {
    try {
      const res = await api.get<FileVersion[]>(`/projects/${projectId}/files/${fileId}/versions`);
      setVersions(res.data);
    } catch {
      setVersions([]);
    }
  };

  const toggleVersions = () => {
    if (!showVersions) fetchVersions();
    setShowVersions(!showVersions);
    if (showVersions) {
      // Closing versions panel — also close diff
      setCompareVersionId(null);
      setCompareContent(null);
    }
  };

  const handleSave = async () => {
    try {
      const res = await api.put<ProjectFile>(`/projects/${projectId}/files/${fileId}`, { content: editContent });
      setFile(res.data);
      setIsEditing(false);
      toast.success(t("files.saved"));
      onSaved?.(file?.file_name || "");
      if (showVersions) fetchVersions();
    } catch {
      toast.error(t("files.saveFailed"));
    }
  };

  const handleRestore = async (versionId: number) => {
    setRestoringId(versionId);
    try {
      const res = await api.post<ProjectFile>(
        `/projects/${projectId}/files/${fileId}/versions/${versionId}/restore`
      );
      setFile(res.data);
      setEditContent(res.data.content || "");
      setCompareVersionId(null);
      setCompareContent(null);
      toast.success(t("files.versionRestored"));
      fetchVersions();
      onSaved?.(file?.file_name || "");
    } catch {
      toast.error(t("files.restoreFailed"));
    } finally {
      setRestoringId(null);
    }
  };

  const handleCompare = async (version: FileVersion) => {
    if (compareVersionId === version.id) {
      // Toggle off
      setCompareVersionId(null);
      setCompareContent(null);
      return;
    }

    setLoadingCompare(true);
    try {
      const res = await api.get<{ id: number; version_label: string; content: string }>(
        `/projects/${projectId}/files/${fileId}/versions/${version.id}`
      );
      setCompareVersionId(version.id);
      setCompareContent(res.data.content);
      setCompareLabel(version.version_label);
      setIsEditing(false);
    } catch {
      toast.error(t("files.compareFailed"));
    } finally {
      setLoadingCompare(false);
    }
  };

  const handleDownload = () => {
    if (!file) return;
    const blob = new Blob([file.content || ""], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = file.file_name;
    a.click();
    URL.revokeObjectURL(url);
  };

  if (!file) return <div className="p-4 text-muted-foreground">{t("common.loading")}</div>;

  const isDiffMode = compareVersionId !== null && compareContent !== null;

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="flex items-center justify-between border-b px-4 py-2">
        <div className="flex items-center gap-2 min-w-0">
          <span className="text-sm font-medium truncate">{file.file_name}</span>
          {file.version_label && (
            <span className="text-[10px] px-1.5 py-0.5 rounded bg-muted text-muted-foreground shrink-0">
              v{file.version_label}
            </span>
          )}
          {file.updated_by_name && (
            <span className="text-[10px] text-muted-foreground shrink-0">
              {file.updated_by_name}
            </span>
          )}
        </div>
        <div className="flex gap-1.5 shrink-0">
          <Button size="sm" variant="ghost" className="h-7 text-xs" onClick={handleDownload} title={t("files.download")}>
            <svg className="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
          </Button>
          <Button
            size="sm"
            variant={showVersions ? "default" : "ghost"}
            className="h-7 text-xs"
            onClick={toggleVersions}
          >
            {t("files.versions")}
          </Button>
          {!isDiffMode && (
            isEditing ? (
              <>
                <Button size="sm" variant="outline" className="h-7 text-xs" onClick={() => setIsEditing(false)}>
                  {t("common.cancel")}
                </Button>
                <Button size="sm" className="h-7 text-xs" onClick={handleSave}>{t("common.save")}</Button>
              </>
            ) : (
              <Button size="sm" variant="outline" className="h-7 text-xs" onClick={() => setIsEditing(true)}>
                {t("common.edit")}
              </Button>
            )
          )}
          {isDiffMode && (
            <Button
              size="sm"
              variant="outline"
              className="h-7 text-xs"
              onClick={() => { setCompareVersionId(null); setCompareContent(null); }}
            >
              {t("files.closeDiff")}
            </Button>
          )}
        </div>
      </div>

      <div className="flex flex-1 overflow-hidden">
        {/* Main content */}
        <div className="flex-1 overflow-hidden">
          {isDiffMode ? (
            <DiffView
              oldText={compareContent}
              newText={file.content || ""}
              oldLabel={`v${compareLabel}`}
              newLabel={`v${file.version_label || "current"}`}
            />
          ) : isEditing ? (
            <div className="h-full overflow-hidden">
              <MarkdownEditor value={editContent} onChange={setEditContent} />
            </div>
          ) : (
            <div className="h-full overflow-auto p-4">
              <MarkdownPreview content={file.content || ""} />
            </div>
          )}
        </div>

        {/* Version sidebar */}
        {showVersions && (
          <div className="w-56 border-l overflow-auto bg-muted/20">
            <div className="p-2 border-b">
              <span className="text-xs font-medium">{t("files.versionHistory")}</span>
            </div>
            <div className="space-y-0.5 p-1">
              {versions.length === 0 && (
                <p className="text-xs text-muted-foreground text-center py-4">{t("files.noVersions")}</p>
              )}
              {versions.map((v, i) => (
                <div
                  key={v.id}
                  className={cn(
                    "rounded-md px-2 py-1.5 text-xs transition-colors",
                    compareVersionId === v.id
                      ? "bg-primary/10 ring-1 ring-primary/30"
                      : "hover:bg-muted",
                    i > 0 && "cursor-pointer"
                  )}
                  onClick={() => i > 0 && handleCompare(v)}
                >
                  <div className="flex items-center justify-between">
                    <span className="font-mono font-medium">
                      v{v.version_label}
                    </span>
                    {i === 0 && (
                      <span className="text-[10px] text-primary font-medium">{t("files.latest")}</span>
                    )}
                    {i > 0 && compareVersionId === v.id && (
                      <Button
                        size="sm"
                        variant="ghost"
                        className="h-5 text-[10px] px-1.5"
                        onClick={(e) => { e.stopPropagation(); handleRestore(v.id); }}
                        disabled={restoringId === v.id}
                      >
                        {restoringId === v.id ? "..." : t("files.restore")}
                      </Button>
                    )}
                  </div>
                  <div className="text-muted-foreground mt-0.5">
                    {v.updated_by_name || "—"}
                    {v.file_size != null && (
                      <span className="ml-1">· {(v.file_size / 1024).toFixed(1)}KB</span>
                    )}
                  </div>
                  {i > 0 && compareVersionId !== v.id && (
                    <div className="text-[10px] text-muted-foreground/60 mt-0.5">
                      {t("files.clickToCompare")}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
