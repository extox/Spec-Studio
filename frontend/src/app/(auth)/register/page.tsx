"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuthStore } from "@/stores/authStore";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { toast } from "sonner";
import { useI18n } from "@/lib/i18n";

export default function RegisterPage() {
  const router = useRouter();
  const { register } = useAuthStore();
  const { t } = useI18n();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      await register(email, password, displayName);
      router.push("/dashboard");
    } catch {
      toast.error(t("auth.registerFailed"));
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-background p-4">
      <div className="fixed inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-primary/[0.03] via-transparent to-transparent pointer-events-none" />

      <Card className="relative w-full max-w-[400px] border-border shadow-lg">
        <CardHeader className="text-center space-y-3 pb-2 pt-8">
          <div className="mx-auto h-10 w-10 rounded-lg bg-primary flex items-center justify-center">
            <span className="text-sm font-bold text-primary-foreground">B</span>
          </div>
          <div className="space-y-1">
            <CardTitle className="text-lg font-semibold tracking-tight">{t("auth.getStarted")}</CardTitle>
            <CardDescription className="text-[13px]">{t("auth.createAccount")}</CardDescription>
          </div>
        </CardHeader>
        <CardContent className="pt-4 pb-8">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-1.5">
              <Label htmlFor="displayName" className="text-[12px] font-medium text-muted-foreground uppercase tracking-wide">{t("auth.displayName")}</Label>
              <Input
                id="displayName"
                type="text"
                placeholder={t("auth.displayNamePlaceholder")}
                value={displayName}
                onChange={(e) => setDisplayName(e.target.value)}
                required
                className="h-9"
              />
            </div>
            <div className="space-y-1.5">
              <Label htmlFor="email" className="text-[12px] font-medium text-muted-foreground uppercase tracking-wide">{t("auth.email")}</Label>
              <Input
                id="email"
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className="h-9"
              />
            </div>
            <div className="space-y-1.5">
              <Label htmlFor="password" className="text-[12px] font-medium text-muted-foreground uppercase tracking-wide">{t("auth.password")}</Label>
              <Input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                minLength={6}
                className="h-9"
              />
            </div>
            <Button type="submit" className="w-full h-9 mt-2 font-medium text-[13px]" disabled={isLoading}>
              {isLoading ? t("auth.creatingAccount") : t("auth.signUp")}
            </Button>
          </form>
          <p className="mt-5 text-center text-[13px] text-muted-foreground">
            {t("auth.hasAccount")}{" "}
            <Link href="/login" className="text-primary font-medium hover:underline underline-offset-4">
              {t("auth.signIn")}
            </Link>
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
