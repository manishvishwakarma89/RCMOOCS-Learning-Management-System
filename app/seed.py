"""
seed.py — Populates rcmoocs_lms with demo data.
Run inside the app container:
  docker compose exec app python seed.py
"""

import os
from datetime import date, timedelta
from app import app
from models import db, Teacher, Skill, Course, Assessment

def seed():
    with app.app_context():
        db.create_all()

        # ── Clear existing data (order matters for FK constraints) ──
        Assessment.query.delete()
        Course.query.delete()
        Skill.query.delete()
        Teacher.query.delete()
        db.session.commit()
        print("Cleared existing data.")

        # ── Teachers ────────────────────────────────────────────────
        teachers = [
            Teacher(name="Papu Kumar",  email="papukumar@ramanujan.du.ac.in",  password="algebra@1234",  subject="Mathematics",      avatar="AJ", color="#7C6AF7"),
            Teacher(name="Virendra Kumar",   email="virendrakumar@ramanujan.du.ac.in",    password="algebra@1234",    subject="Mathematics", avatar="BW", color="#F76A6A"),
            Teacher(name="Rajesh Kumar",    email="rajeshkumar@ramanujan.du.ac.in",  password="rajesh@1234",  subject="Mathematics",     avatar="CS", color="#6AF7A0"),
            Teacher(name="Jyoti Trivedi",    email="jyotitrivedi@ramanujan.du.ac.in",  password="jyoti@1234", subject="Computer Science",avatar="CS", color="#6AF7A0"),
            Teacher(name="Sonia Yadav",    email="soni.yadav@ramanujan.du.ac.in",  password="soni@1234",  subject="Computer Science",     avatar="CS", color="#6AF7A0"),
        ]
        db.session.add_all(teachers)
        db.session.commit()
        print(f"Inserted {len(teachers)} teachers.")

        alice, bob, clara, david = teachers

        # ── Skills ──────────────────────────────────────────────────
        skills = [
            # Alice — Mathematics
            Skill(teacher=alice, title="Algebra Fundamentals",     description="Variables, equations, and functions.",         level="Beginner",     category="Mathematics",      resources=5,  students=120, rating=4.5, tags=["algebra", "equations", "math"],          created=date.today() - timedelta(days=60)),
            Skill(teacher=alice, title="Calculus: Differentiation",description="Limits, derivatives, and applications.",       level="Intermediate", category="Mathematics",      resources=8,  students=85,  rating=4.7, tags=["calculus", "derivatives", "math"],        created=date.today() - timedelta(days=45)),
            Skill(teacher=alice, title="Linear Algebra",           description="Vectors, matrices, and transformations.",      level="Advanced",     category="Mathematics",      resources=10, students=60,  rating=4.8, tags=["linear-algebra", "matrices", "vectors"],  created=date.today() - timedelta(days=30)),

            # Bob — Computer Science
            Skill(teacher=bob,   title="Python Programming",       description="Syntax, data types, and OOP in Python.",       level="Beginner",     category="Programming",      resources=12, students=200, rating=4.9, tags=["python", "programming", "beginner"],      created=date.today() - timedelta(days=90)),
            Skill(teacher=bob,   title="Data Structures",          description="Arrays, linked lists, trees, and graphs.",     level="Intermediate", category="Computer Science", resources=9,  students=150, rating=4.6, tags=["dsa", "algorithms", "cs"],               created=date.today() - timedelta(days=50)),
            Skill(teacher=bob,   title="Web Development with Flask",description="Build web apps using Flask and PostgreSQL.",  level="Intermediate", category="Web Development",  resources=15, students=110, rating=4.7, tags=["flask", "web", "python", "postgresql"],   created=date.today() - timedelta(days=20)),

            # Clara — Data Science
            Skill(teacher=clara, title="Data Analysis with Pandas",description="DataFrames, cleaning, and aggregation.",       level="Beginner",     category="Data Science",     resources=7,  students=180, rating=4.5, tags=["pandas", "data", "python"],              created=date.today() - timedelta(days=70)),
            Skill(teacher=clara, title="Machine Learning Basics",  description="Supervised and unsupervised learning.",        level="Intermediate", category="Data Science",     resources=11, students=130, rating=4.8, tags=["ml", "scikit-learn", "ai"],              created=date.today() - timedelta(days=35)),
            Skill(teacher=clara, title="Deep Learning with PyTorch",description="Neural networks and model training.",         level="Advanced",     category="Data Science",     resources=14, students=75,  rating=4.9, tags=["deep-learning", "pytorch", "neural-nets"],created=date.today() - timedelta(days=10)),

            # David — Physics
            Skill(teacher=david, title="Classical Mechanics",      description="Newton's laws, motion, and energy.",           level="Beginner",     category="Physics",          resources=6,  students=95,  rating=4.4, tags=["mechanics", "physics", "newton"],         created=date.today() - timedelta(days=80)),
            Skill(teacher=david, title="Electromagnetism",         description="Electric fields, circuits, and magnetism.",    level="Intermediate", category="Physics",          resources=8,  students=70,  rating=4.6, tags=["electromagnetism", "circuits", "physics"], created=date.today() - timedelta(days=40)),
            Skill(teacher=david, title="Quantum Physics",          description="Wave-particle duality and quantum states.",    level="Advanced",     category="Physics",          resources=10, students=45,  rating=4.7, tags=["quantum", "physics", "advanced"],         created=date.today() - timedelta(days=15)),
        ]
        db.session.add_all(skills)
        db.session.commit()
        print(f"Inserted {len(skills)} skills.")

        # Unpack for course linking
        alg, calc, linalg, py, dsa, flask_skill, pandas, ml, dl, mech, em, qp = skills

        # ── Courses ─────────────────────────────────────────────────
        courses = [
            Course(teacher=alice, title="Complete Mathematics Program",   description="From algebra to advanced linear algebra.",     duration="12 weeks", students=180, status="active",   created=date.today() - timedelta(days=55), skills=[alg, calc, linalg]),
            Course(teacher=bob,   title="Full Stack Python Development",  description="Python, DSA, and web apps with Flask.",        duration="16 weeks", students=160, status="active",   created=date.today() - timedelta(days=45), skills=[py, dsa, flask_skill]),
            Course(teacher=bob,   title="Python for Beginners",           description="Start coding with Python from scratch.",        duration="6 weeks",  students=220, status="active",   created=date.today() - timedelta(days=85), skills=[py]),
            Course(teacher=clara, title="Data Science Bootcamp",          description="Pandas, ML, and deep learning end-to-end.",    duration="20 weeks", students=140, status="active",   created=date.today() - timedelta(days=65), skills=[pandas, ml, dl]),
            Course(teacher=clara, title="Intro to Machine Learning",      description="Foundations of ML with real datasets.",         duration="8 weeks",  students=100, status="draft",    created=date.today() - timedelta(days=20), skills=[pandas, ml]),
            Course(teacher=david, title="Physics Mastery",                description="Mechanics, electromagnetism, and quantum.",     duration="14 weeks", students=90,  status="active",   created=date.today() - timedelta(days=75), skills=[mech, em, qp]),
            Course(teacher=david, title="Quantum Physics Deep Dive",      description="Advanced quantum theory and applications.",     duration="10 weeks", students=40,  status="archived", created=date.today() - timedelta(days=100), skills=[qp]),
        ]
        db.session.add_all(courses)
        db.session.commit()
        print(f"Inserted {len(courses)} courses.")

        math_course, fullstack, py_begin, ds_boot, intro_ml, physics, quantum = courses

        # ── Assessments ─────────────────────────────────────────────
        assessments = [
            # Mathematics
            Assessment(teacher=alice, course=math_course, title="Algebra Quiz 1",          type="Quiz",       due_date=date.today() + timedelta(days=7),  total_marks=20,  submissions=95,  status="active"),
            Assessment(teacher=alice, course=math_course, title="Calculus Midterm",        type="Exam",       due_date=date.today() + timedelta(days=21), total_marks=100, submissions=80,  status="active"),
            Assessment(teacher=alice, course=math_course, title="Linear Algebra Project",  type="Project",    due_date=date.today() + timedelta(days=35), total_marks=50,  submissions=55,  status="active"),

            # Full Stack Python
            Assessment(teacher=bob,   course=fullstack,   title="Python Basics Quiz",      type="Quiz",       due_date=date.today() + timedelta(days=5),  total_marks=30,  submissions=140, status="active"),
            Assessment(teacher=bob,   course=fullstack,   title="DSA Assignment 1",        type="Assignment", due_date=date.today() + timedelta(days=14), total_marks=50,  submissions=120, status="active"),
            Assessment(teacher=bob,   course=fullstack,   title="Flask App Final Project", type="Project",    due_date=date.today() + timedelta(days=42), total_marks=100, submissions=90,  status="active"),

            # Python Beginners
            Assessment(teacher=bob,   course=py_begin,    title="Hello World Assignment",  type="Assignment", due_date=date.today() + timedelta(days=3),  total_marks=10,  submissions=200, status="active"),

            # Data Science
            Assessment(teacher=clara, course=ds_boot,     title="Pandas Quiz",             type="Quiz",       due_date=date.today() + timedelta(days=10), total_marks=25,  submissions=110, status="active"),
            Assessment(teacher=clara, course=ds_boot,     title="ML Model Assignment",     type="Assignment", due_date=date.today() + timedelta(days=28), total_marks=75,  submissions=85,  status="active"),
            Assessment(teacher=clara, course=ds_boot,     title="Deep Learning Exam",      type="Exam",       due_date=date.today() + timedelta(days=56), total_marks=100, submissions=60,  status="active"),

            # Intro ML
            Assessment(teacher=clara, course=intro_ml,    title="ML Concepts Quiz",        type="Quiz",       due_date=date.today() + timedelta(days=12), total_marks=20,  submissions=0,   status="active"),

            # Physics
            Assessment(teacher=david, course=physics,     title="Mechanics Quiz",          type="Quiz",       due_date=date.today() + timedelta(days=6),  total_marks=20,  submissions=70,  status="active"),
            Assessment(teacher=david, course=physics,     title="Electromagnetism Exam",   type="Exam",       due_date=date.today() + timedelta(days=25), total_marks=100, submissions=55,  status="active"),
            Assessment(teacher=david, course=quantum,     title="Quantum Physics Final",   type="Exam",       due_date=date.today() + timedelta(days=60), total_marks=100, submissions=35,  status="active"),
        ]
        db.session.add_all(assessments)
        db.session.commit()
        print(f"Inserted {len(assessments)} assessments.")

        print("\n✅ Seed complete! Summary:")
        print(f"   Teachers:    {Teacher.query.count()}")
        print(f"   Skills:      {Skill.query.count()}")
        print(f"   Courses:     {Course.query.count()}")
        print(f"   Assessments: {Assessment.query.count()}")
        print("\nLogin credentials:")
        for t in teachers:
            print(f"   {t.email} / {t.password}")

if __name__ == "__main__":
    seed()