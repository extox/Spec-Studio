"use client";

import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { useI18n } from "@/lib/i18n";

interface ImageUploadResult {
  url: string;
  providerFileId?: string;
}

interface UploadedImage {
  name: string;
  url: string;
  previewUrl: string;
  providerFileId?: string;
}

interface ChatInputProps {
  onSend: (message: string, fileIds?: string[]) => void;
  onStop?: () => void;
  onImageUpload?: (file: File) => Promise<ImageUploadResult | null>;
  disabled?: boolean;
  isStreaming?: boolean;
  placeholder?: string;
  insertText?: string;
  onInsertTextConsumed?: () => void;
}

export function ChatInput({ onSend, onStop, onImageUpload, disabled, isStreaming, placeholder, insertText, onInsertTextConsumed }: ChatInputProps) {
  const { t } = useI18n();
  const [message, setMessage] = useState("");
  const [images, setImages] = useState<UploadedImage[]>([]);
  const [uploading, setUploading] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const isComposingRef = useRef(false);

  useEffect(() => {
    textareaRef.current?.focus();
  }, []);

  useEffect(() => {
    if (!disabled) textareaRef.current?.focus();
  }, [message, disabled]);

  useEffect(() => {
    if (insertText) {
      setMessage((prev) => prev ? `${prev} ${insertText}` : insertText);
      onInsertTextConsumed?.();
      textareaRef.current?.focus();
    }
  }, [insertText, onInsertTextConsumed]);

  const handleSubmit = () => {
    const parts: string[] = [];
    if (message.trim()) parts.push(message.trim());
    // Append image markdown
    for (const img of images) {
      parts.push(`![${img.name}](${img.url})`);
    }
    const fullMessage = parts.join("\n");
    if (!fullMessage || disabled) return;

    const fileIds = images.map((img) => img.providerFileId).filter(Boolean) as string[];
    onSend(fullMessage, fileIds.length > 0 ? fileIds : undefined);
    setMessage("");
    setImages([]);
    // Revoke blob URLs
    images.forEach((img) => URL.revokeObjectURL(img.previewUrl));
    if (textareaRef.current) textareaRef.current.style.height = "auto";
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey && !isComposingRef.current) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleImageSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file || !onImageUpload) return;
    setUploading(true);
    try {
      const result = await onImageUpload(file);
      if (result) {
        const previewUrl = URL.createObjectURL(file);
        setImages((prev) => [...prev, { name: file.name, url: result.url, previewUrl, providerFileId: result.providerFileId }]);
      }
    } finally {
      setUploading(false);
      if (fileInputRef.current) fileInputRef.current.value = "";
    }
  };

  const removeImage = (index: number) => {
    setImages((prev) => {
      const removed = prev[index];
      if (removed) URL.revokeObjectURL(removed.previewUrl);
      return prev.filter((_, i) => i !== index);
    });
  };

  const hasContent = message.trim() || images.length > 0;

  return (
    <div className="border-t">
      {/* Image thumbnails */}
      {images.length > 0 && (
        <div className="flex gap-2 px-3 pt-3 pb-1 overflow-x-auto">
          {images.map((img, i) => (
            <div key={i} className="relative shrink-0 group">
              <img
                src={img.previewUrl}
                alt={img.name}
                className="h-16 w-16 object-cover rounded-lg border shadow-sm"
              />
              <button
                onClick={() => removeImage(i)}
                className="absolute -top-1.5 -right-1.5 h-5 w-5 rounded-full bg-destructive text-destructive-foreground flex items-center justify-center text-xs opacity-0 group-hover:opacity-100 transition-opacity shadow-sm"
                title={t("common.remove")}
              >
                ×
              </button>
              <p className="text-[8px] text-muted-foreground text-center mt-0.5 truncate w-16">{img.name}</p>
            </div>
          ))}
          {uploading && (
            <div className="h-16 w-16 rounded-lg border border-dashed flex items-center justify-center shrink-0">
              <span className="h-5 w-5 rounded-full border-2 border-primary border-t-transparent animate-spin" />
            </div>
          )}
        </div>
      )}

      {/* Input row */}
      <div className="flex gap-2 items-end p-3">
        {/* Image upload button */}
        {onImageUpload && (
          <>
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleImageSelect}
              className="hidden"
            />
            <button
              onClick={() => fileInputRef.current?.click()}
              disabled={disabled || uploading}
              className="shrink-0 h-10 w-10 flex items-center justify-center rounded-md hover:bg-muted transition-colors text-muted-foreground hover:text-foreground disabled:opacity-50"
              title={t("chat.uploadImage")}
            >
              {uploading && images.length === 0 ? (
                <span className="h-4 w-4 rounded-full border-2 border-primary border-t-transparent animate-spin" />
              ) : (
                <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              )}
            </button>
          </>
        )}
        <div className="flex-1 relative">
          <Textarea
            ref={textareaRef}
            value={message}
            onChange={(e) => {
              setMessage(e.target.value);
              const ta = e.target;
              ta.style.height = "auto";
              ta.style.height = Math.min(ta.scrollHeight, 130) + "px";
            }}
            onKeyDown={handleKeyDown}
            onCompositionStart={() => { isComposingRef.current = true; }}
            onCompositionEnd={() => { isComposingRef.current = false; }}
            placeholder={placeholder || t("voice.typePlaceholder")}
            className="min-h-[40px] max-h-[130px] resize-none overflow-y-auto"
            rows={1}
            disabled={disabled}
          />
        </div>
        {isStreaming ? (
          <Button variant="destructive" onClick={onStop}>
            <svg className="h-4 w-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <rect x="6" y="6" width="12" height="12" rx="1" strokeWidth={2} />
            </svg>
            {t("common.stop")}
          </Button>
        ) : (
          <Button onClick={handleSubmit} disabled={disabled || !hasContent}>
            {t("common.send")}
          </Button>
        )}
      </div>
    </div>
  );
}
