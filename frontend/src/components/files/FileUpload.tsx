"use client";

import { useRef } from "react";
import { Button } from "@/components/ui/button";
import api from "@/lib/api";
import { toast } from "sonner";
import { useI18n } from "@/lib/i18n";

interface FileUploadProps {
  projectId: number;
  onUploaded: () => void;
}

export function FileUpload({ projectId, onUploaded }: FileUploadProps) {
  const { t } = useI18n();
  const inputRef = useRef<HTMLInputElement>(null);

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      await api.post(`/projects/${projectId}/files/upload`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      toast.success(t("files.uploaded"));
      onUploaded();
    } catch {
      toast.error(t("files.uploadFailed"));
    }

    if (inputRef.current) inputRef.current.value = "";
  };

  return (
    <>
      <input
        ref={inputRef}
        type="file"
        onChange={handleUpload}
        className="hidden"
      />
      <Button size="sm" variant="outline" onClick={() => inputRef.current?.click()}>
        {t("common.upload")}
      </Button>
    </>
  );
}
