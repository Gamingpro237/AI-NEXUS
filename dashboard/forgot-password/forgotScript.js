document.addEventListener("DOMContentLoaded", function() {
    const forgotForm = document.getElementById("forgotForm");
    const emailInput = document.getElementById("email");
    const emailError = document.getElementById("emailError");
  
    // Simple email regex for validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  
    forgotForm.addEventListener("submit", function(e) {
      // Clear any previous error message
      emailError.style.display = "none";
  
      // Validate email format
      if (!emailRegex.test(emailInput.value)) {
        emailError.textContent = "Please enter a valid email address.";
        emailError.style.display = "block";
        e.preventDefault();
      }
    });
  });
  