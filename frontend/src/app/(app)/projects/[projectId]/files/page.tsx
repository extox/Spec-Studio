"use client";

import { useEffect, useState } from "react";
import { useParams, useSearchParams } from "next/navigation";
import { useProjectStore } from "@/stores/projectStore";
import { FileTree } from "@/components/files/FileTree";
import { FileViewer } from "@/components/files/FileViewer";
import { FileUpload } from "@/components/files/FileUpload";
import { FileCreateDialog } from "@/components/files/FileCreateDialog";
import { Button } from "@/components/ui/button";
import api from "@/lib/api";
import { toast } from "sonner";
import type { FileTreeItem } from "@/types";
import { useI18n } from "@/lib/i18n";
import { cn } from "@/lib/utils";

export default function FilesPage() {
  const params = useParams();
  const searchParams = useSearchParams();
  const projectId = Number(params.projectId);
  const { files, fetchFiles } = useProjectStore();
  const [selectedFile, setSelectedFile] = useState<FileTreeItem | null>(null);
  const { t } = useI18n();
  const [panelCollapsed, setPanelCollapsed] = useState(false);

  useEffect(() => {
    fetchFiles(projectId);
  }, [projectId, fetchFiles]);

  // Auto-open the file when a deep link arrives via ?fileId=...
  useEffect(() => {
    const fid = Number(searchParams.get("fileId"));
    if (!fid || !files.length) return;
    if (selectedFile?.id === fid) return;
    const found = files.find((f) => f.id === fid);
    if (found) setSelectedFile(found);
  }, [searchParams, files, selectedFile?.id]);

  const refresh = () => fetchFiles(projectId);

  const handleDownloadAll = async () => {
    try {
      const res = await api.get(`/projects/${projectId}/files/download-all`, {
        responseType: "blob",
      });
      const url = URL.createObjectURL(res.data);
      const a = document.createElement("a");
      a.href = url;
      a.download = `project-${projectId}.zip`;
      a.click();
      URL.revokeObjectURL(url);
    } catch {
      toast.error(t("files.downloadFailed"));
    }
  };

  const handleDeleteFile = async (file: FileTreeItem) => {
    try {
      await api.delete(`/projects/${projectId}/files/${file.id}`);
      toast.success(t("files.deleted"));
      if (selectedFile?.id === file.id) setSelectedFile(null);
      refresh();
    } catch {
      toast.error(t("files.deleteFailed"));
    }
  };

  const handleDeleteDirectory = async (_dir: string, fileIds: number[]) => {
    try {
      await Promise.all(
        fileIds.map((id) => api.delete(`/projects/${projectId}/files/${id}`))
      );
      toast.success(t("files.dirDeleted"));
      if (selectedFile && fileIds.includes(selectedFile.id)) setSelectedFile(null);
      refresh();
    } catch {
      toast.error(t("files.deleteFailed"));
    }
  };

  const handleRenameFile = async (file: FileTreeItem, newName: string) => {
    const dir = file.file_path.includes("/")
      ? file.file_path.substring(0, file.file_path.lastIndexOf("/"))
      : null;
    const newPath = dir ? `${dir}/${newName}` : newName;
    try {
      await api.put(`/projects/${projectId}/files/${file.id}`, {
        file_name: newName,
        file_path: newPath,
      });
      toast.success(t("files.renamed"));
      refresh();
    } catch {
      toast.error(t("files.renameFailed"));
    }
  };

  const handleRenameDirectory = async (oldDir: string, newDir: string) => {
    try {
      await api.put(`/projects/${projectId}/files/rename-directory`, {
        old_dir: oldDir,
        new_dir: newDir,
      });
      toast.success(t("files.renamed"));
      refresh();
    } catch {
      toast.error(t("files.renameFailed"));
    }
  };

  const handleMoveFile = async (file: FileTreeItem, newDir: string) => {
    const newPath = newDir === "." ? file.file_name : `${newDir}/${file.file_name}`;
    try {
      await api.put(`/projects/${projectId}/files/${file.id}`, {
        file_path: newPath,
      });
      toast.success(t("files.moved"));
      refresh();
    } catch {
      toast.error(t("files.moveFailed"));
    }
  };

  const [loadingSamples, setLoadingSamples] = useState(false);
  const [sampleCatalog, setSampleCatalog] = useState<{ id: string; name: string; description: string; tech: string }[]>([]);

  useEffect(() => {
    if (files.length === 0) {
      api.get(`/projects/${projectId}/files/sample-catalog`).then((r) => setSampleCatalog(r.data)).catch(() => {});
    }
  }, [files.length, projectId]);

  const handleLoadSamples = async (sampleId: string) => {
    setLoadingSamples(true);
    try {
      await api.post(`/projects/${projectId}/files/load-samples`, { sample_id: sampleId });
      toast.success(t("files.samplesLoaded"));
      refresh();
    } catch {
      toast.error(t("files.samplesLoadFailed"));
    } finally {
      setLoadingSamples(false);
    }
  };

  return (
    <div className="flex h-full">
      <div className={cn(
        "border-r flex flex-col transition-all duration-200",
        panelCollapsed ? "w-12" : "w-64"
      )}>
        {panelCollapsed ? (
          <div className="flex-1 overflow-hidden py-2">
            {files.map((f) => (
              <button
                key={f.id}
                onClick={() => setSelectedFile(f)}
                className={cn(
                  "w-full px-1 py-1.5 hover:bg-muted transition-colors",
                  selectedFile?.id === f.id && "bg-primary/10"
                )}
                title={f.file_name}
              >
                <span className="text-[9px] text-muted-foreground leading-tight break-all line-clamp-2 block text-center">
                  {f.file_name.replace(/\.md$/, "")}
                </span>
              </button>
            ))}
          </div>
        ) : (
          <>
            <div className="flex items-center border-b p-3">
              <span className="text-sm font-medium">{t("nav.artifacts")}</span>
            </div>
            <div className="flex-1 overflow-auto p-2">
              <FileTree
                files={files}
                selectedId={selectedFile?.id}
                onSelect={setSelectedFile}
                onDeleteFile={handleDeleteFile}
                onDeleteDirectory={handleDeleteDirectory}
                onRenameFile={handleRenameFile}
                onRenameDirectory={handleRenameDirectory}
                onMoveFile={handleMoveFile}
              />
            </div>
            <div className="flex items-center gap-1 border-t p-2">
              <FileCreateDialog projectId={projectId} onCreated={refresh} />
              <FileUpload projectId={projectId} onUploaded={refresh} />
              <Button size="sm" variant="outline" onClick={handleDownloadAll}>
                {t("files.downloadAll")}
              </Button>
            </div>
          </>
        )}
        <button
          onClick={() => setPanelCollapsed(!panelCollapsed)}
          className="flex items-center justify-center h-8 border-t hover:bg-muted transition-colors opacity-40 hover:opacity-100"
          title={panelCollapsed ? t("nav.expand") : t("nav.collapse")}
        >
          <svg
            className={cn("h-3 w-3 text-muted-foreground transition-transform", panelCollapsed && "rotate-180")}
            fill="none" stroke="currentColor" viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 19l-7-7 7-7M18 19l-7-7 7-7" />
          </svg>
        </button>
      </div>
      <div className="flex-1">
        {selectedFile ? (
          <FileViewer projectId={projectId} fileId={selectedFile.id} onSaved={refresh} />
        ) : files.length === 0 ? (
          <div className="flex h-full flex-col items-center justify-center p-8">
            <svg className="h-12 w-12 opacity-20 text-muted-foreground mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            <p className="text-sm text-muted-foreground mb-2">{t("files.noFiles")}</p>
            <p className="text-xs text-muted-foreground/70 mb-6 text-center max-w-md">
              {t("files.loadSamplesDesc")}
            </p>
            <div className="grid gap-3 w-full max-w-lg">
              {sampleCatalog.map((sample) => (
                <button
                  key={sample.id}
                  onClick={() => handleLoadSamples(sample.id)}
                  disabled={loadingSamples}
                  className="text-left p-4 rounded-lg border border-dashed hover:border-primary/40 hover:bg-primary/5 transition-colors disabled:opacity-50"
                >
                  <p className="text-sm font-medium">{sample.name}</p>
                  <p className="text-xs text-muted-foreground mt-1">{sample.description}</p>
                  <p className="text-[10px] text-primary/70 mt-1.5">{sample.tech}</p>
                </button>
              ))}
            </div>
          </div>
        ) : (
          <div className="flex h-full items-center justify-center text-muted-foreground">
            {t("files.selectFile")}
          </div>
        )}
      </div>
    </div>
  );
}
