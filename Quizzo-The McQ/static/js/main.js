// Helper to get backend URL (adjust if needed)
const BACKEND_URL = "http://localhost:5000";

// Signup
const signupForm = document.getElementById('signupForm');
if (signupForm) {
    signupForm.onsubmit = async(e) => {
        e.preventDefault();
        const username = signupForm.username.value;
        const password = signupForm.password.value;
        const res = await fetch(`${BACKEND_URL}/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        const data = await res.json();
        document.getElementById('signupMsg').innerText = data.msg;
        if (res.status === 201) window.location = "login.html";
    };
}

// Login
const loginForm = document.getElementById('loginForm');
if (loginForm) {
    loginForm.onsubmit = async(e) => {
        e.preventDefault();
        const username = loginForm.username.value;
        const password = loginForm.password.value;
        const res = await fetch(`${BACKEND_URL}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password }),
            credentials: 'include'
        });
        const data = await res.json();
        document.getElementById('loginMsg').innerText = data.msg;
        if (res.status === 200) {
            if (data.role === 'admin') window.location = "admin.html";
            else window.location = "quiz.html";
        }
    };
}

// Admin: Add Quiz
const quizForm = document.getElementById('quizForm');
if (quizForm) {
    quizForm.onsubmit = async(e) => {
        e.preventDefault();
        const quiz = {
            title: quizForm.title.value,
            question: quizForm.question.value,
            options: [
                quizForm.option1.value,
                quizForm.option2.value,
                quizForm.option3.value,
                quizForm.option4.value
            ],
            correct: quizForm.correct.value
        };
        const res = await fetch(`${BACKEND_URL}/quiz`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(quiz),
            credentials: 'include'
        });
        const data = await res.json();
        document.getElementById('adminMsg').innerText = data.msg;
        quizForm.reset();
    };
}

// User: Load Quizzes
const quizContainer = document.getElementById('quizContainer');
if (quizContainer) {
    fetch(`${BACKEND_URL}/quizzes`, { credentials: 'include' })
        .then(res => res.json())
        .then(quizzes => {
                quizzes.forEach((quiz, idx) => {
                            const div = document.createElement('div');
                            div.innerHTML = `<h3>${quiz.title}</h3>
          <p>${quiz.question}</p>
          ${quiz.options.map((opt, i) =>
            `<label><input type="radio" name="q${idx}" value="${opt}"> ${opt}</label><br>`
          ).join('')}
          <hr>`;
        quizContainer.appendChild(div);
      });
    });
}

// User: Submit Quiz (basic, needs improvement for real use)
const submitQuiz = document.getElementById('submitQuiz');
if (submitQuiz) {
  submitQuiz.onclick = async () => {
    // For demo: just show a message
    document.getElementById('quizMsg').innerText = "Quiz submitted! (Implement logic)";
  };
}