"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { useProjectStore } from "@/stores/projectStore";
import { useAuthStore } from "@/stores/authStore";
import { MemberList } from "@/components/project/MemberList";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { toast } from "sonner";
import { useI18n } from "@/lib/i18n";

export default function MembersPage() {
  const params = useParams();
  const projectId = Number(params.projectId);
  const { user } = useAuthStore();
  const { members, fetchMembers, addMember, removeMember } = useProjectStore();
  const [email, setEmail] = useState("");
  const [isAdding, setIsAdding] = useState(false);
  const { t } = useI18n();

  useEffect(() => {
    fetchMembers(projectId);
  }, [projectId, fetchMembers]);

  const currentMember = members.find((m) => m.user_id === user?.id);
  const isAdmin = currentMember?.role === "owner";

  const handleAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsAdding(true);
    try {
      await addMember(projectId, email, "member");
      setEmail("");
      toast.success(t("members.added"));
    } catch {
      toast.error(t("members.addFailed"));
    } finally {
      setIsAdding(false);
    }
  };

  const handleRemove = async (userId: number) => {
    try {
      await removeMember(projectId, userId);
      toast.success(t("members.removed"));
    } catch {
      toast.error(t("members.removeFailed"));
    }
  };

  return (
    <div className="p-6 space-y-6">
      <h3 className="text-lg font-semibold">{t("members.title")}</h3>

      {isAdmin && (
        <form onSubmit={handleAdd} className="flex gap-2">
          <Input
            placeholder={t("members.invitePlaceholder")}
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            type="email"
            required
          />
          <Button type="submit" disabled={isAdding}>
            {isAdding ? t("members.adding") : t("members.invite")}
          </Button>
        </form>
      )}

      <MemberList
        members={members}
        currentUserId={user?.id}
        isAdmin={isAdmin}
        onRemove={handleRemove}
      />
    </div>
  );
}
