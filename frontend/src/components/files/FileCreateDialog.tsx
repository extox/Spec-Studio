"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { MarkdownEditor } from "@/components/editor/MarkdownEditor";
import api from "@/lib/api";
import { toast } from "sonner";
import { useI18n } from "@/lib/i18n";

interface BmadTemplate {
  id: string;
  name: string;
  file_name: string;
  phase: string;
  description: string;
}

const TEMPLATE_PATH_MAP: Record<string, string> = {
  "product-brief": "planning-artifacts",
  "prd": "planning-artifacts",
  "architecture": "planning-artifacts",
  "ux-spec": "planning-artifacts",
  "project-context": "planning-artifacts",
  "epic": "planning-artifacts",
  "story": "implementation-artifacts",
  "sprint-status": "implementation-artifacts",
};

interface FileCreateDialogProps {
  projectId: number;
  onCreated: () => void;
}

export function FileCreateDialog({ projectId, onCreated }: FileCreateDialogProps) {
  const { t } = useI18n();
  const [open, setOpen] = useState(false);
  const [fileName, setFileName] = useState("");
  const [filePath, setFilePath] = useState("");
  const [content, setContent] = useState("");
  const [saving, setSaving] = useState(false);
  const [templates, setTemplates] = useState<BmadTemplate[]>([]);
  const [selectedTemplate, setSelectedTemplate] = useState("");
  const [loadingTemplate, setLoadingTemplate] = useState(false);

  useEffect(() => {
    if (open && templates.length === 0) {
      api.get<BmadTemplate[]>("/bmad/templates").then((res) => {
        setTemplates(res.data);
      });
    }
  }, [open, templates.length]);

  const handleTemplateChange = async (templateId: string) => {
    setSelectedTemplate(templateId);
    if (!templateId) return;

    const tmpl = templates.find((t) => t.id === templateId);
    if (!tmpl) return;

    setFileName(tmpl.file_name);
    setFilePath(TEMPLATE_PATH_MAP[templateId] || "");

    setLoadingTemplate(true);
    try {
      const res = await api.get<{ id: string; content: string }>(
        `/bmad/templates/${templateId}/content`
      );
      setContent(res.data.content);
    } catch {
      setContent("");
    } finally {
      setLoadingTemplate(false);
    }
  };

  const handleCreate = async () => {
    const trimmedName = fileName.trim();
    if (!trimmedName) {
      toast.error(t("files.fileNameRequired"));
      return;
    }

    const finalName = trimmedName.endsWith(".md") ? trimmedName : `${trimmedName}.md`;
    const finalPath = filePath.trim()
      ? `${filePath.trim().replace(/\/+$/, "")}/${finalName}`
      : finalName;

    setSaving(true);
    try {
      await api.post(`/projects/${projectId}/files`, {
        file_name: finalName,
        file_path: finalPath,
        file_type: "deliverable",
        content: content || "",
      });
      toast.success(t("files.created"));
      handleClose();
      onCreated();
    } catch {
      toast.error(t("files.createFailed"));
    } finally {
      setSaving(false);
    }
  };

  const handleClose = () => {
    setOpen(false);
    setFileName("");
    setFilePath("");
    setContent("");
    setSelectedTemplate("");
  };

  if (!open) {
    return (
      <Button size="sm" variant="outline" onClick={() => setOpen(true)}>
        {t("files.newFile")}
      </Button>
    );
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className="bg-background border rounded-lg shadow-lg w-[90vw] max-w-3xl max-h-[85vh] flex flex-col">
        <div className="flex items-center justify-between border-b px-4 py-3">
          <h2 className="text-sm font-semibold">{t("files.createMarkdown")}</h2>
          <Button size="sm" variant="ghost" onClick={handleClose}>
            {t("common.close")}
          </Button>
        </div>

        <div className="px-4 py-3 space-y-3 border-b">
          <div>
            <label className="text-xs text-muted-foreground mb-1 block">
              {t("files.template")}
            </label>
            <select
              value={selectedTemplate}
              onChange={(e) => handleTemplateChange(e.target.value)}
              className="w-full rounded-md border px-3 py-1.5 text-sm bg-transparent focus:outline-none focus:ring-2 focus:ring-ring"
            >
              <option value="">{t("files.blankFile")}</option>
              {templates.map((tmpl) => (
                <option key={tmpl.id} value={tmpl.id}>
                  {tmpl.name} — {tmpl.description}
                </option>
              ))}
            </select>
          </div>
          <div className="flex gap-3">
            <div className="flex-1">
              <label className="text-xs text-muted-foreground mb-1 block">
                {t("files.fileName")}
              </label>
              <input
                type="text"
                value={fileName}
                onChange={(e) => setFileName(e.target.value)}
                placeholder="document.md"
                className="w-full rounded-md border px-3 py-1.5 text-sm bg-transparent focus:outline-none focus:ring-2 focus:ring-ring"
              />
            </div>
            <div className="flex-1">
              <label className="text-xs text-muted-foreground mb-1 block">
                {t("files.filePath")}
              </label>
              <input
                type="text"
                value={filePath}
                onChange={(e) => setFilePath(e.target.value)}
                placeholder="planning-artifacts"
                className="w-full rounded-md border px-3 py-1.5 text-sm bg-transparent focus:outline-none focus:ring-2 focus:ring-ring"
              />
            </div>
          </div>
        </div>

        <div className="flex-1 overflow-hidden min-h-[300px]">
          {loadingTemplate ? (
            <div className="flex h-full items-center justify-center text-muted-foreground">
              {t("common.loading")}
            </div>
          ) : (
            <MarkdownEditor value={content} onChange={setContent} />
          )}
        </div>

        <div className="flex justify-end gap-2 border-t px-4 py-3">
          <Button size="sm" variant="outline" onClick={handleClose}>
            {t("common.cancel")}
          </Button>
          <Button size="sm" onClick={handleCreate} disabled={saving || !fileName.trim()}>
            {saving ? t("common.loading") : t("common.save")}
          </Button>
        </div>
      </div>
    </div>
  );
}
