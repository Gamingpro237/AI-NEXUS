// Password Quality Checker and Form Validation
document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("loginForm");
    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");
    const emailError = document.getElementById("emailError");
    const passwordError = document.getElementById("passwordError");
    const strengthBar = document.getElementById("strengthBar");
    const strengthText = document.getElementById("strengthText");
  
    // Simple email regex for validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  
    // Function to check password strength
    function checkPasswordStrength(password) {
      let strength = 0;
      // Criteria checks
      if (password.length >= 8) strength += 1;
      if (/[A-Z]/.test(password)) strength += 1;
      if (/[a-z]/.test(password)) strength += 1;
      if (/\d/.test(password)) strength += 1;
      if (/[\W_]/.test(password)) strength += 1;
      return strength;
    }
  
    // Update the strength meter based on the password input
    passwordInput.addEventListener("input", function () {
      const password = passwordInput.value;
      const strength = checkPasswordStrength(password);
      const percentage = (strength / 5) * 100;
      strengthBar.style.width = percentage + "%";
  
      // Change the color and text based on strength
      if (strength <= 2) {
        strengthBar.style.backgroundColor = "#e74c3c"; // red for weak
        strengthText.textContent = "Weak";
      } else if (strength === 3 || strength === 4) {
        strengthBar.style.backgroundColor = "#f1c40f"; // yellow/orange for medium
        strengthText.textContent = "Medium";
      } else if (strength === 5) {
        strengthBar.style.backgroundColor = "#2ecc71"; // green for strong
        strengthText.textContent = "Strong";
      }
    });
  
    // Validate form on submit
    loginForm.addEventListener("submit", function (e) {
      let valid = true;
  
      // Clear previous error messages
      emailError.style.display = "none";
      passwordError.style.display = "none";
  
      // Validate email format
      if (!emailRegex.test(emailInput.value)) {
        emailError.textContent = "Please enter a valid email address.";
        emailError.style.display = "block";
        valid = false;
      }
  
      // Check password is not empty
      if (passwordInput.value.trim() === "") {
        passwordError.textContent = "Password cannot be empty.";
        passwordError.style.display = "block";
        valid = false;
      }
  
      if (!valid) {
        e.preventDefault(); // Prevent form submission if validation fails
      }
    });
  });
  
  // Google Sign-In Handler
  function handleGoogleSignIn() {
    google.accounts.id.initialize({
      client_id: 'YOUR_GOOGLE_CLIENT_ID',
      callback: (response) => {
        // Handle the ID token (send it to your server for verification)
        console.log(response);
      }
    });
    google.accounts.id.prompt(); // shows the One Tap prompt
  }
  
  // Toggle Password Visibility
  function togglePassword() {
    const pwdField = document.getElementById('password');
    const icon = document.querySelector('.toggle-visibility i');
    if (pwdField.type === 'password') {
      pwdField.type = 'text';
      icon.classList.remove('fa-eye');
      icon.classList.add('fa-eye-slash');
    } else {
      pwdField.type = 'password';
      icon.classList.remove('fa-eye-slash');
      icon.classList.add('fa-eye');
    }
  }
  document.getElementById('loginForm').addEventListener('submit', (e) => {
    // Show spinner, disable button
    document.getElementById('loginButton').disabled = true;
    // Possibly add spinner class or text
  });
  