document.addEventListener("DOMContentLoaded", function () {
  // Dark Mode Toggle using a Button with Icon
  const darkModeBtn = document.getElementById('dark-mode-btn');
  const body = document.body;

  // Set initial state based on stored preference
  if (localStorage.getItem('darkMode') === 'enabled') {
    body.classList.add('dark-mode');
    darkModeBtn.innerHTML = '<i class="fas fa-sun"></i>';
  } else {
    darkModeBtn.innerHTML = '<i class="fas fa-moon"></i>';
  }

  darkModeBtn.addEventListener('click', function() {
    body.classList.toggle('dark-mode');
    if (body.classList.contains('dark-mode')) {
      localStorage.setItem('darkMode', 'enabled');
      darkModeBtn.innerHTML = '<i class="fas fa-sun"></i>';
    } else {
      localStorage.setItem('darkMode', 'disabled');
      darkModeBtn.innerHTML = '<i class="fas fa-moon"></i>';
    }
  });


  // Sidebar Navigation (switching dashboard sections)
  const navLinks = document.querySelectorAll('.nav-link');
  const sections = document.querySelectorAll('.dashboard-section');

  navLinks.forEach(link => {
      link.addEventListener('click', (e) => {
          e.preventDefault();
          const targetSection = link.getAttribute('data-section');

          sections.forEach(section => section.style.display = 'none');
          const targetElement = document.getElementById(targetSection);
          if (targetElement) {
              targetElement.style.display = 'block';
          }

          navLinks.forEach(link => link.classList.remove('active'));
          link.classList.add('active');
      });
  });

  // Sidebar Toggle: Toggle the "collapsed" class on the sidebar and adjust main content width
  const menuToggle = document.getElementById("menu-toggle");
  const sidebar = document.getElementById("sidebar");
  const mainContent = document.getElementById("main-content");

  menuToggle.addEventListener("click", function () {
      sidebar.classList.toggle("collapsed");
      mainContent.classList.toggle("sidebar-collapsed");
  });

  // Chart.js Initialization
  if (typeof Chart === "undefined") {
      console.error("Chart.js not loaded");
      return;
  }
  console.log("Initializing Charts...");

  function createChart(chartId, chartType, chartData) {
      const chartElement = document.getElementById(chartId);
      if (!chartElement) {
          console.warn(`Chart element with id '${chartId}' not found.`);
          return;
      }
      const ctx = chartElement.getContext("2d");
      return new Chart(ctx, {
          type: chartType,
          data: chartData
      });
  }

  createChart("performanceChart", "line", {
      labels: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      datasets: [{
          label: "Accuracy Score",
          data: [88, 85, 90, 92, 88],
          borderColor: "#4361ee",
          backgroundColor: "rgba(67, 97, 238, 0.2)",
          borderWidth: 2,
          fill: true
      }]
  });

  createChart("categoryChart", "doughnut", {
      labels: ["Behavioral", "Technical", "Situational", "General"],
      datasets: [{
          data: [40, 30, 20, 10],
          backgroundColor: ["#4361ee", "#3f37c9", "#4cc9f0", "#f8961e"]
      }]
  });

  createChart("feedbackChart", "bar", {
      labels: ["Positive", "Neutral", "Negative"],
      datasets: [{
          label: "Feedback",
          data: [60, 30, 10],
          backgroundColor: ["#4cc9f0", "#f8961e", "#f72585"]
      }]
  });

  createChart("improvementChart", "polarArea", {
      labels: ["Technical Skills", "Communication", "Confidence"],
      datasets: [{
          data: [50, 35, 15],
          backgroundColor: ["#4361ee", "#4cc9f0", "#f72585"]
      }]
  });

  console.log("Charts initialized successfully.");

  function resizeChart(chartId) {
      const chartCanvas = document.getElementById(chartId);
      if (chartCanvas) {
          chartCanvas.style.width = "100%";
          chartCanvas.style.height = "300px"; // Adjust as needed
      }
  }
  resizeChart("performanceChart");

  // Password Toggle Visibility
  function togglePassword() {
      let passwordField = document.getElementById("password");
      let icon = document.querySelector(".toggle-visibility i");

      if (passwordField.type === "password") {
          passwordField.type = "text";
          icon.classList.remove("fa-eye");
          icon.classList.add("fa-eye-slash");
      } else {
          passwordField.type = "password";
          icon.classList.remove("fa-eye-slash");
          icon.classList.add("fa-eye");
      }
  }

  // Settings Tabs Functionality
// Settings Tabs Functionality
const tabs = document.querySelectorAll(".settings-tab");
const tabSections = document.querySelectorAll(".settings-section");

tabs.forEach(tab => {
  tab.addEventListener("click", function () {
    // Remove active class from all tabs and hide all sections
    tabs.forEach(t => t.classList.remove("active"));
    tabSections.forEach(sec => sec.classList.remove("active"));

    // Activate the clicked tab and its corresponding section
    tab.classList.add("active");
    const targetId = tab.getAttribute("data-tab");
    const targetSection = document.getElementById(targetId);
    if (targetSection) {
      targetSection.classList.add("active");
    }
  });
});

  // Logout handler
  function handleLogout() {
      // Redirect to logout URL or clear authentication tokens
      window.location.href = '/logout';
  }
});
async function fetchDashboardData() {
    try {
        const response = await fetch("http://localhost:8082/dashboard-data");
        const data = await response.json();

        // Update KPI Cards
        document.querySelector(".kpi-card:nth-child(1) .kpi-value").textContent = `${data.accuracyScore}%`;
        document.querySelector(".kpi-card:nth-child(2) .kpi-value").textContent = `${data.avgResponseTime}s`;
        document.querySelector(".kpi-card:nth-child(3) .kpi-value").textContent = `${data.totalSessions}`;
        document.querySelector(".kpi-card:nth-child(4) .kpi-value").textContent = `${data.positiveFeedback}%`;

        // Update Charts
        updateChart(performanceChart, data.performanceMetrics);
        updateChart(categoryChart, Object.values(data.questionCategories));
        updateChart(feedbackChart, Object.values(data.userFeedback));

    } catch (error) {
        console.error("Error fetching dashboard data:", error);
    }
}

// Call on page load
document.addEventListener("DOMContentLoaded", fetchDashboardData);
