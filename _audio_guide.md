
## 📁 업로드 위치
- **로컬**: static/audio/
- **클라우드**: gs://kim-mom-reading-audio/audio//

## 📤 업로드 명령어
```bash
# 로컬 파일들을 클라우드에 업로드
gsutil -m cp static/audio/*.mp3 gs://kim-mom-reading-audio/audio//
gsutil -m acl ch -r -u AllUsers:R gs://kim-mom-reading-audio/audio//
```

## 🔗 URL 형식
https://storage.googleapis.com/kim-mom-reading-audio/audio//01.mp3
