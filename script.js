// 'data' is provided by data.js

function showQuestion() {
  if (data.length === 0) return;
  const qa = data[Math.floor(Math.random() * data.length)];
  document.getElementById('question').innerHTML = `<img src="${qa.question}" alt="question">`;
  document.getElementById('answer').innerHTML = `<img src="${qa.answer}" alt="answer">`;
  document.getElementById('answer').style.display = 'none';
}

document.getElementById('showBtn').addEventListener('click', () => {
  document.getElementById('answer').style.display = 'block';
});

document.getElementById('nextBtn').addEventListener('click', showQuestion);

showQuestion();
