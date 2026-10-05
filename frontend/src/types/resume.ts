export interface Resume {
  id: number;
  file_name: string;
  uploaded_at: string;
  analysis_status:
    | "pending"
    | "analyzing"
    | "completed"
    | "failed"
    | null;
}
export interface ResumeAnalysis {
  id: number;
  resume_id: number;
  summary: string | null;
  skills: string[];
  experience: string[];
  education: string[];
  projects: string[];
  created_at: string;
  status: "pending" | "analyzing" | "completed" | "failed";
}

export interface ResumeUploadResponse {
  id: number;
  file_name: string;
  uploaded_at: string;
}