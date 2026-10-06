
# AI Career Copilot

[![CI](https://img.shields.io/badge/ci-pending-lightgrey)](https://github.com/your-org/your-repo/actions)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](#)

# AI Career Copilot

> An AI-powered career platform for resume analysis, job discovery, and resume-to-job matching.

## Overview

AI Career Copilot helps users understand their resumes, discover relevant job opportunities, and evaluate how well their profile matches specific jobs.

The project combines a FastAPI backend, React frontend, LLM-powered workflows, automated job ingestion, MCP tools, evaluation, testing, Docker, CI/CD, and cloud deployment.

Users can:

- Create an account and authenticate securely
- Upload a PDF resume
- Analyze their resume using AI
- Extract skills, experience, education, and projects
- Discover available job opportunities
- Search and filter jobs
- Match their resume against a specific job
- View matched and missing skills
- Understand why a job matches their profile

Jobs are automatically collected from external job-board platforms and normalized before being stored in PostgreSQL.

---

## Features

### Resume Analysis

Upload a PDF resume and generate structured information including:

- Resume summary
- Skills
- Experience
- Education
- Projects

The LLM output is validated using structured schemas before being stored.

### Job Discovery

Jobs are collected from multiple external job sources:

- Greenhouse
- Lever
- Ashby

Each provider has its own adapter, while all jobs are converted into a common internal schema.

### Job Search

Users can search and filter active jobs by:

- Keywords
- Company
- Location
- Workplace type
- Employment type

Pagination is supported for large job collections.

### Resume-to-Job Matching

A user's resume can be matched against a specific job.

The matching result includes:

- Match score
- Matched skills
- Missing skills
- Match explanation

The matching workflow is implemented using LangGraph and an LLM.

### MCP Integration

The project exposes career-related functionality through the Model Context Protocol.

Available tools:

- `search_jobs`
- `get_job`
- `match_job_to_resume`

The MCP layer reuses the existing application services rather than implementing separate business logic.

### Automated Job Ingestion

A background worker periodically fetches jobs from configured providers.

The ingestion pipeline is:

```text
External Job Source
        ↓
Source Adapter
        ↓
Normalize
        ↓
Validate
        ↓
Upsert
        ↓
PostgreSQL

## Features
- Resume ingestion (file + URL sources)
- Modular analyzers and prompts under `backend/app/ai/`
- Persistent storage with Postgres and Alembic migrations
- Background workers for long-running analysis jobs
- Test suites for core services and integrations

## QuickStart

Clone the repo and follow backend and frontend steps below.

Backend (development)

```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file (see `.env.example`) or set environment variables directly.

Run database migrations:

```powershell
alembic -c backend/alembic.ini upgrade head
```

Start the backend (development mode):

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Frontend (development)

```bash
cd frontend
npm install
npm run dev
```

Run full stack with Docker Compose (optional):

```bash
docker-compose up --build
```

## Usage examples

Upload a resume (example):

```bash
curl -X POST "http://localhost:8000/resumes/upload" -F "file=@/path/to/resume.pdf"
```

Trigger analysis for a resume (example):

```bash
curl -X POST "http://localhost:8000/analyses/123/run"
```

Browse the FastAPI OpenAPI UI at `http://localhost:8000/docs` when the backend is running.

## Environment variables
See `.env.example` in the repository root for common variables. Important ones:
- `DATABASE_URL` — Postgres connection string
- `REDIS_URL` — Redis connection for workers (optional)
- `SECRET_KEY` — application secret used for tokens/sessions
- `AI_PROVIDER` and provider-specific keys (e.g., `OPENAI_API_KEY`)

## Running tests

Run backend tests:

```bash
cd backend
pytest -q
```

Integration tests are available under `tests/`.

## Contributing

- Fork the repo and open a PR against `main`.
- Write tests for new features and follow existing style.
- For large changes, open an issue first to discuss design and migration impact.

See also: add a `CONTRIBUTING.md` for contribution guidelines (I can scaffold this).

## License

This project is provided under the MIT License. See the `LICENSE` file for details.

---
If you'd like, I can also scaffold a `CONTRIBUTING.md`, add a GitHub Actions workflow that runs tests, or create a quick `CODE_OF_CONDUCT.md`.

