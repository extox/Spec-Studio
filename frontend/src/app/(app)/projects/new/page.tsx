"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useProjectStore } from "@/stores/projectStore";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { toast } from "sonner";
import { useI18n } from "@/lib/i18n";

export default function NewProjectPage() {
  const router = useRouter();
  const { createProject } = useProjectStore();
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const { t } = useI18n();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      const project = await createProject(name, description || undefined);
      toast.success(t("projects.created"));
      router.push(`/projects/${project.id}`);
    } catch {
      toast.error(t("projects.createFailed"));
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex justify-center p-6">
      <Card className="w-full max-w-lg">
        <CardHeader>
          <CardTitle>{t("projects.createNew")}</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="name">{t("projects.name")}</Label>
              <Input
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder={t("projects.namePlaceholder")}
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="description">{t("projects.description")}</Label>
              <Textarea
                id="description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder={t("projects.descriptionPlaceholder")}
                rows={3}
              />
            </div>
            <div className="flex gap-3">
              <Button type="button" variant="outline" onClick={() => router.back()}>
                {t("common.cancel")}
              </Button>
              <Button type="submit" disabled={isLoading}>
                {isLoading ? t("projects.creating") : t("dashboard.createProject")}
              </Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
