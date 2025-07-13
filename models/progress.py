# models/progress.py
from models import db
from datetime import datetime

class Progress(db.Model):
    __tablename__ = 'progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    current_chapter = db.Column(db.Integer, default=1)
    completed_chapters = db.Column(db.Text)  # JSON 형태로 완료된 챕터 목록 저장
    started_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    total_score = db.Column(db.Integer, default=0)
    completion_percentage = db.Column(db.Float, default=0.0)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'book_id': self.book_id,
            'current_chapter': self.current_chapter,
            'completed_chapters': self.completed_chapters,
            'started_date': self.started_date.isoformat(),
            'last_activity': self.last_activity.isoformat(),
            'total_score': self.total_score,
            'completion_percentage': self.completion_percentage
        }

class MonthlyReport(db.Model):
    __tablename__ = 'monthly_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    report_month = db.Column(db.String(7), nullable=False)  # YYYY-MM 형식
    books_completed = db.Column(db.Integer, default=0)
    chapters_completed = db.Column(db.Integer, default=0)
    news_articles_read = db.Column(db.Integer, default=0)
    average_score = db.Column(db.Float, default=0.0)
    news_average_score = db.Column(db.Float, default=0.0)
    total_study_time = db.Column(db.Integer, default=0)  # 분 단위
    improvements = db.Column(db.Text)
    recommendations = db.Column(db.Text)
    generated_date = db.Column(db.DateTime, default=datetime.utcnow)
    sent_date = db.Column(db.DateTime)
    parent_email = db.Column(db.String(120), nullable=False)
