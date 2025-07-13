#!/bin/bash

# 현재 시스템 구조 분석 스크립트
echo "=== 현재 시스템 구조 분석 ==="

echo "1. 데이터베이스 파일 찾기"
find . -name "*.db" -o -name "*.sqlite" -o -name "*.sqlite3" 2>/dev/null
echo

echo "2. Python 앱 구조 확인"
echo "app.py 주요 내용:"
head -50 app.py | grep -E "def|class|@app|import|from" | head -20
echo

echo "3. 템플릿 파일 확인"
echo "templates 디렉토리:"
ls -la templates/
echo

echo "4. 모델 구조 확인"
if [ -d "models" ]; then
    echo "models 디렉토리:"
    find models -name "*.py" -exec echo "=== {} ===" \; -exec head -20 {} \;
fi
echo

echo "5. static 파일 확인"
echo "static 디렉토리 구조:"
find static -type f | head -20
echo

echo "6. 기존 해리포터 관련 파일 상세 확인"
echo "=== 해리포터 관련 파일들 ==="
for file in $(find . -name "*harry*" -o -name "*potter*" -o -name "*level4*"); do
    echo "파일: $file"
    if [[ $file == *.html ]]; then
        echo "HTML 파일 내용 (첫 20줄):"
        head -20 "$file"
    elif [[ $file == *.sh ]]; then
        echo "스크립트 파일 내용:"
        cat "$file"
    fi
    echo "------------------------"
done
echo

echo "7. 데이터베이스 스키마 확인"
if [ -f "init_db.py" ]; then
    echo "init_db.py 내용:"
    cat init_db.py | grep -E "CREATE|class|def" -A 5
fi
echo

echo "8. 현재 실행 중인 테스트나 프로세스"
echo "해리포터 관련 실행 가능한 스크립트:"
ls -la *.sh | grep -i harry
echo

echo "=== 분석 완료 ==="
