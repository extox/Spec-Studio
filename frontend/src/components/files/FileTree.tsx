"use client";

import { useState, useRef } from "react";
import { cn } from "@/lib/utils";
import { useI18n } from "@/lib/i18n";
import type { FileTreeItem } from "@/types";

type SortMode = "name" | "date" | "size";

interface FileTreeProps {
  files: FileTreeItem[];
  selectedId?: number;
  onSelect: (file: FileTreeItem) => void;
  onDeleteFile?: (file: FileTreeItem) => void;
  onDeleteDirectory?: (dir: string, fileIds: number[]) => void;
  onRenameFile?: (file: FileTreeItem, newName: string) => void;
  onRenameDirectory?: (oldDir: string, newDir: string) => void;
  onMoveFile?: (file: FileTreeItem, newDir: string) => void;
}

export function FileTree({
  files, selectedId, onSelect,
  onDeleteFile, onDeleteDirectory,
  onRenameFile, onRenameDirectory, onMoveFile,
}: FileTreeProps) {
  const { t } = useI18n();
  const [confirmFileId, setConfirmFileId] = useState<number | null>(null);
  const [confirmDir, setConfirmDir] = useState<string | null>(null);
  const [renamingFileId, setRenamingFileId] = useState<number | null>(null);
  const [renamingDir, setRenamingDir] = useState<string | null>(null);
  const [renameValue, setRenameValue] = useState("");
  const [sortMode, setSortMode] = useState<SortMode>("name");
  const [dragOverDir, setDragOverDir] = useState<string | null>(null);
  const dragFileRef = useRef<FileTreeItem | null>(null);
  const renameInputRef = useRef<HTMLInputElement>(null);

  // Sort files
  const sortedFiles = [...files].sort((a, b) => {
    if (sortMode === "date") return new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime();
    if (sortMode === "size") return (b.file_size || 0) - (a.file_size || 0);
    return a.file_name.localeCompare(b.file_name);
  });

  // Group by directory
  const grouped: Record<string, FileTreeItem[]> = {};
  for (const file of sortedFiles) {
    const dir = file.file_path.includes("/")
      ? file.file_path.substring(0, file.file_path.lastIndexOf("/"))
      : ".";
    if (!grouped[dir]) grouped[dir] = [];
    grouped[dir].push(file);
  }

  const handleDeleteFile = (e: React.MouseEvent, file: FileTreeItem) => {
    e.stopPropagation();
    if (confirmFileId === file.id) {
      onDeleteFile?.(file);
      setConfirmFileId(null);
    } else {
      setConfirmFileId(file.id);
      setConfirmDir(null);
    }
  };

  const handleDeleteDir = (e: React.MouseEvent, dir: string, dirFiles: FileTreeItem[]) => {
    e.stopPropagation();
    if (confirmDir === dir) {
      onDeleteDirectory?.(dir, dirFiles.map((f) => f.id));
      setConfirmDir(null);
    } else {
      setConfirmDir(dir);
      setConfirmFileId(null);
    }
  };

  // Rename file
  const startRenameFile = (e: React.MouseEvent, file: FileTreeItem) => {
    e.stopPropagation();
    setRenamingFileId(file.id);
    setRenameValue(file.file_name);
    setRenamingDir(null);
    setTimeout(() => renameInputRef.current?.select(), 50);
  };

  const commitRenameFile = (file: FileTreeItem) => {
    const trimmed = renameValue.trim();
    if (trimmed && trimmed !== file.file_name) {
      onRenameFile?.(file, trimmed);
    }
    setRenamingFileId(null);
  };

  // Rename directory
  const startRenameDir = (e: React.MouseEvent, dir: string) => {
    e.stopPropagation();
    setRenamingDir(dir);
    setRenameValue(dir);
    setRenamingFileId(null);
    setTimeout(() => renameInputRef.current?.select(), 50);
  };

  const commitRenameDir = (oldDir: string) => {
    const trimmed = renameValue.trim();
    if (trimmed && trimmed !== oldDir) {
      onRenameDirectory?.(oldDir, trimmed);
    }
    setRenamingDir(null);
  };

  const handleRenameKeyDown = (e: React.KeyboardEvent, commit: () => void) => {
    if (e.key === "Enter") commit();
    if (e.key === "Escape") { setRenamingFileId(null); setRenamingDir(null); }
  };

  // Drag and drop
  const handleDragStart = (e: React.DragEvent, file: FileTreeItem) => {
    dragFileRef.current = file;
    e.dataTransfer.effectAllowed = "move";
  };

  const handleDragOver = (e: React.DragEvent, dir: string) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = "move";
    setDragOverDir(dir);
  };

  const handleDragLeave = () => {
    setDragOverDir(null);
  };

  const handleDrop = (e: React.DragEvent, targetDir: string) => {
    e.preventDefault();
    setDragOverDir(null);
    const file = dragFileRef.current;
    if (!file) return;
    const currentDir = file.file_path.includes("/")
      ? file.file_path.substring(0, file.file_path.lastIndexOf("/"))
      : ".";
    if (currentDir !== targetDir) {
      onMoveFile?.(file, targetDir);
    }
    dragFileRef.current = null;
  };

  const cycleSortMode = () => {
    setSortMode((prev) => {
      if (prev === "name") return "date";
      if (prev === "date") return "size";
      return "name";
    });
  };

  const sortLabel = sortMode === "name" ? t("files.sortName") : sortMode === "date" ? t("files.sortDate") : t("files.sortSize");

  return (
    <div className="space-y-1" onClick={() => { setConfirmFileId(null); setConfirmDir(null); }}>
      {/* Sort button */}
      {files.length > 1 && (
        <button
          onClick={cycleSortMode}
          className="flex items-center gap-1 px-2 py-1 text-[10px] text-muted-foreground hover:text-foreground transition-colors w-full"
        >
          <svg className="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4h13M3 8h9m-9 4h6m4 0l4-4m0 0l4 4m-4-4v12" />
          </svg>
          {sortLabel}
        </button>
      )}

      {/* Root drop zone */}
      <div
        onDragOver={(e) => handleDragOver(e, ".")}
        onDragLeave={handleDragLeave}
        onDrop={(e) => handleDrop(e, ".")}
        className={cn(dragOverDir === "." && "ring-2 ring-primary/30 rounded-md")}
      >
        {grouped["."]?.map((file) => (
          <FileRow
            key={file.id}
            file={file}
            selectedId={selectedId}
            confirmFileId={confirmFileId}
            renamingFileId={renamingFileId}
            renameValue={renameValue}
            renameInputRef={renameInputRef}
            indent={false}
            t={t}
            onSelect={onSelect}
            onDelete={onDeleteFile ? (e) => handleDeleteFile(e, file) : undefined}
            onStartRename={onRenameFile ? (e) => startRenameFile(e, file) : undefined}
            onCommitRename={() => commitRenameFile(file)}
            onRenameChange={setRenameValue}
            onRenameKeyDown={(e) => handleRenameKeyDown(e, () => commitRenameFile(file))}
            onDragStart={(e) => handleDragStart(e, file)}
          />
        ))}
      </div>

      {Object.entries(grouped)
        .filter(([dir]) => dir !== ".")
        .map(([dir, dirFiles]) => (
          <div
            key={dir}
            onDragOver={(e) => handleDragOver(e, dir)}
            onDragLeave={handleDragLeave}
            onDrop={(e) => handleDrop(e, dir)}
            className={cn(dragOverDir === dir && "ring-2 ring-primary/30 rounded-md")}
          >
            <div className="group flex items-center justify-between px-2 py-1.5 mt-1">
              <div className="flex items-center gap-1.5 flex-1 min-w-0">
                <svg className="h-4 w-4 text-muted-foreground shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
                </svg>
                {renamingDir === dir ? (
                  <input
                    ref={renameInputRef}
                    value={renameValue}
                    onChange={(e) => setRenameValue(e.target.value)}
                    onBlur={() => commitRenameDir(dir)}
                    onKeyDown={(e) => handleRenameKeyDown(e, () => commitRenameDir(dir))}
                    className="text-xs font-medium bg-transparent border-b border-primary outline-none w-full"
                    onClick={(e) => e.stopPropagation()}
                  />
                ) : (
                  <span className="text-xs font-medium text-muted-foreground truncate">{dir}</span>
                )}
              </div>
              <div className="flex gap-0.5 opacity-0 group-hover:opacity-100 transition-opacity">
                {onRenameDirectory && renamingDir !== dir && (
                  <button
                    onClick={(e) => startRenameDir(e, dir)}
                    className="text-muted-foreground hover:text-foreground px-1"
                    title={t("files.rename")}
                  >
                    <svg className="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </button>
                )}
                {onDeleteDirectory && (
                  <button
                    onClick={(e) => handleDeleteDir(e, dir, dirFiles)}
                    className={cn(
                      "text-xs px-1 rounded transition-colors",
                      confirmDir === dir
                        ? "bg-destructive text-destructive-foreground"
                        : "text-muted-foreground hover:text-destructive"
                    )}
                    title={confirmDir === dir ? t("files.confirmDelete") : t("files.deleteDir")}
                  >
                    {confirmDir === dir ? t("files.confirmDelete") : (
                      <svg className="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    )}
                  </button>
                )}
              </div>
            </div>
            {dirFiles.map((file) => (
              <FileRow
                key={file.id}
                file={file}
                selectedId={selectedId}
                confirmFileId={confirmFileId}
                renamingFileId={renamingFileId}
                renameValue={renameValue}
                renameInputRef={renameInputRef}
                indent={true}
                t={t}
                onSelect={onSelect}
                onDelete={onDeleteFile ? (e) => handleDeleteFile(e, file) : undefined}
                onStartRename={onRenameFile ? (e) => startRenameFile(e, file) : undefined}
                onCommitRename={() => commitRenameFile(file)}
                onRenameChange={setRenameValue}
                onRenameKeyDown={(e) => handleRenameKeyDown(e, () => commitRenameFile(file))}
                onDragStart={(e) => handleDragStart(e, file)}
              />
            ))}
          </div>
        ))}

      {files.length === 0 && (
        <p className="px-3 py-4 text-sm text-muted-foreground text-center">{t("files.noFiles")}</p>
      )}
    </div>
  );
}

// Extracted file row component
function FileRow({
  file, selectedId, confirmFileId, renamingFileId, renameValue, renameInputRef, indent, t,
  onSelect, onDelete, onStartRename, onCommitRename, onRenameChange, onRenameKeyDown, onDragStart,
}: {
  file: FileTreeItem;
  selectedId?: number;
  confirmFileId: number | null;
  renamingFileId: number | null;
  renameValue: string;
  renameInputRef: React.RefObject<HTMLInputElement | null>;
  indent: boolean;
  t: (key: string) => string;
  onSelect: (file: FileTreeItem) => void;
  onDelete?: (e: React.MouseEvent) => void;
  onStartRename?: (e: React.MouseEvent) => void;
  onCommitRename: () => void;
  onRenameChange: (v: string) => void;
  onRenameKeyDown: (e: React.KeyboardEvent) => void;
  onDragStart: (e: React.DragEvent) => void;
}) {
  return (
    <div
      draggable
      onDragStart={onDragStart}
      className={cn(
        "group flex items-center rounded-md transition-colors cursor-grab active:cursor-grabbing",
        indent && "ml-3",
        selectedId === file.id
          ? "bg-primary/10 text-primary"
          : "hover:bg-muted text-muted-foreground hover:text-foreground"
      )}
    >
      <button
        onClick={() => onSelect(file)}
        className="flex-1 text-left px-3 py-1.5 min-w-0"
      >
        <div className="flex items-center gap-2">
          <svg className="h-4 w-4 shrink-0 opacity-60" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          {renamingFileId === file.id ? (
            <input
              ref={renameInputRef}
              value={renameValue}
              onChange={(e) => onRenameChange(e.target.value)}
              onBlur={onCommitRename}
              onKeyDown={onRenameKeyDown}
              className="text-sm bg-transparent border-b border-primary outline-none w-full"
              onClick={(e) => e.stopPropagation()}
            />
          ) : (
            <span className="text-sm truncate">{file.file_name}</span>
          )}
        </div>
        {(file.version_label || file.updated_by_name) && renamingFileId !== file.id && (
          <div className="flex items-center gap-1.5 ml-6 mt-0.5">
            {file.version_label && (
              <span className="text-[9px] opacity-50 font-mono">v{file.version_label}</span>
            )}
            {file.updated_by_name && (
              <span className="text-[9px] opacity-40">{file.updated_by_name}</span>
            )}
          </div>
        )}
      </button>
      <div className="flex gap-0.5 opacity-0 group-hover:opacity-100 transition-opacity shrink-0 mr-1">
        {onStartRename && renamingFileId !== file.id && (
          <button
            onClick={onStartRename}
            className="px-1 py-0.5 text-muted-foreground hover:text-foreground"
            title={t("files.rename")}
          >
            <svg className="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
          </button>
        )}
        {onDelete && (
          <button
            onClick={onDelete}
            className={cn(
              "px-1 py-0.5 rounded transition-colors text-xs",
              confirmFileId === file.id
                ? "bg-destructive text-destructive-foreground"
                : "text-muted-foreground hover:text-destructive"
            )}
            title={confirmFileId === file.id ? t("files.confirmDelete") : t("common.delete")}
          >
            {confirmFileId === file.id ? t("files.confirmDelete") : (
              <svg className="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            )}
          </button>
        )}
      </div>
    </div>
  );
}
