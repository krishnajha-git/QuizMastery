const emailInput = document.querySelector('input[name="email"]');
        const passwordInput = document.querySelector('input[name="password"]');
        const emailError = document.getElementById('emailError');
        const passwordError = document.getElementById('passwordError');

        emailInput.addEventListener('input', () => {
            const emailValue = emailInput.value;
            const emailRegex = /^[a-zA-Z0-9_.]+@gmail\.[a-zA-Z]{3}$/;
            if (!emailRegex.test(emailValue)) {
                emailError.textContent = 'Invalid email format.';
                emailError.style.display = 'block';
            } else {
                emailError.style.display = 'none';
            }
        });

        passwordInput.addEventListener('input', () => {
            const passwordValue = passwordInput.value;
            if (passwordValue.length < 5) {
                passwordError.textContent = 'Password must be at least 5 characters long.';
                passwordError.style.display = 'block';
            } else {
                passwordError.style.display = 'none';
            }
        });

        document.getElementById('loginForm').addEventListener('submit', (event) => {
            const emailValue = emailInput.value;
            const passwordValue = passwordInput.value;
            const emailRegex = /^[a-zA-Z0-9_.]+@gmail\.[a-zA-Z]{3}$/;

            if (!emailRegex.test(emailValue)) {
                emailError.textContent = 'Invalid email format. Please use @gmail.com';
                emailError.style.display = 'block';
                event.preventDefault(); // Prevent form submission if invalid
            } else {
                emailError.style.display = 'none';
            }

            if (passwordValue.length < 5) {
                passwordError.textContent = 'Password must be at least 5 characters long.';
                passwordError.style.display = 'block';
                event.preventDefault(); // Prevent form submission if invalid
            } else {
                passwordError.style.display = 'none';
            }
        });