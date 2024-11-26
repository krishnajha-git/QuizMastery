document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("registerForm");

    const nameInput = document.querySelector('input[name="name"]');
    const emailInput = document.querySelector('input[name="email"]');
    const passwordInput = document.querySelector('input[name="password"]');
    const confirmPasswordInput = document.querySelector('input[name="confirm_password"]');

    const nameError = document.getElementById('nameError');
    const emailError = document.getElementById('emailError');
    const passwordError = document.getElementById('passwordError');
    const confirmPasswordError = document.getElementById('confirmPasswordError');

    // Validation functions
    function validateName() {
        const nameValue = nameInput.value.trim();
        if (nameValue === "") {
            nameError.textContent = 'Name is required.';
            nameError.style.display = 'block';
            return false;
        } else {
            nameError.style.display = 'none';
            return true;
        }
    }

    function validateEmail() {
        const emailValue = emailInput.value;
        const emailRegex = /^[a-zA-Z0-9_.]+@gmail\.[a-zA-Z]+$/;
        if (!emailRegex.test(emailValue)) {
            emailError.textContent = 'Invalid email format. Use @gmail.com';
            emailError.style.display = 'block';
            return false;
        } else {
            emailError.style.display = 'none';
            return true;
        }
    }

    function validatePassword() {
        const passwordValue = passwordInput.value;
        if (passwordValue.length < 5) {
            passwordError.textContent = 'Password must be at least 5 characters long.';
            passwordError.style.display = 'block';
            return false;
        } else {
            passwordError.style.display = 'none';
            return true;
        }
    }

    function validateConfirmPassword() {
        const passwordValue = passwordInput.value;
        const confirmPasswordValue = confirmPasswordInput.value;
        if (passwordValue !== confirmPasswordValue) {
            confirmPasswordError.textContent = 'Passwords do not match.';
            confirmPasswordError.style.display = 'block';
            return false;
        } else {
            confirmPasswordError.style.display = 'none';
            return true;
        }
    }

    // Attach event listeners for live validation
    nameInput.addEventListener("input", validateName);
    emailInput.addEventListener("input", validateEmail);
    passwordInput.addEventListener("input", validatePassword);
    confirmPasswordInput.addEventListener("input", validateConfirmPassword);

    // Final form submission validation
    form.onsubmit = function (event) {
        const isNameValid = validateName();
        const isEmailValid = validateEmail();
        const isPasswordValid = validatePassword();
        const isConfirmPasswordValid = validateConfirmPassword();

        if (!(isNameValid && isEmailValid && isPasswordValid && isConfirmPasswordValid)) {
            event.preventDefault();
        }
    };
});
