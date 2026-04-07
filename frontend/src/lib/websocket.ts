import type { WSMessage } from "@/types";

const WS_BASE_URL = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000";

export class ChatWebSocket {
  private ws: WebSocket | null = null;
  private sessionId: number;
  private token: string;
  private listeners: Map<string, Set<(data: WSMessage) => void>> = new Map();
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private disposed = false;

  constructor(sessionId: number, token: string) {
    this.sessionId = sessionId;
    this.token = token;
  }

  connect(): Promise<void> {
    return new Promise((resolve, reject) => {
      if (this.disposed) {
        reject(new Error("WebSocket disposed"));
        return;
      }

      const url = `${WS_BASE_URL}/ws/chat/${this.sessionId}?token=${this.token}`;
      this.ws = new WebSocket(url);

      this.ws.onopen = () => {
        this.reconnectAttempts = 0;
        resolve();
      };

      this.ws.onmessage = (event) => {
        if (this.disposed) return;
        const data = JSON.parse(event.data) as WSMessage;
        const handlers = this.listeners.get(data.type);
        if (handlers) {
          handlers.forEach((handler) => handler(data));
        }
        // Also notify "all" listeners
        const allHandlers = this.listeners.get("*");
        if (allHandlers) {
          allHandlers.forEach((handler) => handler(data));
        }
      };

      this.ws.onclose = (event) => {
        if (this.disposed) return;
        if (event.code !== 1000 && this.reconnectAttempts < this.maxReconnectAttempts) {
          this.reconnectAttempts++;
          setTimeout(() => this.connect(), 1000 * this.reconnectAttempts);
        }
      };

      this.ws.onerror = () => {
        if (!this.disposed) {
          reject(new Error("WebSocket connection failed"));
        }
      };
    });
  }

  on(type: string, handler: (data: WSMessage) => void) {
    if (!this.listeners.has(type)) {
      this.listeners.set(type, new Set());
    }
    this.listeners.get(type)!.add(handler);
    return () => {
      this.listeners.get(type)?.delete(handler);
    };
  }

  sendChatMessage(content: string, fileIds?: string[]) {
    const msg: Record<string, unknown> = { type: "chat_message", content };
    if (fileIds && fileIds.length > 0) msg.file_ids = fileIds;
    this.send(msg);
  }

  sendWorkflowAction(action: string, data: Record<string, unknown> = {}) {
    this.send({ type: "workflow_action", action, data });
  }

  sendAPCAction(action: "advanced" | "party" | "continue", data: Record<string, unknown> = {}) {
    this.send({ type: "apc_action", action, data });
  }

  saveDeliverable(content: string, fileName: string, filePath?: string) {
    this.send({ type: "save_deliverable", content, file_name: fileName, file_path: filePath || "" });
  }

  switchPersona(personaId: string) {
    this.send({ type: "switch_persona", persona_id: personaId });
  }

  private send(data: Record<string, unknown>) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    }
  }

  disconnect() {
    this.disposed = true;
    this.maxReconnectAttempts = 0;
    if (this.ws) {
      this.ws.onopen = null;
      this.ws.onclose = null;
      this.ws.onerror = null;
      this.ws.onmessage = null;
      if (this.ws.readyState === WebSocket.OPEN || this.ws.readyState === WebSocket.CONNECTING) {
        this.ws.close(1000);
      }
    }
    this.listeners.clear();
  }
}
