const express = require('express');
const path = require('path');
const { createProxyMiddleware } = require('http-proxy-middleware');
const app = express();
const PORT = process.env.PORT || 3002;

// Serve static files from the current directory
app.use(express.static(path.join(__dirname)));

// Serve static files from auth directories
app.use('/auth-login', express.static(path.join(__dirname, 'auth-login')));
app.use('/register', express.static(path.join(__dirname, 'register')));
app.use('/forgot-password', express.static(path.join(__dirname, 'forgot-password')));

// Parse JSON request bodies
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Proxy API requests to the backend
app.use('/api', createProxyMiddleware({
  target: 'http://localhost:8082',
  changeOrigin: true,
  pathRewrite: {
    '^/api': '', // Remove /api prefix when forwarding to backend
  },
  onProxyReq: (proxyReq, req, res) => {
    // If the request has a body, ensure the content-length is set correctly
    if (req.body) {
      const bodyData = JSON.stringify(req.body);
      // Update header
      proxyReq.setHeader('Content-Length', Buffer.byteLength(bodyData));
      // Write body to request
      proxyReq.write(bodyData);
    }
    // Log proxy requests for debugging
    console.log(`Proxying request to: ${req.method} ${proxyReq.path}`);
  },
  onError: (err, req, res) => {
    console.error('Proxy error:', err);
    res.writeHead(500, {
      'Content-Type': 'application/json'
    });
    res.end(JSON.stringify({
      message: 'Error connecting to the backend server',
      detail: err.message
    }));
  },
  // Increase timeout settings
  proxyTimeout: 30000,
  timeout: 30000,
  // Disable buffering to prevent memory issues
  buffer: false,
  // Add additional options for stability
  secure: false,
  ws: false,
  xfwd: false
}));

// Routes for authentication pages
app.get('/login', (req, res) => {
  res.sendFile(path.join(__dirname, 'auth-login', 'login.html'));
  console.log('Login page available at http://localhost:3002/login');
});

app.get('/register', (req, res) => {
  res.sendFile(path.join(__dirname, 'register', 'register.html'));
  console.log('Register page available at http://localhost:3002/register');
});

app.get('/forgot-password', (req, res) => {
  res.sendFile(path.join(__dirname, 'forgot-password', 'forgot.html'));
  console.log('Forgot password page available at http://localhost:3002/forgot-password');
});

// Route for the dashboard (root path)
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'dashboard.html'));
  console.log('Dashboard page available at http://localhost:3002/');
});

// Explicit route for login.js (though this is already handled by static middleware)
app.get('/auth-login/login.js', (req, res) => {
  res.sendFile(path.join(__dirname, 'auth-login/login.js'));
});

// Explicit route for forgotScript.js
app.get('/forgot-password/forgotScript.js', (req, res) => {
  res.sendFile(path.join(__dirname, 'forgot-password/forgotScript.js'));
});

// Explicit route for register.js
app.get('/register/register.js', (req, res) => {
  res.sendFile(path.join(__dirname, 'register/register.js'));
});

// Start the server
app.listen(PORT, () => {
  console.log(`Frontend server running at http://localhost:${PORT}`);
  console.log(`API requests will be proxied to http://localhost:8082`);
});