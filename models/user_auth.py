# models/user_auth.py - 사용자 인증 모델 (관리자 권한 추가)
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin):
    def __init__(self, id, username, password, student_name, level=1, is_admin=False):
        self.id = id
        self.username = username
        self.password = password
        self.student_name = student_name
        self.level = level
        self.is_admin = is_admin  # 관리자 권한 추가
        self.created_at = datetime.now()
    
    def get_id(self):
        return str(self.id)
    
    @staticmethod
    def get(user_id):
        """사용자 ID로 사용자 조회"""
        try:
            return USERS_DB.get(int(user_id))
        except (ValueError, TypeError):
            return None
    
    @staticmethod
    def get_by_username(username):
        """사용자명으로 사용자 조회"""
        for user in USERS_DB.values():
            if user.username == username:
                return user
        return None

# 사용자 데이터베이스 (관리자 계정 포함)
USERS_DB = {
    # 관리자 계정들
    1: User(1, "sue", "sueadmin2024", "수 원장님", 5, is_admin=True),
    2: User(2, "tony", "tonyadmin2024", "토니 부원장님", 5, is_admin=True),
    
    # 일반 학생 계정들
    3: User(3, "student1", "password123", "김영수", 2),
    4: User(4, "student2", "password456", "이미영", 3),
    5: User(5, "student3", "password789", "박준호", 1),
    6: User(6, "demo", "demo", "체험 학생", 3),
}
