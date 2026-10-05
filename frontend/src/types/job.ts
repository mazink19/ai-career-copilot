export interface Job {
  id: number;
  source: string;
  title: string;
  company: string;
  description: string;
  location: string | null;
  workplace_type: string | null;
  employment_type: string | null;
  application_url: string;
  job_url: string | null;
  published_at: string | null;
}

export interface JobMatchAnalysis {
  match_score: number;
  matched_skills: string[];
  missing_skills: string[];
  strengths: string[];
  recommendations: string[];
}

export interface JobSearchResponse {
  jobs: Job[];
  total: number;
  limit: number;
  offset: number;
}