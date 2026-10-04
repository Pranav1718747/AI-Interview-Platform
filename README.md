# 🚀 AI-Interview-Platform

A full-stack, AI-powered **Resume ATS Analysis & Mock Interview Platform** built with **Django REST Framework, OpenRouter (Gemini / Claude / GPT), React 19, and Vite**.

---

## 🌟 Key Features

### 1. 📄 Deep ATS Resume Intelligence (`resumes` & `ai_engine`)
- **Document Support**: Parses `.pdf` (PyMuPDF & pypdf), `.docx` (python-docx), and `.txt` files.
- **ATS Scoring Engine**: Calculates an industry-aligned ATS score (0-100).
- **Skill Extraction**: Identifies verified technical skills and soft skills.
- **Strength & Gap Analysis**: Highlights top career strengths, missing keywords, and actionable suggestions.
- **Matching Role Recommendations**: Suggests best-fit job titles based on resume experience.

### 2. 🎙️ Real-Time AI Mock Interviews (`interviews` & `ai_engine`)
- **Dynamic Question Generation**: Generates 3-7 tailored questions customized to the candidate's target job role, seniority level (Entry, Mid, Senior, Lead), interview style (Technical, Behavioral, System Design), and uploaded resume context.
- **Web Speech Integration**:
  - **Speech-to-Text (STT)**: Candidates can answer questions naturally using their voice via live microphone transcription.
  - **Text-to-Speech (TTS)**: AI reads out interview questions clearly.
- **Real-Time AI Grading**: Evaluates responses for **Technical Depth**, **Communication Clarity**, and **Relevance**.
- **Model Exemplary Answers**: Shows STAR-method model answers for each question.
- **Interactive Camera Preview**: Optional webcam feed to simulate realistic interview conditions.

### 3. 📊 Analytics & Scorecards (`analytics` & `reports`)
- **Executive Scorecard**: Overall readiness assessment and radar pillars (Technical Mastery, Communication, Problem Solving).
- **Growth Trajectory**: Historical progress tracking across past practice sessions.
- **Printable Reports**: Clean report layout for export or review.

---

## 🛠️ Architecture & Tech Stack

- **Backend**: Python 3.14 / Django 5.x, Django REST Framework, SimpleJWT, SQLite / PostgreSQL
- **AI Integration**: OpenRouter API (`google/gemini-2.5-flash` or configurable model) with resilient offline fallback
- **Frontend**: React 19, Vite, Axios, React Router DOM 7, Lucide Icons, Canvas Confetti
- **Styling**: Vanilla CSS Design System with dark glassmorphism, glowing accents, and responsive layout

---

## 🚦 Getting Started

### Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables:**
   Copy `.env.example` to `.env` and set your OpenRouter API key:
   ```env
   SECRET_KEY=your-secret-key
   DEBUG=True
   OPENROUTER_API_KEY=your-openrouter-api-key
   OPENROUTER_MODEL=google/gemini-2.5-flash
   ```

4. **Run Migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Start Django Backend Server:**
   ```bash
   python manage.py runserver 8000
   ```

### Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the Vite development server:**
   ```bash
   npm run dev
   ```
   Open `http://localhost:5173` in your browser.

---

## 📡 API Endpoints Reference

### Authentication (`/api/auth/` & `/api/token/`)
- `POST /api/auth/register/` - Register new user
- `POST /api/token/` - Obtain JWT access & refresh tokens
- `POST /api/token/refresh/` - Refresh JWT access token
- `GET /api/auth/profile/` - Get authenticated user profile

### Resume Management (`/api/resumes/`)
- `GET /api/resumes/` - List user resumes with ATS analysis
- `POST /api/resumes/` - Upload resume file (.pdf/.docx) with auto ATS scan
- `GET /api/resumes/<id>/` - Retrieve resume details and analysis
- `POST /api/resumes/<id>/analyze/` - Re-trigger AI ATS scan
- `DELETE /api/resumes/<id>/` - Delete resume

### AI Mock Interviews (`/api/interviews/`)
- `POST /api/interviews/start/` - Generate tailored questions and start session
- `GET /api/interviews/` - List previous interview sessions
- `GET /api/interviews/<id>/` - Retrieve interview state and questions
- `POST /api/interviews/<id>/questions/<q_id>/answer/` - Submit answer for instant AI evaluation
- `POST /api/interviews/<id>/finish/` - Finalize session and generate full scorecard

### Analytics & Reports (`/api/analytics/` & `/api/reports/`)
- `GET /api/analytics/dashboard/` - Aggregated stats, averages, and score progression
- `GET /api/reports/interview/<id>/` - Structured interview performance audit
