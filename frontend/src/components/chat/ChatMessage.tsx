"use client";

import { useState, useMemo } from "react";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { MarkdownPreview } from "@/components/editor/MarkdownPreview";
import { cn } from "@/lib/utils";
import { useI18n } from "@/lib/i18n";

interface QuickAction {
  key: string;
  label: string;
  message: string;
  variant: "default" | "outline" | "ghost";
}

function detectQuickActions(content: string): QuickAction[] {
  const actions: QuickAction[] = [];

  if (/\[a\]/i.test(content) || /advanced\s*(elicitation)?/i.test(content)) {
    actions.push({ key: "A", label: "[A] Advanced", message: "A", variant: "outline" });
  }
  if (/\[p\]/i.test(content) || /party\s*(mode)?/i.test(content)) {
    actions.push({ key: "P", label: "[P] Party", message: "P", variant: "outline" });
  }
  if (/\[r\]/i.test(content) || /propose\s*(mode)?/i.test(content)) {
    actions.push({ key: "R", label: "[R] Propose", message: "R", variant: "outline" });
  }
  if (/\[c\]/i.test(content) || /\bcontinue\b/i.test(content)) {
    actions.push({ key: "C", label: "[C] Continue", message: "C", variant: "default" });
  }

  return actions;
}

interface ChatMessageProps {
  role: "user" | "assistant" | "system";
  content: string;
  personaAvatar?: string;
  personaName?: string;
  authorName?: string;
  isCurrentUser?: boolean;
  isLastAssistant?: boolean;
  createdAt?: string;
  onSaveDeliverable?: (content: string) => void;
  onQuickAction?: (message: string) => void;
  onBoldClick?: (text: string) => void;
}

function formatTime(dateStr?: string): string {
  if (!dateStr) return "";
  const d = new Date(dateStr);
  return d.toLocaleTimeString("ko-KR", { hour: "2-digit", minute: "2-digit" });
}

export function ChatMessage({
  role, content, personaAvatar, personaName, authorName,
  isCurrentUser = true, isLastAssistant = false, createdAt,
  onSaveDeliverable, onQuickAction, onBoldClick,
}: ChatMessageProps) {
  const isUser = role === "user";
  const isSystem = role === "system";
  const [showActions, setShowActions] = useState(false);
  const [copied, setCopied] = useState(false);
  const { t } = useI18n();

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(content);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // Fallback
      const ta = document.createElement("textarea");
      ta.value = content;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      document.body.removeChild(ta);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const quickActions = useMemo(
    () => (role === "assistant" && isLastAssistant ? detectQuickActions(content) : []),
    [role, content, isLastAssistant]
  );

  if (isSystem) {
    return (
      <div className="flex justify-center py-2">
        <div className="rounded-md border border-dashed px-4 py-2 text-xs text-muted-foreground bg-muted/30 max-w-[90%]">
          <MarkdownPreview content={content} />
        </div>
      </div>
    );
  }

  // Show save button for assistant messages with substantial content
  const canSave = role === "assistant" && content.length > 100 && onSaveDeliverable;

  return (
    <div
      className={cn("group flex gap-3 py-3", isUser && isCurrentUser && "flex-row-reverse")}
      onMouseEnter={() => setShowActions(true)}
      onMouseLeave={() => setShowActions(false)}
    >
      <Avatar className="h-8 w-8 shrink-0 shadow-sm">
        <AvatarFallback className={cn(
          "text-xs font-medium",
          isUser && isCurrentUser
            ? "bg-gradient-to-br from-primary to-primary/80 text-primary-foreground"
            : isUser && !isCurrentUser
            ? "bg-gradient-to-br from-emerald-400 to-emerald-600 text-white"
            : "bg-gradient-to-br from-accent to-secondary text-accent-foreground"
        )}>
          {isUser ? (authorName ? authorName.charAt(0).toUpperCase() : t("chat.me")) : personaAvatar || "AI"}
        </AvatarFallback>
      </Avatar>
      <div className={cn("max-w-[80%]", isUser && isCurrentUser && "text-right")}>
        <div className="flex items-center gap-2 mb-1">
          <p className="text-xs text-muted-foreground">
            {isUser
              ? (isCurrentUser ? t("chat.me") : authorName || t("chat.me"))
              : personaName || t("chat.assistant")}
          </p>
          {createdAt && (
            <span className="text-[10px] text-muted-foreground/50">{formatTime(createdAt)}</span>
          )}
          {showActions && (
            <Button
              size="sm"
              variant="ghost"
              className="h-5 text-[10px] px-1.5 text-muted-foreground hover:text-primary"
              onClick={handleCopy}
              title={t("chat.copy")}
            >
              {copied ? (
                <svg className="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              ) : (
                <svg className="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
              )}
            </Button>
          )}
          {canSave && showActions && (
            <Button
              size="sm"
              variant="ghost"
              className="h-5 text-[10px] px-1.5 text-muted-foreground hover:text-primary"
              onClick={() => onSaveDeliverable(content)}
              title={t("chat.saveAsFileTitle")}
            >
              <svg className="h-3 w-3 mr-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" />
              </svg>
              {t("chat.saveAsFile")}
            </Button>
          )}
        </div>
        <div className={cn(
          "rounded-2xl px-4 py-2.5 text-sm shadow-sm",
          isUser && isCurrentUser
            ? "bg-primary text-primary-foreground rounded-tr-sm"
            : isUser && !isCurrentUser
            ? "bg-emerald-50 border border-emerald-200 rounded-tl-sm text-foreground"
            : "bg-card border rounded-tl-sm"
        )}>
          {role === "assistant" ? (
            <MarkdownPreview content={content} onBoldClick={onBoldClick} />
          ) : (
            <UserMessageContent content={content} />
          )}
        </div>
        {/* Quick action buttons for A/P/C */}
        {quickActions.length > 0 && onQuickAction && (
          <div className="flex gap-2 mt-2">
            {quickActions.map((action) => (
              <Button
                key={action.key}
                size="sm"
                variant={action.variant}
                className="h-7 text-xs"
                onClick={() => onQuickAction(action.message)}
              >
                {action.label}
              </Button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

const IMG_REGEX = /!\[([^\]]*)\]\(([^)]+)\)/g;

function UserMessageContent({ content }: { content: string }) {
  // Split content into text and image parts
  const parts: { type: "text" | "image"; value: string; alt?: string }[] = [];
  let lastIndex = 0;
  let match: RegExpExecArray | null;

  const regex = new RegExp(IMG_REGEX.source, "g");
  while ((match = regex.exec(content)) !== null) {
    // Text before image
    if (match.index > lastIndex) {
      parts.push({ type: "text", value: content.slice(lastIndex, match.index) });
    }
    parts.push({ type: "image", value: match[2], alt: match[1] });
    lastIndex = match.index + match[0].length;
  }
  // Remaining text
  if (lastIndex < content.length) {
    parts.push({ type: "text", value: content.slice(lastIndex) });
  }

  if (parts.length === 0) {
    return <p className="whitespace-pre-wrap">{content}</p>;
  }

  return (
    <div>
      {parts.map((part, i) =>
        part.type === "image" ? (
          <img
            key={i}
            src={part.value}
            alt={part.alt || ""}
            className="max-w-full max-h-64 rounded-lg my-1.5"
            loading="lazy"
          />
        ) : (
          <p key={i} className="whitespace-pre-wrap">{part.value.trim()}</p>
        )
      )}
    </div>
  );
}
