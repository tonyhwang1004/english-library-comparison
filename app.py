# app.py - 수리딩어학원 QR코드 학습 시스템 (완전한 버전)
from flask import Flask, jsonify, request, render_template
from flask_login import LoginManager, current_user, login_required, UserMixin, AnonymousUserMixin
from datetime import datetime, timedelta
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sureading-academy-secret-key-2024'
app.config['JSON_AS_ASCII'] = False

# Flask-Login 설정
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.anonymous_user = AnonymousUserMixin

# 간단한 익명 사용자 처리
# @login_manager.user_loader
# def load_user(user_id):
#     return None

# 템플릿 전역 변수로 current_user 추가
@app.context_processor
def inject_user():
    return dict(current_user=current_user)


# CORS 수동 설정 (flask_cors 대신)
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# 도서 데이터 (QR코드 시스템용)
books_data = [
    {
        "id": 1,
        "title": "Charlotte's Web",
        "author": "E.B. White",
        "level": 3,
        "qr_code": "CW001",
        "audio_url": "",#비움
        "cover_image": "https://suellibrary.store/images/charlottes-web.jpg",
        "total_chapters": 22,
        "description": "윌버와 샬롯의 우정 이야기",
        "reading_time": "45분",
        "difficulty": "중급"
    },
    {
        "id": 2,
        "title": "The Magic Tree House #1",
        "author": "Mary Pope Osborne",
        "level": 2,
        "qr_code": "MTH001",
        "audio_url": "https://suellibrary.store/audio/magic-tree-house-1.mp3",
        "cover_image": "https://suellibrary.store/images/magic-tree-house-1.jpg",
        "total_chapters": 10,
        "description": "잭과 애니의 첫 번째 모험",
        "reading_time": "30분",
        "difficulty": "초급"
    },
    {
        "id": 3,
        "title": "Wonder",
        "author": "R.J. Palacio",
        "level": 4,
        "qr_code": "WND001",
        "audio_url": "https://suellibrary.store/audio/wonder.mp3",
        "cover_image": "https://suellibrary.store/images/wonder.jpg",
        "total_chapters": 8,
        "description": "어기의 용기 있는 성장기",
        "reading_time": "60분",
        "difficulty": "고급"
    }
]

# 학생 데이터
students_data = [
    {
        "id": 1,
        "name": "김지민",
        "english_name": "Jimin",
        "grade": 5,
        "level": 3,
        "class": "채두윜반",
        "parent_phone": "010-1234-5678",
        "student_id": "ST2024001",
        "enrollment_date": "2024-03-01",
        "current_books": [1, 2],
        "completed_books": [],
        "total_study_time": 1250,
        "last_activity": "2025-06-17T10:30:00",
        "status": "active"
    },
    {
        "id": 2,
        "name": "박준호",
        "english_name": "Junho",
        "grade": 6,
        "level": 4,
        "class": "소설클래스",
        "parent_phone": "010-2345-6789",
        "student_id": "ST2024002",
        "enrollment_date": "2024-02-15",
        "current_books": [3],
        "completed_books": [1, 2],
        "total_study_time": 2180,
        "last_activity": "2025-06-17T09:15:00",
        "status": "active"
    },
    {
        "id": 3,
        "name": "이서연",
        "english_name": "Seoyeon",
        "grade": 4,
        "level": 2,
        "class": "채두윜반",
        "parent_phone": "010-3456-7890",
        "student_id": "ST2024003",
        "enrollment_date": "2024-04-10",
        "current_books": [2],
        "completed_books": [1],
        "total_study_time": 890,
        "last_activity": "2025-06-16T16:45:00",
        "status": "active"
    }
]

# 학습 기록 데이터
learning_records = [
    {
        "id": 1,
        "student_id": 1,
        "book_id": 1,
        "chapter": 1,
        "qr_scanned_at": "2025-06-17T10:30:00",
        "audio_listened": True,
        "questions_attempted": 2,
        "questions_correct": 1,
        "time_spent": 25,
        "session_completed": True
    },
    {
        "id": 2,
        "student_id": 1,
        "book_id": 2,
        "chapter": 1,
        "qr_scanned_at": "2025-06-16T15:20:00",
        "audio_listened": True,
        "questions_attempted": 1,
        "questions_correct": 1,
        "time_spent": 18,
        "session_completed": True
    },
    {
        "id": 3,
        "student_id": 2,
        "book_id": 3,
        "chapter": 1,
        "qr_scanned_at": "2025-06-17T09:15:00",
        "audio_listened": True,
        "questions_attempted": 2,
        "questions_correct": 2,
        "time_spent": 35,
        "session_completed": True
    }
]

# 문제 데이터
# 문제 데이터 (확장된 버전)
questions_data = [
    # ===== Charlotte's Web (Book ID: 1) =====
    # Chapter 1
    {
        "id": 1,
        "book_id": 1,
        "chapter": 1,
        "question_type": "listening_comprehension",
        "question": "What is the name of the pig in the story?",
        "options": ["Wilbur", "Charlotte", "Templeton", "Fern"],
        "correct_answer": 0,
        "explanation": "윌버(Wilbur)는 이 이야기의 주인공인 돼지입니다.",
        "audio_timestamp": "00:02:15"
    },
    {
        "id": 2,
        "book_id": 1,
        "chapter": 1,
        "question_type": "vocabulary",
        "question": "What does 'runt' mean in the story?",
        "options": ["큰 동물", "작고 약한 동물", "빠른 동물", "똑똑한 동물"],
        "correct_answer": 1,
        "explanation": "'Runt'는 새끼 중에서 가장 작고 약한 개체를 의미합니다.",
        "audio_timestamp": "00:01:30"
    },
    {
        "id": 3,
        "book_id": 1,
        "chapter": 1,
        "question_type": "listening_comprehension",
        "question": "Who wants to save Wilbur from being killed?",
        "options": ["Mr. Zuckerman", "Fern", "Charlotte", "Templeton"],
        "correct_answer": 1,
        "explanation": "펀(Fern)이 윌버를 구하려고 합니다.",
        "audio_timestamp": "00:03:45"
    },

    # Chapter 2
    {
        "id": 4,
        "book_id": 1,
        "chapter": 2,
        "question_type": "listening_comprehension",
        "question": "Where does Wilbur live after leaving Fern's house?",
        "options": ["In the forest", "At Zuckerman's farm", "In the city", "At the zoo"],
        "correct_answer": 1,
        "explanation": "윌버는 펀의 집을 떠난 후 주커만 농장에서 살게 됩니다.",
        "audio_timestamp": "00:05:20"
    },
    {
        "id": 5,
        "book_id": 1,
        "chapter": 2,
        "question_type": "vocabulary",
        "question": "What does 'lonely' mean?",
        "options": ["행복한", "외로운", "배고픈", "피곤한"],
        "correct_answer": 1,
        "explanation": "'Lonely'는 '외로운, 쓸쓸한'이라는 뜻입니다.",
        "audio_timestamp": "00:07:10"
    },

    # Chapter 3
    {
        "id": 6,
        "book_id": 1,
        "chapter": 3,
        "question_type": "listening_comprehension",
        "question": "Who becomes Wilbur's first friend at the farm?",
        "options": ["Charlotte the spider", "Templeton the rat", "The sheep", "The goose"],
        "correct_answer": 0,
        "explanation": "거미 샬롯이 윌버의 첫 번째 친구가 됩니다.",
        "audio_timestamp": "00:12:30"
    },
    {
        "id": 7,
        "book_id": 1,
        "chapter": 3,
        "question_type": "vocabulary",
        "question": "What does 'web' mean in this context?",
        "options": ["인터넷", "거미줄", "그물", "웹사이트"],
        "correct_answer": 1,
        "explanation": "이 맥락에서 'web'은 거미가 만든 '거미줄'을 의미합니다.",
        "audio_timestamp": "00:14:15"
    },

    # ===== Magic Tree House #1 (Book ID: 2) =====
    # Chapter 1
    {
        "id": 8,
        "book_id": 2,
        "chapter": 1,
        "question_type": "listening_comprehension",
        "question": "Where do Jack and Annie find the tree house?",
        "options": ["In the park", "In the woods", "In their backyard", "At school"],
        "correct_answer": 1,
        "explanation": "잭과 애니는 숲(woods)에서 마법의 나무집을 발견합니다.",
        "audio_timestamp": "00:03:45"
    },
    {
        "id": 9,
        "book_id": 2,
        "chapter": 1,
        "question_type": "vocabulary",
        "question": "What does 'mysterious' mean?",
        "options": ["신비로운", "무서운", "재미있는", "큰"],
        "correct_answer": 0,
        "explanation": "'Mysterious'는 '신비로운, 수수께끼 같은'이라는 뜻입니다.",
        "audio_timestamp": "00:02:20"
    },

    # Chapter 2
    {
        "id": 10,
        "book_id": 2,
        "chapter": 2,
        "question_type": "listening_comprehension",
        "question": "What happens when Annie points to a picture in the book?",
        "options": ["Nothing happens", "The tree house starts spinning", "The book disappears", "They fall asleep"],
        "correct_answer": 1,
        "explanation": "애니가 책의 그림을 가리키자 나무집이 돌기 시작합니다.",
        "audio_timestamp": "00:08:30"
    },
    {
        "id": 11,
        "book_id": 2,
        "chapter": 2,
        "question_type": "vocabulary",
        "question": "What does 'spinning' mean?",
        "options": ["날아가는", "돌고 있는", "떨어지는", "멈춰있는"],
        "correct_answer": 1,
        "explanation": "'Spinning'은 '돌고 있는, 회전하는'이라는 뜻입니다.",
        "audio_timestamp": "00:09:15"
    },

    # Chapter 3
    {
        "id": 12,
        "book_id": 2,
        "chapter": 3,
        "question_type": "listening_comprehension",
        "question": "Where do Jack and Annie travel to?",
        "options": ["The future", "Dinosaur times", "Ancient Egypt", "Medieval times"],
        "correct_answer": 1,
        "explanation": "잭과 애니는 공룡 시대로 여행을 떠납니다.",
        "audio_timestamp": "00:12:45"
    },
    {
        "id": 13,
        "book_id": 2,
        "chapter": 3,
        "question_type": "vocabulary",
        "question": "What does 'prehistoric' mean?",
        "options": ["미래의", "선사시대의", "현재의", "과거의"],
        "correct_answer": 1,
        "explanation": "'Prehistoric'은 '선사시대의, 역사 이전의'라는 뜻입니다.",
        "audio_timestamp": "00:13:20"
    },

    # ===== Wonder (Book ID: 3) =====
    # Chapter 1
    {
        "id": 14,
        "book_id": 3,
        "chapter": 1,
        "question_type": "listening_comprehension",
        "question": "What is special about August's appearance?",
        "options": ["He is very tall", "He has facial differences", "He has blue hair", "He wears glasses"],
        "correct_answer": 1,
        "explanation": "어거스트는 얼굴에 특별한 차이점이 있습니다.",
        "audio_timestamp": "00:05:30"
    },
    {
        "id": 15,
        "book_id": 3,
        "chapter": 1,
        "question_type": "vocabulary",
        "question": "What does 'ordinary' mean?",
        "options": ["특별한", "평범한", "이상한", "아름다운"],
        "correct_answer": 1,
        "explanation": "'Ordinary'는 '평범한, 일반적인'이라는 뜻입니다.",
        "audio_timestamp": "00:02:15"
    },

    # Chapter 2
    {
        "id": 16,
        "book_id": 3,
        "chapter": 2,
        "question_type": "listening_comprehension",
        "question": "How does August feel about starting school?",
        "options": ["Excited", "Nervous", "Angry", "Bored"],
        "correct_answer": 1,
        "explanation": "어거스트는 학교에 가는 것에 대해 긴장하고 있습니다.",
        "audio_timestamp": "00:07:45"
    },
    {
        "id": 17,
        "book_id": 3,
        "chapter": 2,
        "question_type": "vocabulary",
        "question": "What does 'nervous' mean?",
        "options": ["기쁜", "긴장한", "화난", "슬픈"],
        "correct_answer": 1,
        "explanation": "'Nervous'는 '긴장한, 불안한'이라는 뜻입니다.",
        "audio_timestamp": "00:08:20"
    },

    # Chapter 3
    {
        "id": 18,
        "book_id": 3,
        "chapter": 3,
        "question_type": "listening_comprehension",
        "question": "Who shows August around the school?",
        "options": ["The principal", "His teacher", "Three students", "His mom"],
        "correct_answer": 2,
        "explanation": "세 명의 학생들이 어거스트에게 학교를 안내해줍니다.",
        "audio_timestamp": "00:11:30"
    },
    {
        "id": 19,
        "book_id": 3,
        "chapter": 3,
        "question_type": "vocabulary",
        "question": "What does 'tour' mean?",
        "options": ["시험", "견학", "숙제", "점심"],
        "correct_answer": 1,
        "explanation": "'Tour'는 '견학, 둘러보기'라는 뜻입니다.",
        "audio_timestamp": "00:12:10"
    },

    # ===== 추가 챕터들 (각 책당 더 많은 챕터) =====
    # Charlotte's Web Chapter 4
    {
        "id": 20,
        "book_id": 1,
        "chapter": 4,
        "question_type": "listening_comprehension",
        "question": "What does Charlotte write in her web to save Wilbur?",
        "options": ["HELLO", "SOME PIG", "GOODBYE", "HELP ME"],
        "correct_answer": 1,
        "explanation": "샬롯은 윌버를 구하기 위해 거미줄에 'SOME PIG'라고 씁니다.",
        "audio_timestamp": "00:18:45"
    },
    {
        "id": 21,
        "book_id": 1,
        "chapter": 4,
        "question_type": "vocabulary",
        "question": "What does 'miracle' mean?",
        "options": ["문제", "기적", "실수", "계획"],
        "correct_answer": 1,
        "explanation": "'Miracle'은 '기적, 놀라운 일'이라는 뜻입니다.",
        "audio_timestamp": "00:19:30"
    },

    # Magic Tree House Chapter 4
    {
        "id": 22,
        "book_id": 2,
        "chapter": 4,
        "question_type": "listening_comprehension",
        "question": "What kind of dinosaur do Jack and Annie see first?",
        "options": ["T-Rex", "Triceratops", "Pteranodon", "Stegosaurus"],
        "correct_answer": 2,
        "explanation": "잭과 애니가 처음 본 공룡은 프테라노돈입니다.",
        "audio_timestamp": "00:15:20"
    },
    {
        "id": 23,
        "book_id": 2,
        "chapter": 4,
        "question_type": "vocabulary",
        "question": "What does 'enormous' mean?",
        "options": ["작은", "거대한", "빠른", "느린"],
        "correct_answer": 1,
        "explanation": "'Enormous'는 '거대한, 엄청나게 큰'이라는 뜻입니다.",
        "audio_timestamp": "00:16:05"
    },

    # Wonder Chapter 4
    {
        "id": 24,
        "book_id": 3,
        "chapter": 4,
        "question_type": "listening_comprehension",
        "question": "What subject is August best at?",
        "options": ["English", "Math", "Science", "Art"],
        "correct_answer": 2,
        "explanation": "어거스트는 과학 과목을 가장 잘합니다.",
        "audio_timestamp": "00:14:15"
    },
    {
        "id": 25,
        "book_id": 3,
        "chapter": 4,
        "question_type": "vocabulary",
        "question": "What does 'brilliant' mean?",
        "options": ["어두운", "똑똑한", "무서운", "재미없는"],
        "correct_answer": 1,
        "explanation": "'Brilliant'는 '똑똑한, 뛰어난'이라는 뜻입니다.",
        "audio_timestamp": "00:15:00"
    },

    # Charlotte's Web Chapter 5
    {
        "id": 26,
        "book_id": 1,
        "chapter": 5,
        "question_type": "listening_comprehension",
        "question": "How do people react to the words in Charlotte's web?",
        "options": ["They ignore it", "They are amazed", "They are scared", "They don't notice"],
        "correct_answer": 1,
        "explanation": "사람들은 샬롯의 거미줄 글자를 보고 놀라워합니다.",
        "audio_timestamp": "00:22:30"
    },
    {
        "id": 27,
        "book_id": 1,
        "chapter": 5,
        "question_type": "vocabulary",
        "question": "What does 'amazed' mean?",
        "options": ["화난", "놀란", "슬픈", "지친"],
        "correct_answer": 1,
        "explanation": "'Amazed'는 '놀란, 깜짝 놀란'이라는 뜻입니다.",
        "audio_timestamp": "00:23:15"
    }
]

# ================ 기본 라우트들 ================

@app.route("/") 
def home(): 
    if not current_user.is_authenticated: 
        return redirect("/login") 
    return render_template("index.html")

@app.route('/api')
def api_info():
    return jsonify({
        "message": "수리딩어학원 QR코드 학습 시스템",
        "academy": "Sureading Academy",
        "system": "QR Code Based Learning Platform",
        "features": [
            "QR코드 스캔으로 즉시 학습 시작",
            "실시간 음원 재생",
            "단계별 문제 풀이",
            "학습 진도 자동 추적",
            "태블릿 최적화 인터페이스"
        ],
        "status": "running"
    })

@app.route('/api/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "database": "connected",
        "version": "2.0.0 - QR Learning System"
    })

@app.route('/api/test')
def test_api():
    return jsonify({
        'message': 'API 테스트 성공!',
        'timestamp': datetime.utcnow().isoformat()
    })

# ================ QR코드 학습 시스템 API ================

@app.route('/qr/<qr_code>')
def scan_qr(qr_code):
    """QR코드 스캔 시 호출되는 엔드포인트"""
    book = next((book for book in books_data if book['qr_code'] == qr_code.upper()), None)

    if not book:
        return jsonify({"error": "유효하지 않은 QR코드입니다"}), 404

    learning_url = f"https://suellibrary.store/learning/{book['id']}"

    return jsonify({
        "success": True,
        "book": book,
        "learning_url": learning_url,
        "message": f"'{book['title']}' 학습을 시작합니다!",
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/api/learning/<int:book_id>')
def get_learning_content(book_id):
    """특정 도서의 학습 컨텐츠 조회"""
    book = next((book for book in books_data if book['id'] == book_id), None)

    if not book:
        return jsonify({"error": "도서를 찾을 수 없습니다"}), 404

    book_questions = [q for q in questions_data if q['book_id'] == book_id]

    return jsonify({
        "book": book,
        "audio_url": book['audio_url'],
        "total_questions": len(book_questions),
        "chapters": book['total_chapters'],
        "estimated_time": book['reading_time'],
        "learning_started": datetime.utcnow().isoformat()
    })

@app.route('/api/questions/<int:book_id>/<int:chapter>')
def get_chapter_questions(book_id, chapter):
    """특정 도서의 특정 챕터 문제들"""
    book = next((book for book in books_data if book['id'] == book_id), None)

    if not book:
        return jsonify({"error": "도서를 찾을 수 없습니다"}), 404

    chapter_questions = [
        q for q in questions_data
        if q['book_id'] == book_id and q['chapter'] == chapter
    ]

    return jsonify({
        "book_title": book['title'],
        "chapter": chapter,
        "audio_url": book['audio_url'],
        "questions": chapter_questions,
        "total_questions": len(chapter_questions),
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/api/submit-answer', methods=['POST'])
def submit_answer():
    """학생 답안 제출 및 채점"""
    data = request.get_json()

    if not data:
        return jsonify({"error": "답안 데이터가 없습니다"}), 400

    question_id = data.get('question_id')
    student_answer = data.get('answer')
    student_id = data.get('student_id', 'anonymous')

    question = next((q for q in questions_data if q['id'] == question_id), None)

    if not question:
        return jsonify({"error": "문제를 찾을 수 없습니다"}), 404

    is_correct = student_answer == question['correct_answer']

    result = {
        "question_id": question_id,
        "is_correct": is_correct,
        "correct_answer": question['correct_answer'],
        "explanation": question['explanation'],
        "student_answer": student_answer,
        "timestamp": datetime.utcnow().isoformat()
    }

    if is_correct:
        result["message"] = "정답입니다! 🎉"
    else:
        result["message"] = "틀렸습니다. 다시 한번 들어보세요! 🎧"

    return jsonify(result)

@app.route('/api/books')
def get_books():
    """QR코드가 있는 모든 도서 목록"""
    return jsonify({
        "books": books_data,
        "total": len(books_data),
        "qr_scan_url": "https://suellibrary.store/qr/{qr_code}",
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/api/generate-qr/<int:book_id>')
def generate_qr_info(book_id):
    """도서별 QR코드 정보 생성"""
    book = next((book for book in books_data if book['id'] == book_id), None)

    if not book:
        return jsonify({"error": "도서를 찾을 수 없습니다"}), 404

    qr_url = f"https://suellibrary.store/qr/{book['qr_code']}"

    return jsonify({
        "book": book,
        "qr_code": book['qr_code'],
        "qr_url": qr_url,
        "print_info": {
            "title": book['title'],
            "level": f"Level {book['level']}",
            "qr_text": "태블릿으로 QR코드를 스캔하세요!"
        },
        "timestamp": datetime.utcnow().isoformat()
    })

# ================ 학생 관리 API ================

@app.route('/api/students')
def get_students():
    """모든 학생 목록 조회"""
    class_filter = request.args.get('class')
    level_filter = request.args.get('level')
    status_filter = request.args.get('status', 'active')

    filtered_students = students_data.copy()

    if class_filter:
        filtered_students = [s for s in filtered_students if s['class'] == class_filter]

    if level_filter:
        filtered_students = [s for s in filtered_students if s['level'] == int(level_filter)]

    filtered_students = [s for s in filtered_students if s['status'] == status_filter]

    return jsonify({
        "students": filtered_students,
        "total": len(filtered_students),
        "classes": ["채두윜반", "소설클래스", "내신클래스", "영자신문클래스"],
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/api/students/<student_id>')
def get_student(student_id):
    """특정 학생 정보 조회 (ID 또는 학번으로)"""
    student = None

    if student_id.isdigit():
        student = next((s for s in students_data if s['id'] == int(student_id)), None)
    else:
        student = next((s for s in students_data if s['student_id'] == student_id), None)

    if not student:
        return jsonify({"error": "학생을 찾을 수 없습니다"}), 404

    current_books_info = [
        book for book in books_data
        if book['id'] in student['current_books']
    ]

    completed_books_info = [
        book for book in books_data
        if book['id'] in student['completed_books']
    ]

    recent_records = [
        record for record in learning_records
        if record['student_id'] == student['id']
    ][-5:]

    return jsonify({
        "student": student,
        "current_books": current_books_info,
        "completed_books": completed_books_info,
        "recent_activities": recent_records,
        "stats": {
            "total_books_completed": len(student['completed_books']),
            "current_books_count": len(student['current_books']),
            "total_study_hours": round(student['total_study_time'] / 60, 1)
        },
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/api/qr-scan-record', methods=['POST'])
def record_qr_scan():
    """QR코드 스캔 기록 저장"""
    data = request.get_json()

    if not data:
        return jsonify({"error": "스캔 데이터가 없습니다"}), 400

    student_id = data.get('student_id')
    qr_code = data.get('qr_code')

    if not student_id or not qr_code:
        return jsonify({"error": "학생 ID와 QR코드가 필요합니다"}), 400

    student = next((s for s in students_data if s['student_id'] == student_id), None)
    if not student:
        return jsonify({"error": "등록되지 않은 학생입니다"}), 404

    book = next((b for b in books_data if b['qr_code'] == qr_code.upper()), None)
    if not book:
        return jsonify({"error": "유효하지 않은 QR코드입니다"}), 404

    new_record = {
        "id": len(learning_records) + 1,
        "student_id": student['id'],
        "book_id": book['id'],
        "chapter": 1,
        "qr_scanned_at": datetime.utcnow().isoformat(),
        "audio_listened": False,
        "questions_attempted": 0,
        "questions_correct": 0,
        "time_spent": 0,
        "session_completed": False
    }

    learning_records.append(new_record)

    student['last_activity'] = datetime.utcnow().isoformat()

    return jsonify({
        "success": True,
        "student": {
            "name": student['name'],
            "english_name": student['english_name'],
            "level": student['level'],
            "class": student['class']
        },
        "book": book,
        "record_id": new_record['id'],
        "learning_url": f"https://suellibrary.store/learning/{book['id']}?student={student_id}",
        "message": f"{student['name']}님, '{book['title']}' 학습을 시작합니다!",
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/api/students/<student_id>/stats')
def get_student_stats(student_id):
    """학생별 상세 학습 통계"""
    student = None

    if student_id.isdigit():
        student = next((s for s in students_data if s['id'] == int(student_id)), None)
    else:
        student = next((s for s in students_data if s['student_id'] == student_id), None)

    if not student:
        return jsonify({"error": "학생을 찾을 수 없습니다"}), 404

    student_records = [r for r in learning_records if r['student_id'] == student['id']]

    total_sessions = len(student_records)
    total_questions = sum(r['questions_attempted'] for r in student_records)
    correct_answers = sum(r['questions_correct'] for r in student_records)
    accuracy = round((correct_answers / total_questions * 100) if total_questions > 0 else 0, 1)

    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent_records = [
        r for r in student_records
        if datetime.fromisoformat(r['qr_scanned_at'].replace('Z', '+00:00')) > seven_days_ago
    ]

    return jsonify({
        "student": {
            "name": student['name'],
            "student_id": student['student_id'],
            "level": student['level'],
            "class": student['class']
        },
        "overall_stats": {
            "total_study_time": student['total_study_time'],
            "total_sessions": total_sessions,
            "books_completed": len(student['completed_books']),
            "books_in_progress": len(student['current_books']),
            "question_accuracy": f"{accuracy}%",
            "total_questions_answered": total_questions
        },
        "recent_activity": {
            "sessions_last_7_days": len(recent_records),
            "time_spent_last_7_days": sum(r['time_spent'] for r in recent_records)
        },
        "learning_records": student_records[-10:],
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route('/api/classes/<class_name>/students')
def get_class_students(class_name):
    """특정 클래스의 학생들"""
    class_students = [s for s in students_data if s['class'] == class_name]

    if not class_students:
        return jsonify({"error": "해당 클래스를 찾을 수 없습니다"}), 404

    total_students = len(class_students)
    avg_level = round(sum(s['level'] for s in class_students) / total_students, 1)
    total_study_time = sum(s['total_study_time'] for s in class_students)

    return jsonify({
        "class_name": class_name,
        "students": class_students,
        "class_stats": {
            "total_students": total_students,
            "average_level": avg_level,
            "total_study_time": total_study_time,
            "average_study_time": round(total_study_time / total_students) if total_students > 0 else 0
        },
        "timestamp": datetime.utcnow().isoformat()
    })
# ================ 학습 페이지 라우트 ================

@app.route('/learning/<int:book_id>')
def learning_page(book_id):
    """QR코드 스캔 후 실제 학습 페이지"""
    book = next((book for book in books_data if book['id'] == book_id), None)

    if not book:
        return "도서를 찾을 수 없습니다", 404

    # Charlotte's Web (book_id=1)인 경우 전용 템플릿 사용
    if book_id == 1:
        return render_template('charlotte_web_learning.html', book=book)

    # 다른 책들은 기존 학습 템플릿 사용
    return render_template('learning.html', book=book)

@app.route('/learning/<int:book_id>/chapter/<int:chapter>')
def learning_chapter(book_id, chapter):
    """특정 챕터 학습 페이지"""
    book = next((book for book in books_data if book['id'] == book_id), None)

    if not book:
        return "도서를 찾을 수 없습니다", 404

    # 해당 챕터의 문제들
    chapter_questions = [
        q for q in questions_data
        if q['book_id'] == book_id and q['chapter'] == chapter
    ]

    return render_template('learning_chapter.html',
                         book=book,
                         chapter=chapter,
                         questions=chapter_questions)

@app.route('/level-learning.html')
def level_learning():
    return render_template('level-learning.html')
    """레벨테스트 메인 페이지 - 레벨 및 도서 선택"""
    return render_template('level_test_main.html')

@app.route("/level-test/main")
def level_test_main_page():
    """레벨테스트 메인 페이지"""
    return render_template("level_test_main.html")


@app.route("/level-test/start/<int:level>/<book_id>")
def level_test_start(level, book_id):
    """레벨테스트 실행 페이지"""
    return render_template("level_test_execute.html", level=level, book_id=book_id)

# ================ 개별 도서별 레벨테스트 라우트 ================

# Level 1 Books
@app.route("/level-test/start/1/cat-hat")
def level_test_cat_hat():
    """The Cat in the Hat 레벨테스트"""
    return render_template("level_test_execute.html", level=1, book_id="cat-hat")

@app.route("/level-test/start/1/green-eggs-ham")
def level_test_green_eggs():
    """Green Eggs and Ham 레벨테스트"""
    return render_template("level_test_execute.html", level=1, book_id="green-eggs-ham")

@app.route("/level-test/start/1/brown-bear")
def level_test_brown_bear():
    """Brown Bear 레벨테스트"""
    return render_template("level_test_execute.html", level=1, book_id="brown-bear")

# Level 2 Books
@app.route("/level-test/start/2/frog-toad")
def level_test_frog_toad():
    """Frog and Toad 레벨테스트"""
    return render_template("level_test_execute.html", level=2, book_id="frog-toad")

@app.route("/level-test/start/2/henry-mudge")
def level_test_henry_mudge():
    """Henry and Mudge 레벨테스트"""
    return render_template("level_test_execute.html", level=2, book_id="henry-mudge")

@app.route("/level-test/start/2/elephant-piggie")
def level_test_elephant_piggie():
    """Elephant and Piggie 레벨테스트"""
    return render_template("level_test_execute.html", level=2, book_id="elephant-piggie")

# Level 3 Books
@app.route("/level-test/start/3/magic-tree")
def level_test_magic_tree():
    """Magic Tree House 레벨테스트"""
    return render_template("level_test_execute.html", level=3, book_id="magic-tree")

@app.route("/level-test/start/3/junie-b")
def level_test_junie_b():
    """Junie B. Jones 레벨테스트"""
    return render_template("level_test_execute.html", level=3, book_id="junie-b")

@app.route("/level-test/start/3/cam-jansen")
def level_test_cam_jansen():
    """Cam Jansen 레벨테스트"""
    return render_template("level_test_execute.html", level=3, book_id="cam-jansen")

# Level 4 Books
@app.route("/level-test/start/4/holes")
def level_test_holes():
    """Holes 레벨테스트"""
    return render_template("level_test_execute.html", level=4, book_id="holes")

@app.route("/level-test/start/4/bridge-terabithia")
def level_test_bridge_terabithia():
    """Bridge to Terabithia 레벨테스트"""
    return render_template("level_test_execute.html", level=4, book_id="bridge-terabithia")

@app.route("/level-test/start/4/wonder")
def level_test_wonder():
    """Wonder 레벨테스트"""
    return render_template("level_test_execute.html", level=4, book_id="wonder")

# Level 5 Books
@app.route("/level-test/start/5/book-thief")
def level_test_book_thief():
    """The Book Thief 레벨테스트"""
    return render_template("level_test_execute.html", level=5, book_id="book-thief")

@app.route("/level-test/start/5/man-called-ove")
def level_test_man_called_ove():
    """A Man Called Ove 레벨테스트"""
    return render_template("level_test_execute.html", level=5, book_id="man-called-ove")

@app.route("/level-test/start/5/tkam")
def level_test_tkam():
    """To Kill a Mockingbird 레벨테스트"""
    return render_template("level_test_execute.html", level=5, book_id="tkam")


# ================ 개별 도서별 레벨테스트 라우트 ================



# ================ 로그인 및 관리자 시스템 ================

from flask import redirect, url_for, flash, session
from flask_login import login_user, logout_user
from models.user_auth import User, USERS_DB

# Flask-Login user_loader 수정 (기존 None을 실제 사용자로)
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# 로그인 페이지
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # 사용자 인증
        user = User.get_by_username(username)
        if user and user.password == password:
            login_user(user)
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            
            # 관리자면 관리자 페이지로, 아니면 메인 페이지로
            if user.is_admin:
                return redirect('/admin')
            else:
                return redirect('/')
        else:
            flash('로그인 정보가 올바르지 않습니다.', 'error')
    
    return render_template('login.html')

# 로그아웃
@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect('/login')

# 관리자 페이지
@app.route('/admin')
@login_required
def admin():
    # 관리자 권한 체크
    if not (hasattr(current_user, 'is_admin') and current_user.is_admin):
        flash('관리자 권한이 필요합니다.', 'error')
        return redirect('/login')
    
    return render_template('admin.html')

# 기존 메인 페이지에 로그인 체크 추가 (라인 504 수정 필요)
# @app.route('/') 
# def index():
#     if not current_user.is_authenticated:
#         return redirect('/login')
#     return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6666)


# ================ 회원가입 시스템 ================

# 회원가입 페이지
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        student_name = request.form.get('student_name')
        parent_email = request.form.get('parent_email')
        phone = request.form.get('phone')
        class_type = request.form.get('class_type')
        
        # 입력 검증
        if not all([username, password, password_confirm, student_name, parent_email]):
            flash('모든 필수 항목을 입력해주세요.', 'error')
            return render_template('signup.html')
        
        if password != password_confirm:
            flash('비밀번호가 일치하지 않습니다.', 'error')
            return render_template('signup.html')
        
        if len(password) < 4:
            flash('비밀번호는 4자 이상이어야 합니다.', 'error')
            return render_template('signup.html')
        
        # 사용자명 중복 체크
        if User.get_by_username(username):
            flash('이미 존재하는 아이디입니다.', 'error')
            return render_template('signup.html')
        
        # 새 사용자 생성
        new_id = max(USERS_DB.keys()) + 1 if USERS_DB else 1
        new_user = User(new_id, username, password, student_name, 1, False)
        USERS_DB[new_id] = new_user
        
        flash('회원가입이 완료되었습니다! 로그인해주세요.', 'success')
        return redirect('/login')
    
    return render_template('signup.html')


# ================ 마이페이지 (학습현황) ================

@app.route('/my-progress')
@login_required
def my_progress():
    if not current_user.is_authenticated:
        return redirect('/login')
    
    # 템플릿에 맞는 데이터 구조 생성
    progress_data = {
        'student_name': current_user.student_name,
        'current_level': current_user.level,
        'total_books_read': 8,
        'total_study_time': '24시간',
        'recent_books': [
            {
                'title': "Charlotte's Web",
                'qr_code': 'CW001',
                'progress': 75
            },
            {
                'title': "Magic Tree House #1", 
                'qr_code': 'MTH001',
                'progress': 45
            },
            {
                'title': "Frog and Toad",
                'qr_code': 'FT001', 
                'progress': 100
            }
        ],
        'weekly_stats': {
            'quiz_accuracy': 89,
            'books_completed': 2,
            'study_hours': '8시간'
        }
    }
    
    return render_template('my_progress.html', progress=progress_data)


# ================ 추가 관리자 페이지들 ================

# 관리자 - 학생 관리 페이지
@app.route('/admin/students')
@login_required
def admin_students():
    if not (hasattr(current_user, 'is_admin') and current_user.is_admin):
        flash('관리자 권한이 필요합니다.', 'error')
        return redirect('/login')
    
    # 학생 목록 데이터 생성
    students = []
    for user in USERS_DB.values():
        if not user.is_admin:
            students.append({
                'id': user.id,
                'username': user.username,
                'student_name': user.student_name,
                'level': user.level,
                'last_login': '2024-07-12',
                'progress': '진행 중',
                'books_completed': 5
            })
    
    return render_template('admin_students.html', students=students)

# 관리자 - 도서 관리 페이지
@app.route('/admin/books')
@login_required
def admin_books():
    if not (hasattr(current_user, 'is_admin') and current_user.is_admin):
        flash('관리자 권한이 필요합니다.', 'error')
        return redirect('/login')
    
    return render_template('admin_books.html', books=books_data)

# 관리자 - 대시보드 페이지
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not (hasattr(current_user, 'is_admin') and current_user.is_admin):
        flash('관리자 권한이 필요합니다.', 'error')
        return redirect('/login')
    
    return render_template('admin_dashboard.html')

# 관리자 - 분석 페이지
@app.route('/admin/analytics')
@login_required
def admin_analytics():
    if not (hasattr(current_user, 'is_admin') and current_user.is_admin):
        flash('관리자 권한이 필요합니다.', 'error')
        return redirect('/login')
    
    # 분석 데이터
    analytics_data = {
        'monthly_stats': {
            'total_reading_time': '245시간',
            'books_completed': 87,
            'average_score': 85.3,
            'active_students': 15
        },
        'level_distribution': [
            {'level': 1, 'students': 5},
            {'level': 2, 'students': 8}, 
            {'level': 3, 'students': 12},
            {'level': 4, 'students': 6},
            {'level': 5, 'students': 3}
        ]
    }
    
    return render_template('admin_analytics.html', analytics=analytics_data)

