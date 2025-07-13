# models/newspaper.py
from models import db
from datetime import datetime

class NewsArticle(db.Model):
    __tablename__ = 'news_articles'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text)
    category = db.Column(db.String(100), nullable=False)  # Science, Technology, Environment, Politics, Economy
    difficulty_level = db.Column(db.Integer, nullable=False)  # 1-5
    word_count = db.Column(db.Integer)
    source_url = db.Column(db.String(500))
    source_name = db.Column(db.String(100))
    published_date = db.Column(db.DateTime, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    reading_time = db.Column(db.Integer)  # 예상 읽기 시간 (분)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'summary': self.summary,
            'category': self.category,
            'difficulty_level': self.difficulty_level,
            'word_count': self.word_count,
            'source_name': self.source_name,
            'published_date': self.published_date.isoformat(),
            'reading_time': self.reading_time
        }

class NewsQuestion(db.Model):
    __tablename__ = 'news_questions'
    
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('news_articles.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    question_type = db.Column(db.String(50), nullable=False)
    option_a = db.Column(db.String(300), nullable=False)
    option_b = db.Column(db.String(300), nullable=False)
    option_c = db.Column(db.String(300), nullable=False)
    option_d = db.Column(db.String(300), nullable=False)
    correct_answer = db.Column(db.String(1), nullable=False)
    explanation = db.Column(db.Text)
    difficulty = db.Column(db.Integer, default=3)

class NewsReading(db.Model):
    __tablename__ = 'news_readings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('news_articles.id'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    reading_time = db.Column(db.Integer)
    comprehension_score = db.Column(db.Integer)
    vocabulary_score = db.Column(db.Integer)
    total_score = db.Column(db.Integer)
    completed = db.Column(db.Boolean, default=False)

class NewsAnswer(db.Model):
    __tablename__ = 'news_answers'
    
    id = db.Column(db.Integer, primary_key=True)
    reading_id = db.Column(db.Integer, db.ForeignKey('news_readings.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('news_questions.id'), nullable=False)
    selected_answer = db.Column(db.String(1), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    answer_time = db.Column(db.DateTime, default=datetime.utcnow)

class NewsVocabulary(db.Model):
    __tablename__ = 'news_vocabulary'
    
    id = db.Column(db.Integer, primary_key=True)
    article_id = db.Column(db.Integer, db.ForeignKey('news_articles.id'), nullable=False)
    word = db.Column(db.String(100), nullable=False)
    definition = db.Column(db.Text, nullable=False)
    example_sentence = db.Column(db.Text)
    difficulty_level = db.Column(db.Integer, default=3)
    word_type = db.Column(db.String(50))
