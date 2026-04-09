"use client";

import { useEffect, useState, useRef } from "react";
import dynamic from "next/dynamic";
import "@uiw/react-md-editor/markdown-editor.css";
import "@uiw/react-markdown-preview/markdown.css";

const MDEditor = dynamic(() => import("@uiw/react-md-editor"), { ssr: false });
import { useRouter } from "next/navigation";
import { useAuthStore } from "@/stores/authStore";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { toast } from "sonner";
import api from "@/lib/api";
import { useI18n } from "@/lib/i18n";

type Tab = "login-history" | "users" | "projects" | "llm-configs" | "guide";

export default function AdminPage() {
  const { user } = useAuthStore();
  const router = useRouter();
  const { t } = useI18n();
  const [tab, setTab] = useState<Tab>("login-history");

  if (!user?.is_admin) {
    return (
      <div className="p-6 text-center text-muted-foreground py-20">
        {t("admin.noAccess")}
      </div>
    );
  }

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <h2 className="text-2xl font-bold mb-6">{t("admin.title")}</h2>

      {/* Tabs */}
      <div className="flex gap-1 border-b mb-6">
        {(["login-history", "users", "projects", "llm-configs", "guide"] as Tab[]).map((t_) => (
          <button
            key={t_}
            onClick={() => setTab(t_)}
            className={`px-4 py-2 text-sm font-medium border-b-2 transition-colors -mb-px ${
              tab === t_
                ? "border-primary text-primary"
                : "border-transparent text-muted-foreground hover:text-foreground"
            }`}
          >
            {t(`admin.tab_${t_}`)}
          </button>
        ))}
      </div>

      {tab === "login-history" && <LoginHistoryTab t={t} />}
      {tab === "users" && <UsersTab t={t} />}
      {tab === "projects" && <ProjectsTab t={t} />}
      {tab === "llm-configs" && <LLMConfigsTab t={t} />}
      {tab === "guide" && <GuideManagementTab t={t} />}
    </div>
  );
}

// --- Login History ---
function LoginHistoryTab({ t }: { t: (k: string) => string }) {
  const [data, setData] = useState<{ items: any[]; total: number }>({ items: [], total: 0 });
  const [stats, setStats] = useState<{ chart: { date: string; count: number }[]; total_logins: number; unique_users: number } | null>(null);
  const [page, setPage] = useState(1);

  useEffect(() => {
    api.get(`/admin/login-history?page=${page}&per_page=15`).then((r) => setData(r.data));
  }, [page]);

  useEffect(() => {
    api.get("/admin/login-stats?days=14").then((r) => setStats(r.data));
  }, []);

  const maxCount = stats ? Math.max(...stats.chart.map((d) => d.count), 1) : 1;

  return (
    <div className="space-y-4">
      {/* Stats summary + chart */}
      {stats && (
        <div className="grid grid-cols-3 gap-4">
          <Card>
            <CardContent className="p-4 text-center">
              <p className="text-2xl font-bold">{stats.total_logins}</p>
              <p className="text-xs text-muted-foreground">{t("admin.totalLogins")} (14{t("admin.days")})</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-4 text-center">
              <p className="text-2xl font-bold">{stats.unique_users}</p>
              <p className="text-xs text-muted-foreground">{t("admin.uniqueUsers")}</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-4 text-center">
              <p className="text-2xl font-bold">{stats.total_logins > 0 ? (stats.total_logins / 14).toFixed(1) : 0}</p>
              <p className="text-xs text-muted-foreground">{t("admin.avgDaily")}</p>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Chart */}
      {stats && stats.chart.length > 0 && (
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm">{t("admin.loginChart")}</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-end gap-1 h-32">
              {stats.chart.map((d) => (
                <div key={d.date} className="flex-1 flex flex-col items-center gap-1" title={`${d.date}: ${d.count}`}>
                  <span className="text-[9px] text-muted-foreground">{d.count > 0 ? d.count : ""}</span>
                  <div
                    className="w-full rounded-t bg-primary/70 hover:bg-primary transition-colors min-h-[2px]"
                    style={{ height: `${Math.max((d.count / maxCount) * 100, 2)}%` }}
                  />
                  <span className="text-[8px] text-muted-foreground leading-tight">
                    {d.date.slice(5)}
                  </span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Login history table */}
      <Card>
        <CardHeader><CardTitle className="text-base">{t("admin.loginHistory")}</CardTitle></CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b text-left text-xs text-muted-foreground">
                  <th className="pb-2 pr-4">{t("admin.user")}</th>
                  <th className="pb-2 pr-4">{t("admin.email")}</th>
                  <th className="pb-2 pr-4">IP</th>
                  <th className="pb-2 pr-4">{t("admin.browser")}</th>
                  <th className="pb-2">{t("admin.time")}</th>
                </tr>
              </thead>
              <tbody>
                {data.items.map((h: any) => (
                  <tr key={h.id} className="border-b last:border-0">
                    <td className="py-2 pr-4 font-medium">{h.display_name}</td>
                    <td className="py-2 pr-4 text-muted-foreground">{h.email}</td>
                    <td className="py-2 pr-4 text-muted-foreground text-xs">{h.ip_address}</td>
                    <td className="py-2 pr-4 text-muted-foreground text-xs truncate max-w-[200px]">{h.user_agent}</td>
                    <td className="py-2 text-xs text-muted-foreground whitespace-nowrap">
                      {new Date(h.created_at).toLocaleString("ko-KR", {
                        timeZone: "Asia/Seoul",
                        year: "numeric", month: "2-digit", day: "2-digit",
                        hour: "2-digit", minute: "2-digit", second: "2-digit",
                      })}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          {data.total > 15 && (
            <div className="flex justify-center gap-2 mt-4">
              <Button size="sm" variant="outline" disabled={page <= 1} onClick={() => setPage(page - 1)}>{t("projects.prev")}</Button>
              <span className="text-sm text-muted-foreground self-center">{page}</span>
              <Button size="sm" variant="outline" onClick={() => setPage(page + 1)}>{t("projects.next")}</Button>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

// --- Users ---
function UsersTab({ t }: { t: (k: string) => string }) {
  const [users, setUsers] = useState<any[]>([]);
  const [search, setSearch] = useState("");

  const fetchUsers = () => {
    api.get(`/admin/users?search=${search}`).then((r) => setUsers(r.data));
  };

  useEffect(() => { fetchUsers(); }, []);

  const handleToggleAdmin = async (userId: number, current: boolean) => {
    await api.put(`/admin/users/${userId}`, { is_admin: !current });
    fetchUsers();
    toast.success(t("admin.userUpdated"));
  };

  const handleDelete = async (userId: number) => {
    if (!confirm(t("admin.deleteUserConfirm"))) return;
    try {
      await api.delete(`/admin/users/${userId}`);
      fetchUsers();
      toast.success(t("admin.userDeleted"));
    } catch {
      toast.error(t("admin.cannotDeleteSelf"));
    }
  };

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="text-base">{t("admin.userManagement")}</CardTitle>
          <div className="flex gap-2">
            <Input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && fetchUsers()}
              placeholder={t("admin.searchUser")}
              className="w-48 h-8 text-xs"
            />
            <Button size="sm" variant="outline" className="h-8" onClick={fetchUsers}>{t("projects.search")}</Button>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b text-left text-xs text-muted-foreground">
                <th className="pb-2 pr-4">ID</th>
                <th className="pb-2 pr-4">{t("admin.user")}</th>
                <th className="pb-2 pr-4">{t("admin.email")}</th>
                <th className="pb-2 pr-4">{t("admin.role")}</th>
                <th className="pb-2 pr-4">{t("admin.joinDate")}</th>
                <th className="pb-2">{t("admin.actions")}</th>
              </tr>
            </thead>
            <tbody>
              {users.map((u: any) => (
                <tr key={u.id} className="border-b last:border-0">
                  <td className="py-2 pr-4 text-muted-foreground">{u.id}</td>
                  <td className="py-2 pr-4 font-medium">{u.display_name}</td>
                  <td className="py-2 pr-4 text-muted-foreground">{u.email}</td>
                  <td className="py-2 pr-4">
                    <span className={`text-xs px-1.5 py-0.5 rounded ${u.is_admin ? "bg-primary/10 text-primary" : "bg-muted text-muted-foreground"}`}>
                      {u.is_admin ? "Admin" : "User"}
                    </span>
                  </td>
                  <td className="py-2 pr-4 text-xs text-muted-foreground whitespace-nowrap">
                    {new Date(u.created_at).toLocaleDateString("ko-KR", { timeZone: "Asia/Seoul" })}
                  </td>
                  <td className="py-2">
                    <div className="flex gap-1">
                      <Button size="sm" variant="ghost" className="h-6 text-[10px]" onClick={() => handleToggleAdmin(u.id, u.is_admin)}>
                        {u.is_admin ? t("admin.removeAdmin") : t("admin.makeAdmin")}
                      </Button>
                      <Button size="sm" variant="ghost" className="h-6 text-[10px] text-destructive" onClick={() => handleDelete(u.id)}>
                        {t("common.delete")}
                      </Button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </CardContent>
    </Card>
  );
}

// --- Projects ---
function ProjectsTab({ t }: { t: (k: string) => string }) {
  const [projects, setProjects] = useState<any[]>([]);
  const [expandedId, setExpandedId] = useState<number | null>(null);
  const [members, setMembers] = useState<any[]>([]);
  const [addEmail, setAddEmail] = useState("");
  const [addRole, setAddRole] = useState("member");

  const fetchProjects = () => {
    api.get("/admin/projects").then((r) => setProjects(r.data));
  };

  useEffect(() => { fetchProjects(); }, []);

  const handleDelete = async (id: number) => {
    if (!confirm(t("admin.deleteProjectConfirm"))) return;
    await api.delete(`/admin/projects/${id}`);
    fetchProjects();
    if (expandedId === id) setExpandedId(null);
    toast.success(t("admin.projectDeleted"));
  };

  const handlePhaseChange = async (id: number, phase: string) => {
    await api.put(`/admin/projects/${id}/phase`, { phase });
    fetchProjects();
    toast.success(t("admin.phaseUpdated"));
  };

  const toggleExpand = async (id: number) => {
    if (expandedId === id) {
      setExpandedId(null);
      return;
    }
    setExpandedId(id);
    const res = await api.get(`/admin/projects/${id}/members`);
    setMembers(res.data);
    setAddEmail("");
    setAddRole("member");
  };

  const handleAddMember = async (projectId: number) => {
    if (!addEmail.trim()) return;
    try {
      await api.post(`/admin/projects/${projectId}/members`, { email: addEmail.trim(), role: addRole });
      const res = await api.get(`/admin/projects/${projectId}/members`);
      setMembers(res.data);
      setAddEmail("");
      fetchProjects();
      toast.success(t("admin.memberAdded"));
    } catch {
      toast.error(t("admin.memberAddFailed"));
    }
  };

  const handleChangeRole = async (projectId: number, memberId: number, role: string) => {
    await api.put(`/admin/projects/${projectId}/members/${memberId}`, { role });
    const res = await api.get(`/admin/projects/${projectId}/members`);
    setMembers(res.data);
    toast.success(t("admin.userUpdated"));
  };

  const handleRemoveMember = async (projectId: number, memberId: number) => {
    if (!confirm(t("admin.removeMemberConfirm"))) return;
    await api.delete(`/admin/projects/${projectId}/members/${memberId}`);
    const res = await api.get(`/admin/projects/${projectId}/members`);
    setMembers(res.data);
    fetchProjects();
    toast.success(t("admin.memberRemoved"));
  };

  const phases = ["analysis", "planning", "solutioning", "implementation"];

  return (
    <Card>
      <CardHeader><CardTitle className="text-base">{t("admin.projectManagement")}</CardTitle></CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b text-left text-xs text-muted-foreground">
                <th className="pb-2 pr-4">ID</th>
                <th className="pb-2 pr-4">{t("admin.projectName")}</th>
                <th className="pb-2 pr-4">{t("admin.owner")}</th>
                <th className="pb-2 pr-4">{t("admin.phase")}</th>
                <th className="pb-2 pr-4">{t("admin.members")}</th>
                <th className="pb-2 pr-4">{t("admin.lastModified")}</th>
                <th className="pb-2">{t("admin.actions")}</th>
              </tr>
            </thead>
            <tbody>
              {projects.map((p: any) => (
                <>
                  <tr key={p.id} className="border-b last:border-0">
                    <td className="py-2 pr-4 text-muted-foreground">{p.id}</td>
                    <td className="py-2 pr-4 font-medium">{p.name}</td>
                    <td className="py-2 pr-4 text-muted-foreground">{p.owner_name}</td>
                    <td className="py-2 pr-4">
                      <select
                        value={p.phase}
                        onChange={(e) => handlePhaseChange(p.id, e.target.value)}
                        className="text-xs rounded border px-1.5 py-0.5 bg-transparent"
                      >
                        {phases.map((ph) => (
                          <option key={ph} value={ph}>{ph}</option>
                        ))}
                      </select>
                    </td>
                    <td className="py-2 pr-4">
                      <button
                        onClick={() => toggleExpand(p.id)}
                        className={`text-xs px-1.5 py-0.5 rounded transition-colors ${
                          expandedId === p.id ? "bg-primary text-primary-foreground" : "bg-muted text-muted-foreground hover:bg-muted/80"
                        }`}
                      >
                        {p.member_count} {t("admin.members")}
                      </button>
                    </td>
                    <td className="py-2 pr-4 text-xs text-muted-foreground whitespace-nowrap">
                      {new Date(p.updated_at).toLocaleString("ko-KR", { timeZone: "Asia/Seoul", month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" })}
                    </td>
                    <td className="py-2">
                      <Button size="sm" variant="ghost" className="h-6 text-[10px] text-destructive" onClick={() => handleDelete(p.id)}>
                        {t("common.delete")}
                      </Button>
                    </td>
                  </tr>
                  {/* Member management panel */}
                  {expandedId === p.id && (
                    <tr key={`members-${p.id}`}>
                      <td colSpan={7} className="py-3 px-4 bg-muted/20">
                        <div className="space-y-3">
                          <p className="text-xs font-semibold text-muted-foreground">{t("admin.memberList")}</p>
                          <div className="space-y-1">
                            {members.map((m: any) => (
                              <div key={m.id} className="flex items-center gap-3 text-xs py-1">
                                <span className="font-medium w-32 truncate">{m.display_name}</span>
                                <span className="text-muted-foreground w-40 truncate">{m.email}</span>
                                <select
                                  value={m.role}
                                  onChange={(e) => handleChangeRole(p.id, m.id, e.target.value)}
                                  className="rounded border px-1.5 py-0.5 bg-transparent text-xs"
                                >
                                  <option value="owner">owner</option>
                                  <option value="member">member</option>
                                </select>
                                <Button size="sm" variant="ghost" className="h-5 text-[10px] text-destructive" onClick={() => handleRemoveMember(p.id, m.id)}>
                                  {t("common.remove")}
                                </Button>
                              </div>
                            ))}
                          </div>
                          <div className="flex items-center gap-2 pt-2 border-t">
                            <Input
                              value={addEmail}
                              onChange={(e) => setAddEmail(e.target.value)}
                              placeholder={t("admin.addMemberEmail")}
                              className="h-7 text-xs w-48"
                              onKeyDown={(e) => e.key === "Enter" && handleAddMember(p.id)}
                            />
                            <select
                              value={addRole}
                              onChange={(e) => setAddRole(e.target.value)}
                              className="rounded border px-1.5 py-1 bg-transparent text-xs h-7"
                            >
                              <option value="member">member</option>
                            </select>
                            <Button size="sm" className="h-7 text-xs" onClick={() => handleAddMember(p.id)}>
                              {t("admin.addMember")}
                            </Button>
                          </div>
                        </div>
                      </td>
                    </tr>
                  )}
                </>
              ))}
            </tbody>
          </table>
        </div>
      </CardContent>
    </Card>
  );
}

// --- LLM Configs ---
function LLMConfigsTab({ t }: { t: (k: string) => string }) {
  const [configs, setConfigs] = useState<any[]>([]);

  const fetchConfigs = () => {
    api.get("/admin/llm-configs").then((r) => setConfigs(r.data));
  };

  useEffect(() => { fetchConfigs(); }, []);

  const handleDelete = async (id: number) => {
    if (!confirm(t("admin.deleteLLMConfirm"))) return;
    await api.delete(`/admin/llm-configs/${id}`);
    fetchConfigs();
    toast.success(t("admin.llmDeleted"));
  };

  return (
    <Card>
      <CardHeader><CardTitle className="text-base">{t("admin.llmManagement")}</CardTitle></CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b text-left text-xs text-muted-foreground">
                <th className="pb-2 pr-4">ID</th>
                <th className="pb-2 pr-4">{t("admin.user")}</th>
                <th className="pb-2 pr-4">{t("settings.provider")}</th>
                <th className="pb-2 pr-4">{t("settings.model")}</th>
                <th className="pb-2 pr-4">{t("settings.baseUrl")}</th>
                <th className="pb-2 pr-4">{t("common.default")}</th>
                <th className="pb-2">{t("admin.actions")}</th>
              </tr>
            </thead>
            <tbody>
              {configs.map((c: any) => (
                <tr key={c.id} className="border-b last:border-0">
                  <td className="py-2 pr-4 text-muted-foreground">{c.id}</td>
                  <td className="py-2 pr-4">{c.user_name} <span className="text-[10px] text-muted-foreground">({c.user_email})</span></td>
                  <td className="py-2 pr-4 font-medium">{c.provider}</td>
                  <td className="py-2 pr-4">{c.model}</td>
                  <td className="py-2 pr-4 text-xs text-muted-foreground truncate max-w-[200px]">{c.base_url || "-"}</td>
                  <td className="py-2 pr-4">{c.is_default ? "✓" : ""}</td>
                  <td className="py-2">
                    <Button size="sm" variant="ghost" className="h-6 text-[10px] text-destructive" onClick={() => handleDelete(c.id)}>
                      {t("common.delete")}
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </CardContent>
    </Card>
  );
}

// --- Guide Management ---
function GuideManagementTab({ t }: { t: (k: string) => string }) {
  const [pages, setPages] = useState<any[]>([]);
  const [editingPage, setEditingPage] = useState<any | null>(null);
  const [showPreview, setShowPreview] = useState(false);
  const [listCollapsed, setListCollapsed] = useState(false);
  const [translating, setTranslating] = useState(false);
  const [contentLang, setContentLang] = useState<"ko" | "en">("ko");
  const [translatingField, setTranslatingField] = useState<string | null>(null);

  const fetchPages = () => {
    api.get("/guide/admin/pages").then((r) => setPages(r.data));
  };

  useEffect(() => { fetchPages(); }, []);

  const handleCreate = async () => {
    const slug = prompt(t("admin.guideSlugPrompt"), "new-page");
    if (!slug) return;
    const titleVal = prompt(t("admin.guideTitlePrompt"), "New Page");
    if (!titleVal) return;
    await api.post("/guide/admin/pages", { slug, title: titleVal, group_name: "", content_ko: "", content_en: "", sort_order: pages.length });
    fetchPages();
    toast.success(t("admin.guideCreated"));
  };

  const handleSeedDefaults = async () => {
    try {
      const res = await api.post("/guide/admin/seed-defaults");
      fetchPages();
      toast.success(t("admin.guideSeeded", { count: String(res.data.created) }));
    } catch {
      toast.error(t("admin.guideSeedFailed"));
    }
  };

  const handleDuplicate = async (id: number) => {
    try {
      await api.post(`/guide/admin/pages/${id}/duplicate`);
      fetchPages();
      toast.success(t("admin.guideDuplicated"));
    } catch {
      toast.error(t("admin.guideDuplicateFailed"));
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm(t("admin.guideDeleteConfirm"))) return;
    await api.delete(`/guide/admin/pages/${id}`);
    if (editingPage?.id === id) setEditingPage(null);
    fetchPages();
    toast.success(t("admin.guideDeleted"));
  };

  const handleTogglePublish = async (page: any) => {
    await api.put(`/guide/admin/pages/${page.id}`, { is_published: !page.is_published });
    fetchPages();
    if (editingPage?.id === page.id) setEditingPage({ ...editingPage, is_published: !page.is_published });
  };

  const handleSave = async () => {
    if (!editingPage) return;
    await api.put(`/guide/admin/pages/${editingPage.id}`, {
      title: editingPage.title, title_en: editingPage.title_en,
      group_name: editingPage.group_name, group_name_en: editingPage.group_name_en,
      slug: editingPage.slug,
      content_ko: editingPage.content_ko, content_en: editingPage.content_en,
      sort_order: editingPage.sort_order, is_published: editingPage.is_published,
    });
    fetchPages();
    toast.success(t("admin.guideSaved"));
  };

  const handleImageUpload = async () => {
    const input = document.createElement("input");
    input.type = "file";
    input.accept = "image/*";
    input.onchange = async (e) => {
      const file = (e.target as HTMLInputElement).files?.[0];
      if (!file) return;
      const formData = new FormData();
      formData.append("file", file);
      try {
        const res = await api.post("/guide/admin/upload-image", formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });
        const url = res.data.url;
        const fullUrl = url.startsWith("http") ? url : url;
        const imgMd = `\n![${file.name}](${fullUrl})\n`;
        if (editingPage) {
          setEditingPage({ ...editingPage, content_ko: (editingPage.content_ko || "") + imgMd });
        }
        toast.success(t("admin.imageUploaded"));
      } catch {
        toast.error(t("admin.imageUploadFailed"));
      }
    };
    input.click();
  };

  const translateShort = async (text: string, field: "title_en" | "group_name_en") => {
    if (!text.trim()) return;
    setTranslatingField(field);
    try {
      const res = await api.post("/admin/translate-short", { text });
      setEditingPage((prev: any) => prev ? { ...prev, [field]: res.data.translated } : prev);
    } catch {
      toast.error(t("admin.translateFailed"));
    } finally {
      setTranslatingField(null);
    }
  };

  const handleTranslate = async () => {
    if (!editingPage?.content_ko) {
      toast.error(t("admin.translateNoContent"));
      return;
    }
    setTranslating(true);
    try {
      const res = await api.post("/admin/translate", { content: editingPage.content_ko });
      setEditingPage({ ...editingPage, content_en: res.data.translated });
      toast.success(t("admin.translateDone"));
    } catch (err: any) {
      const msg = err?.response?.data?.detail || t("admin.translateFailed");
      toast.error(msg);
    } finally {
      setTranslating(false);
    }
  };

  const openPreviewWindow = (lang: "ko" | "en" = "ko") => {
    if (!editingPage) return;
    const w = window.open("", "_blank", "width=900,height=700,scrollbars=yes,resizable=yes");
    if (!w) return;
    const content = lang === "ko" ? (editingPage.content_ko || "") : (editingPage.content_en || "");
    w.document.write(`<!DOCTYPE html><html><head><meta charset="utf-8"><title>${editingPage.title} - Preview</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@uiw/react-markdown-preview@5/dist/markdown.min.css">
<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"><\/script>
<style>
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;max-width:800px;margin:0 auto;padding:40px 24px;color:#1a1a2e;line-height:1.7;font-size:14px}
table{border-collapse:collapse;width:100%;border:1px solid #e2e8f0;margin:16px 0}
thead{background:#f1f5f9}
th,td{border:1px solid #e2e8f0;padding:8px 12px;text-align:left;font-size:13px}
tbody tr:nth-child(even){background:#f8fafc}
img{max-width:100%;border-radius:8px;margin:12px 0}
blockquote{border-left:4px solid #6366f1;margin:16px 0;padding:8px 16px;background:#f5f3ff}
</style></head><body><div id="content"></div>
<script>document.getElementById('content').innerHTML=marked.parse(${JSON.stringify(content)});<\/script>
</body></html>`);
    w.document.close();
  };

  return (
    <div className="flex gap-4 h-[calc(100vh-220px)]">
      {/* Page list */}
      <Card className={`shrink-0 flex flex-col transition-all duration-200 ${listCollapsed ? "w-10" : "w-64"}`}>
        {listCollapsed ? (
          <CardContent className="flex-1 p-0" />
        ) : (
          <>
            <CardHeader className="pb-2">
              <div className="space-y-1.5">
                <div className="flex items-center justify-between">
                  <CardTitle className="text-sm">{t("admin.guidePages")}</CardTitle>
                  <Button size="sm" variant="outline" className="h-6 text-[10px]" onClick={handleCreate}>
                    {t("admin.guideAddPage")}
                  </Button>
                </div>
                {pages.length === 0 && (
                  <Button size="sm" variant="default" className="w-full h-7 text-xs" onClick={handleSeedDefaults}>
                    {t("admin.guideSeedDefaults")}
                  </Button>
                )}
              </div>
            </CardHeader>
            <CardContent className="flex-1 overflow-auto p-2 space-y-1">
              {pages.map((p: any) => (
                <div key={p.id} className={`group flex items-center justify-between px-2 py-1.5 rounded text-xs cursor-pointer transition-colors ${editingPage?.id === p.id ? "bg-primary/10 text-primary" : "hover:bg-muted"}`} onClick={() => setEditingPage({ ...p })}>
                  <div className="min-w-0">
                    <p className="font-medium truncate">{p.title}</p>
                    <p className="text-[10px] text-muted-foreground">{p.slug}</p>
                  </div>
                  <div className="flex items-center gap-0.5 shrink-0 ml-1">
                    {!p.is_published && <span className="text-[9px] px-1 py-0.5 rounded bg-amber-100 text-amber-700">{t("admin.draft")}</span>}
                    <button onClick={(e) => { e.stopPropagation(); handleDuplicate(p.id); }} className="text-muted-foreground hover:text-foreground opacity-0 group-hover:opacity-100 transition-opacity" title={t("admin.guideDuplicate")}>
                      <svg className="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" /></svg>
                    </button>
                    <button onClick={(e) => { e.stopPropagation(); handleDelete(p.id); }} className="text-muted-foreground hover:text-destructive opacity-0 group-hover:opacity-100 transition-opacity">
                      <svg className="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>
                    </button>
                  </div>
                </div>
              ))}
            </CardContent>
          </>
        )}
        <button
          onClick={() => setListCollapsed(!listCollapsed)}
          className="flex items-center justify-center h-8 border-t hover:bg-muted transition-colors opacity-40 hover:opacity-100"
        >
          <svg className={`h-3 w-3 text-muted-foreground transition-transform ${listCollapsed ? "rotate-180" : ""}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 19l-7-7 7-7M18 19l-7-7 7-7" />
          </svg>
        </button>
      </Card>

      {/* Editor */}
      {editingPage ? (
        <Card className="flex-1 flex flex-col">
          <CardHeader className="pb-2">
            <div className="flex items-center justify-between">
              <CardTitle className="text-sm">{t("admin.guideEdit")}: {editingPage.title}</CardTitle>
              <div className="flex gap-1.5">
                <Button size="sm" variant="outline" className="h-7 text-xs" onClick={handleImageUpload}>{t("admin.uploadImage")}</Button>
                <Button size="sm" variant="outline" className="h-7 text-xs" onClick={() => handleTogglePublish(editingPage)}>{editingPage.is_published ? t("admin.unpublish") : t("admin.publish")}</Button>
                <Button size="sm" className="h-7 text-xs" onClick={handleSave}>{t("common.save")}</Button>
              </div>
            </div>
          </CardHeader>
          <CardContent className="flex-1 overflow-auto space-y-3 p-4">
            {/* Meta fields */}
            <div className="grid grid-cols-3 gap-2">
              <div><label className="text-[10px] text-muted-foreground">{t("admin.guideTitle")} (KO)</label><Input value={editingPage.title} onChange={(e) => setEditingPage({ ...editingPage, title: e.target.value })} className="h-7 text-xs" /></div>
              <div>
                <div className="flex items-center gap-1.5">
                  <label className="text-[10px] text-muted-foreground">{t("admin.guideTitle")} (EN)</label>
                  <button
                    onClick={() => translateShort(editingPage.title, "title_en")}
                    disabled={translatingField === "title_en"}
                    className="inline-flex items-center gap-0.5 text-[9px] px-1.5 py-0.5 rounded bg-primary/10 text-primary hover:bg-primary/20 transition-colors disabled:opacity-50"
                    title={t("admin.translateBtn")}
                  >
                    {translatingField === "title_en" ? (
                      <span className="h-2.5 w-2.5 rounded-full border border-primary border-t-transparent animate-spin" />
                    ) : (
                      <svg className="h-2.5 w-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" /></svg>
                    )}
                    AI
                  </button>
                </div>
                <Input value={editingPage.title_en || ""} onChange={(e) => setEditingPage({ ...editingPage, title_en: e.target.value })} className="h-7 text-xs" />
              </div>
              <div><label className="text-[10px] text-muted-foreground">Slug</label><Input value={editingPage.slug} onChange={(e) => setEditingPage({ ...editingPage, slug: e.target.value })} className="h-7 text-xs" /></div>
            </div>
            <div className="grid grid-cols-4 gap-2">
              <div><label className="text-[10px] text-muted-foreground">{t("admin.guideGroup")} (KO)</label><Input value={editingPage.group_name || ""} onChange={(e) => setEditingPage({ ...editingPage, group_name: e.target.value })} className="h-7 text-xs" /></div>
              <div>
                <div className="flex items-center gap-1.5">
                  <label className="text-[10px] text-muted-foreground">{t("admin.guideGroup")} (EN)</label>
                  <button
                    onClick={() => translateShort(editingPage.group_name || "", "group_name_en")}
                    disabled={translatingField === "group_name_en"}
                    className="inline-flex items-center gap-0.5 text-[9px] px-1.5 py-0.5 rounded bg-primary/10 text-primary hover:bg-primary/20 transition-colors disabled:opacity-50"
                    title={t("admin.translateBtn")}
                  >
                    {translatingField === "group_name_en" ? (
                      <span className="h-2.5 w-2.5 rounded-full border border-primary border-t-transparent animate-spin" />
                    ) : (
                      <svg className="h-2.5 w-2.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" /></svg>
                    )}
                    AI
                  </button>
                </div>
                <Input value={editingPage.group_name_en || ""} onChange={(e) => setEditingPage({ ...editingPage, group_name_en: e.target.value })} className="h-7 text-xs" />
              </div>
              <div><label className="text-[10px] text-muted-foreground">{t("admin.guideSortOrder")}</label><Input type="number" value={editingPage.sort_order} onChange={(e) => setEditingPage({ ...editingPage, sort_order: Number(e.target.value) })} className="h-7 text-xs" /></div>
            </div>

            {/* Language tabs + editor */}
            <div className="flex items-center justify-between">
              <div className="flex border-b">
                <button onClick={() => setContentLang("ko")} className={`px-4 py-1.5 text-xs font-medium border-b-2 -mb-px transition-colors ${contentLang === "ko" ? "border-primary text-primary" : "border-transparent text-muted-foreground hover:text-foreground"}`}>
                  한국어 (KO)
                </button>
                <button onClick={() => setContentLang("en")} className={`px-4 py-1.5 text-xs font-medium border-b-2 -mb-px transition-colors ${contentLang === "en" ? "border-primary text-primary" : "border-transparent text-muted-foreground hover:text-foreground"}`}>
                  English (EN)
                </button>
              </div>
              <div className="flex gap-1.5">
                {contentLang === "en" && (
                  <Button size="sm" variant="outline" className="h-6 text-[10px] gap-1" onClick={handleTranslate} disabled={translating || !editingPage?.content_ko}>
                    {translating ? (
                      <><span className="h-3 w-3 rounded-full border-2 border-primary border-t-transparent animate-spin" />{t("admin.translating")}</>
                    ) : (
                      <><svg className="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" /></svg>{t("admin.translateBtn")}</>
                    )}
                  </Button>
                )}
                <Button size="sm" variant="outline" className="h-6 text-[10px]" onClick={() => openPreviewWindow(contentLang)}>
                  {t("admin.guidePreviewPopup")}
                </Button>
              </div>
            </div>

            <div data-color-mode="light">
              {contentLang === "ko" ? (
                <MDEditor
                  key="editor-ko"
                  value={editingPage.content_ko || ""}
                  onChange={(val) => setEditingPage({ ...editingPage, content_ko: val || "" })}
                  height={450}
                  preview="live"
                />
              ) : (
                <MDEditor
                  key="editor-en"
                  value={editingPage.content_en || ""}
                  onChange={(val) => setEditingPage({ ...editingPage, content_en: val || "" })}
                  height={450}
                  preview="live"
                />
              )}
            </div>
          </CardContent>
        </Card>
      ) : (
        <Card className="flex-1 flex items-center justify-center"><p className="text-sm text-muted-foreground">{t("admin.guideSelectPage")}</p></Card>
      )}
    </div>
  );
}
