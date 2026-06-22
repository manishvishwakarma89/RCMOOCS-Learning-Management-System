-- ============================================================
-- RCMOOCS LMS — Database Schema
-- Generated from models.py
-- ============================================================

-- Teachers
CREATE TABLE IF NOT EXISTS teachers (
    id       SERIAL PRIMARY KEY,
    name     VARCHAR(120)  NOT NULL,
    email    VARCHAR(120)  NOT NULL UNIQUE,
    password VARCHAR(200)  NOT NULL,
    subject  VARCHAR(80),
    avatar   VARCHAR(4),
    color    VARCHAR(10)   DEFAULT '#7C6AF7'
);

-- Skills (uses PostgreSQL native ARRAY for tags)
CREATE TABLE IF NOT EXISTS skills (
    id          SERIAL PRIMARY KEY,
    teacher_id  INTEGER      NOT NULL REFERENCES teachers(id) ON DELETE CASCADE,
    title       VARCHAR(200) NOT NULL,
    description TEXT,
    level       VARCHAR(20)  DEFAULT 'Beginner',
    category    VARCHAR(80),
    resources   INTEGER      DEFAULT 0,
    students    INTEGER      DEFAULT 0,
    rating      FLOAT        DEFAULT 0.0,
    tags        TEXT[]       DEFAULT '{}',
    created     DATE         DEFAULT CURRENT_DATE
);

-- Courses
CREATE TABLE IF NOT EXISTS courses (
    id          SERIAL PRIMARY KEY,
    teacher_id  INTEGER      NOT NULL REFERENCES teachers(id) ON DELETE CASCADE,
    title       VARCHAR(200) NOT NULL,
    description TEXT,
    duration    VARCHAR(50),
    students    INTEGER      DEFAULT 0,
    status      VARCHAR(20)  DEFAULT 'draft',
    created     DATE         DEFAULT CURRENT_DATE
);

-- Many-to-many: courses <-> skills
CREATE TABLE IF NOT EXISTS course_skills (
    course_id INTEGER NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    skill_id  INTEGER NOT NULL REFERENCES skills(id)  ON DELETE CASCADE,
    PRIMARY KEY (course_id, skill_id)
);

-- Assessments
CREATE TABLE IF NOT EXISTS assessments (
    id          SERIAL PRIMARY KEY,
    teacher_id  INTEGER      NOT NULL REFERENCES teachers(id) ON DELETE CASCADE,
    course_id   INTEGER               REFERENCES courses(id)  ON DELETE SET NULL,
    title       VARCHAR(200) NOT NULL,
    type        VARCHAR(40)  DEFAULT 'Quiz',
    due_date    DATE,
    total_marks INTEGER      DEFAULT 100,
    submissions INTEGER      DEFAULT 0,
    status      VARCHAR(20)  DEFAULT 'active'
);