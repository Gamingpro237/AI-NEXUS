// Wait until DOM is fully loaded
document.addEventListener("DOMContentLoaded", function () {
    // Handle Sidebar Navigation
    const links = document.querySelectorAll("#sidebar-wrapper a");
    const sections = document.querySelectorAll(".section");
    
    links.forEach(link => {
      link.addEventListener("click", function (e) {
        e.preventDefault();
        // Hide all sections
        sections.forEach(sec => sec.classList.add("d-none"));
        // Get the target section
        const sectionId = "section-" + this.getAttribute("data-section");
        document.getElementById(sectionId).classList.remove("d-none");
      });
    });
  
    // Toggle sidebar for responsive view
    document.getElementById("menu-toggle").addEventListener("click", function () {
      const wrapper = document.getElementById("wrapper");
      wrapper.classList.toggle("toggled");
    });
  
    // Simulate Notifications
    function showNotification(message) {
      const notificationArea = document.getElementById("notificationArea");
      const alertDiv = document.createElement("div");
      alertDiv.className = "alert alert-info";
      alertDiv.innerText = message;
      notificationArea.appendChild(alertDiv);
      setTimeout(() => {
        alertDiv.remove();
      }, 3000);
    }
    // Example notification
    showNotification("Welcome to your dashboard!");
  
    // Handle Resume Upload
    const uploadForm = document.getElementById("uploadForm");
    const resumeInput = document.getElementById("resumeInput");
    const uploadProgress = document.getElementById("uploadProgress");
    const progressBar = uploadProgress.querySelector(".progress-bar");
  
    uploadForm.addEventListener("submit", function (e) {
      e.preventDefault();
      if (resumeInput.files.length === 0) {
        alert("Please select a file to upload.");
        return;
      }
      // Simulate file upload progress
      uploadProgress.classList.remove("d-none");
      let progress = 0;
      const interval = setInterval(() => {
        progress += 10;
        progressBar.style.width = progress + "%";
        progressBar.innerText = progress + "%";
        if (progress >= 100) {
          clearInterval(interval);
          setTimeout(() => {
            uploadProgress.classList.add("d-none");
            progressBar.style.width = "0%";
            progressBar.innerText = "0%";
            showNotification("Resume uploaded successfully!");
          }, 500);
        }
      }, 200);
    });
  
    // Populate Interview History (sample data)
    const historyTableBody = document.querySelector("#historyTable tbody");
    const sampleHistory = [
      { date: "2023-03-01", time: "10:00 AM", duration: "30 mins", rating: "8/10", details: "Good communication." },
      { date: "2023-03-10", time: "2:00 PM", duration: "25 mins", rating: "7/10", details: "Needs improvement on technical answers." }
    ];
    sampleHistory.forEach(item => {
      const row = document.createElement("tr");
      row.innerHTML = `<td>${item.date}</td>
                       <td>${item.time}</td>
                       <td>${item.duration}</td>
                       <td>${item.rating}</td>
                       <td><button class="btn btn-sm btn-info" onclick="alert('${item.details}')">View</button></td>`;
      historyTableBody.appendChild(row);
    });
  
    // Search and Filter Interview History (basic implementation)
    document.getElementById("filterHistory").addEventListener("click", function () {
      const query = document.getElementById("searchHistory").value.toLowerCase();
      const rows = historyTableBody.querySelectorAll("tr");
      rows.forEach(row => {
        row.style.display = row.innerText.toLowerCase().includes(query) ? "" : "none";
      });
    });
  
    // Performance Chart using Chart.js (sample data)
    const ctx = document.getElementById("performanceChart").getContext("2d");
    const performanceChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
        datasets: [{
          label: 'Average Score',
          data: [7, 8, 7.5, 8.2],
          backgroundColor: 'rgba(40, 167, 69, 0.2)',
          borderColor: 'rgba(40, 167, 69, 1)',
          borderWidth: 2
        }]
      },
      options: {
        responsive: true,
        scales: {
          y: { beginAtZero: true, max: 10 }
        }
      }
    });
  
    // Handle Export Data Button (dummy implementation)
    document.getElementById("exportData").addEventListener("click", function () {
      showNotification("Data exported successfully (simulated).");
    });
  
    // Handle Quick Session Actions
    document.getElementById("startInterview").addEventListener("click", function () {
      showNotification("New interview session started!");
    });
    document.getElementById("resumeSession").addEventListener("click", function () {
      showNotification("Resumed incomplete session.");
    });
  
    // Handle Session Settings Form
    document.getElementById("sessionSettingsForm").addEventListener("submit", function (e) {
      e.preventDefault();
      showNotification("Session settings saved.");
    });
  
    // Handle Settings & Preferences Form
    document.getElementById("settingsForm").addEventListener("submit", function (e) {
      e.preventDefault();
      showNotification("Settings updated successfully.");
    });
  });
  