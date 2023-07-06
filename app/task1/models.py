from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer)
    sex = db.Column(db.Enum('male', 'female'), nullable=False)
    group = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(80))
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculty.id'), nullable=False)
    scores = db.relationship('Score', backref='student', lazy=True)

    def __repr__(self):
        return f'Student({self.firstname} {self.lastname})'


class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    students = db.relationship('Student', backref='faculty', lazy=True)

    def __repr__(self):
        return f'Faculty({self.name})'


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'{self.subject}: {self.score}'
