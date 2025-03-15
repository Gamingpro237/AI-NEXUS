// Password Quality Checker and Form Validation
document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("loginForm");
    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");
    const emailError = document.getElementById("emailError");
    const passwordError = document.getElementById("passwordError");
    const strengthBar = document.getElementById("strengthBar");
    const strengthText = document.getElementById("strengthText");
    const loginButton = document.getElementById("loginButton");
  
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
    loginForm.addEventListener("submit", async function (e) {
      e.preventDefault(); // Always prevent default form submission
      
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
  
      if (valid) {
        try {
          // Show loading state
          loginButton.disabled = true;
          loginButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Logging in...';
          
          // Call the backend API for login
          console.log('Sending login request with data:', {
            email: emailInput.value,
            password: passwordInput.value
          });
          
          try {
            const response = await fetch('/api/login', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({
                email: emailInput.value,
                password: passwordInput.value
              })
            });
            
            console.log('Login response status:', response.status);
            
            // Check if the response is empty
            const responseText = await response.text();
            console.log('Raw response:', responseText);
            
            let data;
            if (responseText) {
              try {
                data = JSON.parse(responseText);
                console.log('Login response data:', data);
              } catch (parseError) {
                console.error('Error parsing JSON response:', parseError);
                throw new Error('Invalid response from server');
              }
            } else {
              console.error('Empty response from server');
              throw new Error('Empty response from server');
            }
            
            if (response.ok) {
              // Store user data in localStorage for session management
              console.log('Login successful! Storing user data and redirecting to dashboard');
              localStorage.setItem('user', JSON.stringify(data.user));
              
              // Add a small delay before redirect to ensure localStorage is set
              setTimeout(() => {
                console.log('Redirecting to dashboard...');
                window.location.href = '/';
              }, 500);
            } else {
              // Display error message
              const errorMessage = data?.detail || "Login failed. Please check your credentials.";
              passwordError.textContent = errorMessage;
              passwordError.style.display = "block";
              
              // Add a note about the valid test account
              if (errorMessage.includes("Invalid email or password")) {
                const noteElement = document.createElement('p');
                noteElement.className = 'login-note';
                noteElement.innerHTML = '<small>Try using email: <strong>hoang.nv.ral@gmail.com</strong> with password: <strong>123456a@</strong></small>';
                passwordError.parentNode.insertBefore(noteElement, passwordError.nextSibling);
              }
            }
          } catch (error) {
            console.error('Login error:', error);
            passwordError.textContent = "An error occurred during login: " + error.message;
            passwordError.style.display = "block";
          } finally {
            // Reset loading state
            loginButton.disabled = false;
            loginButton.innerHTML = 'Log In';
          }
        } catch (error) {
          console.error('Login error:', error);
          passwordError.textContent = "An error occurred during login. Please try again.";
          passwordError.style.display = "block";
          
          // Reset loading state
          loginButton.disabled = false;
          loginButton.innerHTML = 'Log In';
        }
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