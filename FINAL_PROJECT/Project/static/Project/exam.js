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

    document.querySelector("#save").addEventListener('click', () => save_answers());

    // Index buttons
    const indexButtons = document.querySelectorAll(".index-button");
    for (const button of indexButtons) {
        button.onclick = () => {
            currentQuestion = parseInt(button.value);
            showQuestion(currentQuestion);
        }
    }


    // No-answer button
    document.querySelector("#no-answer").addEventListener('click', () => StateIndexButtons("no-answer"));

    // Answered button
    document.querySelector("#answered").addEventListener('click', () => StateIndexButtons("answered"));

    // All button
    document.querySelector("#all").addEventListener('click', () => StateIndexButtons("all"));

    // Marked button
    document.querySelector("#marked").addEventListener('click', () => StateIndexButtons("marked"));

    // Question markers animation
    const pendingButtons = document.querySelectorAll(".question-markers");
    for (const button of pendingButtons) {
        button.addEventListener('click', () => {
          if (button.src.includes("icons8-lazo-marcapaginas.svg")) {
            button.src = "/static/Project/SVGs/icons8-lazo-marcapaginas-amarillo.svg";
          } else {
            button.src = "/static/Project/SVGs/icons8-lazo-marcapaginas.svg";
          }
        });
    }

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


function save_answers() {
  const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
  const exam = document.getElementById('exam');
  if (exam) {
    const questions = document.querySelectorAll(".questionsIds");
    const answers = {};
    let check = "";
    for (const question of questions) {
      // Get the question id by splitting the id using "-" and getting the last element
      const questionId = question.id.split("-")[1];
      const answer = document.querySelector(
        `input[name="question${questionId}"]:checked`
      );
      if (answer) {
        answers[questionId] = answer.value;
      } else {
        check = "No answer";
        break;
      }
    }

    if (check != "No answer") {
      // Get the exam id by the url
      const url = window.location.href;
      const exam_id = url.split("/")[4];  
      // Use fecth to send the answers to the server
      fetch(`/exam/${exam_id}/save/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({
          answers,
        }),
      })
      .then(response => response.json())
      .then(data => {
        console.log(data.message);
        window.location.replace(`/exam_result/${data.exam_result_id}`);
      });

      // Show a message to the user
      const toastLiveExample = document.getElementById('liveToast')
      // Change the background color of the class="toast-header" to green
      document.querySelector(".toast-header").classList.remove("bg-danger");
      document.querySelector(".toast-header").classList.add("bg-success");
      // Change the content of the class me-auto to "Mensaje"
      document.querySelector(".me-auto").innerHTML = "Mensaje";
      // Change the toast body
      document.querySelector("#message").innerHTML = "Examen guardado correctamente";
      const toast = new bootstrap.Toast(toastLiveExample)
      toast.show()

    } else {
      // Show a message to the user
      const toastLiveExample = document.getElementById('liveToast')
      // Change the background color of the class="toast-header" to red
      document.querySelector(".toast-header").classList.remove("bg-success");
      document.querySelector(".toast-header").classList.add("bg-danger");
      // Change the content of the class me-auto to "Mensaje"
      document.querySelector(".me-auto").innerHTML = "Mensaje";
      // Change the toast body
      document.querySelector("#message").innerHTML = "Responde todas las preguntas";
      const toast = new bootstrap.Toast(toastLiveExample)
      toast.show()
      StateIndexButtons("no-answer")
    }
  }
};


function StateIndexButtons(state) {
  switch (state) {
    case "answered":
      const answeredQuestions = getQuestionsByAnswer(true);
      updateIndexButtons(answeredQuestions);
      showQuestionIndex(answeredQuestions[0]);
      break;
    case "no-answer":
      const unansweredQuestions = getQuestionsByAnswer(false);
      updateIndexButtons(unansweredQuestions);
      showQuestionIndex(unansweredQuestions[0]);
      break;
    case "all":
      const allQuestions = getAllQuestions();
      updateIndexButtons(allQuestions);
      showQuestion(1);
      break;
    case "marked":
      const markedQuestions = getQuestionsByMarker(true);
      updateIndexButtons(markedQuestions);
      showQuestionIndex(markedQuestions[0]);
      break;
    default:
      console.error("Error: invalid state in stateIndexButtons function");
  }
}

function getQuestionsByAnswer(answered) {
  const questions = document.querySelectorAll(".questionsIds");
  const questionNumberLoop = [];
  for (const question of questions) {
    const questionId = question.id.split("-")[1];
    const answer = document.querySelector(`input[name="question${questionId}"]:checked`);
    if (answered && answer || !answered && !answer) {
      questionNumberLoop.push(questionId);
    }
  }
  return questionNumberLoop;
}

function getAllQuestions() {
  const questions = document.querySelectorAll(".questionsIds");
  return Array.from(questions).map((question) => question.id.split("-")[1]);
}

function getQuestionsByMarker(marked) {
  const questions = document.querySelectorAll(".question-markers");
  const questionNumberLoop = [];
  for (const question of questions) {
    const questionId = question.id.split("-")[1];
    const isMarked = question.src.includes("icons8-lazo-marcapaginas-amarillo.svg");
    if (marked && isMarked || !marked && !isMarked) {
      questionNumberLoop.push(questionId);
    }
  }
  return questionNumberLoop;
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