"use client";

import { useRef, useCallback, useEffect, useState } from "react";
import { cn } from "@/lib/utils";

interface YamlEditorProps {
  value: string;
  onChange?: (value: string) => void;
  readOnly?: boolean;
  placeholder?: string;
  className?: string;
}

export default function YamlEditor({ value, onChange, readOnly = false, placeholder, className }: YamlEditorProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const lineNumbersRef = useRef<HTMLDivElement>(null);
  const [lineCount, setLineCount] = useState(1);

  // Update line count
  useEffect(() => {
    const count = value ? value.split("\n").length : 1;
    setLineCount(count);
  }, [value]);

  // Sync scroll between line numbers and textarea
  const handleScroll = useCallback(() => {
    if (textareaRef.current && lineNumbersRef.current) {
      lineNumbersRef.current.scrollTop = textareaRef.current.scrollTop;
    }
  }, []);

  return (
    <div className={cn("flex h-full overflow-hidden", className)}>
      {/* Line numbers */}
      <div
        ref={lineNumbersRef}
        className="flex-shrink-0 overflow-hidden select-none bg-muted/30 border-r text-right"
        style={{ width: `${Math.max(String(lineCount).length * 8 + 16, 36)}px` }}
      >
        <div className="py-3 px-1.5">
          {Array.from({ length: lineCount }, (_, i) => (
            <div key={i + 1} className="text-[11px] leading-[1.6] font-mono text-muted-foreground/50 h-[17.6px]">
              {i + 1}
            </div>
          ))}
        </div>
      </div>
      {/* Textarea */}
      <textarea
        ref={textareaRef}
        value={value}
        onChange={onChange ? (e) => onChange(e.target.value) : undefined}
        onScroll={handleScroll}
        readOnly={readOnly}
        placeholder={placeholder}
        spellCheck={false}
        className={cn(
          "flex-1 py-3 px-3 font-mono text-[11px] leading-[1.6] bg-background resize-none focus:outline-none",
          readOnly && "cursor-default"
        )}
      />
    </div>
  );
}
