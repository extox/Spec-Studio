"use client";

import { useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { useProjectStore } from "@/stores/projectStore";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { toast } from "sonner";
import { useI18n } from "@/lib/i18n";

export default function ProjectSettingsPage() {
  const params = useParams();
  const router = useRouter();
  const projectId = Number(params.projectId);
  const { currentProject, updateProject, updatePhase, deleteProject } = useProjectStore();
  const [name, setName] = useState(currentProject?.name || "");
  const [description, setDescription] = useState(currentProject?.description || "");
  const { t } = useI18n();

  const handleForbidden = (err: unknown) => {
    const status = (err as { response?: { status?: number } })?.response?.status;
    if (status === 403) {
      toast.error(t("projectSettings.ownerOnly"));
    }
    return status === 403;
  };

  const handleSave = async () => {
    try {
      await updateProject(projectId, { name, description });
      toast.success(t("projectSettings.updated"));
    } catch (err) {
      if (!handleForbidden(err)) toast.error(t("projectSettings.updateFailed"));
    }
  };

  const handlePhaseChange = async (phase: string | null) => {
    if (!phase) return;
    try {
      await updatePhase(projectId, phase);
      toast.success(t("projectSettings.phaseUpdated"));
    } catch (err) {
      if (!handleForbidden(err)) toast.error(t("projectSettings.phaseUpdateFailed"));
    }
  };

  const handleDelete = async () => {
    if (!confirm(t("projectSettings.deleteConfirm"))) return;
    try {
      await deleteProject(projectId);
      toast.success(t("projectSettings.deleted"));
      router.push("/projects");
    } catch (err) {
      if (!handleForbidden(err)) toast.error(t("projectSettings.deleteFailed"));
    }
  };

  return (
    <div className="p-6 space-y-6 max-w-2xl">
      <h3 className="text-lg font-semibold">{t("projectSettings.title")}</h3>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">{t("projectSettings.general")}</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label>{t("projectSettings.projectName")}</Label>
            <Input value={name} onChange={(e) => setName(e.target.value)} />
          </div>
          <div className="space-y-2">
            <Label>{t("projectSettings.description")}</Label>
            <Textarea value={description} onChange={(e) => setDescription(e.target.value)} rows={3} />
          </div>
          <Button onClick={handleSave}>{t("projectSettings.saveChanges")}</Button>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">{t("projectSettings.phase")}</CardTitle>
        </CardHeader>
        <CardContent>
          <Select value={currentProject?.phase} onValueChange={handlePhaseChange}>
            <SelectTrigger className="w-60">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="analysis">{t("phase.analysis")}</SelectItem>
              <SelectItem value="planning">{t("phase.planning")}</SelectItem>
              <SelectItem value="solutioning">{t("phase.solutioning")}</SelectItem>
              <SelectItem value="implementation">{t("phase.implementation")}</SelectItem>
            </SelectContent>
          </Select>
        </CardContent>
      </Card>

      <Card className="border-destructive">
        <CardHeader>
          <CardTitle className="text-base text-destructive">{t("projectSettings.dangerZone")}</CardTitle>
        </CardHeader>
        <CardContent>
          <Button variant="destructive" onClick={handleDelete}>
            {t("projectSettings.deleteProject")}
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
