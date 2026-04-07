// Auth
export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

// User
export interface User {
  id: number;
  email: string;
  display_name: string;
  is_admin: boolean;
  created_at: string;
}

// Project
export interface Project {
  id: number;
  name: string;
  description: string | null;
  phase: string;
  created_by: number;
  created_at: string;
  updated_at: string;
  member_count?: number;
  owner_name?: string;
}

export interface ProjectMember {
  id: number;
  user_id: number;
  project_id: number;
  role: string;
  invited_at: string;
  display_name?: string;
  email?: string;
}

// Chat
export interface ChatSession {
  id: number;
  project_id: number;
  persona: string;
  workflow: string | null;
  workflow_step: number;
  title: string | null;
  created_by: number;
  created_at: string;
  updated_at: string;
  message_count?: number;
}

export interface ChatMessage {
  id: number;
  session_id: number;
  role: "user" | "assistant" | "system";
  content: string;
  metadata_json?: string | null;
  created_at: string;
}

export interface ChatSessionDetail {
  session: ChatSession;
  messages: ChatMessage[];
}

// Files
export interface ProjectFile {
  id: number;
  project_id: number;
  file_path: string;
  file_name: string;
  file_type: string;
  content?: string | null;
  file_size: number | null;
  mime_type: string | null;
  created_by: number;
  updated_by: number | null;
  created_at: string;
  updated_at: string;
  session_id: number | null;
  version_label: string | null;
  updated_by_name: string | null;
}

export interface FileTreeItem {
  id: number;
  file_path: string;
  file_name: string;
  file_type: string;
  file_size: number | null;
  updated_at: string;
  version_label: string | null;
  updated_by_name: string | null;
}

export interface FileVersion {
  id: number;
  file_id: number;
  version_label: string;
  file_size: number | null;
  updated_by: number;
  updated_by_name: string | null;
  created_at: string;
}

// LLM
export interface LLMConfig {
  id: number;
  provider: string;
  model: string;
  base_url?: string | null;
  is_default: boolean;
  created_at: string;
  api_key_hint?: string;
}

export interface LLMProvider {
  id: string;
  name: string;
  models: string[];
  requires_base_url?: boolean;
}

// BMad
export interface PersonaCapability {
  code: string;
  name: string;
  description: string;
}

export interface Persona {
  id: string;
  name: string;
  description: string;
  phase: string;
  avatar: string;
  workflows: string[];
  capabilities?: PersonaCapability[];
}

export interface Workflow {
  id: string;
  name: string;
  persona: string;
  description: string;
  steps: WorkflowStep[];
  template: string | null;
  supports_apc?: boolean;
}

export interface WorkflowStep {
  step: number;
  name: string;
  description: string;
}

// WebSocket
export interface WSMessage {
  type: string;
  [key: string]: unknown;
}

export interface WSChatStreamStart {
  type: "chat_stream_start";
  message_id: string;
}

export interface WSChatStreamChunk {
  type: "chat_stream_chunk";
  message_id: string;
  content: string;
}

export interface WSChatStreamEnd {
  type: "chat_stream_end";
  message_id: string;
  full_content: string;
  metadata: Record<string, unknown>;
}

export interface WSDeliverableCreated {
  type: "deliverable_created";
  file: { id: number; file_path: string; file_name: string };
}

export interface WSWorkflowUpdate {
  type: "workflow_update";
  current_step: number;
  total_steps: number;
  step_name: string;
  step_description?: string;
}

export interface WSStepTransition {
  type: "step_transition";
  step: number;
  total_steps: number;
  step_name: string;
  step_description: string;
  message: string;
}

export interface WSError {
  type: "error";
  message: string;
}

// Context Expansion
export interface ContextCategory {
  id: string;
  name: string;
  name_en: string;
  description: string;
  icon: string;
}

export interface ContextValidationResult {
  valid: boolean;
  errors: string[];
  warnings: string[];
}
