import { create } from "zustand";
import api from "@/lib/api";
import type { ChatSession, ChatMessage, ChatSessionDetail, Persona, Workflow } from "@/types";

interface MessagePage {
  messages: ChatMessage[];
  total: number;
  has_more: boolean;
}

interface ChatState {
  sessions: ChatSession[];
  currentSession: ChatSession | null;
  messages: ChatMessage[];
  totalMessages: number;
  hasMoreMessages: boolean;
  isLoadingMore: boolean;
  personas: Persona[];
  workflows: Workflow[];
  isStreaming: boolean;
  streamingContent: string;

  fetchSessions: (projectId: number) => Promise<void>;
  createSession: (projectId: number, persona: string, workflow?: string, title?: string) => Promise<ChatSession>;
  fetchSessionDetail: (projectId: number, sessionId: number) => Promise<void>;
  fetchRecentMessages: (projectId: number, sessionId: number, limit?: number) => Promise<void>;
  fetchOlderMessages: (projectId: number, sessionId: number, count?: number) => Promise<void>;
  deleteSession: (projectId: number, sessionId: number) => Promise<void>;
  addLocalMessage: (message: ChatMessage) => void;
  updateStreamingContent: (content: string) => void;
  setIsStreaming: (value: boolean) => void;
  clearStreaming: () => void;
  stopStreaming: () => void;

  fetchPersonas: () => Promise<void>;
  fetchWorkflows: () => Promise<void>;
}

export const useChatStore = create<ChatState>((set, get) => ({
  sessions: [],
  currentSession: null,
  messages: [],
  totalMessages: 0,
  hasMoreMessages: false,
  isLoadingMore: false,
  personas: [],
  workflows: [],
  isStreaming: false,
  streamingContent: "",

  fetchSessions: async (projectId) => {
    const res = await api.get<ChatSession[]>(`/projects/${projectId}/chat/sessions`);
    set({ sessions: res.data });
  },

  createSession: async (projectId, persona, workflow, title) => {
    const res = await api.post<ChatSession>(`/projects/${projectId}/chat/sessions`, {
      persona,
      workflow,
      title,
    });
    set((s) => ({ sessions: [res.data, ...s.sessions] }));
    return res.data;
  },

  fetchSessionDetail: async (projectId, sessionId) => {
    // Fetch session info only, messages loaded separately via pagination
    const res = await api.get<ChatSessionDetail>(`/projects/${projectId}/chat/sessions/${sessionId}`);
    set({ currentSession: res.data.session });
  },

  fetchRecentMessages: async (projectId, sessionId, limit = 5) => {
    const res = await api.get<MessagePage>(
      `/projects/${projectId}/chat/sessions/${sessionId}/messages?limit=${limit}`
    );
    set({
      messages: res.data.messages,
      totalMessages: res.data.total,
      hasMoreMessages: res.data.has_more,
    });
  },

  fetchOlderMessages: async (projectId, sessionId, count = 3) => {
    const { messages, isLoadingMore } = get();
    if (isLoadingMore || messages.length === 0) return;

    const oldestId = messages[0]?.id;
    if (!oldestId) return;

    set({ isLoadingMore: true });
    try {
      const res = await api.get<MessagePage>(
        `/projects/${projectId}/chat/sessions/${sessionId}/messages?limit=${count}&before_id=${oldestId}`
      );
      set((s) => ({
        messages: [...res.data.messages, ...s.messages],
        hasMoreMessages: res.data.has_more,
        isLoadingMore: false,
      }));
    } catch {
      set({ isLoadingMore: false });
    }
  },

  deleteSession: async (projectId, sessionId) => {
    await api.delete(`/projects/${projectId}/chat/sessions/${sessionId}`);
    set((s) => ({
      sessions: s.sessions.filter((s_) => s_.id !== sessionId),
      currentSession: s.currentSession?.id === sessionId ? null : s.currentSession,
    }));
  },

  addLocalMessage: (message) => {
    set((s) => ({
      messages: [...s.messages, message],
      totalMessages: s.totalMessages + 1,
    }));
  },

  _streamingBuffer: "",
  _streamingFlushTimer: null as ReturnType<typeof setTimeout> | null,

  updateStreamingContent: (content) => {
    const state = get() as any;
    state._streamingBuffer += content;

    // Throttle: flush buffer every 16ms (60fps) for smoother streaming
    if (!state._streamingFlushTimer) {
      const timer = setTimeout(() => {
        const s = get() as any;
        if (s._streamingBuffer) {
          set({ streamingContent: s.streamingContent + s._streamingBuffer });
          s._streamingBuffer = "";
        }
        s._streamingFlushTimer = null;
      }, 16);
      state._streamingFlushTimer = timer;
    }
  },

  setIsStreaming: (value) => set({ isStreaming: value }),

  clearStreaming: () => {
    const s = get() as any;
    s._streamingBuffer = "";
    if (s._streamingFlushTimer) { clearTimeout(s._streamingFlushTimer); s._streamingFlushTimer = null; }
    set({ streamingContent: "" });
  },
  stopStreaming: () => {
    const s = get() as any;
    // Flush remaining buffer before stopping
    const final = s.streamingContent + (s._streamingBuffer || "");
    s._streamingBuffer = "";
    if (s._streamingFlushTimer) { clearTimeout(s._streamingFlushTimer); s._streamingFlushTimer = null; }
    set({ streamingContent: "", isStreaming: false });
  },

  fetchPersonas: async () => {
    const res = await api.get<Persona[]>("/bmad/personas");
    set({ personas: res.data });
  },

  fetchWorkflows: async () => {
    const res = await api.get<Workflow[]>("/bmad/workflows");
    set({ workflows: res.data });
  },
}));
