document.addEventListener('DOMContentLoaded', function() {
    
    let currentQuestion = 1;

    // Select by id total-questions and get the number after ":"
    const totalQuestions = document.getElementById('total-questions').textContent.split(":")[1];

    showQuestion(currentQuestion);

    // Next and previous buttons
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

    // Get all the switches
    var switches = document.querySelectorAll('.image-switch');

    // Loop through each switch
    switches.forEach(function(switchInput) {
        // Get the question number from the switch's ID
        var questionNum = switchInput.id.split('-')[2];

        // Get the image and text inputs for this question
        var imageInputs = document.getElementsByClassName('image-input-' + questionNum);
        var textInputs = document.getElementsByClassName('text-input-' + questionNum);

        // Add an event listener to the switch
        switchInput.addEventListener('change', function() {
            if (this.checked) {
                for (var i = 0; i < imageInputs.length; i++) {
                    imageInputs[i].style.display = 'inline-block';
                    textInputs[i].style.display = 'none';
                }
            } else {
                for (var i = 0; i < imageInputs.length; i++) {
                    imageInputs[i].style.display = 'none';
                    textInputs[i].style.display = 'inline-block';
                }
            }
        });
    });


    // Index buttons
    const indexButtons = document.querySelectorAll(".index-button");
    for (const button of indexButtons) {
        button.onclick = () => {
            currentQuestion = parseInt(button.value);
            showQuestion(currentQuestion);
        }
    }

    document.querySelector("#new-question").style.display = "none";

    // New question button
    document.querySelector("#new-question-btn").onclick = () => {
        document.querySelector("#edit-questions").style.display = "none";
        document.querySelector("#new-question").style.display = "block";
    }

    // Edit questions button
    document.querySelector("#edit-questions-btn").onclick = () => {
        document.querySelector("#new-question").style.display = "none";
        document.querySelector("#edit-questions").style.display = "block";
    }

    // Update questions buttons
    const updateButtons = document.querySelectorAll(".update-button");
    for (const button of updateButtons) {
        button.onclick = () => {
            const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
            const questionId = parseInt(button.value);
            const questionText = document.getElementById(`text-question-${questionId}`).value;
            const questionImage = document.getElementById(`image-question-${questionId}`).value;
            const questionCategoryId = document.getElementById(`category-question-${questionId}`).value;
            const questionSubcategoryId = document.getElementById(`subcategory-question-${questionId}`).value;
            const questionOrden = document.getElementById(`orden-question-${questionId}`).value;
            // Select the state of the switch by id
            const questionSwitch = document.getElementById(`image-switch-${questionId}`).checked;

            const options = {};
            let optionCheckStatus = "Normal";
            let answer = "";

            function checkOptionsAndAnswer(questionId, optionSelector, answerInputSelector) {
                const questionOptions = document.querySelectorAll(optionSelector);
                for (const option of questionOptions) {
                    if (option.value === "") {
                        optionCheckStatus = "Empty";
                        break;
                    }
                    const optionId = option.id.split("-")[1];
                    options[optionId] = option.value;
                }
                const radioButtons = document.getElementsByName(`question${questionId}`);
                for (let i = 0; i < radioButtons.length; i++) {
                    if (radioButtons[i].checked) {
                        answer = radioButtons[i].parentNode.querySelector(`${answerInputSelector}-${questionId} input`).value;
                        break;
                    }
                }
            }

            if (questionSwitch) {
                checkOptionsAndAnswer(questionId, `.image-option-${questionId}`, ".image-input");
            } else {
                checkOptionsAndAnswer(questionId, `.text-option-${questionId}`, ".text-input");
            }

            // Select th explanation id
            const explanationId = document.getElementById(`explanation-${questionId}`).value;
            const explanationText = document.querySelector(`#text-explanation-${questionId}`).value;
            const explanationImage = document.querySelector(`#image-explanation-${questionId}`).value;
            const explanationVideo = document.querySelector(`#video-explanation-${questionId}`).value;

            if (answer != "" && questionText != "" && questionOrden != "" && Object.keys(options).length != 0 && optionCheckStatus != "Empty") {
                try {
                    fetch(`/question_update/${questionId}`, {
                    method: "PUT",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": csrfToken
                    },
                    body: JSON.stringify({
                        questionText,
                        questionImage,
                        questionCategoryId,
                        questionSubcategoryId,
                        questionOrden,
                        questionSwitch,
                        options,
                        answer,
                        explanationId,
                        explanationText,
                        explanationImage,
                        explanationVideo
                    })
                    })
                    .then(response => response.json())
                    .then(result => {
                    console.log(result);
                    })

                    // if questionSwitch, replace the source of the options's image with the value of the image input
                    if (questionSwitch) {
                        const questionOptions = document.querySelectorAll(`.exam-image-option-${questionId}`);
                        for (const option of questionOptions) {
                            const optionId = option.id.split("-")[1];
                            option.src = options[optionId];
                        }
                    }

                    // Replace the source and hidden property of the explanation's image and video with the value of the image input and video input, respectively
                    const explanationImageSrc = document.getElementById(`explanation-image-${questionId}`);
                    const explanationVideoSrc = document.getElementById(`explanation-video-${questionId}`);
                    const questionImageSrc = document.getElementById(`option-image-${questionId}`);
                    explanationImageSrc.src = explanationImage;
                    explanationVideoSrc.src = explanationVideo;
                    questionImageSrc.src = questionImage;

                    explanationImageSrc.hidden = explanationImage == "" ? true : false;
                    explanationVideoSrc.hidden = explanationVideo == "" ? true : false;
                    questionImageSrc.hidden = questionImage == "" ? true : false;


                    // Show a message to the user
                    const toastLiveExample = document.getElementById('liveToast')
                    // Change the background color of the class="toast-header" to green
                    document.querySelector(".toast-header").classList.remove("bg-danger");
                    document.querySelector(".toast-header").classList.add("bg-success");
                    // Change the content of the class me-auto to "Mensaje"
                    document.querySelector(".me-auto").innerHTML = "Mensaje";
                    // Change the toast body
                    document.querySelector("#message").innerHTML = "La pregunta se ha actualizado correctamente";
                    const toast = new bootstrap.Toast(toastLiveExample)
                    toast.show()
                } catch (e) {
                    console.error(e);
                }

                // Don't reload the page
                return false;
            
            } else {
                // Show a message to the user
                const toastLiveExample = document.getElementById('liveToast')
                // Change the background color of the class="toast-header" to red
                document.querySelector(".toast-header").classList.remove("bg-success");
                document.querySelector(".toast-header").classList.add("bg-danger");
                // Change the content of the class me-auto to "Mensaje"
                document.querySelector(".me-auto").innerHTML = "Mensaje";
                // Change the toast body
                document.querySelector("#message").innerHTML = "Completa todos los campos de la pregunta";
                const toast = new bootstrap.Toast(toastLiveExample)
                toast.show()

                // Don't reload the page
                return false;
            }
        }
    }

    // Create question button
    document.querySelector("#create-question").onclick = () => {
        const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
        const exam_id = parseInt(document.querySelector("#create-question").value);
        const questionText = document.getElementById("text-new").value;
        const questionImage = document.getElementById("image-new").value;
        const questionCategoryId = document.getElementById("category-new").value;
        const questionSubcategoryId = document.getElementById("subcategory-new").value;
        const questionOrden= document.getElementById("orden-new").value;
        const questionSwitch = document.getElementById("image-switch-0").checked;
        
        const options = {};
        let optionCheckStatus = "Normal";
        let answer = "";

        function checkOptionsAndAnswer(questionOptionsSelector, answerInputSelector) {
            const questionOptions = document.querySelectorAll(questionOptionsSelector);
            for (const option of questionOptions) {
                if (option.value === "") {
                    optionCheckStatus = "Empty";
                    break;
                }
                const optionId = option.id.split("-")[1];
                options[optionId] = option.value;
            }
            const radioButtons = document.getElementsByName("options-new");
            for (let i = 0; i < radioButtons.length; i++) {
                if (radioButtons[i].checked) {
                    answer = radioButtons[i].parentNode.querySelector(answerInputSelector).value;
                    break;
                }
            }
        }

        if (questionSwitch) {
            checkOptionsAndAnswer(".OptionNewImage", ".image-input-0 input");
        } else {
            checkOptionsAndAnswer(".OptionNewText", ".text-input-0 input");
        }

        const explanationText = document.querySelector("#text-explanation-new").value;
        const explanationImage = document.querySelector("#image-explanation-new").value;
        const explanationVideo = document.querySelector("#video-explanation-new").value;

        // If the answer, question text and options are not empty, create the question
        if (answer != "" && questionText != "" && questionOrden != "" && Object.keys(options).length != 0 && optionCheckStatus != "Empty") {
            try {
                fetch(`/new_question/${exam_id}`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": csrfToken
                    },
                    body: JSON.stringify({
                        questionText,
                        questionImage,
                        questionCategoryId,
                        questionSubcategoryId,
                        questionOrden,
                        questionSwitch,
                        options,
                        answer,
                        explanationText,
                        explanationImage,
                        explanationVideo
                    })
                })
                .then(response => response.json())
                .then(result => {
                    console.log(result);
                })

                // Show a message to the user
                const toastLiveExample = document.getElementById('liveToast')
                // Change the background color of the class="toast-header" to green
                document.querySelector(".toast-header").classList.remove("bg-danger");
                document.querySelector(".toast-header").classList.add("bg-success");
                // Change the content of the class me-auto to "Mensaje"
                document.querySelector(".me-auto").innerHTML = "Mensaje";
                // Change the toast body
                document.querySelector("#message").innerHTML = "La pregunta se ha creado correctamente";
                const toast = new bootstrap.Toast(toastLiveExample)
                toast.show()
            } catch (e) {
                console.error(e);
            }

            // Redirect to the exam_edit
            window.location.href = `/exam_edit/${exam_id}/fecha`;
        
        }else {
            // Show a message to the user
            const toastLiveExample = document.getElementById('liveToast')
            // Change the background color of the class="toast-header" to red
            document.querySelector(".toast-header").classList.remove("bg-success");
            document.querySelector(".toast-header").classList.add("bg-danger");
            // Change the content of the class me-auto to "Error"
            document.querySelector(".me-auto").innerHTML = "Error";
            // Change the toast body
            document.querySelector("#message").innerHTML = "Completa todos los campos de la pregunta";
            const toast = new bootstrap.Toast(toastLiveExample)
            toast.show()
            
            return false;
        }
    }

    // Delete buttons
    const deleteButtons = document.querySelectorAll(".delete-button");
    for (const button of deleteButtons) {
        button.onclick = () => {
            // Divide the button id to get the question id and exam id
            const buttonId = button.id.split("-");
            const questionId = parseInt(buttonId[1]);
            const exam_id = parseInt(buttonId[2]);
            
            // Change th href of the element with id="delete-modal" to /question_delete/${questionId}/${exam_id}
            document.querySelector("#delete-modal").href = `/question_delete/${questionId}/${exam_id}`;
        }
    }

    // Preview buttons
    const previewButtons = document.querySelectorAll(".preview-button");
    for (const button of previewButtons) {
        button.onclick = () => {
            // Divide the button id to get the question id and exam id
            const questionId = parseInt(button.id.split("-")[1]);
            
            const questionText = document.getElementById(`text-question-${questionId}`).value;
            const questionImage = document.getElementById(`image-question-${questionId}`).value;
            const questionCategorySelect = document.getElementById(`category-question-${questionId}`);
            const questionCategory = questionCategorySelect.options[questionCategorySelect.selectedIndex].text;
            const questionSubcategorySelect = document.getElementById(`subcategory-question-${questionId}`);
            const questionSubcategory = questionSubcategorySelect.options[questionSubcategorySelect.selectedIndex].text;
            const questionSwitch = document.getElementById(`image-switch-${questionId}`).checked;

            let questionOptionsSelector, optionsByName, answerInputSelector;
            if (questionSwitch) {
                questionOptionsSelector = `.image-option-${questionId}`;
                optionsByName = `question${questionId}`;
                answerInputSelector = `.image-input-${questionId} input`;
            } else {
                questionOptionsSelector = `.text-option-${questionId}`;
                optionsByName = `question${questionId}`;
                answerInputSelector = `.text-input-${questionId} input`;
            }

            const explanationText = document.querySelector(`#text-explanation-${questionId}`).value;
            const explanationImage = document.querySelector(`#image-explanation-${questionId}`).value;
            const explanationVideo = document.querySelector(`#video-explanation-${questionId}`).value;

            previewQuestion(questionText, questionImage, questionCategory, questionSubcategory, questionSwitch, questionOptionsSelector, optionsByName, answerInputSelector, explanationText, explanationImage, explanationVideo);
        }
    }

    document.querySelector("#new-question-preview").onclick = () => {
        const questionText = document.getElementById("text-new").value;
        const questionImage = document.getElementById("image-new").value;
        const questionCategorySelect = document.getElementById("category-new");
        const questionCategory = questionCategorySelect.options[questionCategorySelect.selectedIndex].text;
        const questionSubcategorySelect = document.getElementById("subcategory-new");
        const questionSubcategory = questionSubcategorySelect.options[questionSubcategorySelect.selectedIndex].text;
        const questionSwitch = document.getElementById("image-switch-0").checked;

        let questionOptionsSelector, optionsByName, answerInputSelector;

        if (questionSwitch) {
            questionOptionsSelector = ".OptionNewImage";
            optionsByName = "options-new"
            answerInputSelector = ".image-input-0 input";
        } else {
            questionOptionsSelector = ".OptionNewText";
            optionsByName = "options-new"
            answerInputSelector = ".text-input-0 input";
        }

        const explanationText = document.querySelector("#text-explanation-new").value;
        const explanationImage = document.querySelector("#image-explanation-new").value;
        const explanationVideo = document.querySelector("#video-explanation-new").value;

        previewQuestion(questionText, questionImage, questionCategory, questionSubcategory, questionSwitch, questionOptionsSelector, optionsByName, answerInputSelector, explanationText, explanationImage, explanationVideo);
    }

    document.getElementById('add-option').addEventListener('click', function() {
        var form = document.getElementById('FormNew');
        var lastQuestion = form.lastElementChild;
        var newQuestion = lastQuestion.cloneNode(true);
        var lastId = lastQuestion.id.slice(-1);
        var newId = parseInt(lastId) + 1;
        newQuestion.id = 'formNewQuestion-' + newId;
        newQuestion.querySelector('input[type="text"]').id = 'textOptionNew-' + newId;
        newQuestion.querySelector('input[type="text"]').value = '';
        newQuestion.querySelector('input[type="url"]').id = 'imageOptionNew-' + newId;
        newQuestion.querySelector('input[type="url"]').value = '';
        newQuestion.querySelector('.text-input-0').style.display = 'inline-block';
        newQuestion.querySelector('.image-input-0').style.display = 'none';
        newQuestion.querySelector('.delete-new-option').addEventListener('click', deleteQuestion);
        form.insertBefore(newQuestion, null);
    });
    
    function deleteQuestion(event) {
    var question = event.target.closest('.form-new-question');
    question.parentNode.removeChild(question);
    }

    var deleteNewButtons = document.querySelectorAll('.delete-new-option');
    for (const deleteNewButton of deleteNewButtons) {
        deleteNewButton.addEventListener('click', deleteQuestion);
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

function previewQuestion(questionText, questionImage, questionCategory, questionSubcategory, questionSwitch, questionOptionsSelector, optionsByName, answerInputSelector, explanationText, explanationImage, explanationVideo){
    const preview = document.getElementById("preview-content");
    let optionCheckStatus = "Normal";
    // Get the options
    const options = [];
    const questionOptionsSelected = document.querySelectorAll(questionOptionsSelector);
    for (const option of questionOptionsSelected) {
        if (option.value === ""){
            optionCheckStatus = "Error";
            break;
        }
        options.push(option.value);
    }

    if (!questionText || !questionCategory || !questionSubcategory || optionCheckStatus == "Error") {
        preview.innerHTML = '<div class="alert alert-danger" role="alert">Por favor, rellena todos los campos obligatorios.</div>';
    } else {
        let answer = "";
        const radioButtons = document.getElementsByName(optionsByName);
        for (let i = 0; i < radioButtons.length; i++) {
            if (radioButtons[i].checked) {
                answer = radioButtons[i].parentNode.querySelector(answerInputSelector).value;
                break;
            }
        }
        // Create the preview
        const optionsHtml = options.map((option) => {
            const inputHtml = `<input class="form-check-input" type="radio" style="opacity: 1;" ${answer == option ? 'checked disabled' : 'disabled'}>`;
            const labelHtml = questionSwitch
            ? `<label class="form-check-label" style="opacity: 1;"><img src="${option}" class="style-image-option" alt="Image"></label>`
            : `<label class="form-check-label" style="opacity: 1;">${option}</label>`;
            return `<div class="form-check">${inputHtml}${labelHtml}</div>`;
        }).join('');
        
        const questionOptions = optionsHtml;
        const questionCategoryAndSubcategory = `<p class="card-text"><small class="text-muted">Categoria: ${questionCategory} | Subcategoria: ${questionSubcategory}</small></p>`;

        let questionContentHtml = questionText;
        if (questionImage) {
            questionContentHtml += `<img src="${questionImage}" class="exam-image" alt="Image">`;
        }

        let questionExplanationHtml = '<hr class="border border-secondary border-2 opacity-50"><strong>Explicación</strong>\n\n' + explanationText;
        if (explanationImage) {
            questionExplanationHtml += `<hr><img src="${explanationImage}" class="exam-image" alt="Image">`;
        } 
        if (explanationVideo) {
            questionExplanationHtml += `<hr><div class="d-flex justify-content-center align-items-center"><iframe width="560" height="315" src="${explanationVideo}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe></div>`;
        }
        
        const content = questionContentHtml + '\n\n' + questionOptions +'\n\n' + questionCategoryAndSubcategory +'\n\n' + questionExplanationHtml
        preview.innerHTML = `<p>${content
            .replace(/(\r\n|\n|\r){2,}/g, "</p><p>")
            .replace(/(\r\n|\n|\r)/g, "<br>")}</p>`;
        // Procesar el contenido de MathJax y actualizar el contenido del modal
        MathJax.typesetPromise([preview]).catch((err) => console.log(err));
    }
}