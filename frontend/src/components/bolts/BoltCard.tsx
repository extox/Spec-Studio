"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { useI18n } from "@/lib/i18n";

export interface Bolt {
  id: number;
  bolt_number: number;
  title: string;
  story_anchor: string | null;
  persona_id: string;
  workflow_id: string | null;
  status: "todo" | "in_bolt" | "awaiting_approval" | "done" | "blocked";
  estimated_minutes: number;
  approval_required: boolean;
  started_at: string | null;
  completed_at: string | null;
  blocker_reason: string | null;
}

const PERSONA_AVATAR: Record<string, string> = {
  developer: "💻",
  "qa-engineer": "🧪",
  "devops-engineer": "⚙️",
  "scrum-master": "📊",
  architect: "🏗️",
};

interface BoltCardProps {
  bolt: Bolt;
  onStart?: (b: Bolt) => void;
  onComplete?: (b: Bolt, notes?: string) => void;
  onApprove?: (b: Bolt) => void;
  onBlock?: (b: Bolt, reason: string) => void;
  onUnblock?: (b: Bolt) => void;
  onDelete?: (b: Bolt) => void;
}

export function BoltCard({ bolt, onStart, onComplete, onApprove, onBlock, onUnblock, onDelete }: BoltCardProps) {
  const { t } = useI18n();
  const [showBlock, setShowBlock] = useState(false);
  const [blockReason, setBlockReason] = useState("");
  const [showComplete, setShowComplete] = useState(false);
  const [completeNotes, setCompleteNotes] = useState("");

  const elapsed = (startIso: string | null): string => {
    if (!startIso) return "";
    const start = new Date(startIso).getTime();
    const ms = Date.now() - start;
    const m = Math.floor(ms / 60_000);
    if (m < 1) return t("bolt.elapsedJustNow");
    if (m < 60) return t("bolt.elapsedMinutes", { n: String(m) });
    return t("bolt.elapsedHoursMinutes", { h: String(Math.floor(m / 60)), m: String(m % 60) });
  };

  return (
    <div className="border rounded-md p-2.5 bg-background hover:shadow-sm transition-shadow text-xs">
      <div className="flex items-start justify-between gap-2">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-1.5">
            <span className="text-[10px] font-mono text-muted-foreground">#{bolt.bolt_number}</span>
            {bolt.story_anchor && (
              <span className="text-[10px] font-mono px-1 rounded bg-muted">
                {bolt.story_anchor}
              </span>
            )}
          </div>
          <p className="font-medium mt-1 break-words">{bolt.title}</p>
        </div>
        <span className="text-base shrink-0" title={bolt.persona_id}>
          {PERSONA_AVATAR[bolt.persona_id] || "🤖"}
        </span>
      </div>

      <div className="flex items-center gap-2 mt-1.5 text-[10px] text-muted-foreground">
        <span>{t("bolt.minutes", { n: String(bolt.estimated_minutes) })}</span>
        {bolt.workflow_id && <span className="font-mono">{bolt.workflow_id}</span>}
        {bolt.status === "in_bolt" && bolt.started_at && (
          <span className="text-orange-600 font-medium">{elapsed(bolt.started_at)}</span>
        )}
      </div>

      {bolt.status === "blocked" && bolt.blocker_reason && (
        <p className="text-[10px] text-destructive mt-1.5 italic">⛔ {bolt.blocker_reason}</p>
      )}

      <div className="flex flex-wrap gap-1 mt-2">
        {bolt.status === "todo" && onStart && (
          <Button size="sm" variant="outline" className="h-6 text-[10px] px-2" onClick={() => onStart(bolt)}>
            {t("bolt.start")}
          </Button>
        )}
        {bolt.status === "in_bolt" && onComplete && (
          <Button size="sm" variant="outline" className="h-6 text-[10px] px-2" onClick={() => setShowComplete(true)}>
            {t("bolt.complete")}
          </Button>
        )}
        {bolt.status === "awaiting_approval" && onApprove && (
          <Button size="sm" variant="default" className="h-6 text-[10px] px-2" onClick={() => onApprove(bolt)}>
            {t("bolt.approve")}
          </Button>
        )}
        {(bolt.status === "todo" || bolt.status === "in_bolt") && onBlock && (
          <Button
            size="sm"
            variant="ghost"
            className="h-6 text-[10px] px-2 text-muted-foreground hover:text-destructive"
            onClick={() => setShowBlock(true)}
          >
            {t("bolt.block")}
          </Button>
        )}
        {bolt.status === "blocked" && onUnblock && (
          <Button size="sm" variant="outline" className="h-6 text-[10px] px-2" onClick={() => onUnblock(bolt)}>
            {t("bolt.unblock")}
          </Button>
        )}
        {onDelete && (bolt.status === "todo" || bolt.status === "blocked") && (
          <Button
            size="sm"
            variant="ghost"
            className="h-6 text-[10px] px-2 ml-auto text-muted-foreground hover:text-destructive"
            onClick={() => onDelete(bolt)}
          >
            ×
          </Button>
        )}
      </div>

      {showBlock && (
        <div className="mt-2 space-y-1">
          <textarea
            value={blockReason}
            onChange={(e) => setBlockReason(e.target.value)}
            placeholder={t("bolt.blockReasonPlaceholder")}
            className="w-full text-[10px] border rounded px-1.5 py-1 resize-none"
            rows={2}
          />
          <div className="flex gap-1">
            <Button
              size="sm"
              variant="default"
              className="h-6 text-[10px] px-2"
              onClick={() => {
                if (blockReason.trim() && onBlock) {
                  onBlock(bolt, blockReason.trim());
                  setShowBlock(false);
                  setBlockReason("");
                }
              }}
            >
              {t("bolt.submit")}
            </Button>
            <Button size="sm" variant="ghost" className="h-6 text-[10px] px-2" onClick={() => setShowBlock(false)}>
              {t("bolt.cancel")}
            </Button>
          </div>
        </div>
      )}

      {showComplete && (
        <div className="mt-2 space-y-1">
          <textarea
            value={completeNotes}
            onChange={(e) => setCompleteNotes(e.target.value)}
            placeholder={t("bolt.completeNotesPlaceholder")}
            className="w-full text-[10px] border rounded px-1.5 py-1 resize-none"
            rows={2}
          />
          <div className="flex gap-1">
            <Button
              size="sm"
              variant="default"
              className="h-6 text-[10px] px-2"
              onClick={() => {
                if (onComplete) onComplete(bolt, completeNotes.trim() || undefined);
                setShowComplete(false);
                setCompleteNotes("");
              }}
            >
              {t("bolt.submit")}
            </Button>
            <Button size="sm" variant="ghost" className="h-6 text-[10px] px-2" onClick={() => setShowComplete(false)}>
              {t("bolt.cancel")}
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}
