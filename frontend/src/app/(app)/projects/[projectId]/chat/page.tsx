"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { useChatStore } from "@/stores/chatStore";
import { PersonaSelector } from "@/components/chat/PersonaSelector";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import type { Persona, Workflow } from "@/types";
import { useI18n } from "@/lib/i18n";

export default function ChatSessionsPage() {
  const params = useParams();
  const router = useRouter();
  const projectId = Number(params.projectId);
  const { sessions, fetchSessions, createSession, deleteSession } = useChatStore();
  const [showSelector, setShowSelector] = useState(false);
  const { t } = useI18n();

  useEffect(() => {
    fetchSessions(projectId);
  }, [projectId, fetchSessions]);

  const handleCreateSession = async (persona: Persona, workflow?: Workflow) => {
    try {
      const title = workflow
        ? `${persona.name} - ${workflow.name}`
        : `Chat with ${persona.name}`;
      const session = await createSession(
        projectId,
        persona.id,
        workflow?.id,
        title,
      );
      router.push(`/projects/${projectId}/chat/${session.id}`);
    } catch {
      toast.error(t("chat.createFailed"));
    }
  };

  const handleDelete = async (sessionId: number) => {
    if (!confirm(t("chat.deleteConfirm"))) return;
    try {
      await deleteSession(projectId, sessionId);
      toast.success(t("chat.sessionDeleted"));
    } catch {
      toast.error(t("chat.deleteFailed"));
    }
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold">{t("chat.sessions")}</h3>
        <Button onClick={() => setShowSelector(!showSelector)}>
          {showSelector ? t("common.cancel") : t("chat.newChat")}
        </Button>
      </div>

      {showSelector && (
        <PersonaSelector onSelect={handleCreateSession} />
      )}

      <div className="space-y-2">
        {sessions.map((session) => (
          <Card
            key={session.id}
            className="cursor-pointer hover:shadow-sm transition-shadow"
          >
            <CardContent className="flex items-center justify-between p-4">
              <div
                className="flex-1"
                onClick={() => router.push(`/projects/${projectId}/chat/${session.id}`)}
              >
                <p className="font-medium text-sm">{session.title || t("chat.untitled")}</p>
                <div className="flex items-center gap-2 mt-1">
                  <Badge variant="outline" className="text-xs">{session.persona}</Badge>
                  {session.workflow && (
                    <Badge variant="secondary" className="text-xs">{session.workflow}</Badge>
                  )}
                  <span className="text-xs text-muted-foreground">
                    {session.message_count || 0} {t("chat.messages")}
                  </span>
                </div>
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={(e) => { e.stopPropagation(); handleDelete(session.id); }}
              >
                {t("common.delete")}
              </Button>
            </CardContent>
          </Card>
        ))}

        {sessions.length === 0 && !showSelector && (
          <div className="py-10 text-center text-muted-foreground">
            {t("chat.noSessions")}
          </div>
        )}
      </div>
    </div>
  );
}
