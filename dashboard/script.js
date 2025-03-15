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

  async function fetchDashboardData() {
    try {
        // Check if user is logged in
        const user = JSON.parse(localStorage.getItem('user') || '{}');
        if (!user.id) {
            console.warn('User not logged in, redirecting to login page');
            window.location.href = '/login';
            return;
        }

        // Show loading state
        document.querySelectorAll('.kpi-card .kpi-value').forEach(el => {
            el.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        });

        // Fetch data from backend API
        const response = await fetch(`/api/nexus_performance_analytics?user_id=${user.id}`);
        
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        
        const apiData = await response.json();
        const data = apiData.data || [];
        
        // Find the most recent analytics for this user
        const userAnalytics = data.filter(item => item.user_id === user.id)
                                 .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))[0] || {};
        
        // Transform backend data to frontend format
        const dashboardData = {
            accuracyScore: userAnalytics.accuracy_score || 0,
            avgResponseTime: userAnalytics.avg_response_time || 0,
            totalSessions: 0, // Will be fetched separately
            positiveFeedback: userAnalytics.positive_feedback_percentage || 0,
            performanceMetrics: {
                labels: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                datasets: [{
                    data: [
                        userAnalytics.day1_score || 0, 
                        userAnalytics.day2_score || 0, 
                        userAnalytics.day3_score || 0, 
                        userAnalytics.day4_score || 0, 
                        userAnalytics.day5_score || 0
                    ]
                }]
            }
        };

        // Fetch session count
        const sessionsResponse = await fetch(`/api/nexus_interview_sessions?user_id=${user.id}`);
        if (sessionsResponse.ok) {
            const sessionsData = await sessionsResponse.json();
            dashboardData.totalSessions = sessionsData.data ? sessionsData.data.length : 0;
        }

        // Fetch question categories
        const categoriesResponse = await fetch('/api/nexus_question_category_stats');
        if (categoriesResponse.ok) {
            const categoriesData = await categoriesResponse.json();
            const categories = categoriesData.data || [];
            
            dashboardData.questionCategories = {
                Behavioral: categories.find(c => c.category_name === 'Behavioral')?.question_count || 0,
                Technical: categories.find(c => c.category_name === 'Technical')?.question_count || 0,
                Situational: categories.find(c => c.category_name === 'Situational')?.question_count || 0,
                General: categories.find(c => c.category_name === 'General')?.question_count || 0
            };
        }

        // Fetch user feedback
        const feedbackResponse = await fetch('/api/nexus_user_feedback_evaluation');
        if (feedbackResponse.ok) {
            const feedbackData = await feedbackResponse.json();
            const feedback = feedbackData.data || [];
            
            // Count feedback types
            let positive = 0, neutral = 0, negative = 0;
            feedback.forEach(item => {
                if (item.rating >= 4) positive++;
                else if (item.rating >= 3) neutral++;
                else negative++;
            });
            
            dashboardData.userFeedback = {
                Positive: positive,
                Neutral: neutral,
                Negative: negative
            };
        }

        // Update KPI Cards
        document.querySelector(".kpi-card:nth-child(1) .kpi-value").textContent = `${dashboardData.accuracyScore.toFixed(1)}%`;
        document.querySelector(".kpi-card:nth-child(2) .kpi-value").textContent = `${dashboardData.avgResponseTime.toFixed(1)}s`;
        document.querySelector(".kpi-card:nth-child(3) .kpi-value").textContent = `${dashboardData.totalSessions}`;
        document.querySelector(".kpi-card:nth-child(4) .kpi-value").textContent = `${dashboardData.positiveFeedback.toFixed(1)}%`;

        // Update Charts
        updateCharts(dashboardData);

        // Fetch and display recent sessions
        fetchRecentSessions(user.id);

    } catch (error) {
        console.error("Error fetching dashboard data:", error);
        // Show error state or fallback to mock data
        document.querySelectorAll('.kpi-card .kpi-value').forEach(el => {
            el.textContent = 'N/A';
        });
    }
}

async function fetchRecentSessions(userId) {
    try {
        const response = await fetch(`/api/nexus_interview_sessions?user_id=${userId}`);
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        
        const data = await response.json();
        const sessions = data.data || [];
        
        // Sort sessions by date (newest first)
        const recentSessions = sessions.sort((a, b) => 
            new Date(b.session_date) - new Date(a.session_date)
        ).slice(0, 3); // Get only the 3 most recent
        
        const sessionList = document.querySelector('.session-list');
        if (!sessionList) return;
        
        // Clear existing sessions
        sessionList.innerHTML = '';
        
        // Add recent sessions to the list
        recentSessions.forEach(session => {
            // Format date
            const sessionDate = new Date(session.session_date);
            const formattedDate = sessionDate.toLocaleDateString('en-US', { 
                weekday: 'short',
                month: 'short', 
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
            
            // Create session item
            const sessionItem = document.createElement('li');
            sessionItem.className = 'session-item';
            sessionItem.innerHTML = `
                <div class="session-info">
                    <div class="session-id">Session #${session.id}</div>
                    <div class="session-date">${formattedDate}</div>
                </div>
                <div class="session-metrics">
                    <div class="session-metric">
                        <div class="metric-value">${session.accuracy_score || 'N/A'}</div>
                        <div class="metric-label">Accuracy</div>
                    </div>
                    <div class="session-metric">
                        <div class="metric-value">${session.question_count || 'N/A'}</div>
                        <div class="metric-label">Questions</div>
                    </div>
                    <div class="session-metric">
                        <div class="metric-value">${session.duration_minutes || 'N/A'}</div>
                        <div class="metric-label">Duration</div>
                    </div>
                </div>
            `;
            
            sessionList.appendChild(sessionItem);
        });
        
    } catch (error) {
        console.error("Error fetching recent sessions:", error);
    }
}

function updateCharts(data) {
    // Update Performance Chart
    if (window.performanceChart) {
        window.performanceChart.data.datasets[0].data = data.performanceMetrics.datasets[0].data;
        window.performanceChart.update();
    }
    
    // Update Category Chart
    if (window.categoryChart) {
        window.categoryChart.data.datasets[0].data = [
            data.questionCategories.Behavioral,
            data.questionCategories.Technical,
            data.questionCategories.Situational,
            data.questionCategories.General
        ];
        window.categoryChart.update();
    }
    
    // Update Feedback Chart
    if (window.feedbackChart) {
        window.feedbackChart.data.datasets[0].data = [
            data.userFeedback.Positive,
            data.userFeedback.Neutral,
            data.userFeedback.Negative
        ];
        window.feedbackChart.update();
    }
}

// Check authentication status on page load
document.addEventListener("DOMContentLoaded", function() {
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    
    // If not on login page and user is not logged in, redirect to login
    if (!window.location.pathname.includes('/login') && 
        !window.location.pathname.includes('/register') && 
        !window.location.pathname.includes('/forgot-password') && 
        !user.id) {
        window.location.href = '/login';
        return;
    }
    
    // If on dashboard, fetch data
    if (window.location.pathname === '/' || window.location.pathname === '/dashboard') {
        fetchDashboardData();
    }
    
    // Add logout functionality
    const logoutBtn = document.querySelector('.logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function() {
            localStorage.removeItem('user');
            window.location.href = '/login';
        });
    }
});

// Store chart instances globally for later updates
window.performanceChart = null;
window.categoryChart = null;
window.feedbackChart = null;
window.improvementChart = null;

// Initialize charts and store references
document.addEventListener("DOMContentLoaded", function() {
    function createChart(chartId, chartType, chartData) {
        const chartElement = document.getElementById(chartId);
        if (!chartElement) {
            console.warn(`Chart element with id '${chartId}' not found.`);
            return null;
        }
        const ctx = chartElement.getContext("2d");
        return new Chart(ctx, {
            type: chartType,
            data: chartData
        });
    }

    window.performanceChart = createChart("performanceChart", "line", {
        labels: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        datasets: [{
            label: "Accuracy Score",
            data: [0, 0, 0, 0, 0], // Will be populated by API data
            borderColor: "#4361ee",
            backgroundColor: "rgba(67, 97, 238, 0.2)",
            borderWidth: 2,
            fill: true
        }]
    });

    window.categoryChart = createChart("categoryChart", "doughnut", {
        labels: ["Behavioral", "Technical", "Situational", "General"],
        datasets: [{
            data: [0, 0, 0, 0], // Will be populated by API data
            backgroundColor: ["#4361ee", "#3f37c9", "#4cc9f0", "#f8961e"]
        }]
    });

    window.feedbackChart = createChart("feedbackChart", "bar", {
        labels: ["Positive", "Neutral", "Negative"],
        datasets: [{
            label: "Feedback",
            data: [0, 0, 0], // Will be populated by API data
            backgroundColor: ["#4cc9f0", "#f8961e", "#f72585"]
        }]
    });

    window.improvementChart = createChart("improvementChart", "polarArea", {
        labels: ["Technical Skills", "Communication", "Confidence"],
        datasets: [{
            data: [50, 35, 15],
            backgroundColor: ["#4361ee", "#4cc9f0", "#f72585"]
        }]
    });
});

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
