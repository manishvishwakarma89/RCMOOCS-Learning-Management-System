from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from models import db, Teacher, Skill, Course, Assessment
from datetime import datetime
import os

# Load .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'lms-secret-key-2024')

# PostgreSQL connection — set DATABASE_URL in your .env or environment
DATABASE_URL = os.environ.get(
    'DATABASE_URL',
    f'postgresql://{os.environ.get("USER", "postgres")}@localhost:5432/rcmoocs_lms'
)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# ── helpers ────────────────────────────────────────────────────────────────────

def get_teacher():
    if 'teacher_id' not in session:
        return None
    return db.session.get(Teacher, session['teacher_id'])

# ── auth ───────────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return redirect(url_for('dashboard') if 'teacher_id' in session else url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        teacher = Teacher.query.filter_by(
            email=request.form['email'],
            password=request.form['password']
        ).first()
        if teacher:
            session['teacher_id'] = teacher.id
            return redirect(url_for('dashboard'))
        flash('Invalid credentials', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ── dashboard ──────────────────────────────────────────────────────────────────

@app.route('/dashboard')
def dashboard():
    teacher = get_teacher()
    if not teacher:
        return redirect(url_for('login'))
    my_skills      = Skill.query.filter_by(teacher_id=teacher.id).all()
    my_courses     = Course.query.filter_by(teacher_id=teacher.id).all()
    my_assessments = Assessment.query.filter_by(teacher_id=teacher.id).all()
    stats = {
        'skills':      len(my_skills),
        'courses':     len(my_courses),
        'assessments': len(my_assessments),
        'students':    sum(c.students for c in my_courses),
    }
    return render_template('dashboard.html', teacher=teacher, stats=stats,
                           skills=my_skills[:3], courses=my_courses[:3])

# ── skills ─────────────────────────────────────────────────────────────────────

@app.route('/skills')
def skills():
    teacher = get_teacher()
    if not teacher:
        return redirect(url_for('login'))
    my_skills = Skill.query.filter_by(teacher_id=teacher.id).order_by(Skill.created.desc()).all()
    return render_template('skills.html', teacher=teacher, skills=my_skills)

@app.route('/skills/add', methods=['GET', 'POST'])
def add_skill():
    teacher = get_teacher()
    if not teacher:
        return redirect(url_for('login'))
    if request.method == 'POST':
        tags = [t.strip() for t in request.form.get('tags', '').split(',') if t.strip()]
        skill = Skill(
            teacher_id  = teacher.id,
            title       = request.form['title'],
            description = request.form['description'],
            level       = request.form['level'],
            category    = request.form['category'],
            resources   = int(request.form.get('resources', 0) or 0),
            tags        = tags,
        )
        db.session.add(skill)
        db.session.commit()
        flash('Skill added successfully!', 'success')
        return redirect(url_for('skills'))
    return render_template('skill_form.html', teacher=teacher, skill=None, action='Add')

@app.route('/skills/edit/<int:skill_id>', methods=['GET', 'POST'])
def edit_skill(skill_id):
    teacher = get_teacher()
    if not teacher:
        return redirect(url_for('login'))
    skill = Skill.query.filter_by(id=skill_id, teacher_id=teacher.id).first_or_404()
    if request.method == 'POST':
        skill.title       = request.form['title']
        skill.description = request.form['description']
        skill.level       = request.form['level']
        skill.category    = request.form['category']
        skill.resources   = int(request.form.get('resources', 0) or 0)
        skill.tags        = [t.strip() for t in request.form.get('tags', '').split(',') if t.strip()]
        db.session.commit()
        flash('Skill updated successfully!', 'success')
        return redirect(url_for('skills'))
    return render_template('skill_form.html', teacher=teacher, skill=skill, action='Edit')

@app.route('/skills/delete/<int:skill_id>', methods=['POST'])
def delete_skill(skill_id):
    teacher = get_teacher()
    if not teacher:
        return redirect(url_for('login'))
    skill = Skill.query.filter_by(id=skill_id, teacher_id=teacher.id).first_or_404()
    db.session.delete(skill)
    db.session.commit()
    flash('Skill deleted.', 'info')
    return redirect(url_for('skills'))

# ── courses ────────────────────────────────────────────────────────────────────

@app.route('/courses')
def courses():
    teacher = get_teacher()
    if not teacher:
        return redirect(url_for('login'))
    my_courses = Course.query.filter_by(teacher_id=teacher.id).order_by(Course.created.desc()).all()
    return render_template('courses.html', teacher=teacher, courses=my_courses)

@app.route('/courses/add', methods=['GET', 'POST'])
def add_course():
    teacher = get_teacher()
    if not teacher:
        return redirect(url_for('login'))
    my_skills = Skill.query.filter_by(teacher_id=teacher.id).all()
    if request.method == 'POST':
        selected = Skill.query.filter(
            Skill.id.in_(request.form.getlist('skill_ids')),
            Skill.teacher_id == teacher.id
        ).all()
        course = Course(
            teacher_id  = teacher.id,
            title       = request.form['title'],
            description = request.form['description'],
            duration    = request.form.get('duration', ''),
            status      = request.form.get('status', 'draft'),
            skills      = selected,
        )
        db.session.add(course)
        db.session.commit()
        flash('Course created successfully!', 'success')
        return redirect(url_for('courses'))
    return render_template('course_form.html', teacher=teacher, course=None,
                           skills=my_skills, action='Add')

@app.route('/courses/edit/<int:course_id>', methods=['GET', 'POST'])
def edit_course(course_id):
    teacher = get_teacher()
    if not teacher:
        return redirect(url_for('login'))
    course    = Course.query.filter_by(id=course_id, teacher_id=teacher.id).first_or_404()
    my_skills = Skill.query.filter_by(teacher_id=teacher.id).all()
    if request.method == 'POST':
        course.title       = request.form['title']
        course.description = request.form['description']
        course.duration    = request.form.get('duration', '')
        course.status      = request.form.get('status', 'draft')
        course.skills      = Skill.query.filter(
            Skill.id.in_(request.form.getlist('skill_ids')),
            Skill.teacher_id == teacher.id
        ).all()
        db.session.commit()
        flash('Course updated!', 'success')
        return redirect(url_for('courses'))
    return render_template('course_form.html', teacher=teacher, course=course,
                           skills=my_skills, action='Edit')

@app.route('/courses/delete/<int:course_id>', methods=['POST'])
def delete_course(course_id):
    teacher = get_teacher()
    if not teacher:
        return redirect(url_for('login'))
    course = Course.query.filter_by(id=course_id, teacher_id=teacher.id).first_or_404()
    db.session.delete(course)
    db.session.commit()
    flash('Course deleted.', 'info')
    return redirect(url_for('courses'))

# ── assessments ────────────────────────────────────────────────────────────────

@app.route('/assessments')
def assessments():
    teacher = get_teacher()
    if not teacher:
        return redirect(url_for('login'))
    my_assessments = Assessment.query.filter_by(teacher_id=teacher.id).order_by(Assessment.due_date).all()
    my_courses = {c.id: c.title for c in Course.query.filter_by(teacher_id=teacher.id).all()}
    return render_template('assessments.html', teacher=teacher,
                           assessments=my_assessments, courses=my_courses)

@app.route('/assessments/add', methods=['GET', 'POST'])
def add_assessment():
    teacher = get_teacher()
    if not teacher:
        return redirect(url_for('login'))
    my_courses = Course.query.filter_by(teacher_id=teacher.id).all()
    if request.method == 'POST':
        assessment = Assessment(
            teacher_id  = teacher.id,
            title       = request.form['title'],
            type        = request.form['type'],
            course_id   = int(request.form['course_id']),
            due_date    = datetime.strptime(request.form['due_date'], '%Y-%m-%d').date(),
            total_marks = int(request.form.get('total_marks', 100) or 100),
        )
        db.session.add(assessment)
        db.session.commit()
        flash('Assessment created!', 'success')
        return redirect(url_for('assessments'))
    return render_template('assessment_form.html', teacher=teacher,
                           courses=my_courses, action='Add')

@app.route('/assessments/delete/<int:assessment_id>', methods=['POST'])
def delete_assessment(assessment_id):
    teacher = get_teacher()
    if not teacher:
        return redirect(url_for('login'))
    a = Assessment.query.filter_by(id=assessment_id, teacher_id=teacher.id).first_or_404()
    db.session.delete(a)
    db.session.commit()
    flash('Assessment deleted.', 'info')
    return redirect(url_for('assessments'))

# ── api ────────────────────────────────────────────────────────────────────────

@app.route('/api/stats')
def api_stats():
    teacher = get_teacher()
    if not teacher:
        return jsonify({'error': 'unauthorized'}), 401
    my_courses = Course.query.filter_by(teacher_id=teacher.id).all()
    return jsonify({
        'skills':   Skill.query.filter_by(teacher_id=teacher.id).count(),
        'courses':  len(my_courses),
        'students': sum(c.students for c in my_courses),
    })

# ── init ───────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0',port=5000)
