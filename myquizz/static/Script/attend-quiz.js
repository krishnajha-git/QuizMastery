
    const form = document.querySelector('form');
    // Log form submission event
    document.getElementById('quiz-form').onsubmit = function (event) {
        console.log('Form is being submitted.');
    };
    function validateName(input) {
        const nameValue = input.value.trim();
        if (nameValue.length === 0) {
            document.getElementById('nameError').style.display = 'block';
        } else {
            document.getElementById('nameError').style.display = 'none';
        }
    }
    
    function validateEmail(input) {
        const emailValue = input.value.trim();
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/; // Simple email validation regex
        if (!emailPattern.test(emailValue)) {
            document.getElementById('emailError').style.display = 'block';
        } else {
            document.getElementById('emailError').style.display = 'none';
        }
    }

    