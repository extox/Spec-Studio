"use client";

import { useEffect, useRef, useState, useCallback, useMemo } from "react";
import { useChatStore } from "@/stores/chatStore";
import { useAuthStore } from "@/stores/authStore";
import { ChatMessage } from "./ChatMessage";
import { ChatInput } from "./ChatInput";
import { WorkflowPanel } from "./WorkflowPanel";
import { ChatWebSocket } from "@/lib/websocket";
import { toast } from "sonner";
import api from "@/lib/api";
import type { Workflow, WSMessage } from "@/types";
import { useI18n } from "@/lib/i18n";

interface ChatWindowProps {
  projectId: number;
  sessionId: number;
  onDeliverableCreated?: (file: { id: number; file_path: string; file_name: string }) => void;
}

export function ChatWindow({ projectId, sessionId, onDeliverableCreated }: ChatWindowProps) {
  const {
    currentSession, messages, isStreaming, streamingContent,
    hasMoreMessages, isLoadingMore,
    fetchSessionDetail, fetchRecentMessages, fetchOlderMessages,
    addLocalMessage, updateStreamingContent,
    setIsStreaming, clearStreaming, stopStreaming, workflows,
  } = useChatStore();

  const { t } = useI18n();
  const { user: currentUser } = useAuthStore();
  const wsRef = useRef<ChatWebSocket | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);
  const scrollContainerRef = useRef<HTMLDivElement>(null);
  const [workflowStep, setWorkflowStep] = useState(0);
  const [myStreamingRequest, setMyStreamingRequest] = useState(false);
  const [personaOverride, setPersonaOverride] = useState<{ id: string; name: string; avatar: string } | null>(null);
  const [streamingPersona, setStreamingPersona] = useState<{ name: string; avatar: string } | null>(null);
  const [boldInsertText, setBoldInsertText] = useState("");
  const isStreamingRef = useRef(false);

  useEffect(() => {
    isStreamingRef.current = isStreaming;
  }, [isStreaming]);

  const workflow: Workflow | null = currentSession?.workflow
    ? workflows.find((w) => w.id === currentSession.workflow) || null
    : null;

  useEffect(() => {
    fetchSessionDetail(projectId, sessionId);
    fetchRecentMessages(projectId, sessionId, 3).then(() => {
      // Scroll to bottom after initial load
      requestAnimationFrame(() => {
        scrollRef.current?.scrollIntoView();
      });
    });
  }, [projectId, sessionId, fetchSessionDetail, fetchRecentMessages]);

  useEffect(() => {
    if (currentSession) {
      setWorkflowStep(currentSession.workflow_step);
    }
  }, [currentSession]);

  useEffect(() => {
    let cancelled = false;
    const token = localStorage.getItem("access_token") || "";
    const ws = new ChatWebSocket(sessionId, token);

    ws.connect().catch(() => {
      if (!cancelled) {
        toast.error(t("chat.wsConnectionFailed"));
      }
    });

    // Another user sent a message in this session
    ws.on("user_message", (data: WSMessage) => {
      if (cancelled) return;
      const msg = data as unknown as { content: string; user_id: number; display_name: string };
      addLocalMessage({
        id: Date.now(),
        session_id: sessionId,
        role: "user",
        content: msg.content,
        metadata_json: JSON.stringify({ user_id: msg.user_id, display_name: msg.display_name }),
        created_at: new Date().toISOString(),
      });
    });

    ws.on("chat_stream_start", (data: WSMessage) => {
      if (cancelled) return;
      setIsStreaming(true);
      clearStreaming();
      const info = data as unknown as { persona_id?: string; persona_name?: string; persona_avatar?: string };
      if (info.persona_name) {
        setStreamingPersona({ name: info.persona_name, avatar: info.persona_avatar || "AI" });
      } else {
        setStreamingPersona(null);
      }
    });

    ws.on("chat_stream_chunk", (data: WSMessage) => {
      if (cancelled) return;
      const chunk = data as unknown as { content: string };
      updateStreamingContent(chunk.content);
    });

    ws.on("chat_stream_end", (data: WSMessage) => {
      if (cancelled) return;
      const msg = data as unknown as { full_content: string; metadata: Record<string, unknown> };
      addLocalMessage({
        id: Date.now(),
        session_id: sessionId,
        role: "assistant",
        content: msg.full_content,
        metadata_json: JSON.stringify(msg.metadata || {}),
        created_at: new Date().toISOString(),
      });
      stopStreaming();
      setStreamingPersona(null);
      setMyStreamingRequest(false);
    });

    ws.on("deliverable_created", (data: WSMessage) => {
      if (cancelled) return;
      const file = (data as unknown as { file: { id: number; file_path: string; file_name: string } }).file;
      toast.success(t("chat.deliverableCreated", { name: file.file_name }));
      onDeliverableCreated?.(file);
    });

    ws.on("workflow_update", (data: WSMessage) => {
      if (cancelled) return;
      const update = data as unknown as { current_step: number };
      setWorkflowStep(update.current_step);
    });

    ws.on("step_transition", (data: WSMessage) => {
      if (cancelled) return;
      const transition = data as unknown as { step: number; step_name: string; message: string };
      setWorkflowStep(transition.step);
      addLocalMessage({
        id: Date.now(),
        session_id: sessionId,
        role: "system",
        content: transition.message,
        created_at: new Date().toISOString(),
      });
    });

    ws.on("deliverable_compiling", (data: WSMessage) => {
      if (cancelled) return;
      const info = data as unknown as { file_name: string; message: string };
      toast.info(t("chat.generating", { name: info.file_name }));
      addLocalMessage({
        id: Date.now(),
        session_id: sessionId,
        role: "system",
        content: info.message,
        created_at: new Date().toISOString(),
      });
    });

    ws.on("workflow_complete", (data: WSMessage) => {
      if (cancelled) return;
      const info = data as unknown as { file_name: string };
      toast.success(t("chat.deliverableSaved", { name: info.file_name }));
    });

    ws.on("persona_switched", (data: WSMessage) => {
      if (cancelled) return;
      const info = data as unknown as { persona_id: string; persona_name: string; persona_avatar: string };
      setPersonaOverride({ id: info.persona_id, name: info.persona_name, avatar: info.persona_avatar });
      fetchSessionDetail(projectId, sessionId);
    });

    ws.on("error", (data: WSMessage) => {
      if (cancelled) return;
      const err = data as unknown as { message: string };
      toast.error(err.message);
      stopStreaming();
    });

    wsRef.current = ws;

    return () => {
      cancelled = true;
      if (isStreamingRef.current) {
        // Keep WebSocket alive so server can finish saving the message to DB.
        // Clear UI streaming state so navigation is not blocked.
        stopStreaming();
        setMyStreamingRequest(false);
        setTimeout(() => ws.disconnect(), 60000);
      } else {
        ws.disconnect();
      }
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sessionId]);

  // Load older messages when scrolling to top
  const handleScroll = useCallback(() => {
    const container = scrollContainerRef.current;
    if (!container || !hasMoreMessages || isLoadingMore) return;
    if (container.scrollTop < 80) {
      const prevHeight = container.scrollHeight;
      fetchOlderMessages(projectId, sessionId, 3).then(() => {
        // Preserve scroll position after prepending older messages
        requestAnimationFrame(() => {
          const newHeight = container.scrollHeight;
          container.scrollTop = newHeight - prevHeight;
        });
      });
    }
  }, [hasMoreMessages, isLoadingMore, projectId, sessionId, fetchOlderMessages]);

  // Auto-scroll to bottom for new messages
  const prevMessageCountRef = useRef(messages.length);
  useEffect(() => {
    if (messages.length > prevMessageCountRef.current) {
      scrollRef.current?.scrollIntoView({ behavior: "smooth" });
    }
    prevMessageCountRef.current = messages.length;
  }, [messages.length]);

  // Auto-scroll for streaming content
  useEffect(() => {
    if (streamingContent) {
      scrollRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [streamingContent]);

  const handleSend = useCallback((content: string, fileIds?: string[]) => {
    addLocalMessage({
      id: Date.now(),
      session_id: sessionId,
      role: "user",
      content,
      created_at: new Date().toISOString(),
    });
    setMyStreamingRequest(true);
    wsRef.current?.sendChatMessage(content, fileIds);
  }, [sessionId, addLocalMessage]);

  const handleWorkflowAction = useCallback((action: string) => {
    wsRef.current?.sendWorkflowAction(action);
  }, []);

  const handleAPCAction = useCallback((action: "advanced" | "party" | "propose" | "continue") => {
    wsRef.current?.sendAPCAction(action);
  }, []);

  const handleSaveDeliverable = useCallback((content: string) => {
    // Suggest a default file name based on workflow template
    let defaultName = "deliverable.md";
    if (workflow?.template) {
      const templateFileMap: Record<string, string> = {
        "product-brief": "product-brief.md",
        "prd": "PRD.md",
        "architecture": "architecture.md",
        "epic": "epics.md",
        "story": "story.md",
        "ux-spec": "ux-spec.md",
        "project-context": "project-context.md",
        "sprint-status": "sprint-status.md",
      };
      defaultName = templateFileMap[workflow.template] || "deliverable.md";
    }
    const userFileName = prompt(t("chat.saveFileNamePrompt"), defaultName);
    if (!userFileName) return;
    const fileName = userFileName.endsWith(".md") ? userFileName : `${userFileName}.md`;
    wsRef.current?.saveDeliverable(content, fileName);
  }, [workflow, t]);

  const resolvePersona = (id: string) => {
    return ALL_PERSONAS.find((p) => p.id === id) || { id, name: id, avatar: "AI" };
  };

  const personaInfo = personaOverride
    ? { avatar: personaOverride.avatar, name: personaOverride.name }
    : currentSession
    ? resolvePersona(currentSession.persona)
    : undefined;

  // Extract persona info from message metadata (for party mode messages)
  const getMessagePersona = (msg: { metadata_json?: string | null }) => {
    if (!msg.metadata_json) return null;
    try {
      const meta = JSON.parse(msg.metadata_json);
      if (meta.party_mode && meta.persona) {
        const allPersonas: Record<string, { name: string; avatar: string }> = {
          analyst: { name: "Analyst (Mary)", avatar: "🔍" },
          pm: { name: "PM (John)", avatar: "📋" },
          architect: { name: "Architect (Winston)", avatar: "🏗️" },
          "ux-designer": { name: "UX Designer (Sally)", avatar: "🎨" },
          "scrum-master": { name: "Scrum Master (Bob)", avatar: "📊" },
          "tech-writer": { name: "Tech Writer (Paige)", avatar: "📝" },
        };
        return allPersonas[meta.persona] || null;
      }
    } catch { /* ignore */ }
    return null;
  };

  const handleSwitchPersona = useCallback((personaId: string) => {
    wsRef.current?.switchPersona(personaId);
  }, []);

  return (
    <div className="flex h-full flex-col">
      {/* Persona indicator + switcher */}
      <div className="flex items-center gap-2 border-b px-4 py-1.5">
        <span className="text-sm">{personaInfo?.avatar}</span>
        <span className="text-xs font-medium">{personaInfo?.name}</span>
        <PersonaSwitcher
          currentPersonaId={personaOverride?.id || currentSession?.persona || ""}
          onSwitch={handleSwitchPersona}
          t={t}
        />
      </div>
      <WorkflowPanel
        workflow={workflow}
        currentStep={workflowStep}
        onAction={handleWorkflowAction}
        onAPCAction={handleAPCAction}
        disabled={isStreaming}
      />
      <div
        ref={scrollContainerRef}
        onScroll={handleScroll}
        className="flex-1 overflow-y-auto px-4"
      >
        <div className="space-y-1 py-4">
          {isLoadingMore && (
            <div className="flex justify-center py-2">
              <p className="text-xs text-muted-foreground animate-pulse">{t("common.loading")}</p>
            </div>
          )}
          {hasMoreMessages && !isLoadingMore && (
            <div className="flex justify-center py-2">
              <p className="text-xs text-muted-foreground">
                {t("chat.loadMore")}
              </p>
            </div>
          )}
          {/* Persona guide when no messages */}
          {messages.length === 0 && !isStreaming && (
            <PersonaGuide
              persona={currentSession?.persona || "default"}
              onSend={handleSend}
              t={t}
            />
          )}
          {messages.map((msg, idx) => {
            let authorName: string | undefined;
            let isCurrentUser = true;
            if (msg.role === "user" && msg.metadata_json) {
              try {
                const meta = JSON.parse(msg.metadata_json);
                authorName = meta.display_name;
                isCurrentUser = currentUser ? meta.user_id === currentUser.id : true;
              } catch { /* ignore */ }
            }
            // Check if this is the last assistant message (for quick action buttons)
            const isLastAssistant = msg.role === "assistant" && !isStreaming &&
              idx === messages.length - 1 || (
                msg.role === "assistant" &&
                !messages.slice(idx + 1).some((m) => m.role === "assistant")
              );
            const msgPersona = getMessagePersona(msg);
            return (
              <ChatMessage
                key={msg.id}
                role={msg.role}
                content={msg.content}
                personaAvatar={msgPersona?.avatar || personaInfo?.avatar}
                personaName={msgPersona?.name || personaInfo?.name}
                authorName={authorName}
                isCurrentUser={isCurrentUser}
                isLastAssistant={isLastAssistant && !isStreaming}
                createdAt={msg.created_at}
                onSaveDeliverable={handleSaveDeliverable}
                onQuickAction={(msg) => {
                  const apcMap: Record<string, "advanced" | "party" | "propose" | "continue"> = {
                    A: "advanced", P: "party", R: "propose", C: "continue",
                  };
                  const apcAction = apcMap[msg];
                  if (apcAction && currentSession?.workflow) {
                    handleAPCAction(apcAction);
                  } else {
                    handleSend(msg);
                  }
                }}
                onBoldClick={(text) => setBoldInsertText(text)}
              />
            );
          })}
          {isStreaming && (
            streamingContent ? (
              <div className="flex gap-3 py-3">
                <div className="h-8 w-8 shrink-0 rounded-full bg-gradient-to-br from-accent to-secondary flex items-center justify-center text-xs font-medium text-accent-foreground shadow-sm">
                  {streamingPersona?.avatar || personaInfo?.avatar || "AI"}
                </div>
                <div className="max-w-[80%]">
                  <p className="text-xs text-muted-foreground mb-1">
                    {streamingPersona?.name || personaInfo?.name || "AI"}
                  </p>
                  <div className="rounded-2xl rounded-tl-sm px-4 py-2.5 text-sm shadow-sm bg-card border">
                    <pre className="whitespace-pre-wrap font-sans break-words">{streamingContent}</pre>
                  </div>
                </div>
              </div>
            ) : (
              <div className="flex gap-3 py-3">
                <div className="h-8 w-8 shrink-0 rounded-full bg-muted flex items-center justify-center text-xs">
                  {streamingPersona?.avatar || personaInfo?.avatar || "AI"}
                </div>
                <div className="flex items-center gap-1.5 px-3 py-2 rounded-lg bg-muted">
                  <span className="h-2 w-2 rounded-full bg-muted-foreground/40 animate-bounce" style={{ animationDelay: "0ms" }} />
                  <span className="h-2 w-2 rounded-full bg-muted-foreground/40 animate-bounce" style={{ animationDelay: "150ms" }} />
                  <span className="h-2 w-2 rounded-full bg-muted-foreground/40 animate-bounce" style={{ animationDelay: "300ms" }} />
                </div>
              </div>
            )
          )}
          <div ref={scrollRef} />
        </div>
      </div>
      <ChatInput
        onSend={handleSend}
        onStop={() => { stopStreaming(); setMyStreamingRequest(false); }}
        onImageUpload={async (file) => {
          try {
            const formData = new FormData();
            formData.append("file", file);
            const res = await api.post(`/projects/${projectId}/chat/upload-image`, formData, {
              headers: { "Content-Type": "multipart/form-data" },
            });
            const apiBase = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";
            return {
              url: `${apiBase.replace("/api", "")}${res.data.url}`,
              providerFileId: res.data.provider_file_id || undefined,
            };
          } catch {
            return null;
          }
        }}
        disabled={isStreaming && myStreamingRequest}
        isStreaming={isStreaming && myStreamingRequest}
        placeholder={t("chat.messagePlaceholder", { persona: currentSession?.persona || t("chat.assistant") })}
        insertText={boldInsertText}
        onInsertTextConsumed={() => setBoldInsertText("")}
      />
    </div>
  );
}


function PersonaGuide({
  persona,
  onSend,
  t,
}: {
  persona: string;
  onSend: (content: string) => void;
  t: (key: string) => string;
}) {
  const key = ["analyst", "pm", "architect", "ux-designer", "scrum-master", "tech-writer"].includes(persona)
    ? persona
    : "default";

  const title = t(`chat.guide.${key}.title`);
  const tips = t(`chat.guide.${key}.tips`).split("|");
  const examples = t(`chat.guide.${key}.examples`).split("|");

  return (
    <div className="flex flex-col items-center justify-center py-12 px-4">
      <h3 className="text-lg font-semibold mb-6">{title}</h3>

      <div className="grid gap-6 w-full max-w-lg">
        {/* Tips */}
        <div>
          <p className="text-xs font-medium text-muted-foreground mb-2">{t("chat.guide.tipsLabel")}</p>
          <div className="space-y-1.5">
            {tips.map((tip, i) => (
              <div key={i} className="flex items-start gap-2 text-sm text-muted-foreground">
                <span className="text-primary mt-0.5 shrink-0">•</span>
                <span>{tip}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Example prompts - clickable */}
        <div>
          <p className="text-xs font-medium text-muted-foreground mb-2">{t("chat.guide.tryLabel")}</p>
          <div className="space-y-1.5">
            {examples.map((example, i) => (
              <button
                key={i}
                onClick={() => onSend(example)}
                className="w-full text-left px-3 py-2 text-sm rounded-lg border border-dashed hover:border-primary hover:bg-primary/5 text-muted-foreground hover:text-foreground transition-colors"
              >
                &ldquo;{example}&rdquo;
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

const ALL_PERSONAS = [
  { id: "analyst", name: "Analyst (Mary)", avatar: "🔍" },
  { id: "pm", name: "PM (John)", avatar: "📋" },
  { id: "architect", name: "Architect (Winston)", avatar: "🏗️" },
  { id: "ux-designer", name: "UX Designer (Sally)", avatar: "🎨" },
  { id: "scrum-master", name: "Scrum Master (Bob)", avatar: "📊" },
  { id: "tech-writer", name: "Tech Writer (Paige)", avatar: "📝" },
];

function PersonaSwitcher({
  currentPersonaId,
  onSwitch,
  t,
}: {
  currentPersonaId: string;
  onSwitch: (personaId: string) => void;
  t: (key: string) => string;
}) {
  const [open, setOpen] = useState(false);

  return (
    <div className="relative">
      <button
        onClick={() => setOpen(!open)}
        className="text-[10px] text-muted-foreground hover:text-primary transition-colors px-1.5 py-0.5 rounded hover:bg-muted"
      >
        {t("chat.switchPersona")}
      </button>
      {open && (
        <>
          <div className="fixed inset-0 z-40" onClick={() => setOpen(false)} />
          <div className="absolute left-0 top-full mt-1 z-50 bg-popover border rounded-lg shadow-lg py-1 min-w-[200px]">
            {ALL_PERSONAS.map((p) => (
              <button
                key={p.id}
                onClick={() => { onSwitch(p.id); setOpen(false); }}
                className={`flex items-center gap-2 w-full px-3 py-1.5 text-xs hover:bg-muted transition-colors text-left ${
                  p.id === currentPersonaId ? "bg-primary/10 text-primary font-medium" : ""
                }`}
              >
                <span>{p.avatar}</span>
                <span>{p.name}</span>
                {p.id === currentPersonaId && (
                  <span className="ml-auto text-[10px] text-primary">✓</span>
                )}
              </button>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
