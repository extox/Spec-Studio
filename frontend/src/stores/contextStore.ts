import { create } from "zustand";
import api from "@/lib/api";
import type { FileTreeItem, ProjectFile, ContextCategory } from "@/types";

interface ContextState {
  contextFiles: FileTreeItem[];
  categories: ContextCategory[];
  isLoading: boolean;

  fetchContextFiles: (projectId: number) => Promise<void>;
  fetchCategories: (projectId: number) => Promise<void>;
  createContextFile: (projectId: number, category: string, fileName: string, content: string) => Promise<ProjectFile>;
  updateContextFile: (projectId: number, fileId: number, content: string, fileName?: string) => Promise<ProjectFile>;
  deleteContextFile: (projectId: number, fileId: number) => Promise<void>;
}

export const useContextStore = create<ContextState>((set) => ({
  contextFiles: [],
  categories: [],
  isLoading: false,

  fetchContextFiles: async (projectId) => {
    set({ isLoading: true });
    try {
      const res = await api.get<FileTreeItem[]>(`/projects/${projectId}/context`);
      set({ contextFiles: res.data, isLoading: false });
    } catch {
      set({ isLoading: false });
    }
  },

  fetchCategories: async (projectId) => {
    try {
      const res = await api.get<ContextCategory[]>(`/projects/${projectId}/context/categories`);
      set({ categories: res.data });
    } catch {
      // ignore
    }
  },

  createContextFile: async (projectId, category, fileName, content) => {
    const res = await api.post<ProjectFile>(`/projects/${projectId}/context`, {
      category,
      file_name: fileName,
      content,
    });
    // Refresh file list
    const listRes = await api.get<FileTreeItem[]>(`/projects/${projectId}/context`);
    set({ contextFiles: listRes.data });
    return res.data;
  },

  updateContextFile: async (projectId, fileId, content, fileName) => {
    const body: Record<string, string> = { content };
    if (fileName) body.file_name = fileName;
    const res = await api.put<ProjectFile>(`/projects/${projectId}/context/${fileId}`, body);
    // Refresh file list
    const listRes = await api.get<FileTreeItem[]>(`/projects/${projectId}/context`);
    set({ contextFiles: listRes.data });
    return res.data;
  },

  deleteContextFile: async (projectId, fileId) => {
    await api.delete(`/projects/${projectId}/context/${fileId}`);
    set((s) => ({ contextFiles: s.contextFiles.filter((f) => f.id !== fileId) }));
  },
}));
