"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import api from "@/lib/api";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import { useI18n, type TranslationKey } from "@/lib/i18n";
import { MarkdownPreview } from "@/components/editor/MarkdownPreview";

type StoryStatus = "todo" | "in_progress" | "review" | "done" | "blocked";

type StoryCard = {
  id: number;
  story_id: string;
  file_path: string;
  file_name: string;
  title: string;
  status: StoryStatus;
  file_status?: string | null;
  epic?: string | null;
  estimate?: string | null;
  owner?: string | null;
  updated_at?: string | null;
};

type Board = {
  columns: { status: StoryStatus; items: StoryCard[] }[];
  total: number;
};

const COLUMN_META: Record<StoryStatus, { labelKey: TranslationKey; color: string }> = {
  todo: { labelKey: "board.col.todo", color: "border-slate-300" },
  in_progress: { labelKey: "board.col.in_progress", color: "border-orange-400" },
  review: { labelKey: "board.col.review", color: "border-amber-400" },
  done: { labelKey: "board.col.done", color: "border-emerald-500" },
  blocked: { labelKey: "board.col.blocked", color: "border-rose-500" },
};

const STATUS_ORDER: StoryStatus[] = ["todo", "in_progress", "review", "done", "blocked"];

type GenerateResult = {
  created: { story_id: string; file_path: string; file_id: number; title: string }[];
  skipped: { story_id: string; reason: string }[];
  failed: { story_id: string; reason: string }[];
  error?: string;
};

type EpicSummary = {
  epic_num: number;
  epic_title: string;
  total: number;
  missing: number;
};

type EpicListResult = {
  epics: EpicSummary[];
  error?: string;
};

export default function StoryBoardPage() {
  const params = useParams();
  const projectId = Number(params.projectId);
  const { t } = useI18n();
  const [board, setBoard] = useState<Board | null>(null);
  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [epics, setEpics] = useState<EpicSummary[]>([]);
  const [showEpicMenu, setShowEpicMenu] = useState(false);
  const epicMenuRef = useRef<HTMLDivElement | null>(null);
  const [draggingId, setDraggingId] = useState<number | null>(null);
  const [dragOver, setDragOver] = useState<StoryStatus | null>(null);
  const [previewing, setPreviewing] = useState<StoryCard | null>(null);
  const [previewContent, setPreviewContent] = useState<string>("");
  const [previewLoading, setPreviewLoading] = useState(false);
  const router = useRouter();

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const res = await api.get<Board>(`/projects/${projectId}/story-board`);
      setBoard(res.data);
    } catch {
      toast.error(t("board.loadFailed"));
    } finally {
      setLoading(false);
    }
  }, [projectId, t]);

  const loadEpics = useCallback(async () => {
    try {
      const res = await api.get<EpicListResult>(
        `/projects/${projectId}/story-board/epics`,
      );
      setEpics(res.data.epics ?? []);
    } catch {
      setEpics([]);
    }
  }, [projectId]);

  useEffect(() => {
    load();
    loadEpics();
  }, [load, loadEpics]);

  useEffect(() => {
    if (!previewing) return;
    const handleKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") closePreview();
    };
    document.addEventListener("keydown", handleKey);
    return () => document.removeEventListener("keydown", handleKey);
  }, [previewing]);

  useEffect(() => {
    if (!showEpicMenu) return;
    const handlePointerDown = (e: MouseEvent) => {
      if (
        epicMenuRef.current &&
        !epicMenuRef.current.contains(e.target as Node)
      ) {
        setShowEpicMenu(false);
      }
    };
    const handleKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") setShowEpicMenu(false);
    };
    document.addEventListener("mousedown", handlePointerDown);
    document.addEventListener("keydown", handleKey);
    return () => {
      document.removeEventListener("mousedown", handlePointerDown);
      document.removeEventListener("keydown", handleKey);
    };
  }, [showEpicMenu]);

  const openPreview = async (story: StoryCard) => {
    setPreviewing(story);
    setPreviewContent("");
    setPreviewLoading(true);
    try {
      const res = await api.get<{ content: string | null }>(
        `/projects/${projectId}/files/${story.id}`,
      );
      setPreviewContent(res.data.content ?? "");
    } catch {
      toast.error(t("board.previewFailed"));
      setPreviewing(null);
    } finally {
      setPreviewLoading(false);
    }
  };

  const closePreview = () => {
    setPreviewing(null);
    setPreviewContent("");
  };

  const goEdit = (story: StoryCard) => {
    router.push(`/projects/${projectId}/files?fileId=${story.id}`);
  };

  const deleteStory = async (story: StoryCard) => {
    const ok = window.confirm(
      t("board.deleteConfirm", { id: story.story_id, title: story.title }),
    );
    if (!ok) return;
    try {
      await api.delete(`/projects/${projectId}/files/${story.id}`);
      toast.success(t("board.deleteOk", { id: story.story_id }));
      if (previewing?.id === story.id) closePreview();
      await Promise.all([load(), loadEpics()]);
    } catch {
      toast.error(t("board.deleteFailed"));
    }
  };

  const moveTo = async (story: StoryCard, next: StoryStatus) => {
    if (story.status === next) return;
    try {
      await api.patch(`/projects/${projectId}/story-board/${story.story_id}/status`, {
        status: next,
      });
      toast.success(t("board.moveOk", { id: story.story_id, status: t(COLUMN_META[next].labelKey) }));
      load();
    } catch {
      toast.error(t("board.moveFail"));
    }
  };

  const runGenerate = async (epicNum: number | null) => {
    if (generating) return;
    setShowEpicMenu(false);
    setGenerating(true);
    const BATCH = 3;
    const baseUrl =
      epicNum === null
        ? `/projects/${projectId}/story-board/generate-all`
        : `/projects/${projectId}/story-board/generate-epic/${epicNum}`;

    const totalCreated: GenerateResult["created"] = [];
    const totalSkipped: GenerateResult["skipped"] = [];
    const totalFailed: GenerateResult["failed"] = [];
    let stopReason: "done" | "error" | "exhausted" | "fail" = "done";
    let lastError: string | undefined;
    let safetyMaxLoops = 50; // hard cap to prevent runaway loops

    try {
      while (safetyMaxLoops-- > 0) {
        let res;
        try {
          res = await api.post<GenerateResult>(`${baseUrl}?limit=${BATCH}`);
        } catch {
          stopReason = "fail";
          break;
        }
        const { created, skipped, failed, error } = res.data;
        if (error) {
          lastError = error;
          stopReason = "error";
          break;
        }
        totalCreated.push(...created);
        totalFailed.push(...failed);
        // Skipped reasons we ALWAYS see again include "already exists" — that's
        // why we only count *new* progress to decide loop termination.
        const newSkipped = skipped.filter(
          (s) => s.reason !== "already exists" && s.reason !== "max_stories reached",
        );
        totalSkipped.push(...newSkipped);

        // Live progress toast.
        toast.info(
          t("board.generateProgress", {
            done: String(totalCreated.length),
          }),
        );

        // Reload board incrementally so the user sees cards appearing.
        await load();

        if (created.length === 0) {
          // Nothing new this round — either everything is done, or we're
          // hitting a non-progressing failure mode. Stop.
          stopReason = "exhausted";
          break;
        }
      }
    } finally {
      try {
        await Promise.all([load(), loadEpics()]);
      } catch {
        /* ignore */
      }
      setGenerating(false);
    }

    if (stopReason === "fail") {
      toast.error(t("board.generateFailed"));
      return;
    }
    if (stopReason === "error" && lastError) {
      toast.error(t("board.generateError", { reason: lastError }));
      return;
    }
    if (totalCreated.length === 0 && totalFailed.length === 0) {
      toast.info(
        t("board.generateNoneNeeded", { skipped: String(totalSkipped.length) }),
      );
      return;
    }
    toast.success(
      t("board.generateOk", {
        created: String(totalCreated.length),
        skipped: String(totalSkipped.length),
        failed: String(totalFailed.length),
      }),
    );
    if (totalFailed.length > 0) {
      const first = totalFailed[0];
      toast.error(`${first.story_id}: ${first.reason}`);
    }
  };

  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center justify-between border-b px-4 py-2">
        <div>
          <h1 className="text-base font-semibold">{t("board.title")}</h1>
          <p className="text-[11px] text-muted-foreground">{t("board.subtitle")}</p>
        </div>
        <div className="flex items-center gap-3">
          {board && (
            <span className="text-[11px] text-muted-foreground">
              {t("board.totalStories")}: <strong className="text-foreground">{board.total}</strong>
            </span>
          )}
          <div className="relative inline-flex" ref={epicMenuRef}>
            <Button
              size="sm"
              variant="default"
              onClick={() => runGenerate(null)}
              disabled={generating || loading}
              className="rounded-r-none"
            >
              {generating ? t("board.generating") : t("board.generateAll")}
            </Button>
            <Button
              size="sm"
              variant="default"
              onClick={() => setShowEpicMenu((v) => !v)}
              disabled={generating || loading || epics.length === 0}
              className="rounded-l-none border-l border-primary-foreground/20 px-1.5"
              title={t("board.generateByEpic")}
            >
              ▾
            </Button>
            {showEpicMenu && epics.length > 0 && (
              <div className="absolute right-0 top-full z-50 mt-1 w-64 rounded-md border bg-popover text-popover-foreground shadow-xl">
                <div className="px-3 py-1.5 text-[10px] font-semibold uppercase text-muted-foreground border-b bg-popover rounded-t-md">
                  {t("board.generateByEpic")}
                </div>
                <ul className="max-h-72 overflow-auto py-1 bg-popover rounded-b-md">
                  {epics.map((e) => (
                    <li key={e.epic_num}>
                      <button
                        type="button"
                        className="w-full text-left px-3 py-1.5 text-xs hover:bg-muted disabled:opacity-50 flex items-center justify-between gap-2"
                        disabled={e.missing === 0}
                        onClick={() => runGenerate(e.epic_num)}
                      >
                        <span className="truncate">
                          E{e.epic_num} · {e.epic_title}
                        </span>
                        <span className="shrink-0 text-[10px] text-muted-foreground">
                          {e.missing}/{e.total}
                        </span>
                      </button>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
          <Button size="sm" variant="outline" onClick={load} disabled={loading || generating}>
            {t("board.reload")}
          </Button>
        </div>
      </div>

      <div className="flex-1 overflow-hidden p-3 min-h-0">
        <div
          className="grid gap-3 h-full min-h-0"
          style={{ gridTemplateColumns: `repeat(${STATUS_ORDER.length}, minmax(220px, 1fr))` }}
        >
          {STATUS_ORDER.map((status) => {
            const col = board?.columns.find((c) => c.status === status);
            const items = col?.items ?? [];
            const meta = COLUMN_META[status];
            const isDropTarget = dragOver === status;
            return (
              <div
                key={status}
                className={`border-t-2 ${meta.color} bg-muted/30 rounded-md flex flex-col min-h-0 transition-colors ${
                  isDropTarget ? "ring-2 ring-primary/50 bg-muted/60" : ""
                }`}
                onDragOver={(e) => {
                  if (draggingId === null) return;
                  e.preventDefault();
                  e.dataTransfer.dropEffect = "move";
                  if (dragOver !== status) setDragOver(status);
                }}
                onDragLeave={(e) => {
                  // Only clear if leaving the column wrapper itself.
                  if (e.currentTarget === e.target) setDragOver(null);
                }}
                onDrop={(e) => {
                  e.preventDefault();
                  setDragOver(null);
                  if (draggingId === null) return;
                  const allItems =
                    board?.columns.flatMap((c) => c.items) ?? [];
                  const dropped = allItems.find((it) => it.id === draggingId);
                  setDraggingId(null);
                  if (dropped) moveTo(dropped, status);
                }}
              >
                <div className="sticky top-0 z-10 flex items-center justify-between bg-muted/60 backdrop-blur px-2 pt-2 pb-1.5 rounded-t-md">
                  <span className="text-xs font-semibold">{t(meta.labelKey)}</span>
                  <span className="text-[10px] text-muted-foreground">{items.length}</span>
                </div>
                <div className="flex-1 overflow-y-auto px-2 pb-2 space-y-2 min-h-0">
                  {items.length === 0 ? (
                    <p className="text-[10px] text-muted-foreground italic px-1">{t("board.empty")}</p>
                  ) : (
                    items.map((s) => (
                      <StoryCardView
                        key={s.id}
                        story={s}
                        dragging={draggingId === s.id}
                        onDragStart={() => setDraggingId(s.id)}
                        onDragEnd={() => {
                          setDraggingId(null);
                          setDragOver(null);
                        }}
                        onPreview={() => openPreview(s)}
                        onEdit={() => goEdit(s)}
                        onDelete={() => deleteStory(s)}
                      />
                    ))
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {previewing && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-6"
          onClick={closePreview}
        >
          <div
            className="bg-background rounded-lg shadow-2xl flex flex-col w-[min(90vw,900px)] h-[min(85vh,900px)] overflow-hidden"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between gap-3 border-b px-4 py-2.5">
              <div className="min-w-0 flex-1">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold text-primary">{previewing.story_id}</span>
                  <span className="text-[10px] text-muted-foreground truncate">
                    {previewing.file_path}
                  </span>
                </div>
                <h2 className="text-sm font-semibold truncate">{previewing.title}</h2>
              </div>
              <div className="flex items-center gap-2 shrink-0">
                <Button
                  size="sm"
                  variant="default"
                  onClick={() => {
                    const target = previewing;
                    closePreview();
                    if (target) goEdit(target);
                  }}
                >
                  {t("board.openInEditor")}
                </Button>
                <Button size="sm" variant="ghost" onClick={closePreview}>
                  ✕
                </Button>
              </div>
            </div>
            <div className="flex-1 overflow-auto px-6 py-4">
              {previewLoading ? (
                <p className="text-sm text-muted-foreground">{t("board.previewLoading")}</p>
              ) : previewContent ? (
                <MarkdownPreview content={previewContent} />
              ) : (
                <p className="text-sm text-muted-foreground">{t("board.previewEmpty")}</p>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function StoryCardView({
  story,
  dragging,
  onDragStart,
  onDragEnd,
  onPreview,
  onEdit,
  onDelete,
}: {
  story: StoryCard;
  dragging: boolean;
  onDragStart: () => void;
  onDragEnd: () => void;
  onPreview: () => void;
  onEdit: () => void;
  onDelete: () => void;
}) {
  const { t } = useI18n();
  return (
    <div
      draggable
      onDragStart={(e) => {
        e.dataTransfer.effectAllowed = "move";
        e.dataTransfer.setData("text/plain", String(story.id));
        onDragStart();
      }}
      onDragEnd={onDragEnd}
      className={`group rounded-md border bg-background p-2 shadow-sm cursor-grab active:cursor-grabbing transition-opacity ${
        dragging ? "opacity-40" : "hover:shadow-md"
      }`}
    >
      <div className="flex items-start justify-between gap-1">
        <span className="text-[10px] font-bold text-primary">{story.story_id}</span>
        {story.estimate && (
          <span className="text-[9px] text-muted-foreground">{story.estimate}</span>
        )}
      </div>
      <div className="mt-1 text-xs font-medium leading-snug line-clamp-2">{story.title}</div>
      {story.file_status && (
        <div className="mt-1 text-[9px] text-muted-foreground">
          status: <code>{story.file_status}</code>
        </div>
      )}
      {story.owner && (
        <div className="mt-1 text-[10px] text-muted-foreground">@{story.owner}</div>
      )}
      <div
        className="mt-2 flex items-center gap-1 opacity-60 group-hover:opacity-100 transition-opacity"
        onMouseDown={(e) => e.stopPropagation()}
      >
        <button
          type="button"
          onClick={(e) => {
            e.stopPropagation();
            onPreview();
          }}
          className="text-[10px] px-1.5 py-0.5 rounded border border-border hover:bg-muted text-muted-foreground hover:text-foreground transition-colors"
          title={t("board.preview")}
        >
          {t("board.preview")}
        </button>
        <button
          type="button"
          onClick={(e) => {
            e.stopPropagation();
            onEdit();
          }}
          className="text-[10px] px-1.5 py-0.5 rounded border border-border hover:bg-muted text-muted-foreground hover:text-foreground transition-colors"
          title={t("board.edit")}
        >
          {t("board.edit")}
        </button>
        <button
          type="button"
          onClick={(e) => {
            e.stopPropagation();
            onDelete();
          }}
          className="ml-auto text-[10px] px-1.5 py-0.5 rounded border border-destructive/40 text-destructive hover:bg-destructive hover:text-destructive-foreground transition-colors"
          title={t("board.delete")}
        >
          {t("board.delete")}
        </button>
      </div>
    </div>
  );
}
