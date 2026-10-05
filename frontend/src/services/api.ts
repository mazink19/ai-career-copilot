import type {
  Resume,
  ResumeAnalysis,
  ResumeUploadResponse,
} from "../types/resume";

import type {
  User,
} from "../types/auth";

import type {
  JobMatchAnalysis,
  JobSearchResponse,
} from "../types/job";

const API_URL = "http://127.0.0.1:8000";

// ---------------- Authentication ---------------- //

function getToken(): string | null {
  return localStorage.getItem("access_token");
}

function isTokenExpired(token: string): boolean {
  try {
    const payload = JSON.parse(
      atob(token.split(".")[1])
    );
    console.log("Issued:", new Date(payload.iat * 1000));
    console.log("Expires:", new Date(payload.exp * 1000));
    console.log("Now:", new Date());
    if (!payload.exp) {
      return true;
    }

    return payload.exp * 1000 <= Date.now();
  } catch {
    return true;
  }
}

export function logout(): void {
  localStorage.removeItem("access_token");
  window.dispatchEvent(new Event("logout"));
}

export function isAuthenticated(): boolean {
  const token = getToken();

  if (!token) {
    return false;
  }

  if (isTokenExpired(token)) {
    logout();
    return false;
  }

  return true;
}

// ---------------- API Response Handling ---------------- //

async function handleResponse<T>(
  response: Response
): Promise<T> {
  if (response.status === 401) {
    logout();

    throw new Error(
      "Your session has expired. Please log in again."
    );
  }

  if (!response.ok) {
    let message = "Something went wrong.";

    try {
      const data = await response.json();

      if (typeof data.detail === "string") {
        message = data.detail;
      }
    } catch {
      // Response was not JSON.
    }

    throw new Error(message);
  }

  return response.json();
}

// ---------------- Authentication Headers ---------------- //

function authHeaders(): HeadersInit {
  const token = getToken();

  if (!token) {
    return {};
  }

  if (isTokenExpired(token)) {
    logout();
    return {};
  }

  return {
    Authorization: `Bearer ${token}`,
  };
}

/* ---------------- Resume ---------------- */

export async function uploadResume(
  file: File
): Promise<ResumeUploadResponse> {
  const formData = new FormData();

  formData.append("file", file);

  const response = await fetch(
    `${API_URL}/resumes/upload`,
    {
      method: "POST",
      headers: {
        ...authHeaders(),
      },
      body: formData,
    }
  );

  return handleResponse<ResumeUploadResponse>(response);
}

/* ---------------- Resume List ---------------- */

export async function getResumes(): Promise<Resume[]> {
  const response = await fetch(`${API_URL}/resumes`, {
    headers: {
      ...authHeaders(),
    },
  });

  return handleResponse<Resume[]>(response);
}

/* ---------------- Resume Analysis ---------------- */

export async function getResumeAnalysis(
  resumeId: number
): Promise<ResumeAnalysis> {
  const response = await fetch(
    `${API_URL}/resumes/${resumeId}/analysis`,
    {
      headers: {
        ...authHeaders(),
      },
    }
  );

  return handleResponse<ResumeAnalysis>(response);
}

/* ---------------- Resume Deletion ---------------- */

export async function deleteResume(
  resumeId: number
): Promise<void> {
  const response = await fetch(
    `${API_URL}/resumes/${resumeId}`,
    {
      method: "DELETE",
      headers: {
        ...authHeaders(),
      },
    }
  );

  if (response.status === 401) {
    logout();
    throw new Error(
      "Your session has expired. Please log in again."
    );
  }

  if (!response.ok) {
    throw new Error("Failed to delete resume.");
  }
}

/* ---------------- Jobs ---------------- */

export interface JobSearchParams {
  search?: string;
  company?: string;
  location?: string;
  workplace_type?: string;
  employment_type?: string;
  limit?: number;
  offset?: number;
}

export async function getJobs(
  params: JobSearchParams = {}
): Promise<JobSearchResponse> {
  const query = new URLSearchParams();

  if (params.search) {
    query.set("search", params.search);
  }

  if (params.company) {
    query.set("company", params.company);
  }

  if (params.location) {
    query.set("location", params.location);
  }

  if (params.workplace_type) {
    query.set("workplace_type", params.workplace_type);
  }

  if (params.employment_type) {
    query.set("employment_type", params.employment_type);
  }

  query.set("limit", String(params.limit ?? 20));
  query.set("offset", String(params.offset ?? 0));

  const response = await fetch(
    `${API_URL}/jobs?${query.toString()}`,
    {
      headers: {
        ...authHeaders(),
      },
    }
  );

  return handleResponse<JobSearchResponse>(response);
}

/* ---------------- Job Matching ---------------- */

export async function matchJob(
  jobId: number
): Promise<JobMatchAnalysis> {
  const response = await fetch(
    `${API_URL}/jobs/${jobId}/match`,
    {
      method: "POST",
      headers: {
        ...authHeaders(),
      },
    }
  );

  return handleResponse<JobMatchAnalysis>(response);
}

/* ---------------- User Profile ---------------- */
/* ---------------- User Profile ---------------- */

export async function getCurrentUser(): Promise<User> {
  const response = await fetch(`${API_URL}/auth/me`, {
    headers: {
      ...authHeaders(),
    },
  });

  return handleResponse<User>(response);
}

export async function updateProfile(
  firstName: string,
  lastName: string
): Promise<User> {
  const response = await fetch(`${API_URL}/auth/me`, {
    method: "PATCH",
    headers: {
      ...authHeaders(),
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      first_name: firstName,
      last_name: lastName,
    }),
  });

  return handleResponse<User>(response);
}