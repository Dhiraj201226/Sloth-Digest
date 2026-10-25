/**
 * Sloth Digest — Frontend API Client
 * Strictly calls localhost backend at http://localhost:8000
 */

export interface SourceCitation {
  message_id: string;
  line_number: number;
  sender: string;
  timestamp: string;
  raw_text: string;
}

export interface ActionItem {
  id: string;
  description: string;
  assignee_target: string;
  urgency: string;
  source: SourceCitation;
}

export interface DeadlineItem {
  id: string;
  date_mentioned: string;
  event_description: string;
  source: SourceCitation;
}

export interface DigestResponse {
  id: string;
  created_at: string;
  chat_name: string;
  start_date?: string;
  end_date?: string;
  total_messages: number;
  safe_to_ignore_count: number;
  two_line_summary: string;
  action_items: ActionItem[];
  deadlines: DeadlineItem[];
  model_used: string;
  processing_duration_sec: number;
}

export interface SystemHealth {
  status: string;
  is_offline: boolean;
  ollama_connected: boolean;
  active_model: string;
  available_models: string[];
  host: string;
  error_message?: string;
}

export interface ProgressEvent {
  task_id: string;
  status: string;
  current_chunk: number;
  total_chunks: number;
  percent: number;
  elapsed_sec: number;
  estimated_remaining_sec: number;
  message: string;
}

export interface TidySuggestion {
  file_path: string;
  original_name: string;
  suggested_name: string;
  action: 'rename' | 'archive' | 'keep';
  reason: string;
}

export interface SyntheticSample {
  id: string;
  filename: string;
  size_bytes: number;
}

const getApiBase = (): string => {
  if (typeof window !== 'undefined') {
    // When served from FastAPI on port 8000, use same-origin relative path
    if (window.location.port === '8000' || !window.location.port) {
      return '/api';
    }
    // In dev mode (e.g. port 5173), match the current browser hostname
    const host = window.location.hostname || '127.0.0.1';
    return `http://${host}:8000/api`;
  }
  return '/api';
};

const API_BASE = getApiBase();

export async function fetchHealth(): Promise<SystemHealth> {

  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error("Health check failed");
  return res.json();
}

export async function fetchLatestDigest(): Promise<DigestResponse | null> {
  const res = await fetch(`${API_BASE}/digest/latest`);
  if (!res.ok) throw new Error("Failed to fetch latest digest");
  const data = await res.json();
  return data;
}

export async function uploadChat(file: File, modelName?: string): Promise<DigestResponse> {
  const formData = new FormData();
  formData.append("file", file);
  if (modelName) formData.append("model", modelName);

  const res = await fetch(`${API_BASE}/digest/upload`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({ detail: "Upload failed" }));
    throw new Error(errorData.detail || "Failed to digest chat");
  }
  return res.json();
}

export async function fetchSyntheticSamples(): Promise<SyntheticSample[]> {
  const res = await fetch(`${API_BASE}/synthetic/samples`);
  if (!res.ok) return [];
  return res.json();
}

export async function digestSyntheticSample(sampleId: string): Promise<DigestResponse> {
  const res = await fetch(`${API_BASE}/synthetic/digest/${sampleId}`, {
    method: "POST",
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({ detail: "Sample digestion failed" }));
    throw new Error(errorData.detail || "Failed to digest sample chat");
  }
  return res.json();
}

export async function fetchTidierSuggestions(): Promise<TidySuggestion[]> {
  const res = await fetch(`${API_BASE}/tidier/scan`);
  if (!res.ok) return [];
  return res.json();
}

export async function applyTidierSuggestions(suggestions: TidySuggestion[]): Promise<any> {
  const res = await fetch(`${API_BASE}/tidier/apply`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(suggestions),
  });
  return res.json();
}
