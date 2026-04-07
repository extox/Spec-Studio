"use client";

import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import type { ProjectMember } from "@/types";

interface MemberListProps {
  members: ProjectMember[];
  currentUserId?: number;
  isAdmin?: boolean;
  onRemove?: (userId: number) => void;
}

export function MemberList({ members, currentUserId, isAdmin, onRemove }: MemberListProps) {
  return (
    <div className="space-y-2">
      {members.map((member) => (
        <div key={member.id} className="flex items-center justify-between rounded-md border p-3">
          <div className="flex items-center gap-3">
            <Avatar className="h-8 w-8">
              <AvatarFallback>
                {member.display_name?.[0]?.toUpperCase() || "?"}
              </AvatarFallback>
            </Avatar>
            <div>
              <p className="text-sm font-medium">{member.display_name}</p>
              <p className="text-xs text-muted-foreground">{member.email}</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Badge variant={member.role === "owner" ? "default" : "secondary"}>
              {member.role}
            </Badge>
            {isAdmin && member.role !== "owner" && member.user_id !== currentUserId && onRemove && (
              <Button
                variant="ghost"
                size="sm"
                onClick={() => onRemove(member.user_id)}
              >
                Remove
              </Button>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
