# 모델에 관련된 코드

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    __tablename__ = 'Student'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(64))
    studentid = db.Column(db.String(32))
    studentname = db.Column(db.String(8))