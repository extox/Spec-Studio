"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import { Check, CheckCircle2, EyeOff, ExternalLink, GitBranch } from "lucide-react";
import api from "@/lib/api";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetHeader, SheetTitle } from "@/components/ui/sheet";
import { MarkdownPreview } from "@/components/editor/MarkdownPreview";
import { useI18n } from "@/lib/i18n";
import type { Issue } from "./IssueList";
import { translateRuleMessage, translateRuleSuggestion } from "./ruleI18n";
import { ResolutionGuide } from "./ResolutionGuide";

interface IssueDrawerProps {
  projectId: number;
  issue: Issue | null;
  fileName: string | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onUpdateStatus: (id: number, status: Issue["status"]) => void;
  onPrev?: () => void;
  onNext?: () => void;
}

export function IssueDrawer({
  projectId,
  issue,
  fileName,
  open,
  onOpenChange,
  onUpdateStatus,
  onPrev,
  onNext,
}: IssueDrawerProps) {
  const { t } = useI18n();
  const [content, setContent] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const previewRef = useRef<HTMLDivElement>(null);
  const previewSectionRef = useRef<HTMLDivElement>(null);
  const scrollContainerRef = useRef<HTMLDivElement>(null);
  const stickyGuideRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!open || !issue?.file_id) {
      setContent("");
      return;
    }
    setLoading(true);
    api
      .get(`/projects/${projectId}/files/${issue.file_id}`)
      .then((res) => setContent(res.data.content || ""))
      .catch(() => toast.error(t("valid.previewFailed")))
      .finally(() => setLoading(false));
  }, [open, issue?.file_id, projectId, t]);

  // When content loads (or issue changes), find the anchor inside the preview,
  // wrap it with a red highlight box, and scroll the container so the highlight
  // sits just below the sticky resolution-guide header.
  useEffect(() => {
    if (!open || !content) return;

    const root = previewRef.current;
    const container = scrollContainerRef.current;
    if (!root || !container) return;

    // Clear any previous highlights before applying new ones.
    root
      .querySelectorAll<HTMLElement>("[data-issue-highlight]")
      .forEach((el) => {
        el.classList.remove(
          "outline",
          "outline-2",
          "outline-rose-500",
          "outline-offset-2",
          "rounded",
          "bg-rose-50/70",
          "shadow-[inset_4px_0_0_0_#f43f5e]",
          "px-1"
        );
        el.removeAttribute("data-issue-highlight");
      });

    const id = window.requestAnimationFrame(() => {
      // Default scroll: park preview header near the top.
      const section = previewSectionRef.current;
      let scrollTarget: HTMLElement | null = section;

      // Find the anchor occurrence inside the preview content.
      if (issue?.anchor) {
        const anchor = issue.anchor;
        const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
        let node: Node | null = walker.nextNode();
        while (node) {
          if (node.nodeValue && node.nodeValue.includes(anchor)) {
            // Find the closest block-level ancestor (table row, paragraph,
            // heading, list item) so the box wraps the whole offending region.
            let el: HTMLElement | null = node.parentElement;
            while (
              el &&
              el !== root &&
              !["TR", "P", "LI", "H1", "H2", "H3", "H4", "H5", "PRE", "BLOCKQUOTE"].includes(
                el.tagName
              )
            ) {
              el = el.parentElement;
            }
            const target = el && el !== root ? el : node.parentElement;
            if (target) {
              target.dataset.issueHighlight = "true";
              target.classList.add(
                "outline",
                "outline-2",
                "outline-rose-500",
                "outline-offset-2",
                "rounded",
                "bg-rose-50/70",
                "shadow-[inset_4px_0_0_0_#f43f5e]",
                "px-1"
              );
              scrollTarget = target;
            }
            break;
          }
          node = walker.nextNode();
        }
      }

      if (scrollTarget) {
        // Account for the sticky guide header above the scroll content.
        const containerRect = container.getBoundingClientRect();
        const targetRect = scrollTarget.getBoundingClientRect();
        const stickyHeight = stickyGuideRef.current?.offsetHeight ?? 0;
        const delta = targetRect.top - containerRect.top - stickyHeight - 12;
        container.scrollTo({
          top: container.scrollTop + delta,
          behavior: "smooth",
        });
      }
    });
    return () => window.cancelAnimationFrame(id);
  }, [open, issue?.id, issue?.anchor, content]);

  // Keyboard shortcuts: j/k for next/prev, a/r/s for ack/resolve/suppress.
  useEffect(() => {
    if (!open) return;
    const handler = (e: KeyboardEvent) => {
      if ((e.target as HTMLElement | null)?.tagName?.match(/INPUT|TEXTAREA/))
        return;
      if (!issue) return;
      const k = e.key.toLowerCase();
      if (k === "j" || e.key === "ArrowDown") {
        e.preventDefault();
        onNext?.();
      } else if (k === "k" || e.key === "ArrowUp") {
        e.preventDefault();
        onPrev?.();
      } else if (issue.status === "open") {
        if (k === "a") onUpdateStatus(issue.id, "acknowledged");
        else if (k === "r") onUpdateStatus(issue.id, "resolved");
        else if (k === "s") onUpdateStatus(issue.id, "suppressed");
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [open, issue, onNext, onPrev, onUpdateStatus]);

  const headerLabel = useMemo(() => {
    if (!issue) return "";
    const fn = fileName ?? t("valid.openFile");
    return issue.anchor ? `${fn} #${issue.anchor}` : fn;
  }, [issue, fileName, t]);

  return (
    <Sheet open={open} onOpenChange={onOpenChange}>
      <SheetContent
        side="right"
        className="!max-w-none w-[min(48rem,55vw)] sm:!max-w-none flex flex-col"
      >
        <SheetHeader>
          <SheetTitle className="text-sm">
            {issue ? translateRuleMessage(t, issue) : ""}
          </SheetTitle>
          <p className="text-[11px] text-muted-foreground">
            {issue?.rule_id}
            {issue?.severity && ` · ${issue.severity}`}
          </p>
          {issue?.suggestion && (
            <p className="text-[11px] italic text-muted-foreground mt-1">
              💡 {translateRuleSuggestion(t, issue)}
            </p>
          )}
          <div className="flex flex-wrap gap-1.5 mt-2">
            {issue?.status === "open" ? (
              <>
                <button
                  type="button"
                  onClick={() => onUpdateStatus(issue.id, "acknowledged")}
                  title="단축키: a"
                  className="inline-flex items-center gap-1 text-[11px] px-2.5 py-1.5 rounded border border-amber-300 bg-amber-50 text-amber-800 hover:bg-amber-100 hover:border-amber-400 active:scale-95 transition shadow-sm"
                >
                  <Check className="h-3.5 w-3.5" />
                  {t("valid.ack")}
                  <kbd className="ml-1 text-[9px] bg-amber-200/70 rounded px-1 py-px font-mono">a</kbd>
                </button>
                <button
                  type="button"
                  onClick={() => onUpdateStatus(issue.id, "resolved")}
                  title="단축키: r"
                  className="inline-flex items-center gap-1 text-[11px] px-2.5 py-1.5 rounded border border-emerald-300 bg-emerald-50 text-emerald-800 hover:bg-emerald-100 hover:border-emerald-400 active:scale-95 transition shadow-sm"
                >
                  <CheckCircle2 className="h-3.5 w-3.5" />
                  {t("valid.resolve")}
                  <kbd className="ml-1 text-[9px] bg-emerald-200/70 rounded px-1 py-px font-mono">r</kbd>
                </button>
                <button
                  type="button"
                  onClick={() => onUpdateStatus(issue.id, "suppressed")}
                  title="단축키: s"
                  className="inline-flex items-center gap-1 text-[11px] px-2.5 py-1.5 rounded border border-slate-300 bg-slate-50 text-slate-700 hover:bg-slate-100 hover:border-slate-400 active:scale-95 transition shadow-sm"
                >
                  <EyeOff className="h-3.5 w-3.5" />
                  {t("valid.suppress")}
                  <kbd className="ml-1 text-[9px] bg-slate-200/70 rounded px-1 py-px font-mono">s</kbd>
                </button>
              </>
            ) : issue ? (
              <button
                type="button"
                onClick={() => onUpdateStatus(issue.id, "open")}
                className="inline-flex items-center gap-1 text-[11px] px-2.5 py-1.5 rounded border border-slate-300 bg-white hover:bg-slate-50 active:scale-95 transition shadow-sm"
              >
                {t("valid.reopen")}
              </button>
            ) : null}
            {issue?.file_id && (
              <Link
                href={`/projects/${projectId}/files?fileId=${issue.file_id}`}
                className="inline-flex items-center gap-1 text-[11px] px-2.5 py-1 rounded border bg-sky-50 text-sky-800 hover:bg-sky-100"
              >
                <ExternalLink className="h-3 w-3" />
                {t("valid.openInArtifacts")}
              </Link>
            )}
            {issue?.anchor && (
              <Link
                href={`/projects/${projectId}/traceability?focus=${encodeURIComponent(issue.anchor)}`}
                className="inline-flex items-center gap-1 text-[11px] px-2.5 py-1 rounded border bg-violet-50 text-violet-800 hover:bg-violet-100"
              >
                <GitBranch className="h-3 w-3" />
                {t("valid.openInTrace")}
              </Link>
            )}
          </div>
          <div className="flex items-center gap-2 mt-2 text-[11px] text-muted-foreground">
            <span>{headerLabel}</span>
            <span className="ml-auto flex gap-1">
              <Button
                size="sm"
                variant="ghost"
                className="h-6 px-2 text-[11px]"
                onClick={onPrev}
                title="k / ↑"
              >
                ↑ {t("valid.prev")}
              </Button>
              <Button
                size="sm"
                variant="ghost"
                className="h-6 px-2 text-[11px]"
                onClick={onNext}
                title="j / ↓"
              >
                ↓ {t("valid.next")}
              </Button>
            </span>
          </div>
        </SheetHeader>

        <div
          className="flex-1 overflow-auto border-t relative"
          ref={scrollContainerRef}
        >
          {/* Sticky resolution guide — stays pinned at the top of the preview. */}
          {issue && (
            <div
              ref={stickyGuideRef}
              className="sticky top-0 z-10 bg-background border-b px-4 py-2"
            >
              <ResolutionGuide issue={issue} projectId={projectId} />
            </div>
          )}
          <div className="px-4 py-3 space-y-3">
            {loading ? (
              <p className="text-xs text-muted-foreground">{t("valid.loading")}</p>
            ) : !issue?.file_id ? (
              <p className="text-xs text-muted-foreground italic">
                {t("valid.noPreview")}
              </p>
            ) : (
              <div ref={previewSectionRef}>
                <p className="text-[11px] font-semibold text-slate-700 mb-1.5">
                  📄 {fileName ?? t("valid.openFile")}
                </p>
                <div
                  className="prose prose-sm max-w-none rounded border bg-slate-50/40 px-3 py-2"
                  ref={previewRef}
                >
                  <MarkdownPreview content={content} />
                </div>
              </div>
            )}
          </div>
        </div>
      </SheetContent>
    </Sheet>
  );
}
