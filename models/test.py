# models/test.py
from models import db
from datetime import datetime

class TestResult(db.Model):
    __tablename__ = 'test_results'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    chapter = db.Column(db.Integer, nullable=False)
    test_type = db.Column(db.String(20), nullable=False)  # 'level_test' or 'chapter_test'
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    passed = db.Column(db.Boolean, nullable=False)  # 80점 이상이면 True
    test_date = db.Column(db.DateTime, default=datetime.utcnow)
    time_taken = db.Column(db.Integer)  # 소요 시간 (초)
    
    # 관계 설정
    answers = db.relationship('Answer', backref='test_result', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'book_id': self.book_id,
            'chapter': self.chapter,
            'test_type': self.test_type,
            'score': self.score,
            'total_questions': self.total_questions,
            'passed': self.passed,
            'test_date': self.test_date.isoformat(),
            'time_taken': self.time_taken
        }

class Answer(db.Model):
    __tablename__ = 'answers'
    
    id = db.Column(db.Integer, primary_key=True)
    test_result_id = db.Column(db.Integer, db.ForeignKey('test_results.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    selected_answer = db.Column(db.String(1), nullable=False)  # A, B, C, D
    is_correct = db.Column(db.Boolean, nullable=False)
    answer_time = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'test_result_id': self.test_result_id,
            'question_id': self.question_id,
            'selected_answer': self.selected_answer,
            'is_correct': self.is_correct,
            'answer_time': self.answer_time.isoformat()
        }

