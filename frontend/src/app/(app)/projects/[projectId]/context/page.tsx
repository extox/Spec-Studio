"use client";

import { useEffect, useState, useCallback } from "react";
import { useParams } from "next/navigation";
import { useContextStore } from "@/stores/contextStore";
import { Button } from "@/components/ui/button";
import api from "@/lib/api";
import { toast } from "sonner";
import type { FileTreeItem, ProjectFile, ContextCategory, FileVersion } from "@/types";
import { useI18n } from "@/lib/i18n";
import { cn } from "@/lib/utils";
import dynamic from "next/dynamic";
import YamlEditor from "@/components/context/YamlEditor";
const SystemDrawingCanvas = dynamic(() => import("@/components/context/SystemDrawingCanvas"), { ssr: false });

// Category icon map
const categoryIcons: Record<string, string> = {
  "system-architecture": "\uD83C\uDFD7\uFE0F",
  "legacy-system": "\uD83C\uDFD7\uFE0F",
  "architecture": "\uD83C\uDFD7\uFE0F",
};

// Categories that support canvas view
const CANVAS_CATEGORIES = ["system-architecture", "legacy-system", "architecture"];

function getCategoryFromPath(filePath: string): string {
  const parts = filePath.split("/");
  return parts.length >= 2 ? parts[1] : "custom";
}

// Category display order
const CATEGORY_ORDER: Record<string, number> = {
  "system-architecture": 1,
  "legacy-system": 2,
  "architecture": 3,
};

export default function ContextPage() {
  const params = useParams();
  const projectId = Number(params.projectId);
  const { contextFiles, categories, isLoading, fetchContextFiles, fetchCategories } = useContextStore();
  const [selectedFile, setSelectedFile] = useState<FileTreeItem | null>(null);
  const [fileContent, setFileContent] = useState<string>("");
  const [originalContent, setOriginalContent] = useState<string>("");
  const [isSaving, setIsSaving] = useState(false);
  const [isCreating, setIsCreating] = useState(false);
  const [showCreateDialog, setShowCreateDialog] = useState(false);
  const [newCategory, setNewCategory] = useState("");
  const [newFileName, setNewFileName] = useState("");
  const [yamlValid, setYamlValid] = useState<boolean | null>(null);
  const [yamlErrors, setYamlErrors] = useState<string[]>([]);
  const [panelCollapsed, setPanelCollapsed] = useState(false);
  const [viewMode, setViewMode] = useState<"yaml" | "canvas">("canvas");
  // Version management
  const [showVersionPanel, setShowVersionPanel] = useState(false);
  const [versions, setVersions] = useState<FileVersion[]>([]);
  const [isLoadingVersions, setIsLoadingVersions] = useState(false);
  const [diffContent, setDiffContent] = useState<string | null>(null);
  const [diffLabel, setDiffLabel] = useState("");
  const { t } = useI18n();

  // AI Review state
  const [showReviewDialog, setShowReviewDialog] = useState(false);
  const [reviewStep, setReviewStep] = useState<"idle" | "reviewing" | "reviewed" | "generating" | "tobe-ready">("idle");
  const [reviewResult, setReviewResult] = useState("");
  const [tobeYaml, setTobeYaml] = useState("");
  const [tobeWarnings, setTobeWarnings] = useState<string[]>([]);
  const [tobeFileName, setTobeFileName] = useState("");
  const [reviewInstruction, setReviewInstruction] = useState("");
  const [isSavingTobe, setIsSavingTobe] = useState(false);

  // AI Import state
  const [showImportDialog, setShowImportDialog] = useState(false);
  const [importStep, setImportStep] = useState<"upload" | "processing" | "preview">("upload");
  const [importCategory, setImportCategory] = useState("");
  const [importInstruction, setImportInstruction] = useState("");
  const [importFile, setImportFile] = useState<File | null>(null);
  const [importExtractedText, setImportExtractedText] = useState("");
  const [importYaml, setImportYaml] = useState("");
  const [importFileName, setImportFileName] = useState("");
  const [importWarnings, setImportWarnings] = useState<string[]>([]);
  const [isImporting, setIsImporting] = useState(false);
  const [isSavingImport, setIsSavingImport] = useState(false);

  useEffect(() => {
    fetchContextFiles(projectId);
    fetchCategories(projectId);
  }, [projectId, fetchContextFiles, fetchCategories]);

  // Load file content when selected
  useEffect(() => {
    if (!selectedFile) return;
    api.get<ProjectFile>(`/projects/${projectId}/context/${selectedFile.id}`).then((res) => {
      setFileContent(res.data.content || "");
      setOriginalContent(res.data.content || "");
      setYamlValid(null);
      setYamlErrors([]);
      setViewMode("canvas");
      setShowVersionPanel(false);
      setVersions([]);
      setDiffContent(null);
    }).catch(() => {
      toast.error("Failed to load file");
    });
  }, [selectedFile, projectId]);

  const hasChanges = fileContent !== originalContent;
  const canShowCanvas = selectedFile && CANVAS_CATEGORIES.includes(getCategoryFromPath(selectedFile.file_path));

  // Group files by category
  const grouped = contextFiles.reduce<Record<string, FileTreeItem[]>>((acc, f) => {
    const cat = getCategoryFromPath(f.file_path);
    (acc[cat] ||= []).push(f);
    return acc;
  }, {});

  const handleSave = async () => {
    if (!selectedFile) return;
    setIsSaving(true);
    try {
      await useContextStore.getState().updateContextFile(projectId, selectedFile.id, fileContent);
      setOriginalContent(fileContent);
      toast.success(t("contextMgmt.saved"));
      // Auto-show version panel after save
      handleLoadVersions();
    } catch (e: any) {
      const detail = e?.response?.data?.detail;
      if (detail?.errors) {
        toast.error(detail.errors.join(", "));
      } else {
        toast.error(t("contextMgmt.saveFailed"));
      }
    } finally {
      setIsSaving(false);
    }
  };

  const handleLoadVersions = async () => {
    if (!selectedFile) return;
    setIsLoadingVersions(true);
    try {
      const res = await api.get<FileVersion[]>(`/projects/${projectId}/files/${selectedFile.id}/versions`);
      setVersions(res.data);
      setShowVersionPanel(true);
    } catch {
      toast.error(t("files.compareFailed"));
    } finally {
      setIsLoadingVersions(false);
    }
  };

  const handleViewVersion = async (versionId: number, label: string) => {
    if (!selectedFile) return;
    try {
      const res = await api.get<{ content: string; version_label: string }>(`/projects/${projectId}/files/${selectedFile.id}/versions/${versionId}`);
      setDiffContent(res.data.content);
      setDiffLabel(label);
      setViewMode("yaml"); // Show in YAML mode to compare
    } catch {
      toast.error(t("files.compareFailed"));
    }
  };

  const handleRestoreVersion = async (versionId: number) => {
    if (!selectedFile) return;
    try {
      await api.post(`/projects/${projectId}/files/${selectedFile.id}/versions/${versionId}/restore`);
      toast.success(t("files.versionRestored"));
      // Reload file content
      const res = await api.get<ProjectFile>(`/projects/${projectId}/context/${selectedFile.id}`);
      setFileContent(res.data.content || "");
      setOriginalContent(res.data.content || "");
      setDiffContent(null);
      handleLoadVersions(); // Refresh version list
    } catch {
      toast.error(t("files.restoreFailed"));
    }
  };

  const handleStartReview = async () => {
    if (!fileContent.trim()) return;
    setShowReviewDialog(true);
    setReviewStep("reviewing");
    setReviewResult("");
    setTobeYaml("");
    setTobeWarnings([]);
    setTobeFileName(selectedFile ? `to-be-${selectedFile.file_name.replace(/\.ya?ml$/, "")}` : "to-be-architecture");
    try {
      const res = await api.post<{ review: string }>(
        `/projects/${projectId}/context/review-architecture`,
        { yaml_content: fileContent, custom_instruction: reviewInstruction },
        { timeout: 180000 }
      );
      setReviewResult(res.data.review);
      setReviewStep("reviewed");
    } catch (e: any) {
      const detail = e?.response?.data?.detail;
      toast.error(typeof detail === "string" ? detail : t("contextMgmt.reviewFailed"));
      setReviewStep("idle");
      setShowReviewDialog(false);
    }
  };

  const handleGenerateTobe = async () => {
    if (!reviewResult) return;
    setReviewStep("generating");
    try {
      const res = await api.post<{ tobe_yaml: string; warnings: string[] }>(
        `/projects/${projectId}/context/generate-tobe`,
        { asis_yaml: fileContent, review_result: reviewResult, custom_instruction: reviewInstruction },
        { timeout: 180000 }
      );
      setTobeYaml(res.data.tobe_yaml);
      setTobeWarnings(res.data.warnings);
      setReviewStep("tobe-ready");
    } catch (e: any) {
      const detail = e?.response?.data?.detail;
      toast.error(typeof detail === "string" ? detail : t("contextMgmt.tobeFailed"));
      setReviewStep("reviewed");
    }
  };

  const handleSaveTobe = async () => {
    if (!tobeYaml || !tobeFileName) return;
    setIsSavingTobe(true);
    try {
      await api.post(`/projects/${projectId}/context/save-tobe`, {
        content: tobeYaml,
        file_name: tobeFileName,
        source_file: selectedFile?.file_name || "",
      });
      toast.success(t("contextMgmt.tobeSaved"));
      setShowReviewDialog(false);
      setReviewStep("idle");
      fetchContextFiles(projectId);
    } catch (e: any) {
      const detail = e?.response?.data?.detail;
      if (detail?.errors) toast.error(detail.errors.join(", "));
      else toast.error(t("contextMgmt.saveFailed"));
    } finally {
      setIsSavingTobe(false);
    }
  };

  const handleCreate = async () => {
    if (!newCategory) return;
    setIsCreating(true);
    // Auto-generate file name if not provided
    const fileName = newFileName.trim() || `${newCategory}-${Date.now()}`;
    try {
      // Get template
      const templateRes = await api.get<{ content: string }>(`/projects/${projectId}/context/templates/${newCategory}`);
      const f = await useContextStore.getState().createContextFile(
        projectId, newCategory, fileName, templateRes.data.content
      );
      setShowCreateDialog(false);
      setNewCategory("");
      setNewFileName("");
      toast.success(t("contextMgmt.created"));
      // Select the new file
      const refreshed = useContextStore.getState().contextFiles;
      const created = refreshed.find((cf) => cf.id === f.id);
      if (created) setSelectedFile(created);
    } catch (e: any) {
      const detail = e?.response?.data?.detail;
      if (typeof detail === "string") {
        toast.error(detail);
      } else {
        toast.error(t("contextMgmt.createFailed"));
      }
    } finally {
      setIsCreating(false);
    }
  };

  const handleDelete = async (file: FileTreeItem) => {
    if (!confirm(t("contextMgmt.deleteConfirm"))) return;
    try {
      await useContextStore.getState().deleteContextFile(projectId, file.id);
      if (selectedFile?.id === file.id) {
        setSelectedFile(null);
        setFileContent("");
        setOriginalContent("");
      }
      toast.success(t("contextMgmt.deleted"));
    } catch {
      toast.error(t("contextMgmt.deleteFailed"));
    }
  };

  const handleValidate = async () => {
    if (!selectedFile) return;
    const category = getCategoryFromPath(selectedFile.file_path);
    try {
      const res = await api.post<{ valid: boolean; errors: string[]; warnings: string[] }>(
        `/projects/${projectId}/context/validate`,
        { content: fileContent, category }
      );
      setYamlValid(res.data.valid);
      setYamlErrors([...res.data.errors, ...res.data.warnings]);
    } catch {
      setYamlValid(false);
      setYamlErrors(["Validation request failed"]);
    }
  };

  const handleUpload = async (category: string) => {
    const input = document.createElement("input");
    input.type = "file";
    input.accept = ".yaml,.yml";
    input.onchange = async (e) => {
      const file = (e.target as HTMLInputElement).files?.[0];
      if (!file) return;
      const formData = new FormData();
      formData.append("file", file);
      try {
        await api.post(`/projects/${projectId}/context/upload?category=${category}`, formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });
        toast.success(t("contextMgmt.created"));
        fetchContextFiles(projectId);
      } catch (e: any) {
        const detail = e?.response?.data?.detail;
        if (detail?.errors) {
          toast.error(detail.errors.join(", "));
        } else {
          toast.error(t("contextMgmt.createFailed"));
        }
      }
    };
    input.click();
  };

  const handleImportAnalyze = async () => {
    if (!importFile || !importCategory) return;
    setImportStep("processing");
    setIsImporting(true);
    try {
      const formData = new FormData();
      formData.append("file", importFile);
      const res = await api.post<{
        extracted_text: string;
        structured_yaml: string;
        category: string;
        file_name: string;
        warnings: string[];
      }>(
        `/projects/${projectId}/context/import-document?category=${importCategory}&custom_instruction=${encodeURIComponent(importInstruction)}`,
        formData,
        { headers: { "Content-Type": "multipart/form-data" }, timeout: 120000 }
      );
      setImportExtractedText(res.data.extracted_text);
      setImportYaml(res.data.structured_yaml);
      setImportFileName(res.data.file_name);
      setImportWarnings(res.data.warnings);
      setImportStep("preview");
    } catch (e: any) {
      const detail = e?.response?.data?.detail;
      toast.error(typeof detail === "string" ? detail : t("contextMgmt.importFailed"));
      setImportStep("upload");
    } finally {
      setIsImporting(false);
    }
  };

  const handleImportSave = async () => {
    if (!importYaml || !importFileName || !importCategory) return;
    setIsSavingImport(true);
    try {
      const f = await api.post<ProjectFile>(`/projects/${projectId}/context/import-save`, {
        category: importCategory,
        file_name: importFileName,
        content: importYaml,
      });
      toast.success(t("contextMgmt.importSaved"));
      setShowImportDialog(false);
      resetImportState();
      fetchContextFiles(projectId);
      // Select the new file
      const refreshed = useContextStore.getState().contextFiles;
      const created = refreshed.find((cf) => cf.id === f.data.id);
      if (created) setSelectedFile(created);
    } catch (e: any) {
      const detail = e?.response?.data?.detail;
      if (detail?.errors) {
        toast.error(detail.errors.join(", "));
      } else {
        toast.error(t("contextMgmt.saveFailed"));
      }
    } finally {
      setIsSavingImport(false);
    }
  };

  const resetImportState = () => {
    setImportStep("upload");
    setImportCategory("");
    setImportInstruction("");
    setImportFile(null);
    setImportExtractedText("");
    setImportYaml("");
    setImportFileName("");
    setImportWarnings([]);
  };

  return (
    <div className="flex h-full">
      {/* Left panel — file list */}
      <div className={cn(
        "border-r flex flex-col transition-all duration-200",
        panelCollapsed ? "w-12" : "w-72"
      )}>
        {panelCollapsed ? (
          <div className="flex-1 overflow-hidden py-2">
            {contextFiles.map((f) => (
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
                  {f.file_name.replace(/\.ya?ml$/, "")}
                </span>
              </button>
            ))}
          </div>
        ) : (
          <>
            <div className="flex items-center justify-between border-b p-3">
              <span className="text-sm font-medium">{t("contextMgmt.title")}</span>
              <span className="text-[10px] text-muted-foreground">
                {t("contextMgmt.filesCount", { count: String(contextFiles.length) })}
              </span>
            </div>
            <div className="flex-1 overflow-auto">
              {Object.keys(CATEGORY_ORDER).map((cat) => {
                const files = grouped[cat];
                if (!files?.length) return null;
                const catInfo = categories.find((c) => c.id === cat);
                return (
                  <div key={cat} className="border-b last:border-b-0">
                    <div className="flex items-center gap-2 px-3 py-2 bg-muted/30">
                      <span className="text-sm">{categoryIcons[cat] || "\uD83D\uDCCE"}</span>
                      <span className="text-xs font-medium text-muted-foreground">{catInfo?.name || cat}</span>
                      <span className="text-[10px] text-muted-foreground ml-auto">{files.length}</span>
                    </div>
                    {files.map((f) => (
                      <div
                        key={f.id}
                        className={cn(
                          "flex items-start gap-2 px-3 py-2 cursor-pointer transition-colors group",
                          selectedFile?.id === f.id
                            ? "bg-primary/10 text-primary"
                            : "hover:bg-muted/50 text-foreground"
                        )}
                        onClick={() => setSelectedFile(f)}
                      >
                        <div className="flex-1 min-w-0">
                          <div className="text-xs truncate">{f.file_name}</div>
                          <div className="flex items-center gap-1.5 mt-0.5">
                            {f.version_label && (
                              <span className="text-[9px] font-mono text-muted-foreground">v{f.version_label}</span>
                            )}
                            {f.updated_by_name && (
                              <span className="text-[9px] text-muted-foreground">{f.updated_by_name}</span>
                            )}
                          </div>
                        </div>
                        <button
                          onClick={(e) => { e.stopPropagation(); handleDelete(f); }}
                          className="opacity-0 group-hover:opacity-100 text-destructive hover:text-destructive/80 transition-opacity mt-0.5"
                          title={t("common.delete")}
                        >
                          <svg className="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                          </svg>
                        </button>
                      </div>
                    ))}
                  </div>
                );
              })}
              {contextFiles.length === 0 && !isLoading && (
                <div className="flex flex-col items-center justify-center p-6 text-center">
                  <svg className="h-8 w-8 opacity-20 text-muted-foreground mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />
                  </svg>
                  <p className="text-xs text-muted-foreground">{t("contextMgmt.noFiles")}</p>
                </div>
              )}
            </div>
            <div className="flex flex-col gap-1 border-t p-2">
              <Button size="sm" variant="outline" onClick={() => setShowCreateDialog(true)} className="w-full text-xs">
                <svg className="h-3 w-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" /></svg>
                {t("contextMgmt.newModel")}
              </Button>
              <Button
                size="sm"
                variant="outline"
                onClick={() => { resetImportState(); setShowImportDialog(true); }}
                className="w-full text-xs border-blue-200 text-blue-600 hover:bg-blue-50 hover:text-blue-700"
              >
                <svg className="h-3.5 w-3.5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
                {t("contextMgmt.importDoc")}
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

      {/* Right panel — editor or empty state */}
      <div className="flex-1 flex flex-col">
        {selectedFile ? (
          <>
            {/* Toolbar */}
            <div className="flex items-center justify-between border-b px-4 py-2">
              <div className="flex items-center gap-2">
                <span className="text-sm">{categoryIcons[getCategoryFromPath(selectedFile.file_path)] || "\uD83D\uDCCE"}</span>
                <span className="text-sm font-medium">{selectedFile.file_name}</span>
                {hasChanges && (
                  <span className="text-[10px] px-1.5 py-0.5 rounded bg-amber-100 text-amber-700">{t("contextMgmt.modified")}</span>
                )}
              </div>
              <div className="flex items-center gap-2">
                {/* Canvas/YAML toggle */}
                {canShowCanvas && (
                  <div className="flex items-center border rounded-md overflow-hidden">
                    <button
                      onClick={() => setViewMode("canvas")}
                      className={cn(
                        "px-2.5 py-1 text-[10px] font-medium transition-colors",
                        viewMode === "canvas" ? "bg-primary text-primary-foreground" : "hover:bg-muted"
                      )}
                    >
                      Canvas
                    </button>
                    <button
                      onClick={() => setViewMode("yaml")}
                      className={cn(
                        "px-2.5 py-1 text-[10px] font-medium transition-colors",
                        viewMode === "yaml" ? "bg-primary text-primary-foreground" : "hover:bg-muted"
                      )}
                    >
                      YAML
                    </button>
                  </div>
                )}
                {yamlValid !== null && (
                  <span className={cn(
                    "text-[10px] px-1.5 py-0.5 rounded",
                    yamlValid ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"
                  )}>
                    {yamlValid ? t("contextMgmt.validYaml") : t("contextMgmt.invalidYaml")}
                  </span>
                )}
                {canShowCanvas && (
                  <Button size="sm" variant="outline" onClick={() => { setReviewInstruction(""); setShowReviewDialog(true); setReviewStep("idle"); }} className="text-xs h-7 border-violet-200 text-violet-600 hover:bg-violet-50 hover:text-violet-700">
                    <svg className="h-3 w-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" /></svg>
                    {t("contextMgmt.aiReview")}
                  </Button>
                )}
                <Button size="sm" variant="outline" onClick={handleLoadVersions} disabled={isLoadingVersions} className="text-xs h-7">
                  <svg className="h-3 w-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                  {t("files.versions")}
                </Button>
                <Button size="sm" variant="outline" onClick={handleValidate} className="text-xs h-7">
                  {t("contextMgmt.validate")}
                </Button>
                <Button size="sm" onClick={handleSave} disabled={!hasChanges || isSaving} className="text-xs h-7">
                  {isSaving ? "..." : t("common.save")}
                </Button>
              </div>
            </div>
            {/* Validation errors/warnings */}
            {yamlErrors.length > 0 && (
              <div className={cn(
                "px-4 py-2 text-xs border-b",
                yamlValid ? "bg-amber-50 text-amber-700" : "bg-red-50 text-red-700"
              )}>
                {yamlErrors.map((err, i) => (
                  <div key={i}>{err}</div>
                ))}
              </div>
            )}
            {/* Editor + Version panel */}
            <div className="flex-1 flex overflow-hidden">
              {/* Editor area */}
              <div className={cn("flex-1 overflow-hidden", diffContent ? "border-r" : "")}>
                {diffContent ? (
                  /* Diff view: current vs version side by side */
                  <div className="flex h-full">
                    <div className="flex-1 flex flex-col border-r">
                      <div className="px-3 py-1.5 bg-muted/50 border-b text-[10px] font-medium flex items-center justify-between">
                        <span>{t("contextMgmt.currentVersion")}</span>
                      </div>
                      <YamlEditor value={fileContent} readOnly className="flex-1" />
                    </div>
                    <div className="flex-1 flex flex-col">
                      <div className="px-3 py-1.5 bg-amber-50 border-b text-[10px] font-medium flex items-center justify-between">
                        <span>{diffLabel}</span>
                        <button onClick={() => setDiffContent(null)} className="text-muted-foreground hover:text-foreground">
                          <svg className="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>
                        </button>
                      </div>
                      <YamlEditor value={diffContent || ""} readOnly className="flex-1 bg-amber-50/30" />
                    </div>
                  </div>
                ) : viewMode === "canvas" && canShowCanvas ? (
                  <SystemDrawingCanvas
                    yamlContent={fileContent}
                    onYamlChange={(newYaml) => setFileContent(newYaml)}
                  />
                ) : (
                  <YamlEditor
                    value={fileContent}
                    onChange={(v) => setFileContent(v)}
                    placeholder="YAML content..."
                    className="h-full"
                  />
                )}
              </div>

              {/* Version history panel */}
              {showVersionPanel && (
                <div className="w-56 border-l overflow-auto bg-background flex flex-col">
                  <div className="flex items-center justify-between px-3 py-1.5 border-b">
                    <span className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider">{t("files.versionHistory")}</span>
                    <button onClick={() => { setShowVersionPanel(false); setDiffContent(null); }} className="text-muted-foreground hover:text-foreground">
                      <svg className="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>
                    </button>
                  </div>
                  <div className="flex-1 overflow-auto">
                    {versions.length === 0 ? (
                      <div className="p-3 text-xs text-muted-foreground text-center">{t("files.noVersions")}</div>
                    ) : (
                      versions.map((v, i) => (
                        <div key={v.id} className="border-b last:border-b-0 px-3 py-2 hover:bg-muted/50 transition-colors">
                          <div className="flex items-center justify-between">
                            <span className="text-xs font-mono font-medium">{v.version_label}</span>
                            {i === 0 && <span className="text-[9px] px-1 py-0.5 rounded bg-primary/10 text-primary">{t("files.latest")}</span>}
                          </div>
                          {v.updated_by_name && (
                            <div className="text-[10px] text-muted-foreground mt-0.5">{v.updated_by_name}</div>
                          )}
                          <div className="text-[10px] text-muted-foreground">
                            {new Date(v.created_at).toLocaleString("ko-KR", { timeZone: "Asia/Seoul", month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" })}
                            {v.file_size != null && <span className="ml-1">({(v.file_size / 1024).toFixed(1)}KB)</span>}
                          </div>
                          <div className="flex gap-1 mt-1">
                            <button
                              onClick={() => handleViewVersion(v.id, v.version_label)}
                              className="text-[10px] text-primary hover:underline"
                            >
                              {t("contextMgmt.compare")}
                            </button>
                            {i > 0 && (
                              <button
                                onClick={() => { if (confirm(t("contextMgmt.versionRestoreConfirm", { version: v.version_label }))) handleRestoreVersion(v.id); }}
                                className="text-[10px] text-amber-600 hover:underline"
                              >
                                {t("files.restore")}
                              </button>
                            )}
                          </div>
                        </div>
                      ))
                    )}
                  </div>
                </div>
              )}
            </div>
          </>
        ) : (
          <div className="flex h-full flex-col items-center justify-center p-8">
            {contextFiles.length === 0 ? (
              <div className="text-center max-w-sm">
                <div className="h-16 w-16 rounded-2xl bg-gradient-to-br from-primary/10 to-primary/5 flex items-center justify-center mx-auto mb-4">
                  <svg className="h-8 w-8 text-primary/40" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                  </svg>
                </div>
                <p className="text-sm font-medium mb-1">{t("contextMgmt.emptyTitle")}</p>
                <p className="text-xs text-muted-foreground mb-5">{t("contextMgmt.emptyDesc")}</p>
                <Button onClick={() => setShowCreateDialog(true)}>
                  <svg className="h-4 w-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" /></svg>
                  {t("contextMgmt.emptyAction")}
                </Button>
              </div>
            ) : (
              <div className="text-center">
                <svg className="h-10 w-10 opacity-15 text-muted-foreground mx-auto mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122" />
                </svg>
                <p className="text-sm text-muted-foreground">{t("contextMgmt.selectFile")}</p>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Create dialog (modal) */}
      {showCreateDialog && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50" onClick={() => setShowCreateDialog(false)}>
          <div className="bg-background rounded-2xl shadow-2xl w-full max-w-md overflow-hidden" onClick={(e) => e.stopPropagation()}>
            {/* Header with gradient */}
            <div className="bg-gradient-to-br from-primary/10 via-primary/5 to-transparent px-6 pt-6 pb-4">
              <div className="flex items-center gap-3 mb-2">
                <div className="h-10 w-10 rounded-xl bg-primary/10 flex items-center justify-center">
                  <svg className="h-5 w-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                  </svg>
                </div>
                <div>
                  <h3 className="text-lg font-bold">{t("contextMgmt.modelingTitle")}</h3>
                  <p className="text-xs text-muted-foreground">{t("contextMgmt.modelingDesc")}</p>
                </div>
              </div>
            </div>

            <div className="px-6 pb-6">
              {/* File name */}
              <div className="mb-5">
                <label className="text-sm font-medium mb-1.5 block">{t("contextMgmt.modelName")} <span className="text-muted-foreground font-normal text-xs">{t("contextMgmt.modelNameOptional")}</span></label>
                <input
                  type="text"
                  value={newFileName}
                  onChange={(e) => setNewFileName(e.target.value)}
                  placeholder={t("contextMgmt.modelNamePlaceholder")}
                  className="w-full px-3.5 py-2.5 border rounded-lg text-sm bg-background focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary transition-all"
                  autoFocus
                  onKeyDown={(e) => { if (e.key === "Enter") { setNewCategory("system-architecture"); setTimeout(handleCreate, 0); } }}
                />
                <p className="text-[10px] text-muted-foreground mt-1.5">
                  {newFileName ? `context/system-architecture/${newFileName}.yaml` : t("contextMgmt.modelNameAuto")}
                </p>
              </div>

              {/* Features preview */}
              <div className="grid grid-cols-3 gap-2 mb-5">
                {[
                  { icon: "🎨", label: t("contextMgmt.featureCanvas") },
                  { icon: "🔲", label: t("contextMgmt.featureBoundary") },
                  { icon: "🔗", label: t("contextMgmt.featureConnection") },
                ].map((f) => (
                  <div key={f.label} className="flex flex-col items-center gap-1 p-2 rounded-lg bg-muted/30 text-center">
                    <span className="text-base">{f.icon}</span>
                    <span className="text-[10px] text-muted-foreground">{f.label}</span>
                  </div>
                ))}
              </div>

              {/* Actions */}
              <div className="flex gap-2">
                <Button variant="outline" className="flex-1" onClick={() => setShowCreateDialog(false)}>
                  {t("common.cancel")}
                </Button>
                <Button
                  className="flex-1"
                  onClick={() => { setNewCategory("system-architecture"); setTimeout(handleCreate, 0); }}
                  disabled={isCreating}
                >
                  {isCreating ? t("contextMgmt.creating") : t("contextMgmt.startModeling")}
                </Button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* AI Import dialog */}
      {showImportDialog && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50" onClick={() => { if (importStep !== "processing") { setShowImportDialog(false); resetImportState(); } }}>
          <div
            className={cn(
              "bg-background rounded-lg shadow-lg p-6 max-h-[90vh] overflow-auto",
              importStep === "preview" ? "w-full max-w-5xl" : "w-full max-w-lg"
            )}
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold flex items-center gap-2">
                <svg className="h-5 w-5 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
                {t("contextMgmt.importDoc")}
              </h3>
              {importStep !== "processing" && (
                <button onClick={() => { setShowImportDialog(false); resetImportState(); }} className="text-muted-foreground hover:text-foreground">
                  <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              )}
            </div>

            {/* Step 1: Upload */}
            {importStep === "upload" && (
              <div className="space-y-4">
                <p className="text-sm text-muted-foreground">{t("contextMgmt.importDocDesc")}</p>

                {/* Category */}
                <div>
                  <label className="text-sm font-medium mb-2 block">{t("contextMgmt.selectCategory")}</label>
                  <div className="grid grid-cols-3 gap-2">
                    {categories.map((cat) => (
                      <button
                        key={cat.id}
                        onClick={() => setImportCategory(cat.id)}
                        className={cn(
                          "flex flex-col items-center gap-1 p-2.5 rounded-lg border text-center transition-colors",
                          importCategory === cat.id
                            ? "border-primary bg-primary/5"
                            : "border-border hover:border-primary/40 hover:bg-muted/50"
                        )}
                      >
                        <span className="text-base">{categoryIcons[cat.id] || "\uD83D\uDCCE"}</span>
                        <span className="text-[10px] font-medium leading-tight">{cat.name}</span>
                      </button>
                    ))}
                  </div>
                </div>

                {/* File */}
                {importCategory && (
                  <div>
                    <label className="text-sm font-medium mb-1 block">{t("contextMgmt.importSelectFile")}</label>
                    <div
                      className={cn(
                        "border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors",
                        importFile ? "border-primary/40 bg-primary/5" : "border-border hover:border-primary/30"
                      )}
                      onClick={() => {
                        const input = document.createElement("input");
                        input.type = "file";
                        input.accept = ".pdf,.docx,.txt,.md,.csv,.sql,.ddl,.yaml,.yml,.json,.xml,.html,.log,.tsv";
                        input.onchange = (e) => {
                          const f = (e.target as HTMLInputElement).files?.[0];
                          if (f) setImportFile(f);
                        };
                        input.click();
                      }}
                    >
                      {importFile ? (
                        <div className="flex items-center justify-center gap-2">
                          <svg className="h-5 w-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                          </svg>
                          <span className="text-sm font-medium">{importFile.name}</span>
                          <span className="text-xs text-muted-foreground">({(importFile.size / 1024).toFixed(1)} KB)</span>
                        </div>
                      ) : (
                        <>
                          <svg className="h-8 w-8 mx-auto text-muted-foreground/50 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                          </svg>
                          <p className="text-sm text-muted-foreground">{t("contextMgmt.importSelectFile")}</p>
                          <p className="text-[10px] text-muted-foreground/70 mt-1">{t("contextMgmt.importSupportedFormats")}</p>
                        </>
                      )}
                    </div>
                  </div>
                )}

                {/* Custom instruction */}
                {importFile && (
                  <div>
                    <label className="text-sm font-medium mb-1 block">{t("contextMgmt.importCustomInstruction")}</label>
                    <textarea
                      value={importInstruction}
                      onChange={(e) => setImportInstruction(e.target.value)}
                      placeholder={t("contextMgmt.importCustomInstructionPlaceholder")}
                      className="w-full px-3 py-2 border rounded-md text-sm bg-background resize-none focus:outline-none focus:ring-1 focus:ring-primary"
                      rows={2}
                    />
                  </div>
                )}

                {/* Action */}
                <div className="flex justify-end gap-2 pt-2">
                  <Button variant="outline" size="sm" onClick={() => { setShowImportDialog(false); resetImportState(); }}>
                    {t("common.cancel")}
                  </Button>
                  <Button
                    size="sm"
                    onClick={handleImportAnalyze}
                    disabled={!importFile || !importCategory}
                    className="bg-blue-600 hover:bg-blue-700"
                  >
                    {t("contextMgmt.importDoc")}
                  </Button>
                </div>
              </div>
            )}

            {/* Step 2: Processing */}
            {importStep === "processing" && (
              <div className="flex flex-col items-center justify-center py-12">
                <div className="h-10 w-10 border-2 border-blue-500 border-t-transparent rounded-full animate-spin mb-4" />
                <p className="text-sm text-muted-foreground">{t("contextMgmt.importAnalyzing")}</p>
                <p className="text-[10px] text-muted-foreground/60 mt-1">{importFile?.name}</p>
              </div>
            )}

            {/* Step 3: Preview */}
            {importStep === "preview" && (
              <div className="space-y-4">
                {/* Warnings */}
                {importWarnings.length > 0 && (
                  <div className="bg-amber-50 border border-amber-200 rounded-lg px-3 py-2">
                    {importWarnings.map((w, i) => (
                      <p key={i} className="text-xs text-amber-700">{w}</p>
                    ))}
                  </div>
                )}

                {/* Two-panel preview */}
                <div className="grid grid-cols-2 gap-4" style={{ height: "50vh" }}>
                  {/* Left: extracted text */}
                  <div className="flex flex-col border rounded-lg overflow-hidden">
                    <div className="px-3 py-2 bg-muted/50 border-b text-xs font-medium">
                      {t("contextMgmt.importExtractedText")}
                    </div>
                    <div className="flex-1 overflow-auto p-3">
                      <pre className="text-xs text-muted-foreground whitespace-pre-wrap font-mono">{importExtractedText}</pre>
                    </div>
                  </div>

                  {/* Right: structured YAML (editable) */}
                  <div className="flex flex-col border rounded-lg overflow-hidden">
                    <div className="px-3 py-2 bg-muted/50 border-b text-xs font-medium">
                      {t("contextMgmt.importStructuredYaml")}
                    </div>
                    <YamlEditor
                      value={importYaml}
                      onChange={(v) => setImportYaml(v)}
                      className="flex-1"
                    />
                  </div>
                </div>

                {/* File name + actions */}
                <div className="flex items-center gap-3">
                  <div className="flex-1">
                    <label className="text-xs font-medium mb-1 block">{t("contextMgmt.importFileName")}</label>
                    <input
                      type="text"
                      value={importFileName}
                      onChange={(e) => setImportFileName(e.target.value)}
                      className="w-full px-3 py-1.5 border rounded-md text-sm bg-background focus:outline-none focus:ring-1 focus:ring-primary"
                    />
                    <p className="text-[10px] text-muted-foreground mt-0.5">
                      context/{importCategory}/{importFileName || "..."}.yaml
                    </p>
                  </div>
                  <div className="flex gap-2 pt-4">
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => { resetImportState(); setShowImportDialog(true); }}
                    >
                      {t("contextMgmt.importNewFile")}
                    </Button>
                    <Button
                      size="sm"
                      onClick={handleImportSave}
                      disabled={!importYaml || !importFileName || isSavingImport}
                      className="bg-blue-600 hover:bg-blue-700"
                    >
                      {isSavingImport ? t("contextMgmt.importSaving") : t("contextMgmt.importSaveResult")}
                    </Button>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* AI Review dialog */}
      {showReviewDialog && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50" onClick={() => { if (reviewStep === "idle" || reviewStep === "reviewed" || reviewStep === "tobe-ready") { setShowReviewDialog(false); setReviewStep("idle"); } }}>
          <div
            className={cn("bg-background rounded-2xl shadow-2xl max-h-[90vh] overflow-auto", reviewStep === "idle" ? "w-full max-w-md" : "w-full max-w-5xl")}
            onClick={(e) => e.stopPropagation()}
          >
            {/* Header */}
            <div className="bg-gradient-to-br from-violet-50 to-violet-25 dark:from-violet-950/30 px-6 pt-5 pb-4 rounded-t-2xl">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <div className="h-10 w-10 rounded-xl bg-violet-100 dark:bg-violet-900 flex items-center justify-center">
                    <svg className="h-5 w-5 text-violet-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" /></svg>
                  </div>
                  <div>
                    <h3 className="text-lg font-bold">{t("contextMgmt.reviewTitle")}</h3>
                    <p className="text-xs text-muted-foreground">{t("contextMgmt.reviewDesc")}</p>
                  </div>
                </div>
                {reviewStep !== "reviewing" && reviewStep !== "generating" && (
                  <button onClick={() => { setShowReviewDialog(false); setReviewStep("idle"); }} className="text-muted-foreground hover:text-foreground">
                    <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>
                  </button>
                )}
              </div>
            </div>

            <div className="px-6 pb-6">
              {/* Step: idle — configure & start */}
              {reviewStep === "idle" && (
                <div className="space-y-4 pt-4">
                  <div className="grid grid-cols-5 gap-2">
                    {[
                      { icon: "🏗️", label: t("contextMgmt.perspectiveInfra") },
                      { icon: "☁️", label: t("contextMgmt.perspectiveCloud") },
                      { icon: "🛡️", label: t("contextMgmt.perspectiveSecurity") },
                      { icon: "🗄️", label: t("contextMgmt.perspectiveData") },
                      { icon: "⚙️", label: t("contextMgmt.perspectiveApp") },
                    ].map((p) => (
                      <div key={p.label} className="flex flex-col items-center gap-1 p-2 rounded-lg bg-violet-50 dark:bg-violet-950/20 text-center">
                        <span className="text-lg">{p.icon}</span>
                        <span className="text-[10px] text-violet-700 dark:text-violet-300 font-medium">{p.label}</span>
                      </div>
                    ))}
                  </div>
                  <div>
                    <label className="text-sm font-medium mb-1 block">{t("contextMgmt.reviewInstruction")} <span className="text-muted-foreground text-xs font-normal">{t("contextMgmt.modelNameOptional")}</span></label>
                    <textarea
                      value={reviewInstruction}
                      onChange={(e) => setReviewInstruction(e.target.value)}
                      placeholder={t("contextMgmt.reviewInstructionPlaceholder")}
                      className="w-full px-3 py-2 border rounded-lg text-sm bg-background resize-none focus:outline-none focus:ring-2 focus:ring-violet-200"
                      rows={2}
                    />
                  </div>
                  <div className="flex gap-2">
                    <Button variant="outline" className="flex-1" onClick={() => setShowReviewDialog(false)}>{t("common.cancel")}</Button>
                    <Button className="flex-1 bg-violet-600 hover:bg-violet-700" onClick={handleStartReview} disabled={!fileContent.trim()}>
                      {t("contextMgmt.startReview")}
                    </Button>
                  </div>
                </div>
              )}

              {/* Step: reviewing */}
              {reviewStep === "reviewing" && (
                <div className="flex flex-col items-center justify-center py-16">
                  <div className="h-12 w-12 border-2 border-violet-500 border-t-transparent rounded-full animate-spin mb-4" />
                  <p className="text-sm font-medium">{t("contextMgmt.reviewing")}</p>
                  <p className="text-xs text-muted-foreground mt-1">{t("contextMgmt.reviewingDesc")}</p>
                </div>
              )}

              {/* Step: reviewed — show review + offer To-Be generation */}
              {(reviewStep === "reviewed" || reviewStep === "generating" || reviewStep === "tobe-ready") && (
                <div className="space-y-4 pt-4">
                  {/* Review result */}
                  <div className="border rounded-xl overflow-hidden">
                    <div className="px-4 py-2 bg-violet-50 dark:bg-violet-950/20 border-b flex items-center justify-between">
                      <span className="text-xs font-semibold text-violet-700">{t("contextMgmt.reviewResult")}</span>
                      {reviewStep === "reviewed" && (
                        <Button size="sm" className="text-xs h-7 bg-violet-600 hover:bg-violet-700" onClick={handleGenerateTobe}>
                          <svg className="h-3 w-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
                          {t("contextMgmt.generateTobe")}
                        </Button>
                      )}
                    </div>
                    <div className="p-4 max-h-[40vh] overflow-auto prose prose-sm prose-slate dark:prose-invert max-w-none">
                      <div className="text-xs leading-relaxed whitespace-pre-wrap">{reviewResult}</div>
                    </div>
                  </div>

                  {/* Generating spinner */}
                  {reviewStep === "generating" && (
                    <div className="flex items-center justify-center py-8 border rounded-xl">
                      <div className="h-8 w-8 border-2 border-violet-500 border-t-transparent rounded-full animate-spin mr-3" />
                      <div>
                        <p className="text-sm font-medium">{t("contextMgmt.generatingTobe")}</p>
                        <p className="text-xs text-muted-foreground">{t("contextMgmt.generatingTobeDesc")}</p>
                      </div>
                    </div>
                  )}

                  {/* To-Be result */}
                  {reviewStep === "tobe-ready" && (
                    <>
                      {tobeWarnings.length > 0 && (
                        <div className="bg-amber-50 border border-amber-200 rounded-lg px-3 py-2">
                          {tobeWarnings.map((w, i) => <p key={i} className="text-xs text-amber-700">{w}</p>)}
                        </div>
                      )}
                      <div className="border rounded-xl overflow-hidden">
                        <div className="px-4 py-2 bg-emerald-50 dark:bg-emerald-950/20 border-b">
                          <span className="text-xs font-semibold text-emerald-700">{t("contextMgmt.tobeYaml")}</span>
                        </div>
                        <YamlEditor value={tobeYaml} onChange={(v) => setTobeYaml(v)} className="h-[30vh]" />
                      </div>
                      <div className="flex items-center gap-3">
                        <div className="flex-1">
                          <label className="text-xs font-medium mb-1 block">{t("contextMgmt.tobeFileName")}</label>
                          <input
                            type="text"
                            value={tobeFileName}
                            onChange={(e) => setTobeFileName(e.target.value)}
                            className="w-full px-3 py-2 border rounded-lg text-sm bg-background focus:outline-none focus:ring-2 focus:ring-emerald-200"
                          />
                          <p className="text-[10px] text-muted-foreground mt-1">context/system-architecture/{tobeFileName || "..."}.yaml</p>
                        </div>
                        <div className="flex gap-2 pt-5">
                          <Button variant="outline" size="sm" onClick={handleGenerateTobe}>{t("contextMgmt.regenerate")}</Button>
                          <Button size="sm" onClick={handleSaveTobe} disabled={!tobeYaml || !tobeFileName || isSavingTobe} className="bg-emerald-600 hover:bg-emerald-700">
                            {isSavingTobe ? t("contextMgmt.importSaving") : t("contextMgmt.saveTobe")}
                          </Button>
                        </div>
                      </div>
                    </>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
