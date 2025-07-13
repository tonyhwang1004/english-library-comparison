// SureReading 데이터 번들 - bash로 생성됨
// 생성일시: Thu Jul 10 13:21:27 UTC 2025
window.SUREADING_DATA = {
  books: {
    level1: [
      {
  "id": "PP001",
  "title": "Peppa Pig - Muddy Puddles",
  "author": "Ladybird Books",
  "cover": "🐷",
  "coverColor": "linear-gradient(45deg, #ff6b6b, #ee5a24)",
  "words": 1200,
  "qrCode": "PP001",
  "summary": "Peppa and George love jumping in muddy puddles!"
}
    ],
    level2: [
      {
  "id": "FT001",
  "title": "The Three Little Pigs",
  "author": "Traditional",
  "cover": "🐷",
  "coverColor": "linear-gradient(45deg, #ff9a56, #ffad56)",
  "words": 1800,
  "qrCode": "FT001",
  "summary": "Three little pigs build houses to protect themselves from the big bad wolf."
},
      {
  "id": "MTH001",
  "title": "Math Adventure - Number Island",
  "author": "Educational Press", 
  "cover": "🏝️",
  "coverColor": "linear-gradient(45deg, #4ecdc4, #44a08d)",
  "words": 2500,
  "qrCode": "MTH001",
  "summary": "Explore Number Island where math becomes a thrilling adventure!"
}
    ],
    level3: [
      {
  "id": "CW001",
  "title": "Charlotte's Web",
  "author": "E.B. White",
  "cover": "🕷️", 
  "coverColor": "linear-gradient(45deg, #fd79a8, #fdcb6e)",
  "words": 31938,
  "qrCode": "CW001",
  "summary": "The timeless story of friendship between Wilbur the pig and Charlotte the spider."
}
    ],
    level4: [
      {
  "id": "HP001",
  "title": "Harry Potter and the Philosopher's Stone (Simplified)",
  "author": "J.K. Rowling",
  "cover": "⚡",
  "coverColor": "linear-gradient(45deg, #8B0000, #FFD700)",
  "words": 45000,
  "qrCode": "HP001", 
  "summary": "A young wizard discovers his magical heritage and begins his journey at Hogwarts School of Witchcraft and Wizardry."
}
    ],
    level5: [
      {
  "id": "LR001",
  "title": "Lord of the Rings: Fellowship (Advanced Reading)",
  "author": "J.R.R. Tolkien",
  "cover": "💍",
  "coverColor": "linear-gradient(45deg, #2F4F4F, #8FBC8F)",
  "words": 75000,
  "qrCode": "LR001",
  "summary": "An epic fantasy adventure following the quest to destroy the One Ring and save Middle-earth from the Dark Lord Sauron."
}
    ],
  },
  questions: {
    "FT001": {
  "bookId": "FT001",
  "totalChapters": 2,
  "chapters": {
    "0": {
      "chapterTitle": "Building Houses",
      "questionCount": 2,
      "questions": [
        {
          "question": "What materials did the three pigs use for their houses?",
          "options": ["Straw, sticks, bricks", "Wood, stone, metal", "Paper, plastic, glass", "Sand, mud, clay"],
          "answer": 0,
          "explanation": "The three pigs used straw, sticks, and bricks to build their houses."
        }
      ]
    }
  }
},
    "HP001": {
  "bookId": "HP001",
  "totalChapters": 5,
  "chapters": {
    "0": {
      "chapterTitle": "The Boy Who Lived",
      "questionCount": 4,
      "questions": [
        {
          "question": "What makes Harry Potter special in the wizarding world?",
          "options": ["He can fly", "He survived a killing curse", "He's very smart", "He's very rich"],
          "answer": 1,
          "explanation": "Harry survived the killing curse as a baby, making him famous."
        }
      ]
    }
  }
},
    "LR001": {
  "bookId": "LR001", 
  "totalChapters": 6,
  "chapters": {
    "0": {
      "chapterTitle": "A Long-expected Party",
      "questionCount": 3,
      "questions": [
        {
          "question": "What is the significance of the One Ring in Middle-earth?",
          "options": ["It grants immortality", "It controls all other rings", "It provides wisdom", "It creates gold"],
          "answer": 1,
          "explanation": "The One Ring was made to control all other Rings of Power."
        }
      ]
    }
  }
},
    "MTH001": {
  "bookId": "MTH001", 
  "totalChapters": 4,
  "chapters": {
    "0": {
      "chapterTitle": "Arrival at Number Island",
      "questionCount": 2,
      "questions": [
        {
          "question": "If you have 3 apples and find 4 more, how many do you have?",
          "options": ["6", "7", "8", "9"],
          "answer": 1,
          "explanation": "3 + 4 = 7 apples!"
        }
      ]
    }
  }
},
    "PP001": {
  "bookId": "PP001",
  "totalChapters": 3,
  "chapters": {
    "0": {
      "chapterTitle": "Getting Ready",
      "questionCount": 3,
      "questions": [
        {
          "question": "What does Peppa love to do on rainy days?",
          "options": ["Stay inside", "Jump in muddy puddles", "Read books", "Sleep"],
          "answer": 1,
          "explanation": "Peppa loves jumping in muddy puddles!"
        },
        {
          "question": "Who is Peppa's little brother?",
          "options": ["Pedro", "George", "Richard", "Danny"],
          "answer": 1,
          "explanation": "George is Peppa's little brother."
        }
      ]
    }
  }
}
  },
  metadata: {
    generatedAt: new Date().toISOString(),
    generator: "bash",
    totalBooks: 0,
    totalQuestions: 0
  }
};

// 통계 계산
Object.values(window.SUREADING_DATA.books).forEach(levelBooks => {
  window.SUREADING_DATA.metadata.totalBooks += levelBooks.length;
});
window.SUREADING_DATA.metadata.totalQuestions = Object.keys(window.SUREADING_DATA.questions).length;

// 호환성을 위한 전역 변수
window.books = window.SUREADING_DATA.books;
window.questions = window.SUREADING_DATA.questions;

console.log('📚 SureReading 데이터 로딩 완료!');
console.log('📊 총 ' + window.SUREADING_DATA.metadata.totalBooks + '권, ' + 
           window.SUREADING_DATA.metadata.totalQuestions + '개 문제 세트');
