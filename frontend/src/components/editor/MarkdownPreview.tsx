"use client";

import dynamic from "next/dynamic";
import "@uiw/react-markdown-preview/markdown.css";

const MDPreview = dynamic(
  () => import("@uiw/react-md-editor").then((mod) => mod.default.Markdown),
  { ssr: false }
);

interface MarkdownPreviewProps {
  content: string;
  onBoldClick?: (text: string) => void;
}

function cleanFileMarkers(text: string): string {
  return text
    .replace(/<!--\s*SAVE_FILE:\s*.+?\s*-->\s*\n?/g, "")
    .replace(/\n?\s*<!--\s*END_FILE\s*-->/g, "");
}

export function MarkdownPreview({ content, onBoldClick }: MarkdownPreviewProps) {
  const APC_PATTERN = /^\[?[APRC]\]?\s*(Advanced|Party|Propose|Continue|Elicitation|Mode)/i;

  const handleClick = (e: React.MouseEvent) => {
    if (!onBoldClick) return;
    const target = e.target as HTMLElement;
    if (target.tagName === "STRONG" || target.closest("strong")) {
      const strong = target.tagName === "STRONG" ? target : target.closest("strong");
      if (strong) {
        const text = strong.textContent || "";
        if (APC_PATTERN.test(text)) return;
        onBoldClick(text);
      }
    }
  };

  // Mark APC bold elements to exclude from click styling
  const applyApcExclusion = (el: HTMLDivElement | null) => {
    if (!el || !onBoldClick) return;
    el.querySelectorAll("strong").forEach((strong) => {
      if (APC_PATTERN.test(strong.textContent || "")) {
        strong.setAttribute("data-no-click", "true");
      } else {
        strong.removeAttribute("data-no-click");
      }
    });
  };

  return (
    <div
      ref={applyApcExclusion}
      data-color-mode="light"
      onClick={handleClick}
      className={onBoldClick ? "[&_strong:not([data-no-click])]:cursor-pointer [&_strong:not([data-no-click])]:hover:text-primary [&_strong:not([data-no-click])]:hover:underline [&_strong]:transition-colors" : ""}
    >
      <MDPreview source={cleanFileMarkers(content)} />
    </div>
  );
}
