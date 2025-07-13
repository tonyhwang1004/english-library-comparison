#!/bin/bash
#  테스트 스크립트

echo "🧪  테스트 시작"
echo "======================"

# Flask 서버 재시작
echo "🔄 Flask 서버 재시작..."
pkill -f "python.*app.py" 2>/dev/null || true
sleep 2
python3 app.py &

sleep 3

# 브라우저 테스트 (Linux의 경우)
if command -v xdg-open &> /dev/null; then
    echo "🌐 브라우저에서 테스트 페이지 열기..."
    xdg-open "http://localhost:5000"
    sleep 2
    xdg-open "http://localhost:5000/_learning"
fi

echo "✅ 테스트 준비 완료!"
echo ""
echo "📋 확인 사항:"
echo "1. 메인 페이지에서  카드 확인"
echo "2. 책 클릭해서 학습 페이지 진입"
echo "3. 음원 플레이어 확인 (음원 업로드 후)"
echo "4. 각 챕터의 문제 풀기 테스트"
echo ""
echo "🎵 음원 업로드가 필요하면 _audio_guide.md 참고"
