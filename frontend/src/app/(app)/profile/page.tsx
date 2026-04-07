"use client";

import { useState } from "react";
import { useAuthStore } from "@/stores/authStore";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { toast } from "sonner";
import api from "@/lib/api";
import { useI18n } from "@/lib/i18n";

export default function ProfilePage() {
  const { user, fetchUser } = useAuthStore();
  const { t } = useI18n();

  const [displayName, setDisplayName] = useState(user?.display_name || "");
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [savingName, setSavingName] = useState(false);
  const [savingPassword, setSavingPassword] = useState(false);

  const handleSaveName = async () => {
    if (!displayName.trim()) {
      toast.error(t("profile.nameRequired"));
      return;
    }
    setSavingName(true);
    try {
      await api.put("/users/me", { display_name: displayName.trim() });
      await fetchUser();
      toast.success(t("profile.nameUpdated"));
    } catch {
      toast.error(t("profile.updateFailed"));
    } finally {
      setSavingName(false);
    }
  };

  const handleSavePassword = async () => {
    if (!newPassword) {
      toast.error(t("profile.newPasswordRequired"));
      return;
    }
    if (newPassword.length < 8) {
      toast.error(t("profile.passwordTooShort"));
      return;
    }
    if (newPassword !== confirmPassword) {
      toast.error(t("profile.passwordMismatch"));
      return;
    }
    setSavingPassword(true);
    try {
      await api.put("/users/me", { password: newPassword });
      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");
      toast.success(t("profile.passwordUpdated"));
    } catch {
      toast.error(t("profile.updateFailed"));
    } finally {
      setSavingPassword(false);
    }
  };

  if (!user) return <div className="p-6 text-muted-foreground">{t("common.loading")}</div>;

  return (
    <div className="p-6 max-w-2xl mx-auto space-y-6">
      <h2 className="text-2xl font-bold">{t("profile.title")}</h2>

      {/* Email (read-only) */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">{t("profile.accountInfo")}</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label>{t("profile.email")}</Label>
            <Input value={user.email} disabled className="bg-muted/50" />
            <p className="text-xs text-muted-foreground">{t("profile.emailReadonly")}</p>
          </div>
          <div className="space-y-2">
            <Label>{t("profile.joinDate")}</Label>
            <p className="text-sm text-muted-foreground">
              {new Date(user.created_at).toLocaleString("ko-KR", {
                timeZone: "Asia/Seoul",
                year: "numeric", month: "long", day: "numeric",
              })}
            </p>
          </div>
        </CardContent>
      </Card>

      {/* Display Name */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">{t("profile.changeName")}</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label>{t("profile.displayName")}</Label>
            <Input
              value={displayName}
              onChange={(e) => setDisplayName(e.target.value)}
              placeholder={t("profile.displayNamePlaceholder")}
            />
          </div>
          <Button onClick={handleSaveName} disabled={savingName}>
            {savingName ? t("common.loading") : t("common.save")}
          </Button>
        </CardContent>
      </Card>

      {/* Change Password */}
      <Card>
        <CardHeader>
          <CardTitle className="text-base">{t("profile.changePassword")}</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label>{t("profile.newPassword")}</Label>
            <Input
              type="password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              placeholder={t("profile.newPasswordPlaceholder")}
            />
          </div>
          <div className="space-y-2">
            <Label>{t("profile.confirmPassword")}</Label>
            <Input
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder={t("profile.confirmPasswordPlaceholder")}
            />
          </div>
          <Button onClick={handleSavePassword} disabled={savingPassword}>
            {savingPassword ? t("common.loading") : t("profile.updatePassword")}
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
