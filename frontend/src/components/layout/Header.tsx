"use client";

import Link from "next/link";
import { useAuthStore } from "@/stores/authStore";
import { useI18n } from "@/lib/i18n";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { useRouter } from "next/navigation";

export function Header() {
  const { user, logout } = useAuthStore();
  const router = useRouter();
  const { locale, setLocale, t } = useI18n();

  const initials = user?.display_name
    ?.split(" ")
    .map((n) => n[0])
    .join("")
    .toUpperCase()
    .slice(0, 2) || "?";

  return (
    <header className="flex h-12 items-center justify-between border-b border-border bg-card/95 glass px-5 sticky top-0 z-50">
      <Link href="/dashboard" className="flex items-center gap-2.5 group">
        <div className="h-7 w-7 rounded-md bg-primary flex items-center justify-center">
          <span className="text-xs font-bold text-primary-foreground tracking-tight">B</span>
        </div>
        <span className="text-[13px] font-semibold tracking-tight text-foreground">Dev.AI Spec Studio</span>
      </Link>
      <div className="flex items-center gap-2">
        <button
          className="flex items-center h-6 rounded-md bg-muted text-[10px] font-medium cursor-pointer select-none overflow-hidden"
          onClick={() => setLocale(locale === "ko" ? "en" : "ko")}
          title="Switch language"
        >
          <span className={`px-2 py-0.5 transition-all duration-150 ${locale === "ko" ? "bg-primary text-primary-foreground font-semibold" : "text-muted-foreground hover:text-foreground"}`}>
            KO
          </span>
          <span className={`px-2 py-0.5 transition-all duration-150 ${locale === "en" ? "bg-primary text-primary-foreground font-semibold" : "text-muted-foreground hover:text-foreground"}`}>
            EN
          </span>
        </button>
        <div className="h-4 w-px bg-border" />
        <DropdownMenu>
          <DropdownMenuTrigger>
            <Avatar className="h-7 w-7 cursor-pointer ring-1 ring-border hover:ring-primary/40 transition-all">
              <AvatarFallback className="bg-primary/8 text-primary text-[10px] font-semibold">{initials}</AvatarFallback>
            </Avatar>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end" className="w-56">
            <div className="flex items-center gap-3 p-3">
              <Avatar className="h-8 w-8">
                <AvatarFallback className="bg-primary/8 text-primary text-xs font-semibold">{initials}</AvatarFallback>
              </Avatar>
              <div className="flex flex-col leading-none">
                <p className="text-sm font-medium">{user?.display_name}</p>
                <p className="text-xs text-muted-foreground mt-1">{user?.email}</p>
              </div>
            </div>
            <DropdownMenuSeparator />
            <DropdownMenuItem onClick={() => router.push("/profile")}>
              {t("nav.profile")}
            </DropdownMenuItem>
            <DropdownMenuItem onClick={() => router.push("/settings")}>
              {t("nav.settings")}
            </DropdownMenuItem>
            {user?.is_admin && (
              <DropdownMenuItem onClick={() => router.push("/admin")}>
                {t("nav.admin")}
              </DropdownMenuItem>
            )}
            <DropdownMenuSeparator />
            <DropdownMenuItem onClick={() => { logout(); router.push("/login"); }} className="text-destructive focus:text-destructive">
              {t("auth.signOut")}
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </header>
  );
}
