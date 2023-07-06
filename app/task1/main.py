from random import randint

from flask import Flask, render_template
from app.task1.models import db, Student, Faculty, Score

app = Flask(__name__)
app.secret_key = b'jhgmvytjy56r55rjfkur5ece5roti8yb8yy7t6rvkt6kuvt'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///home1.db'
db.init_app(app)


@app.route('/')
def index():
    return render_template('base.html')


@app.cli.command('init-db')
def init_db():
    db.create_all()


@app.cli.command('fill-db')
def fill_tables():
    count = 5
    for faculty in range(1, count + 1):
        new_faculty = Faculty(name=f'Факультет{faculty}')
        db.session.add(new_faculty)
    db.session.commit()

    for student in range(1, count ** 2):
        faculty = Faculty.query.filter_by(name=f'Факультет{student % count + 1}').first()
        new_student = Student(firstname=f'Имя {student}',
                              lastname=f'Фамилия {student}',
                              age=student + 17,
                              sex='male' if student % 2 == 0 else 'female',
                              group=1 if student % 2 == 0 else 2,
                              faculty=faculty)
        db.session.add(new_student)
        for i in range(1, 6):
            new_score = Score(student_id=student,
                              subject=f'Предмет {i}',
                              score=randint(1, 6))
            db.session.add(new_score)
    db.session.commit()


@app.route('/students/')
def all_students():
    students = Student.query.all()
    context = {
        'title': 'Студенты',
        'students': students}
    return render_template('students.html', **context)
