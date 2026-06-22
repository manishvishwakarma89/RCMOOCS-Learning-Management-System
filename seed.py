from app import app, db
from models import Teacher, Skill, Course, Assessment
from datetime import date

with app.app_context():
    db.create_all()

    # Create teacher
    if not Teacher.query.first():
        teacher = Teacher(
            name     = "Priyanka",
            email    = "priyanka@lms.com",
            password = "admin123"
        )
        db.session.add(teacher)
        db.session.commit()
        print("✅ Teacher created")
    else:
        teacher = Teacher.query.first()
        print("ℹ️  Teacher already exists")

    # Create skills
    if not Skill.query.first():
        skills = [
            Skill(teacher_id=teacher.id, title="Python Basics",     level="beginner",     category="Programming", description="Intro to Python",      resources=5,  tags=["python", "beginner"]),
            Skill(teacher_id=teacher.id, title="Flask Web Dev",     level="intermediate", category="Web",         description="Build APIs with Flask", resources=8,  tags=["flask", "web"]),
            Skill(teacher_id=teacher.id, title="PostgreSQL",        level="intermediate", category="Database",    description="SQL and schema design", resources=6,  tags=["sql", "postgres"]),
            Skill(teacher_id=teacher.id, title="Docker Basics",     level="beginner",     category="DevOps",      description="Containers and compose",resources=4,  tags=["docker"]),
        ]
        db.session.add_all(skills)
        db.session.commit()
        print("✅ Skills created")
    else:
        skills = Skill.query.all()
        print("ℹ️  Skills already exist")

    # Create courses
    if not Course.query.first():
        courses = [
            Course(teacher_id=teacher.id, title="Python for Beginners", description="Zero to hero in Python", duration="8 weeks", status="published", students=24, skills=skills[:2]),
            Course(teacher_id=teacher.id, title="Full Stack with Flask", description="Build and deploy web apps", duration="12 weeks", status="published", students=18, skills=skills[1:3]),
            Course(teacher_id=teacher.id, title="DevOps Fundamentals",  description="Docker, CI/CD basics",    duration="6 weeks", status="draft",     students=0,  skills=skills[2:]),
        ]
        db.session.add_all(courses)
        db.session.commit()
        print("✅ Courses created")
    else:
        courses = Course.query.all()
        print("ℹ️  Courses already exist")

    # Create assessments
    if not Assessment.query.first():
        assessments = [
            Assessment(teacher_id=teacher.id, title="Python Quiz 1",    type="quiz",       course_id=courses[0].id, due_date=date(2024, 8, 15), total_marks=50),
            Assessment(teacher_id=teacher.id, title="Flask Assignment",  type="assignment", course_id=courses[1].id, due_date=date(2024, 9, 1),  total_marks=100),
            Assessment(teacher_id=teacher.id, title="Docker Final Exam", type="exam",       course_id=courses[2].id, due_date=date(2024, 10, 1), total_marks=100),
        ]
        db.session.add_all(assessments)
        db.session.commit()
        print("✅ Assessments created")

    print("\n🎉 Seeding complete! Login with priyanka@lms.com / admin123")