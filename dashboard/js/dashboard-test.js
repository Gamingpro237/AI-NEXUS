document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('main-content');
    const darkModeToggle = document.getElementById('dark-mode-toggle');
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('.dashboard-section');
    const sidebarToggleBtn = document.getElementById('sidebar-toggle');
    
    // Charts initialization
    initializeCharts();
    
    // Sidebar toggle functionality
    sidebarToggleBtn.addEventListener('click', function() {
        sidebar.classList.toggle('active');
        
        // On mobile
        if (window.innerWidth <= 768) {
            if (sidebar.classList.contains('active')) {
                document.body.style.overflow = 'hidden'; // Prevent background scrolling
            } else {
                document.body.style.overflow = 'auto';
            }
        } else {
            // On desktop
            sidebar.classList.toggle('collapsed');
            mainContent.classList.toggle('expanded');
        }
    });
    
    // Dark mode toggle
    function toggleDarkMode() {
        document.body.classList.toggle('dark-mode');
        const isDarkMode = document.body.classList.contains('dark-mode');
        darkModeToggle.checked = isDarkMode;
        localStorage.setItem('darkMode', isDarkMode);
    }
    
    // Event listener for dark mode toggle
    darkModeToggle.addEventListener('change', toggleDarkMode);
    
    // Check for saved dark mode preference and apply it
    if (localStorage.getItem('darkMode') === 'true') {
        document.body.classList.add('dark-mode');
        darkModeToggle.checked = true;
    }
    
    // Navigation menu functionality
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove active class from all links
            navLinks.forEach(l => l.classList.remove('active'));
            
            // Add active class to clicked link
            this.classList.add('active');
            
            // Hide all sections
            sections.forEach(section => section.style.display = 'none');
            
            // Show the selected section
            const targetSection = this.getAttribute('data-section');
            document.getElementById(targetSection).style.display = 'block';
            
            // Update page title
            document.querySelector('.page-title h1').textContent = this.textContent.trim();
            
            // Close sidebar on mobile after navigation
            if (window.innerWidth <= 768) {
                sidebar.classList.remove('active');
                document.body.style.overflow = 'auto';
            }
        });
    });
    
    // Responsive sidebar for mobile
    const handleResize = () => {
        if (window.innerWidth <= 768) {
            sidebar.classList.remove('active');
            sidebar.classList.remove('collapsed');
            mainContent.classList.remove('expanded');
            mainContent.style.marginLeft = '0';
        } else {
            mainContent.style.marginLeft = sidebar.classList.contains('collapsed') ? 
                'var(--sidebar-collapsed-width)' : 'var(--sidebar-width)';
        }
    };
    
    // Initial call and event listener for resize
    window.addEventListener('resize', handleResize);
    handleResize();
    
    // Initialize charts
    function initializeCharts() {
        // Performance Chart
        const performanceCtx = document.getElementById('performanceChart').getContext('2d');
        const performanceChart = new Chart(performanceCtx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'],
                datasets: [{
                    label: 'Accuracy (%)',
                    data: [82, 79, 78, 81, 84, 87, 89],
                    borderColor: '#4361ee',
                    backgroundColor: 'rgba(67, 97, 238, 0.1)',
                    tension: 0.3,
                    fill: true
                }, {
                    label: 'Response Time (s)',
                    data: [1.8, 1.7, 1.6, 1.5, 1.4, 1.3, 1.2],
                    borderColor: '#4cc9f0',
                    backgroundColor: 'rgba(76, 201, 240, 0.1)',
                    tension: 0.3,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        min: 70
                    }
                }
            }
        });
        
        // Category Chart
        const categoryCtx = document.getElementById('categoryChart').getContext('2d');
        const categoryChart = new Chart(categoryCtx, {
            type: 'doughnut',
            data: {
                labels: ['Technical', 'Behavioral', 'Experience', 'Scenario', 'Company-specific'],
                datasets: [{
                    data: [30, 25, 20, 15, 10],
                    backgroundColor: [
                        '#4361ee',
                        '#3f37c9',
                        '#4cc9f0',
                        '#f72585',
                        '#f8961e'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                    }
                }
            }
        });
        
        // Feedback Chart
        const feedbackCtx = document.getElementById('feedbackChart').getContext('2d');
        const feedbackChart = new Chart(feedbackCtx, {
            type: 'bar',
            data: {
                labels: ['Content', 'Clarity', 'Structure', 'Relevance', 'Example Quality'],
                datasets: [{
                    label: 'Average Score (1-5)',
                    data: [4.2, 3.8, 4.1, 4.5, 3.9],
                    backgroundColor: '#4361ee',
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 5
                    }
                }
            }
        });
        
        // Improvement Areas Chart
        const improvementCtx = document.getElementById('improvementChart').getContext('2d');
        const improvementChart = new Chart(improvementCtx, {
            type: 'radar',
            data: {
                labels: ['Technical Accuracy', 'Conciseness', 'Specificity', 'Structure', 'Relevance', 'Example Quality'],
                datasets: [{
                    label: 'Current Performance',
                    data: [85, 70, 80, 75, 90, 65],
                    backgroundColor: 'rgba(67, 97, 238, 0.2)',
                    borderColor: '#4361ee',
                    borderWidth: 2,
                    pointBackgroundColor: '#4361ee'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            stepSize: 20
                        }
                    }
                }
            }
        });
    }
});