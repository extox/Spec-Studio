import { create } from "zustand";
import api from "@/lib/api";
import type { Project, ProjectMember, FileTreeItem } from "@/types";

interface ProjectState {
  projects: Project[];
  currentProject: Project | null;
  members: ProjectMember[];
  files: FileTreeItem[];
  isLoading: boolean;

  fetchProjects: () => Promise<void>;
  fetchProject: (id: number) => Promise<void>;
  createProject: (name: string, description?: string) => Promise<Project>;
  updateProject: (id: number, data: Partial<Project>) => Promise<void>;
  deleteProject: (id: number) => Promise<void>;
  updatePhase: (id: number, phase: string) => Promise<void>;

  fetchMembers: (projectId: number) => Promise<void>;
  addMember: (projectId: number, email: string, role: string) => Promise<void>;
  removeMember: (projectId: number, userId: number) => Promise<void>;

  fetchFiles: (projectId: number) => Promise<void>;
}

export const useProjectStore = create<ProjectState>((set) => ({
  projects: [],
  currentProject: null,
  members: [],
  files: [],
  isLoading: false,

  fetchProjects: async () => {
    set({ isLoading: true });
    const res = await api.get<Project[]>("/projects");
    set({ projects: res.data, isLoading: false });
  },

  fetchProject: async (id) => {
    const res = await api.get<Project>(`/projects/${id}`);
    set({ currentProject: res.data });
  },

  createProject: async (name, description) => {
    const res = await api.post<Project>("/projects", { name, description });
    set((s) => ({ projects: [res.data, ...s.projects] }));
    return res.data;
  },

  updateProject: async (id, data) => {
    const res = await api.put<Project>(`/projects/${id}`, data);
    set((s) => ({
      projects: s.projects.map((p) => (p.id === id ? res.data : p)),
      currentProject: s.currentProject?.id === id ? res.data : s.currentProject,
    }));
  },

  deleteProject: async (id) => {
    await api.delete(`/projects/${id}`);
    set((s) => ({
      projects: s.projects.filter((p) => p.id !== id),
      currentProject: s.currentProject?.id === id ? null : s.currentProject,
    }));
  },

  updatePhase: async (id, phase) => {
    const res = await api.put<Project>(`/projects/${id}/phase`, { phase });
    set((s) => ({
      currentProject: s.currentProject?.id === id ? res.data : s.currentProject,
    }));
  },

  fetchMembers: async (projectId) => {
    const res = await api.get<ProjectMember[]>(`/projects/${projectId}/members`);
    set({ members: res.data });
  },

  addMember: async (projectId, email, role) => {
    const res = await api.post<ProjectMember>(`/projects/${projectId}/members`, {
      email,
      role,
    });
    set((s) => ({ members: [...s.members, res.data] }));
  },

  removeMember: async (projectId, userId) => {
    await api.delete(`/projects/${projectId}/members/${userId}`);
    set((s) => ({ members: s.members.filter((m) => m.user_id !== userId) }));
  },

  fetchFiles: async (projectId) => {
    const res = await api.get<FileTreeItem[]>(`/projects/${projectId}/files`);
    set({ files: res.data });
  },
}));
