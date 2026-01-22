# Local Setup Guide for HBD Dashboard

## Prerequisites

1. **Python 3.8+** - Check with `python --version`
2. **Node.js 16+ and npm** - Check with `node --version` and `npm --version`
3. **MySQL Server** - Running on localhost:3306
4. **Git** (if cloning from repository)

---

## Step 1: Database Setup

1. **Install MySQL Server** (if not already installed)
   - Download from: https://dev.mysql.com/downloads/mysql/
   - Or use XAMPP/WAMP which includes MySQL

2. **Create the database:**
   ```sql
   CREATE DATABASE dummy;
   ```
   Or use MySQL Workbench/phpMyAdmin to create a database named `dummy`

3. **Update database credentials** (if needed):
   - Edit `backend/database/session.py` (line 10)
   - Edit `backend/config.py` (line 5)
   - Current default: `root:vivek123@localhost:3306/dummy`
   - Change `root` and `vivek123` to your MySQL username and password

---

## Step 2: Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd HBD_Dashboard/backend
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment:**
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **Linux/Mac:**
     ```bash
     source venv/bin/activate
     ```

4. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install pymysql  # Required for MySQL connection (missing from requirements.txt)
   ```

5. **Install Playwright browsers:**
   ```bash
   playwright install
   ```
   This installs browser binaries needed for web scraping features.

6. **Set up environment variables (optional):**
   Create a `.env` file in the `backend` directory:
   ```
   SECRET_KEY=your-secret-key-here
   JWT_SECRET_KEY=your-jwt-secret-key-here
   ```
   If not set, default values will be used (not recommended for production).

7. **Run the Flask backend:**
   ```bash
   python app.py
   ```
   The server will start on `http://127.0.0.1:5000` (default Flask port)

---

## Step 3: Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd HBD_Dashboard/frontend
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```
   The frontend will typically run on `http://localhost:5173` (Vite default port)

---

## Step 4: Verify Setup

1. **Backend:** Open `http://127.0.0.1:5000` in your browser (should see Flask response or API endpoints)
2. **Frontend:** Open `http://localhost:5173` in your browser (should see the dashboard)

---

## Important Notes

### Database Configuration
- The project uses MySQL database named `dummy`
- Default credentials: `root` / `vivek123`
- Update these in:
  - `backend/database/session.py` (line 10)
  - `backend/config.py` (line 5)

### API Connection
- Frontend is configured to connect to backend at `http://127.0.0.1:5000`
- This is set in `frontend/src/utils/Api.jsx` (line 4)
- If you change the backend port, update this file

### Playwright
- Playwright is used for web scraping (Google Maps, Amazon, etc.)
- Browser binaries are installed with `playwright install`
- This is required for scraper features to work

### Missing Dependency
- `pymysql` is required but not in `requirements.txt`
- Install it manually: `pip install pymysql`

---

## Troubleshooting

### Database Connection Issues
- Ensure MySQL is running: `mysql -u root -p`
- Check if database `dummy` exists
- Verify credentials in `session.py` and `config.py`

### Port Already in Use
- Backend: Change port in `app.py` (line 634): `app.run(debug=True, port=5001)`
- Frontend: Vite will automatically use next available port

### Playwright Issues
- Run `playwright install` again
- On Linux, you may need: `playwright install-deps`

### Module Not Found Errors
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

---

## Project Structure

```
HBD_Dashboard/
├── backend/          # Flask API server
│   ├── app.py       # Main Flask application
│   ├── config.py    # Configuration
│   ├── routes/      # API route handlers
│   ├── model/       # Database models
│   └── database/    # Database session management
└── frontend/        # React frontend
    ├── src/         # React source code
    └── public/      # Static assets
```

---

## Next Steps

1. Create database tables (they should be created automatically when you run the app)
2. Set up authentication (check `routes/auth_route.py`)
3. Import initial data if needed
4. Configure production settings for deployment

