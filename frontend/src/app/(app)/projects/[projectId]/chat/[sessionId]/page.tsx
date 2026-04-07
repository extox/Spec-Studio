"use client";

import { useState, useEffect, useCallback } from "react";
import { useParams } from "next/navigation";
import { ChatWindow } from "@/components/chat/ChatWindow";
import { FileViewer } from "@/components/files/FileViewer";
import { useChatStore } from "@/stores/chatStore";
import { useProjectStore } from "@/stores/projectStore";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { useI18n } from "@/lib/i18n";

export default function ChatSessionPage() {
  const params = useParams();
  const projectId = Number(params.projectId);
  const sessionId = Number(params.sessionId);
  const { fetchWorkflows, addLocalMessage } = useChatStore();
  const { files, fetchFiles } = useProjectStore();
  const [selectedFileId, setSelectedFileId] = useState<number | null>(null);
  const [showPanel, setShowPanel] = useState(false);
  const { t } = useI18n();

  useEffect(() => {
    fetchWorkflows();
    fetchFiles(projectId);
  }, [projectId, fetchWorkflows, fetchFiles]);

  const handleDeliverableCreated = (file: { id: number; file_path: string; file_name: string }) => {
    setSelectedFileId(file.id);
    setShowPanel(true);
    fetchFiles(projectId);
  };

  const handleFileSaved = useCallback((fileName: string) => {
    // Notify chat that a file was modified via document panel
    addLocalMessage({
      id: Date.now(),
      session_id: sessionId,
      role: "system",
      content: t("chat.fileUpdatedNotice", { name: fileName }),
      created_at: new Date().toISOString(),
    });
    fetchFiles(projectId);
  }, [sessionId, projectId, addLocalMessage, fetchFiles, t]);

  return (
    <div className="flex h-full">
      <div className={cn("flex-1 min-w-0", showPanel && "border-r")}>
        <ChatWindow
          projectId={projectId}
          sessionId={sessionId}
          onDeliverableCreated={handleDeliverableCreated}
        />
      </div>

      {showPanel && (
        <div className="w-[45%] flex flex-col">
          <div className="flex items-center border-b px-3 py-2 gap-2">
            <span className="text-sm font-medium shrink-0">{t("chat.documentPanel")}</span>
            <div className="flex-1 flex gap-1 overflow-x-auto">
              {files.map((f) => (
                <Button
                  key={f.id}
                  size="sm"
                  variant={selectedFileId === f.id ? "default" : "ghost"}
                  className="h-6 text-xs shrink-0"
                  onClick={() => setSelectedFileId(f.id)}
                >
                  {f.file_name}
                </Button>
              ))}
            </div>
            <Button
              size="sm"
              variant="ghost"
              className="h-6 text-xs shrink-0"
              onClick={() => setShowPanel(false)}
            >
              {t("common.close")}
            </Button>
          </div>
          {selectedFileId && (
            <FileViewer
              projectId={projectId}
              fileId={selectedFileId}
              onSaved={handleFileSaved}
            />
          )}
        </div>
      )}

      {!showPanel && files.length > 0 && (
        <Button
          variant="outline"
          size="sm"
          className="absolute right-4 top-4 z-10"
          onClick={() => {
            setShowPanel(true);
            if (!selectedFileId && files.length > 0) {
              setSelectedFileId(files[0].id);
            }
          }}
        >
          {t("chat.showDocuments")}
        </Button>
      )}
    </div>
  );
}
