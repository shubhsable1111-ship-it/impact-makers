# Frontend - LoneGuard AI Credit Risk Assessment

This directory contains the frontend web application for the LoneGuard AI Credit Risk Assessment system.

## Structure

```
frontend/
├── index.html              # Category selection page (Borrower/Bank)
├── register.html           # Borrower registration form
├── registrection.html      # Bank registration form
├── dashboard.html          # File upload dashboard
├── score.html              # Credit score display page
├── calculate-score.html    # Score calculation form
├── css/
│   ├── style.css          # Main stylesheet
│   └── style1.css         # Registration form styles
└── js/
    ├── api.js             # API utility functions
    ├── register.js        # Registration logic
    ├── calculate.js       # Score calculation logic
    ├── profile.js         # Profile management
    └── result.js          # Results display logic
```

## Running the Frontend

### Development

1. **Start the Backend Server** (from project root):
   ```bash
   cd backend
   python -m uvicorn app.main:app --reload
   ```
   Backend will run on `http://localhost:8000`

2. **Open Frontend** (one of these options):
   - **Option A**: Open `frontend/index.html` directly in a browser
   - **Option B**: Use a local web server (recommended):
     ```bash
     cd frontend
     python -m http.server 3000
     ```
     Then navigate to `http://localhost:3000`

### Production Configuration

**Important**: The frontend is configured to connect to `http://localhost:8000` by default. For production deployment:

1. Update the `BASE_URL` in `js/api.js`:
   ```javascript
   const BASE_URL = "https://your-backend-domain.com";
   ```

2. Deploy frontend files to your hosting service (e.g., Netlify, Vercel, GitHub Pages, AWS S3)

## Features

- **Category Selection**: Choose between Borrower and Bank roles
- **User Registration**: Register new users with job type and activity duration
- **File Upload Dashboard**: Upload CSV transaction data and bank balance proofs
- **Credit Score Analysis**: AI-powered credit risk assessment
- **Responsive Design**: Works on desktop and mobile devices

## Technologies Used

- **HTML5**: Structure and content
- **CSS3**: Styling with modern gradients and animations
- **Vanilla JavaScript**: No frameworks, lightweight and fast
- **Fetch API**: Backend communication

## Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge

## Notes

- All API interactions use the Fetch API
- Forms include client-side validation
- Error handling with user-friendly alerts
- Local storage used for session management
