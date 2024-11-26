let questionIndex = 0;
        
        function addQuestion() {
            questionIndex++;
        
            const questionContainer = document.createElement('div');
            questionContainer.classList.add('question-container');
            questionContainer.id = `question_${questionIndex}`;
        
            questionContainer.innerHTML = `
                <input type="text" id="question_${questionIndex}" name="question_${questionIndex}" placeholder="Question" maxlength="200" required>
                <div class="error-message" id="questionError_${questionIndex}" style="display:none;">Question cannot be empty or exceed 200 characters.</div>

                <div class="options" id="options_${questionIndex}">
                <input type="text" name="option_1_${questionIndex}" id="option_1_${questionIndex}" placeholder="Option 1" maxlength="100" required oninput="updateSelectOption(${questionIndex}, 1)">
                <div class="error-message" id="option1Error_${questionIndex}" style="display:none;"></div>

                <input type="text" name="option_2_${questionIndex}" id="option_2_${questionIndex}" placeholder="Option 2" maxlength="100" required oninput="updateSelectOption(${questionIndex}, 2)">
                <div class="error-message" id="option2Error_${questionIndex}" style="display:none;"></div>

                <input type="text" name="option_3_${questionIndex}" id="option_3_${questionIndex}" placeholder="Option 3" maxlength="100" required oninput="updateSelectOption(${questionIndex}, 3)">
                <div class="error-message" id="option3Error_${questionIndex}" style="display:none;"></div>

                <input type="number" id="score_${questionIndex}" name="score_${questionIndex}" placeholder="Score" min="0" required oninput="validateScore(this)">
                <div class="error-message" id="scoreError_${questionIndex}" style="display:none;"></div>

                <div class="error-message" id="scoreError_${questionIndex}" style="color: red; display: none;">
                    {% if error %}
                        Decimal and alphabets are not allowed.
                    {% endif %}
                </div>
                <select class="multi-select" id="correctOption_${questionIndex}" name="correctOption_${questionIndex}">
                    <option value="Option 1">Option 1</option>
                    <option value="Option 2">Option 2</option>
                    <option value="Option 3">Option 3</option>
                </select>
                <button type="button" class="button-green" onclick="saveAnswer(${questionIndex})">Save</button>
            </div>
        
                <button type="button" class="remove-button" onclick="removeQuestion(${questionIndex})">-</button>
            `;
        
            document.getElementById('questionsList').appendChild(questionContainer);
            // Bind validation for the newly added question
            bindQuestionValidation(questionIndex);
        }
        
        // Validate Question
        function validateQuestion(input, questionIndex) {
            const questionValue = input.value.trim();
            const errorMessage = document.getElementById(`questionError_${questionIndex}`);
            
            // Check if the question is empty or too long
            if (!questionValue) {
                errorMessage.style.display = 'block';
                errorMessage.textContent = 'Question cannot be empty.';
            } else if (questionValue.length > 200) {
                errorMessage.style.display = 'block';
                errorMessage.textContent = 'Question cannot exceed 200 characters.';
            } else {
                errorMessage.style.display = 'none';
            }
        }

// Validate Option
function validateOption(input, questionIndex, optionIndex) {
    const optionValue = input.value.trim();
    const errorMessage = document.getElementById(`option${optionIndex}Error_${questionIndex}`);
    
    if (!optionValue) {
        errorMessage.style.display = 'block';
        errorMessage.textContent = `Option ${optionIndex} cannot be empty.`;
    } else {
        errorMessage.style.display = 'none';
    }
}

// Validate Score
function validateScore(input, questionIndex) {
    const scoreValue = input.value.trim();
    const errorMessage = document.getElementById(`scoreError_${questionIndex}`);
    
    if (!scoreValue.match(/^\d+$/)) {
        errorMessage.style.display = 'block';
        errorMessage.textContent = 'Score must be a valid number.';
    } else {
        errorMessage.style.display = 'none';
    }
}

function validateTitle(input) {
    const titleValue = input.value.trim();
    const titleError = document.getElementById('titleError');
    if (titleValue.length === 0 || titleValue.length > 200) {
        titleError.style.display = 'block';
        titleError.textContent = 'Title cannot be empty or exceed 200 characters.';
    } else {
        titleError.style.display = 'none';
    }
}

function validateDescription(input) {
    const descriptionValue = input.value.trim();
    const descriptionError = document.getElementById('descriptionError');
    if (descriptionValue.length === 0 || descriptionValue.length > 1000) {
        descriptionError.style.display = 'block';
        descriptionError.textContent = 'Description cannot be empty or exceed 1000 characters.';
    } else {
        descriptionError.style.display = 'none';
    }
}


// Static Validation for Image
function validateFile() {
    const fileInput = document.getElementById('quiz_img');
    const filePath = fileInput.value;
    const allowedExtensions = /(\.jpg|\.jpeg|\.png|\.gif)$/i;
    const fileError = document.getElementById('fileError');
    
    if (filePath.length === 0) {
        fileError.style.display = 'block';
        fileError.textContent = 'Image cannot be empty.';
    } else if (!allowedExtensions.exec(filePath)) {
        fileError.style.display = 'block';
        fileError.textContent = 'Please upload a valid image file (jpg, jpeg, png, gif).';
        fileInput.value = ''; // Clear invalid file input
    } else {
        fileError.style.display = 'none';
    }
}

// Bind events for dynamic inputs
function bindQuestionValidation(questionIndex) {
    const questionInput = document.getElementById(`question_${questionIndex}`);
    const option1Input = document.getElementById(`option_1_${questionIndex}`);
    const option2Input = document.getElementById(`option_2_${questionIndex}`);
    const option3Input = document.getElementById(`option_3_${questionIndex}`);
    const scoreInput = document.getElementById(`score_${questionIndex}`);
    
    // Add event listeners to each input for live validation
    questionInput.addEventListener('input', () => validateQuestion(questionInput, questionIndex));
    option1Input.addEventListener('input', () => validateOption(option1Input, questionIndex, 1));
    option2Input.addEventListener('input', () => validateOption(option2Input, questionIndex, 2));
    option3Input.addEventListener('input', () => validateOption(option3Input, questionIndex, 3));
    scoreInput.addEventListener('input', () => validateScore(scoreInput, questionIndex));
}

        function updateSelectOption(questionIndex, optionIndex) {
            const optionInput = document.getElementById(`option_${optionIndex}_${questionIndex}`).value;
            const correctOptionSelect = document.getElementById(`correctOption_${questionIndex}`);

            // Update the corresponding option in the select element
            correctOptionSelect.options[optionIndex - 1].text = optionInput || `Option ${optionIndex}`;
            correctOptionSelect.options[optionIndex - 1].value = optionInput || `Option ${optionIndex}`;
        }
        // Function to save the answer and revert to options view
        // Function to save the answer and revert to options view
        function saveAnswer(index) {
            const optionsDiv = document.getElementById(`options_${index}`);
            const correctOption = document.getElementById(`correctOption_${index}`).value;
        
            // Reset background color for all options
            const options = optionsDiv.querySelectorAll('input[type="text"]');
            options.forEach(option => {
                option.style.backgroundColor = ''; // Remove any background color
                option.classList.remove('correct-answer');
            });
        
            // Highlight the correct option in green
            const correctOptionElement = Array.from(options).find(option => option.value === correctOption);
            if (correctOptionElement) {
                correctOptionElement.style.backgroundColor = 'lightgreen';
                correctOptionElement.classList.add('correct-answer');
            }
        }

        


        // Function to remove a question
        function removeQuestion(index) {
            const questionElement = document.getElementById(`question_${index}`);
            if (questionElement) {
                questionElement.remove();
            }
        }

        

        function exitQuiz() {
            window.history.back(); // Redirect to the previous page
        }