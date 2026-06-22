from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

db = SQLAlchemy()

# Many-to-many join table: courses ↔ skills
course_skills = db.Table(
    'course_skills',
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id', ondelete='CASCADE'), primary_key=True),
    db.Column('skill_id',  db.Integer, db.ForeignKey('skills.id',  ondelete='CASCADE'), primary_key=True),
)


class Teacher(db.Model):
    __tablename__ = 'teachers'

    id       = db.Column(db.Integer, primary_key=True)
    name     = db.Column(db.String(120), nullable=False)
    email    = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)   # plain for demo; use bcrypt in prod
    subject  = db.Column(db.String(80))
    avatar   = db.Column(db.String(4))   # 2-letter initials
    color    = db.Column(db.String(10), default='#7C6AF7')

    skills      = db.relationship('Skill',      backref='teacher', lazy='dynamic', cascade='all, delete-orphan')
    courses     = db.relationship('Course',     backref='teacher', lazy='dynamic', cascade='all, delete-orphan')
    assessments = db.relationship('Assessment', backref='teacher', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self):
        return dict(id=self.id, name=self.name, email=self.email,
                    subject=self.subject, avatar=self.avatar, color=self.color)


class Skill(db.Model):
    __tablename__ = 'skills'

    id          = db.Column(db.Integer, primary_key=True)
    teacher_id  = db.Column(db.Integer, db.ForeignKey('teachers.id', ondelete='CASCADE'), nullable=False)
    title       = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    level       = db.Column(db.String(20), default='Beginner')   # Beginner / Intermediate / Advanced
    category    = db.Column(db.String(80))
    resources   = db.Column(db.Integer, default=0)
    students    = db.Column(db.Integer, default=0)
    rating      = db.Column(db.Float, default=0.0)
    tags        = db.Column(db.ARRAY(db.String), default=list)   # PostgreSQL native array
    created     = db.Column(db.Date, default=date.today)

    def tags_str(self):
        return ', '.join(self.tags or [])

    def to_dict(self):
        return dict(
            id=self.id, title=self.title, description=self.description,
            level=self.level, category=self.category, resources=self.resources,
            students=self.students, rating=self.rating,
            tags=self.tags or [], created=str(self.created),
        )


class Course(db.Model):
    __tablename__ = 'courses'

    id          = db.Column(db.Integer, primary_key=True)
    teacher_id  = db.Column(db.Integer, db.ForeignKey('teachers.id', ondelete='CASCADE'), nullable=False)
    title       = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    duration    = db.Column(db.String(50))
    students    = db.Column(db.Integer, default=0)
    status      = db.Column(db.String(20), default='draft')   # draft / active / archived
    created     = db.Column(db.Date, default=date.today)

    skills = db.relationship('Skill', secondary=course_skills, lazy='subquery',
                             backref=db.backref('courses', lazy=True))

    def skill_ids(self):
        return [s.id for s in self.skills]

    def to_dict(self):
        return dict(
            id=self.id, title=self.title, description=self.description,
            duration=self.duration, students=self.students, status=self.status,
            created=str(self.created), skill_ids=self.skill_ids(),
        )


class Assessment(db.Model):
    __tablename__ = 'assessments'

    id          = db.Column(db.Integer, primary_key=True)
    teacher_id  = db.Column(db.Integer, db.ForeignKey('teachers.id', ondelete='CASCADE'), nullable=False)
    course_id   = db.Column(db.Integer, db.ForeignKey('courses.id',  ondelete='SET NULL'), nullable=True)
    title       = db.Column(db.String(200), nullable=False)
    type        = db.Column(db.String(40), default='Quiz')   # Quiz / Assignment / Exam / Project
    due_date    = db.Column(db.Date)
    total_marks = db.Column(db.Integer, default=100)
    submissions = db.Column(db.Integer, default=0)
    status      = db.Column(db.String(20), default='active')

    course = db.relationship('Course', backref='assessments')

    def to_dict(self):
        return dict(
            id=self.id, title=self.title, type=self.type,
            course_id=self.course_id, due_date=str(self.due_date),
            total_marks=self.total_marks, submissions=self.submissions, status=self.status,
        )
