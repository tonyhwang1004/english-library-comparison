# init_db.py
from app import app, db
from models.user import User
from models.book import Book, Question
from models.newspaper import NewsArticle, NewsQuestion, NewsVocabulary
from datetime import datetime, timedelta
import random

def init_database():
    """데이터베이스 초기화 및 기본 데이터 생성"""
    print("🔧 데이터베이스를 초기화합니다...")
    
    with app.app_context():
        # 모든 테이블 삭제 후 재생성
        db.drop_all()
        db.create_all()
        print("✅ 데이터베이스 테이블이 생성되었습니다.")
        
        # 기본 책 데이터 추가
        create_default_books()
        
        # 영자신문 샘플 기사 추가
        create_sample_news()
        
        # 관리자 계정 생성
        create_admin_user()
        
        # 샘플 학생 계정 생성
        create_sample_students()
        
        db.session.commit()
        print("🎉 기본 데이터가 성공적으로 추가되었습니다!")

def create_default_books():
    """5단계 레벨별 기본 도서 생성"""
    print("📚 기본 도서를 추가하는 중...")
    
    books_data = [
        # Level 1
        {"title": "Charlotte's Web", "author": "E.B. White", "level": 1, "chapters": 22},
        {"title": "The Giver", "author": "Lois Lowry", "level": 1, "chapters": 23},
        {"title": "Holes", "author": "Louis Sachar", "level": 1, "chapters": 20},
        
        # Level 2
        {"title": "Bridge to Terabithia", "author": "Katherine Paterson", "level": 2, "chapters": 13},
        {"title": "Number the Stars", "author": "Lois Lowry", "level": 2, "chapters": 17},
        {"title": "Island of the Blue Dolphins", "author": "Scott O'Dell", "level": 2, "chapters": 29},
        
        # Level 3
        {"title": "The Outsiders", "author": "S.E. Hinton", "level": 3, "chapters": 12},
        {"title": "Hatchet", "author": "Gary Paulsen", "level": 3, "chapters": 19},
        {"title": "Where the Red Fern Grows", "author": "Wilson Rawls", "level": 3, "chapters": 20},
        
        # Level 4
        {"title": "The Hunger Games", "author": "Suzanne Collins", "level": 4, "chapters": 27},
        {"title": "Percy Jackson: The Lightning Thief", "author": "Rick Riordan", "level": 4, "chapters": 22},
        {"title": "Wonder", "author": "R.J. Palacio", "level": 4, "chapters": 30},
        
        # Level 5 (지정된 책들)
        {"title": "The Book Thief", "author": "Markus Zusak", "level": 5, "chapters": 10},
        {"title": "A Man Called Ove", "author": "Fredrik Backman", "level": 5, "chapters": 39},
        {"title": "To Kill a Mockingbird", "author": "Harper Lee", "level": 5, "chapters": 31}
    ]
    
    for book_info in books_data:
        book = Book(
            title=book_info["title"],
            author=book_info["author"],
            level=book_info["level"],
            total_chapters=book_info["chapters"],
            description=f"Level {book_info['level']} 영어 도서 - {book_info['author']} 작품",
            created_date=datetime.utcnow()
        )
        db.session.add(book)
        print(f"  📖 {book_info['title']} - Level {book_info['level']}")

def create_sample_news():
    """영자신문 샘플 기사 생성"""
    print("📰 영자신문 샘플 기사를 추가하는 중...")
    
    articles_data = [
        {
            'title': 'Scientists Discover New Species of Deep-Sea Fish',
            'content': '''Marine biologists have discovered a fascinating new species of deep-sea fish in the Pacific Ocean. The fish, named Abyssobrotula galapagoensis, was found at depths of over 8,000 meters near the Galápagos Islands.

The discovery was made during a recent expedition using advanced underwater vehicles. The fish exhibits unique adaptations to extreme pressure and complete darkness, including enlarged eyes and specialized organs for detecting vibrations.

Dr. Sarah Johnson, lead researcher of the expedition, explained that this finding helps us understand how life adapts to extreme environments. The fish's genetic analysis reveals it diverged from related species millions of years ago.

This discovery highlights the importance of deep-sea exploration and conservation. Many species in these depths remain unknown to science, and protecting these ecosystems is crucial for maintaining biodiversity.''',
            'category': 'Science',
            'difficulty_level': 3,
            'source_name': 'Science Daily'
        },
        {
            'title': 'Global Renewable Energy Capacity Reaches Record High',
            'content': '''The International Renewable Energy Agency (IRENA) announced that global renewable energy capacity reached a record 3,372 gigawatts in 2023, representing a 9.6% increase from the previous year.

Solar power led the growth with 346 GW of new installations, followed by wind energy with 116 GW. This expansion demonstrates the accelerating transition toward clean energy sources worldwide.

The report highlights that renewable energy now accounts for more than 42% of global power generation capacity. Countries in Asia dominated the additions, with China alone contributing 63% of new renewable capacity.

However, experts warn that current growth rates, while impressive, still fall short of what's needed to meet climate goals. The Paris Agreement targets require tripling renewable capacity by 2030.''',
            'category': 'Environment',
            'difficulty_level': 4,
            'source_name': 'Reuters'
        },
        {
            'title': 'AI Technology Revolutionizes Medical Diagnosis',
            'content': '''Artificial intelligence is transforming medical diagnosis with unprecedented accuracy and speed. Recent studies show AI systems can now detect certain diseases earlier and more accurately than traditional methods.

A new AI model developed by researchers can identify skin cancer with 95% accuracy, surpassing dermatologists in some cases. The system analyzes thousands of images to recognize patterns invisible to the human eye.

Similar breakthroughs are occurring in radiology, where AI assists in interpreting X-rays, MRIs, and CT scans. This technology is particularly valuable in areas with limited access to medical specialists.

However, experts emphasize that AI should complement, not replace, human medical expertise. The technology works best when combined with doctors' clinical judgment and patient interaction skills.''',
            'category': 'Technology',
            'difficulty_level': 4,
            'source_name': 'Medical News Today'
        }
    ]
    
    for article_info in articles_data:
        article = NewsArticle(
            title=article_info['title'],
            content=article_info['content'],
            category=article_info['category'],
            difficulty_level=article_info['difficulty_level'],
            source_name=article_info['source_name'],
            published_date=datetime.utcnow() - timedelta(days=random.randint(1, 7)),
            word_count=len(article_info['content'].split()),
            reading_time=max(3, len(article_info['content'].split()) // 200),
            is_active=True
        )
        db.session.add(article)
        print(f"  📰 {article_info['title']} - {article_info['category']}")

def create_admin_user():
    """관리자 계정 생성"""
    print("👤 관리자 계정을 생성하는 중...")
    
    admin = User(
        username='admin',
        email='admin@sureading.com',
        student_name='관리자',
        parent_email='admin@sureading.com',
        phone='010-4602-1953',
        current_level=5,
        class_type='관리자',
        registration_date=datetime.utcnow(),
        is_active=True
    )
    admin.set_password('admin123')
    db.session.add(admin)
    print("  ✅ 관리자 계정 생성 완료 (ID: admin, PW: admin123)")

def create_sample_students():
    """샘플 학생 계정들 생성"""
    print("👥 샘플 학생 계정들을 생성하는 중...")
    
    students_data = [
        {
            'username': 'student1',
            'student_name': '김영수',
            'email': 'student1@test.com',
            'parent_email': 'parent1@test.com',
            'class_type': '채두윜반',
            'level': 2
        },
        {
            'username': 'student2', 
            'student_name': '이민정',
            'email': 'student2@test.com',
            'parent_email': 'parent2@test.com',
            'class_type': '소설클래스',
            'level': 3
        },
        {
            'username': 'student3',
            'student_name': '박서준',
            'email': 'student3@test.com', 
            'parent_email': 'parent3@test.com',
            'class_type': '영자신문클래스',
            'level': 4
        }
    ]
    
    for student_info in students_data:
        student = User(
            username=student_info['username'],
            email=student_info['email'],
            student_name=student_info['student_name'],
            parent_email=student_info['parent_email'],
            phone='010-1234-5678',
            current_level=student_info['level'],
            class_type=student_info['class_type'],
            registration_date=datetime.utcnow(),
            is_active=True
        )
        student.set_password('test123')
        db.session.add(student)
        print(f"  👤 {student_info['student_name']} ({student_info['username']}) - {student_info['class_type']}")

if __name__ == '__main__':
    init_database()
    print("\n🎉 데이터베이스 초기화가 완료되었습니다!")
    print("\n📋 생성된 계정 정보:")
    print("관리자: admin / admin123")
    print("학생1: student1 / test123")
    print("학생2: student2 / test123") 
    print("학생3: student3 / test123")
