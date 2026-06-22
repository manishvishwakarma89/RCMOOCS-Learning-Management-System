# EduForge LMS — Flask + PostgreSQL

A Learning Management System for teachers built with Flask and PostgreSQL.

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set up PostgreSQL
```sql
-- In psql:
CREATE DATABASE rcmoocs_lms;
```

### 3. Configure environment
```bash
cp .env.example .env
# Edit .env and set your DATABASE_URL and SECRET_KEY
```

Example `.env`:
```
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/rcmoocs_lms
SECRET_KEY=your-secret-key-here
```

### 4. Seed the database (optional demo data)
```bash
python seed.py
```

### 5. Run the app
```bash
python app.py
```

Open http://localhost:5000

## Database Schema

| Table | Description |
|---|---|
| `teachers` | Teacher accounts |
| `skills` | Individual skills (uses PostgreSQL ARRAY for tags) |
| `courses` | Courses grouping skills |
| `course_skills` | Many-to-many join table |
| `assessments` | Quizzes, exams, assignments |

## Features
- **Skills Library** — Add/edit/delete skills with levels, categories, tags (stored as PG arrays)
- **Courses** — Link multiple skills into structured courses
- **Assessments** — Quizzes, assignments, exams tied to courses
- **Dashboard** — Stats overview per teacher

## Production Notes
- Replace plain-text passwords with `bcrypt` hashing
- Use `gunicorn` as the WSGI server
- Set `FLASK_DEBUG=0` in production
