document.addEventListener('DOMContentLoaded', function() {
    
    let currentQuestion = 1;

    // Select by id total-questions and get the number after ":"
    const totalQuestions = document.getElementById('total-questions').textContent.split(":")[1];

    showQuestion(currentQuestion);

    // Botones de siguiente y anterior
    document.querySelector("#next").onclick = () => {
        if (currentQuestion < totalQuestions) {
            currentQuestion++;
            showQuestion(currentQuestion);
        }
    }

    document.querySelector("#previous").onclick = () => {
        if (currentQuestion > 1) {
            currentQuestion--;
            showQuestion(currentQuestion);
        }
    }

    // Index buttons
    const indexButtons = document.querySelectorAll(".index-button");
    for (const button of indexButtons) {
        button.onclick = () => {
            currentQuestion = parseInt(button.value);
            showQuestion(currentQuestion);
        }
    }


    // Correct button
    document.querySelector("#correct").addEventListener('click', () => StateIndexButtons("correct"));

    // Incorrect button
    document.querySelector("#incorrect").addEventListener('click', () => StateIndexButtons("incorrect"));

    // All button
    document.querySelector("#all").addEventListener('click', () => StateIndexButtons("all"));

});

function showQuestion(questionNumber) {
  // Ocultar todas las preguntas
  const exam = document.getElementById('exam');
  if (exam) {
      const questions = document.querySelectorAll(".questionLoopNumber");
      for (const question of questions) {
          const questionIdNumber = question.id.split("-")[1];
          if (questionIdNumber == questionNumber) {
              question.style.display = "block";
              const questionId = question.children[0].id.split("-")[1];
              const indexButton = document.getElementById(`indexButton-${questionId}`);
              // Change the class of the button to "btn-dark"
              indexButton.classList.remove("btn-primary");
              indexButton.classList.add("btn-dark");
          } else {
            question.style.display = "none";
            const questionId = question.children[0].id.split("-")[1];
            const indexButton = document.getElementById(`indexButton-${questionId}`);
            // Change the class of the button to "btn-primary"
            indexButton.classList.remove("btn-dark");
            indexButton.classList.add("btn-primary");
          }
      }

      // Redirect the user to the top of the page with a smooth transition
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
  }
}


function StateIndexButtons(state) {
  switch (state) {
    case "correct":
        const correctQuestions = getQuestionsByStatus(true);
        updateIndexButtons(correctQuestions);
        showQuestionIndex(correctQuestions[0]);
        break;
    case "incorrect":
        const incorrectQuestions = getQuestionsByStatus(false);
        updateIndexButtons(incorrectQuestions);
        showQuestionIndex(incorrectQuestions[0]);
        break;
    case "all":
        const allQuestions = getAllQuestions();
        updateIndexButtons(allQuestions);
        showQuestion(1);
        break;
    default:
        console.error("Error: invalid state in stateIndexButtons function");
  }
}

function getQuestionsByStatus(status) {
  const questions = document.querySelectorAll(".questionsIds");
  const questionNumberLoop = [];
  for (const question of questions) {
    const questionId = question.id.split("-")[1];
    const question_status = document.getElementById(`questionStatus-${questionId}`);
    const isCorrect = question_status.textContent.trim() === "Correcto" ? true : false;
    if ((status && isCorrect) || (!status && !isCorrect)) {
      questionNumberLoop.push(questionId);
    }
  }
  return questionNumberLoop;
}

function getAllQuestions() {
  const questions = document.querySelectorAll(".questionsIds");
  return Array.from(questions).map((question) => question.id.split("-")[1]);
}

function updateIndexButtons(questionIds) {
  const indexButtons = document.querySelectorAll(".index-button");
  for (const button of indexButtons) {
    const indexId = button.id.split("-")[1];
    const shouldDisplay = questionIds.includes(indexId);
    button.parentElement.style.display = shouldDisplay ? "block" : "none";
  }
}

function showQuestionIndex(questionId) {
  const valueIndexButton = document.querySelector(`#indexButton-${questionId}`).value;
  showQuestion(valueIndexButton);
}