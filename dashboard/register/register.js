document.addEventListener('DOMContentLoaded', function () {
    const registerForm = document.getElementById('registerForm');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirmPassword');
    const confirmPasswordError = document.getElementById('confirmPasswordError');
  
    // Validate passwords on input change
    confirmPasswordInput.addEventListener('input', function () {
      if (passwordInput.value !== confirmPasswordInput.value) {
        confirmPasswordError.textContent = 'Passwords do not match.';
        confirmPasswordError.style.display = 'block';
      } else {
        confirmPasswordError.textContent = '';
        confirmPasswordError.style.display = 'none';
      }
    });
  
    // Validate on form submission
    registerForm.addEventListener('submit', function (e) {
      if (passwordInput.value !== confirmPasswordInput.value) {
        e.preventDefault();
        confirmPasswordError.textContent = 'Passwords do not match.';
        confirmPasswordError.style.display = 'block';
      }
    });
  });
  