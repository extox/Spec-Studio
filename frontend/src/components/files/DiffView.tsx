"use client";

import { useMemo } from "react";
import { cn } from "@/lib/utils";

interface DiffViewProps {
  oldText: string;
  newText: string;
  oldLabel: string;
  newLabel: string;
}

interface DiffLine {
  type: "same" | "added" | "removed";
  content: string;
  oldLineNo: number | null;
  newLineNo: number | null;
}

function computeDiff(oldText: string, newText: string): DiffLine[] {
  const oldLines = oldText.split("\n");
  const newLines = newText.split("\n");

  // Simple LCS-based diff
  const m = oldLines.length;
  const n = newLines.length;

  // Build LCS table
  const dp: number[][] = Array.from({ length: m + 1 }, () => Array(n + 1).fill(0));
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      if (oldLines[i - 1] === newLines[j - 1]) {
        dp[i][j] = dp[i - 1][j - 1] + 1;
      } else {
        dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
      }
    }
  }

  // Backtrack to get diff
  const result: DiffLine[] = [];
  let i = m, j = n;
  const stack: DiffLine[] = [];

  while (i > 0 || j > 0) {
    if (i > 0 && j > 0 && oldLines[i - 1] === newLines[j - 1]) {
      stack.push({ type: "same", content: oldLines[i - 1], oldLineNo: i, newLineNo: j });
      i--; j--;
    } else if (j > 0 && (i === 0 || dp[i][j - 1] >= dp[i - 1][j])) {
      stack.push({ type: "added", content: newLines[j - 1], oldLineNo: null, newLineNo: j });
      j--;
    } else {
      stack.push({ type: "removed", content: oldLines[i - 1], oldLineNo: i, newLineNo: null });
      i--;
    }
  }

  stack.reverse();
  return stack;
}

export function DiffView({ oldText, newText, oldLabel, newLabel }: DiffViewProps) {
  const diffLines = useMemo(() => computeDiff(oldText, newText), [oldText, newText]);

  const addedCount = diffLines.filter((l) => l.type === "added").length;
  const removedCount = diffLines.filter((l) => l.type === "removed").length;

  return (
    <div className="h-full flex flex-col">
      <div className="flex items-center gap-3 px-4 py-2 border-b bg-muted/30 text-xs">
        <span className="font-medium text-red-600">{oldLabel}</span>
        <span className="text-muted-foreground">→</span>
        <span className="font-medium text-green-600">{newLabel}</span>
        <span className="ml-auto text-muted-foreground">
          <span className="text-green-600">+{addedCount}</span>
          {" "}
          <span className="text-red-600">-{removedCount}</span>
        </span>
      </div>
      <div className="flex-1 overflow-auto">
        <table className="w-full text-xs font-mono border-collapse">
          <tbody>
            {diffLines.map((line, idx) => (
              <tr
                key={idx}
                className={cn(
                  line.type === "added" && "bg-green-50 dark:bg-green-950/30",
                  line.type === "removed" && "bg-red-50 dark:bg-red-950/30",
                )}
              >
                <td className="select-none text-right px-2 py-0 text-muted-foreground/50 w-10 border-r">
                  {line.oldLineNo ?? ""}
                </td>
                <td className="select-none text-right px-2 py-0 text-muted-foreground/50 w-10 border-r">
                  {line.newLineNo ?? ""}
                </td>
                <td className="select-none px-1 py-0 w-5 text-center">
                  {line.type === "added" && <span className="text-green-600">+</span>}
                  {line.type === "removed" && <span className="text-red-600">-</span>}
                </td>
                <td className="px-2 py-0 whitespace-pre-wrap break-all">
                  {line.content}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
