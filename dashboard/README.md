# AI-NEXUS Dashboard

This is the frontend dashboard for the AI-NEXUS project. It provides a user interface for interacting with the AI interview responder system, displaying analytics, and managing user sessions.

## Prerequisites

- Node.js (v14 or higher)
- npm (v6 or higher)
- Backend API server running (see backend README.md)

## Installation

1. Clone the repository (if you haven't already):
   ```
   git clone https://github.com/yourusername/AI-NEXUS.git
   cd AI-NEXUS/dashboard
   ```

2. Install dependencies:
   ```
   npm install
   ```

## Running the Frontend

1. Make sure the backend API server is running first:
   ```
   # In the backend directory
   uvicorn main:app --host 0.0.0.0 --port 8082
   ```

2. Start the frontend server:
   ```
   # In the dashboard directory
   npm start
   ```

   Or for development with auto-reload:
   ```
   npm run dev
   ```

3. Access the dashboard in your browser:
   ```
   http://localhost:3001
   ```

## Features

- User authentication (login/register)
- Dashboard overview with key performance indicators
- Interview session management
- Question and response analysis
- User feedback visualization
- Model configuration settings

## Project Structure

- `index.js` - Express server setup and API proxy configuration
- `dashboard.html` - Main dashboard interface
- `script.js` - Dashboard functionality and data fetching
- `styles.css` - Dashboard styling
- `auth-login/` - Login page and authentication
- `register/` - User registration
- `forgot-password/` - Password recovery

## API Integration

The frontend communicates with the backend API through a proxy setup in the Express server. All API requests are forwarded to the backend server running on port 8082.

Example API endpoints:
- `/api/login` - User authentication
- `/api/register` - User registration
- `/api/nexus_interview_sessions` - Interview session data
- `/api/nexus_performance_analytics` - Performance metrics

## Development

To modify the frontend:
1. Edit the HTML files for layout changes
2. Edit the JavaScript files for functionality changes
3. Edit the CSS files for styling changes

The Express server will automatically serve the updated files.

## Troubleshooting

- If you encounter CORS issues, ensure the backend server is running and the proxy is correctly configured in `index.js`
- If authentication fails, check the backend server logs for details
- For data loading issues, check the browser console for error messages
