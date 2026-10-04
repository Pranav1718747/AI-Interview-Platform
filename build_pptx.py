import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_deck(output_path):
    prs = Presentation()
    # 16:9 widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Theme colors
    COLOR_BG = RGBColor(10, 14, 26)         # Deep Navy Background #0a0e1a
    COLOR_CARD = RGBColor(18, 24, 42)       # Card Slate #12182a
    COLOR_CARD_BORDER = RGBColor(40, 50, 75)# Border Line
    COLOR_PRIMARY = RGBColor(99, 102, 241)  # Electric Indigo #6366f1
    COLOR_CYAN = RGBColor(6, 182, 212)      # Accent Cyan #06b6d4
    COLOR_EMERALD = RGBColor(16, 185, 129)  # Accent Emerald #10b981
    COLOR_ROSE = RGBColor(244, 63, 94)      # Accent Rose #f43f5e
    COLOR_AMBER = RGBColor(245, 158, 11)    # Accent Amber #f59e0b
    COLOR_TEXT_MAIN = RGBColor(248, 250, 252) # White #f8fafc
    COLOR_TEXT_MUTED = RGBColor(148, 163, 184) # Muted #94a3b8
    COLOR_TEXT_DIM = RGBColor(100, 116, 139)   # Dim #64748b

    def add_base_slide(badge_text, title_text, subtitle_text=""):
        slide = prs.slides.add_slide(blank_layout)
        
        # Background fill
        bg_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg_shape.fill.solid()
        bg_shape.fill.fore_color.rgb = COLOR_BG
        bg_shape.line.fill.background()

        # Header Badge
        if badge_text:
            badge_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.5), Inches(3.2), Inches(0.35))
            badge_box.fill.solid()
            badge_box.fill.fore_color.rgb = RGBColor(25, 33, 58)
            badge_box.line.color.rgb = COLOR_PRIMARY
            badge_box.line.width = Pt(1)
            tf = badge_box.text_frame
            tf.word_wrap = True
            tf.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = tf.paragraphs[0]
            p.text = badge_text.upper()
            p.font.size = Pt(9.5)
            p.font.bold = True
            p.font.color.rgb = COLOR_PRIMARY
            p.alignment = PP_ALIGN.CENTER

        # Title
        title_top = Inches(0.95) if badge_text else Inches(0.6)
        tx_box = slide.shapes.add_textbox(Inches(0.8), title_top, Inches(11.7), Inches(0.6))
        tf = tx_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_MAIN

        # Subtitle
        if subtitle_text:
            sub_box = slide.shapes.add_textbox(Inches(0.8), title_top + Inches(0.45), Inches(11.7), Inches(0.4))
            tf_s = sub_box.text_frame
            tf_s.word_wrap = True
            p_s = tf_s.paragraphs[0]
            p_s.text = subtitle_text
            p_s.font.size = Pt(11)
            p_s.font.color.rgb = COLOR_TEXT_MUTED

        return slide

    def add_speaker_notes(slide, notes_text):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = notes_text

    def create_card(slide, left, top, width, height, bg_color=COLOR_CARD, border_color=COLOR_CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
        return card

    # ==========================================
    # SLIDE 1: Title
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = COLOR_BG
    bg1.line.fill.background()

    # Main Card
    create_card(s1, 1.2, 1.2, 10.933, 5.1, bg_color=RGBColor(14, 20, 36), border_color=COLOR_PRIMARY)
    
    # Title Content
    tb1 = s1.shapes.add_textbox(Inches(1.8), Inches(1.8), Inches(9.733), Inches(3.8))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    
    p = tf1.paragraphs[0]
    p.text = "AI INTERVIEW & RESUME PLATFORM"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN
    p.alignment = PP_ALIGN.CENTER
    
    p2 = tf1.add_paragraph()
    p2.text = "Complete Technical Architecture & System Design"
    p2.font.size = Pt(28)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_TEXT_MAIN
    p2.alignment = PP_ALIGN.CENTER
    p2.space_before = Pt(12)
    p2.space_after = Pt(16)
    
    p3 = tf1.add_paragraph()
    p3.text = "A Full-Stack Deep Dive: React 19 • Django 5 REST Framework • OpenRouter Gemini 2.5 • Web Speech STT/TTS"
    p3.font.size = Pt(12.5)
    p3.font.color.rgb = COLOR_TEXT_MUTED
    p3.alignment = PP_ALIGN.CENTER
    
    p4 = tf1.add_paragraph()
    p4.text = "Engineering Architecture & Codebase Blueprint"
    p4.font.size = Pt(11)
    p4.font.color.rgb = COLOR_TEXT_DIM
    p4.alignment = PP_ALIGN.CENTER
    p4.space_before = Pt(24)

    add_speaker_notes(s1, 
        "What this means: Introduces the project identity, technology stack, and full-stack scope.\n"
        "Verbal Pitch: 'Welcome everyone. Today I will walk you through the complete, end-to-end technical architecture of our AI Interview & Resume Intelligence Platform. This system combines multi-format document text extraction, large language model orchestration, browser-native speech processing, and relational data modeling into a high-performance web platform.'\n"
        "Interviewer Question: 'Why did you decouple the React frontend and Django backend rather than using Django Templates or Next.js?'\n"
        "Answer: 'Decoupling React from Django allows us to maintain a clean stateless REST API, leverage native browser Web Speech APIs without server-side audio rendering overhead, and support multi-platform client expansion.'"
    )

    # Helper function for text list cards
    def populate_card_bullets(card_shape, heading, items, heading_color=COLOR_CYAN):
        tf = card_shape.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.TOP
        p = tf.paragraphs[0]
        p.text = heading
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = heading_color
        p.space_after = Pt(8)
        
        for it in items:
            p_i = tf.add_paragraph()
            p_i.text = f"•  {it}"
            p_i.font.size = Pt(10.5)
            p_i.font.color.rgb = COLOR_TEXT_MUTED
            p_i.space_after = Pt(4)

    # ==========================================
    # SLIDE 2: Project Overview
    # ==========================================
    s2 = add_base_slide("Executive Summary", "Project Overview & Core Capabilities", "Automating resume intelligence, tailored mock interviews, and real-time rubric scoring")
    c1 = create_card(s2, 0.8, 1.9, 3.6, 4.8)
    populate_card_bullets(c1, "1. ATS Resume Intelligence", [
        "PDF & DOCX text extraction pipeline",
        "ATS compatibility score (0-100)",
        "Verified technical & soft skills extraction",
        "Actionable strengths & weakness audit",
        "Missing industry keyword recommendations",
        "Direct CTA to launch role mock interview"
    ], COLOR_PRIMARY)

    c2 = create_card(s2, 4.8, 1.9, 3.6, 4.8)
    populate_card_bullets(c2, "2. AI Mock Interview Room", [
        "Dynamic question generation via LLM",
        "Tailored to Role, Seniority & Resume",
        "Web Speech API Voice-to-Text answering",
        "Multi-accent switcher (en-US, en-IN, en-GB)",
        "Text-to-Speech question audio reader",
        "Optional WebRTC camera preview mirror"
    ], COLOR_CYAN)

    c3 = create_card(s2, 8.8, 1.9, 3.6, 4.8)
    populate_card_bullets(c3, "3. Grading & Analytics", [
        "Turn-by-turn real-time rubric grading",
        "Scores: Technical, Clarity, Relevance",
        "Structured Markdown model STAR answers",
        "Post-interview readiness scorecard",
        "Radar competency breakdown pillars",
        "Historical trajectory tracking over time"
    ], COLOR_EMERALD)

    add_speaker_notes(s2,
        "What this means: Summarizes the 3 main functional pillars implemented in the repo.\n"
        "Verbal Pitch: 'The platform solves two major problems in tech hiring: generic static questions and lack of actionable rubric feedback. We bridge resume analysis directly with interactive voice interviews.'\n"
        "Likely Question: 'How does the question generator avoid repeating questions across sessions?'\n"
        "Answer: 'The LLM question generator receives candidate resume skills and job specifications dynamically, generating bespoke questions for the requested level and category.'"
    )

    # ==========================================
    # SLIDE 3: System at a Glance
    # ==========================================
    s3 = add_base_slide("System Blueprint", "High-Level Architecture & Component Map", "3-Tier Decoupled Client-Server & AI Orchestration Layer")
    c_arch1 = create_card(s3, 0.8, 1.9, 3.6, 4.8)
    populate_card_bullets(c_arch1, "Presentation Tier", [
        "React 19 Single Page Application (SPA)",
        "Vite 8 build tooling & sub-second HMR",
        "Native Web Speech STT & TTS engines",
        "Centralized Axios with JWT interceptors",
        "Dark Glassmorphic UI design tokens",
        "Client port: http://localhost:5173"
    ], COLOR_CYAN)

    c_arch2 = create_card(s3, 4.8, 1.9, 3.6, 4.8)
    populate_card_bullets(c_arch2, "API & Service Tier", [
        "Django 5.1 & Django REST Framework",
        "SimpleJWT stateless token authentication",
        "Document parsers (PyMuPDF & docx)",
        "prompt_service & ai_service modules",
        "Domain apps: users, resumes, interviews",
        "Server port: http://localhost:8000"
    ], COLOR_PRIMARY)

    c_arch3 = create_card(s3, 8.8, 1.9, 3.6, 4.8)
    populate_card_bullets(c_arch3, "Data & AI Tier", [
        "OpenRouter LLM: google/gemini-2.5-flash",
        "Token-bounded calls (max_tokens: 1500)",
        "SQLite 3 relational persistence (db.sqlite3)",
        "Django ORM with cascading foreign keys",
        "Local media storage (backend/media/)",
        "Zero mock fallbacks: direct AI execution"
    ], COLOR_EMERALD)

    add_speaker_notes(s3,
        "What this means: Shows the 3 architectural tiers and where each responsibility sits.\n"
        "Verbal Pitch: 'The frontend handles audio transcription and rendering, the Django backend handles business validation and document extraction, and OpenRouter delivers LLM evaluation with relational SQLite storage.'\n"
        "Likely Question: 'Why use OpenRouter instead of calling the Google Gemini SDK directly?'\n"
        "Answer: 'OpenRouter uses the OpenAI-compatible REST API standard, allowing zero-code model swapping to Claude, Llama 3, or GPT-4o by changing a single environment variable.'"
    )

    # ==========================================
    # SLIDE 4: Complete Technology Stack
    # ==========================================
    s4 = add_base_slide("Technology Audit", "Complete Technology Stack Breakdown", "Verified packages, libraries, and frameworks actually used in codebase")
    
    table_shape = s4.shapes.add_table(7, 4, Inches(0.8), Inches(1.9), Inches(11.733), Inches(4.8))
    table = table_shape.table
    table.columns[0].width = Inches(2.2)
    table.columns[1].width = Inches(2.4)
    table.columns[2].width = Inches(2.8)
    table.columns[3].width = Inches(4.333)

    headers = ["Layer", "Technology & Version", "Key File Location", "Architectural Role & Purpose"]
    for col_idx, text in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(25, 33, 58)
        p = cell.text_frame.paragraphs[0]
        p.text = text
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_PRIMARY

    rows = [
        ("Frontend UI", "React 19.2 + Vite 8.1", "frontend/package.json", "Declarative UI rendering with sub-second HMR development."),
        ("Routing & HTTP", "React Router 7 + Axios 1.18", "src/App.jsx, src/api/client.js", "SPA client-side routing & automatic JWT interceptor injection."),
        ("Voice & Display", "Web Speech API + react-markdown", "InterviewRoomPage, MarkdownView", "Native browser STT/TTS & structured Markdown model answers."),
        ("Backend Core", "Django 5.1 + Python 3.14", "backend/core/settings.py", "Modular monolith web framework with ORM and migrations."),
        ("REST & Auth", "DRF 3.15 + SimpleJWT 5.3", "core/settings.py, core/urls.py", "REST serializers, class-based views, stateless HMAC JWTs."),
        ("AI & Docs", "OpenRouter + PyMuPDF / docx", "ai_engine/services/*", "Gemini 2.5 Flash LLM gateway + binary PDF/DOCX parsers.")
    ]

    for row_idx, row_data in enumerate(rows, 1):
        for col_idx, text in enumerate(row_data):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_CARD if row_idx % 2 == 0 else RGBColor(14, 18, 32)
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.size = Pt(9.5)
            p.font.color.rgb = COLOR_TEXT_MAIN if col_idx == 1 else COLOR_TEXT_MUTED

    add_speaker_notes(s4,
        "What this means: Deep audit of every single library verified in the codebase.\n"
        "Verbal Pitch: 'Every library serves a concrete purpose without bloat. React 19 provides fast UI updates, SimpleJWT guarantees stateless authentication, and PyMuPDF parses resumes in milliseconds.'"
    )

    # ==========================================
    # SLIDE 5: Architectural Style — Modular Monolith
    # ==========================================
    s5 = add_base_slide("Architectural Style", "Layered Modular Monolith Architecture", "Logical separation of concerns within a unified, maintainable backend codebase")
    
    layers = [
        ("1. Presentation Layer (React 19)", "Dashboard, ResumeManager, InterviewRoom, ResultPage. Consumes REST JSON; manages UI state.", COLOR_CYAN),
        ("2. API & Security Layer (DRF & SimpleJWT)", "core/urls.py dispatches requests. Middleware validates CORS and verifies JWT signatures.", COLOR_PRIMARY),
        ("3. Service & Business Layer", "ai_service.py, prompt_service.py, document_service.py. Encapsulates document parsing and LLM prompts.", COLOR_EMERALD),
        ("4. Data Access Layer (Django ORM)", "User, Resume, ResumeAnalysis, InterviewSession, Question, Response models & serializers.", COLOR_AMBER),
        ("5. Persistence Layer (SQLite & Media)", "ACID relational storage in db.sqlite3; uploaded resume files saved in media/resumes/.", COLOR_ROSE)
    ]

    for i, (l_title, l_desc, l_col) in enumerate(layers):
        top_pos = 1.9 + i * 0.95
        card = create_card(s5, 0.8, top_pos, 11.733, 0.8)
        tf = card.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.text = l_title
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = l_col
        p2 = tf.add_paragraph()
        p2.text = l_desc
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = COLOR_TEXT_MUTED

    add_speaker_notes(s5,
        "What this means: Shows that views delegate heavy logic to service layers.\n"
        "Verbal Pitch: 'We chose a layered modular monolith. Controllers/views do not contain prompt strings or parsing code; they call domain services, keeping code testable and easy to maintain.'"
    )

    # ==========================================
    # SLIDE 6: Frontend Architecture & Client Pipeline
    # ==========================================
    s6 = add_base_slide("Frontend Architecture", "Client Application Architecture & Pipeline", "React 19 SPA routing, centralized interceptors, and audio-visual sub-pipelines")
    
    c_f1 = create_card(s6, 0.8, 1.9, 5.7, 4.8)
    populate_card_bullets(c_f1, "Client Pipeline & Routing", [
        "BrowserRouter wrapped in AuthProvider context",
        "Public Routes: LandingPage, LoginPage, RegisterPage",
        "ProtectedRoute: checks AuthContext.user & token",
        "Renders loading spinner during token verification",
        "Axios Request Interceptor: injects Bearer token",
        "Axios Response Interceptor: 401 catch & refresh retry",
        "Zero external UI framework: vanilla CSS tokens"
    ], COLOR_CYAN)

    c_f2 = create_card(s6, 6.8, 1.9, 5.7, 4.8)
    populate_card_bullets(c_f2, "Interactive Audio/Visual Systems", [
        "Web Speech Recognition API with interim buffer",
        "Language switchers: en-US, en-IN, en-GB",
        "finalTranscriptRef preserves keyboard edits",
        "Web Speech Synthesis: reads questions aloud",
        "HTML5 MediaDevices: camera mirror preview",
        "ScoreMeter: SVG animated radial score gauge",
        "MarkdownView: structured react-markdown display"
    ], COLOR_PRIMARY)

    add_speaker_notes(s6,
        "What this means: Detailed breakdown of the frontend client engine.\n"
        "Verbal Pitch: 'The frontend coordinates multiple browser APIs: speech recognition for answers, speech synthesis for question audio, camera preview for realism, and Axios interceptors for seamless JWT management.'"
    )

    # ==========================================
    # SLIDE 7: Frontend Component Tree
    # ==========================================
    s7 = add_base_slide("Component Hierarchy", "React 19 Component Hierarchy & Trees", "Declarative component tree mapping pages, guards, and shared widgets")
    
    c_tree1 = create_card(s7, 0.8, 1.9, 5.7, 4.8)
    populate_card_bullets(c_tree1, "Core Shell & Route Structure", [
        "App.jsx (AuthProvider, BrowserRouter)",
        "├── Navbar.jsx (Logo, Active Links, Profile, Logout)",
        "├── Public Routes (Landing, Login, Register)",
        "└── ProtectedRoute.jsx (Auth guard wrapper)",
        "    ├── DashboardPage.jsx (Overview & KPIs)",
        "    ├── ResumeManagerPage.jsx (Upload & ATS Modal)",
        "    ├── InterviewSetupPage.jsx (Configurator)",
        "    ├── InterviewRoomPage.jsx (Live Session)",
        "    ├── InterviewResultPage.jsx (Scorecard)",
        "    └── AnalyticsPage.jsx (Trajectory Table)"
    ], COLOR_CYAN)

    c_tree2 = create_card(s7, 6.8, 1.9, 5.7, 4.8)
    populate_card_bullets(c_tree2, "Shared Reusable Components", [
        "• ScoreMeter.jsx: Radial SVG circular progress gauge",
        "  - Inputs: score (0-100), size, strokeWidth, label",
        "  - Dynamic coloring: Emerald (>=80), Indigo (>=65), Red",
        "• CameraPreview.jsx: Local WebRTC video stream",
        "  - Toggle on/off without sending video to server",
        "• MarkdownView.jsx: Formatted typography renderer",
        "  - Renders h3, h4, lists, bold keywords, code blocks"
    ], COLOR_EMERALD)

    add_speaker_notes(s7,
        "What this means: Shows how components are organized and shared.\n"
        "Verbal Pitch: 'Notice how ScoreMeter and MarkdownView are reused across multiple pages, enforcing visual consistency across ATS review, live interview feedback, and the final scorecard.'"
    )

    # ==========================================
    # SLIDE 8: State Management Taxonomy
    # ==========================================
    s8 = add_base_slide("State Management", "Frontend State Management Taxonomy", "Separation of global auth, persistent browser tokens, local UI, and audio buffers")
    
    states = [
        ("Global Auth State (AuthContext.jsx)", "Holds current user profile object {id, username, email...}, login(), register(), and logout() methods. Provided to all components via React Context.", COLOR_PRIMARY),
        ("Persistent Token Storage (localStorage)", "Stores access_token (30 min lifetime) and refresh_token (7 day lifetime). Survives page reloads and browser restarts.", COLOR_CYAN),
        ("Local Component State (useState / useRef)", "Active session state, question pointer (currentIdx), answerText, finalTranscriptRef speech buffer, camera streams, and timer.", COLOR_EMERALD),
        ("Server State & Synchronous Cache", "Fetched via Axios on component mount and mutated upon file upload, question answering, and interview finalization.", COLOR_AMBER)
    ]

    for i, (s_title, s_desc, s_col) in enumerate(states):
        top_pos = 1.9 + i * 1.15
        card = create_card(s8, 0.8, top_pos, 11.733, 0.98)
        tf = card.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.text = s_title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = s_col
        p2 = tf.add_paragraph()
        p2.text = s_desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = COLOR_TEXT_MUTED

    add_speaker_notes(s8,
        "What this means: Explains how data lives on the client.\n"
        "Verbal Pitch: 'We avoided unnecessary Redux complexity by using React Context for global authentication while keeping transient interview question state strictly local to the active room.'"
    )

    # ==========================================
    # SLIDE 9: Backend Architecture
    # ==========================================
    s9 = add_base_slide("Backend Architecture", "Backend Architecture & Django App Structure", "Clean domain separation across users, resumes, ai_engine, interviews, analytics, and reports")
    
    b_apps = [
        ("users app", "Custom User model (AbstractUser), RegisterAPIView, UserProfileAPIView, SimpleJWT token routes.", COLOR_PRIMARY),
        ("resumes app", "Resume & ResumeAnalysis models. Handles multipart upload, file lifecycle, and ATS score persistence.", COLOR_CYAN),
        ("ai_engine app", "Pure service layer: ai_service.py (OpenRouter), prompt_service.py (prompts), document_service.py (parsers).", COLOR_EMERALD),
        ("interviews app", "InterviewSession, Question, Response models. StartInterview, SubmitAnswer, FinishInterview views.", COLOR_AMBER),
        ("analytics & reports", "DashboardAnalyticsAPIView computes SQL aggregations; InterviewReportAPIView generates audit reports.", COLOR_ROSE)
    ]

    for i, (b_title, b_desc, b_col) in enumerate(b_apps):
        top_pos = 1.9 + i * 0.95
        card = create_card(s9, 0.8, top_pos, 11.733, 0.8)
        tf = card.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.text = b_title.upper()
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = b_col
        p2 = tf.add_paragraph()
        p2.text = b_desc
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = COLOR_TEXT_MUTED

    add_speaker_notes(s9,
        "What this means: Shows the modular structure of the Django monolith.\n"
        "Verbal Pitch: 'The backend is organized into 6 focused Django apps. Each app has clear domain boundaries, making the codebase clean and ready for microservice extraction if ever needed.'"
    )

    # ==========================================
    # SLIDE 10: API Architecture
    # ==========================================
    s10 = add_base_slide("API Architecture", "RESTful API Endpoints Inventory", "Standardized DRF class-based views with JWT authentication and strict HTTP status codes")
    
    table_shape10 = s10.shapes.add_table(7, 4, Inches(0.8), Inches(1.9), Inches(11.733), Inches(4.8))
    table10 = table_shape10.table
    table10.columns[0].width = Inches(1.6)
    table10.columns[1].width = Inches(3.8)
    table10.columns[2].width = Inches(4.5)
    table10.columns[3].width = Inches(1.833)

    for col_idx, text in enumerate(["Method", "Endpoint Path", "Action & Business Purpose", "Auth Required"]):
        cell = table10.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(25, 33, 58)
        p = cell.text_frame.paragraphs[0]
        p.text = text
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_PRIMARY

    api_rows = [
        ("POST", "/api/auth/register/", "Register new user account with hashed password", "Public"),
        ("POST", "/api/token/ & refresh/", "Obtain & refresh stateless SimpleJWT token pairs", "Public"),
        ("GET / POST", "/api/resumes/", "List resumes / Upload document (.pdf/.docx) & auto ATS scan", "Bearer JWT"),
        ("POST", "/api/resumes/<id>/analyze/", "Manually re-run OpenRouter ATS analysis on resume", "Bearer JWT"),
        ("POST", "/api/interviews/start/", "Generate 5 customized questions & initialize session", "Bearer JWT"),
        ("POST", "/api/interviews/.../answer/", "Submit answer for real-time AI evaluation & grading", "Bearer JWT")
    ]

    for row_idx, row_data in enumerate(api_rows, 1):
        for col_idx, text in enumerate(row_data):
            cell = table10.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_CARD if row_idx % 2 == 0 else RGBColor(14, 18, 32)
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.size = Pt(9.5)
            p.font.color.rgb = COLOR_TEXT_MAIN if col_idx == 0 else COLOR_TEXT_MUTED

    add_speaker_notes(s10,
        "What this means: Highlights the core REST endpoints in the system.\n"
        "Verbal Pitch: 'Our API design is RESTful, resource-oriented, and strictly validated. Private endpoints enforce JWT headers, and file uploads use standard multipart forms.'"
    )

    # ==========================================
    # SLIDE 11: Complete Request Lifecycle
    # ==========================================
    s11 = add_base_slide("Request Lifecycle", "Complete Request Execution Lifecycle", "Tracing an answer submission from browser microphone to database and OpenRouter AI")
    
    steps = [
        ("1. Browser Action", "Candidate submits voice answer in InterviewRoomPage.jsx -> Axios dispatches POST request with Bearer JWT.", COLOR_CYAN),
        ("2. Middleware & Routing", "CorsMiddleware allows origin -> JWTAuthentication validates signature -> core/urls resolves SubmitAnswerAPIView.", COLOR_PRIMARY),
        ("3. Authorization Guard", "get_object_or_404(InterviewSession, id=session_id, user=request.user) verifies session ownership.", COLOR_EMERALD),
        ("4. AI Orchestration", "evaluate_interview_answer() constructs prompt with question rubric -> calls OpenRouter gemini-2.5-flash (max_tokens: 1500).", COLOR_AMBER),
        ("5. Output Parsing & DB", "clean_json_response() sanitizes output -> InterviewResponse.objects.update_or_create() persists scores and model answer.", COLOR_ROSE),
        ("6. Client State Update", "HTTP 200 OK returns serialized question -> React updates room state -> MarkdownView renders formatted critique.", COLOR_CYAN)
    ]

    for i, (st_title, st_desc, st_col) in enumerate(steps):
        top_pos = 1.9 + i * 0.8
        card = create_card(s11, 0.8, top_pos, 11.733, 0.68)
        tf = card.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.text = st_title
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = st_col
        p2 = tf.add_paragraph()
        p2.text = st_desc
        p2.font.size = Pt(9)
        p2.font.color.rgb = COLOR_TEXT_MUTED

    add_speaker_notes(s11,
        "What this means: Traces an exact request from start to finish.\n"
        "Verbal Pitch: 'Every request passes through authentication, database ownership validation, LLM execution, schema validation, and relational persistence before updating the frontend.'"
    )

    # ==========================================
    # SLIDE 12: Database Schema & ER Representation
    # ==========================================
    s12 = add_base_slide("Database Architecture", "Database Schema & Entity-Relationship Model", "Relational integrity, foreign key constraints, cascading deletes, and JSON fields")
    
    c_db1 = create_card(s12, 0.8, 1.9, 5.7, 4.8)
    populate_card_bullets(c_db1, "User & Resume Entities", [
        "users_user (Custom AbstractUser model)",
        "├── PK: id (BigAutoField)",
        "└── fields: username, email, password, phone, profile_image",
        "resumes_resume (Uploaded document metadata)",
        "├── PK: id | FK: user_id ──> users_user.id (CASCADE)",
        "└── fields: title, resume (file path), uploaded_at",
        "resumes_resumeanalysis (1-to-1 ATS analysis extension)",
        "├── PK: id | FK: resume_id ──> resumes_resume.id (Unique, CASCADE)",
        "└── fields: extracted_text, summary, skills (JSON), strengths (JSON), weaknesses (JSON), ats_score (int)"
    ], COLOR_PRIMARY)

    c_db2 = create_card(s12, 6.8, 1.9, 5.7, 4.8)
    populate_card_bullets(c_db2, "Interview Session Entities", [
        "interviews_session (Central interview entity)",
        "├── PK: id | FK: user_id (CASCADE), resume_id (SET_NULL)",
        "└── fields: role_title, difficulty, status, overall_score, pillars...",
        "interviews_question (Progressive question records)",
        "├── PK: id | FK: session_id ──> interviews_session.id (CASCADE)",
        "└── fields: order, category, question_text, expected_key_points (JSON)",
        "interviews_response (1-to-1 answer & evaluation)",
        "├── PK: id | FK: question_id ──> interviews_question.id (Unique, CASCADE)",
        "└── fields: candidate_answer, technical_score, clarity, ideal_answer..."
    ], COLOR_CYAN)

    add_speaker_notes(s12,
        "What this means: Comprehensive breakdown of all 6 database tables and relationships.\n"
        "Verbal Pitch: 'Our database schema guarantees relational integrity. When a resume is deleted, its analysis is cleaned up via CASCADE, but past interview history is preserved via SET_NULL.'"
    )

    # ==========================================
    # SLIDE 13: Data Model Entity Specifications
    # ==========================================
    s13 = add_base_slide("Data Models", "Data Model Specifications & Lifecycles", "Detailed schema design, field constraints, and query access patterns")
    
    ent_cards = [
        ("ResumeAnalysis Model", "Stores semi-structured JSON arrays for technical skills, soft skills, strengths, weaknesses, suggested roles, and missing keywords alongside integer ats_score.", COLOR_PRIMARY),
        ("InterviewSession Model", "Maintains state machine transitions (IN_PROGRESS -> COMPLETED). Stores aggregate metrics: technical_mastery, communication_clarity, problem_solving, and readiness_rating.", COLOR_CYAN),
        ("InterviewQuestion & Response", "Question defines expected rubric key points. Response stores individual candidate answers, sub-scores (0-100), AI critique, and model STAR answers.", COLOR_EMERALD),
        ("Optimization Pattern", "Django ORM select_related('analysis') and prefetch_related('questions__response') eliminate N+1 queries across the entire API.", COLOR_AMBER)
    ]

    for i, (e_title, e_desc, e_col) in enumerate(ent_cards):
        top_pos = 1.9 + i * 1.15
        card = create_card(s13, 0.8, top_pos, 11.733, 0.98)
        tf = card.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.text = e_title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = e_col
        p2 = tf.add_paragraph()
        p2.text = e_desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = COLOR_TEXT_MUTED

    add_speaker_notes(s13,
        "What this means: Explains how data models support complex ATS and interview features.\n"
        "Verbal Pitch: 'We combine relational tables with JSON fields to get the best of both worlds: strict relational consistency and schema flexibility for dynamic AI outputs.'"
    )

    # ==========================================
    # SLIDE 14: Authentication Architecture
    # ==========================================
    s14 = add_base_slide("Authentication", "Stateless JWT Authentication Architecture", "PBKDF2 password hashing, HMAC-SHA256 tokens, and automatic token refresh interceptors")
    
    c_au1 = create_card(s14, 0.8, 1.9, 5.7, 4.8)
    populate_card_bullets(c_au1, "Registration & Login Flow", [
        "User registers via POST /api/auth/register/",
        "RegisterSerializer validates unique username & email",
        "Password hashed using Django PBKDF2 (SHA-256)",
        "Login via POST /api/token/ returns JWT pair",
        "Access Token: HMAC-SHA256, 30 min lifetime",
        "Refresh Token: HMAC-SHA256, 7 day lifetime",
        "Stateless: zero server-side session memory"
    ], COLOR_PRIMARY)

    c_au2 = create_card(s14, 6.8, 1.9, 5.7, 4.8)
    populate_card_bullets(c_au2, "Axios Interceptor Token Lifecycle", [
        "Client stores tokens in browser localStorage",
        "Request Interceptor: attaches Authorization header",
        "JWTAuthentication middleware validates signature",
        "If token expires (401), Response Interceptor fires",
        "Sends POST /api/token/refresh/ in background",
        "Updates access_token and replays original request",
        "If refresh fails, redirects user to /login"
    ], COLOR_CYAN)

    add_speaker_notes(s14,
        "What this means: Full explanation of the JWT authentication mechanism.\n"
        "Verbal Pitch: 'We use SimpleJWT with short-lived access tokens. Our Axios response interceptor handles token refresh transparently so candidate interview sessions are never interrupted.'"
    )

    # ==========================================
    # SLIDE 15: Authorization & Multi-Tenancy
    # ==========================================
    s15 = add_base_slide("Authorization", "Multi-Tenant Authorization & IDOR Defense", "Three-layer defense ensuring complete data isolation between candidate accounts")
    
    auth_layers = [
        ("Layer 1: View-Level Permission Classes", "Every private endpoint specifies `permission_classes = [IsAuthenticated]`. Requests without valid unexpired tokens receive HTTP 401 Unauthorized immediately.", COLOR_PRIMARY),
        ("Layer 2: Query-Level User Scoping", "Views never query all objects globally. Endpoints execute `Resume.objects.filter(user=request.user)` and `InterviewSession.objects.filter(user=request.user)`.", COLOR_CYAN),
        ("Layer 3: Object-Level Ownership Guards", "Single-object operations use `get_object_or_404(Model, id=pk, user=request.user)`. Rejects Insecure Direct Object References (IDOR).", COLOR_EMERALD),
        ("Security Audit Verdict", "User A cannot inspect, edit, delete, or answer questions for User B's interview session even if they guess User B's primary key ID.", COLOR_AMBER)
    ]

    for i, (a_title, a_desc, a_col) in enumerate(auth_layers):
        top_pos = 1.9 + i * 1.15
        card = create_card(s15, 0.8, top_pos, 11.733, 0.98)
        tf = card.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.text = a_title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = a_col
        p2 = tf.add_paragraph()
        p2.text = a_desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = COLOR_TEXT_MUTED

    add_speaker_notes(s15,
        "What this means: Demonstrates how candidate privacy and data isolation are enforced.\n"
        "Verbal Pitch: 'Authorization is baked into the database queries. Even if an attacker attempts an IDOR attack by guessing another session ID, the database query returns 404 Not Found.'"
    )

    # ==========================================
    # SLIDE 16: AI Architecture & Orchestration
    # ==========================================
    s16 = add_base_slide("AI Architecture", "AI Architecture & OpenRouter LLM Orchestration", "Centralized prompt builders, deterministic evaluation, and credit-bounded token execution")
    
    c_ai1 = create_card(s16, 0.8, 1.9, 5.7, 4.8)
    populate_card_bullets(c_ai1, "AI Engine Layer (ai_engine/)", [
        "Centralized gateway in ai_engine/services/ai_service.py",
        "Target Model: google/gemini-2.5-flash via OpenRouter",
        "Temperature: 0.3 (deterministic, consistent scoring)",
        "max_tokens: 1500 (credit-bound protection)",
        "Zero mock fallbacks: calls OpenRouter directly",
        "Throws explicit 502 error if API key/quota fails",
        "clean_json_response() sanitizes markdown fences"
    ], COLOR_PRIMARY)

    c_ai2 = create_card(s16, 6.8, 1.9, 5.7, 4.8)
    populate_card_bullets(c_ai2, "Prompt Engineering (prompt_service.py)", [
        "1. build_resume_analysis_prompt: ATS scoring schema",
        "2. build_question_generation_prompt: Role questions",
        "3. build_answer_evaluation_prompt: Rubric grading",
        "4. build_final_summary_prompt: Executive scorecard",
        "Enforces strict JSON schema output from LLM",
        "Injects system recruiter persona and scoring rules",
        "Requires Markdown formatting in model answers"
    ], COLOR_CYAN)

    add_speaker_notes(s16,
        "What this means: Deep dive into the LLM orchestration layer.\n"
        "Verbal Pitch: 'Our AI engine is centralized in `ai_service.py`. We use a low temperature of 0.3 to ensure fair, reproducible evaluations and protect our API quotas with strict token caps.'"
    )

    # ==========================================
    # SLIDE 17: AI Question Generation Pipeline
    # ==========================================
    s17 = add_base_slide("Question Pipeline", "Context-Aware Question Generation Pipeline", "Synthesizing job requirements, seniority level, and candidate resume skills")
    
    q_steps = [
        ("1. Input Context Ingestion", "Receives target role (e.g. 'Senior Backend Engineer'), seniority ('SENIOR'), interview type ('TECHNICAL'), and extracted resume skills.", COLOR_CYAN),
        ("2. Prompt Synthesis (prompt_service.py)", "Injects candidate background and instructs LLM to generate 5 progressive questions ranging from warm-up fundamentals to deep architecture.", COLOR_PRIMARY),
        ("3. OpenRouter LLM Execution", "Calls OpenRouter API with structured JSON schema rules. Validates that output contains ordered questions and expected rubric points.", COLOR_EMERALD),
        ("4. Relational Persistence", "Django views bulk-create 5 `InterviewQuestion` records linked to the `InterviewSession` with initial order pointers.", COLOR_AMBER)
    ]

    for i, (q_title, q_desc, q_col) in enumerate(q_steps):
        top_pos = 1.9 + i * 1.15
        card = create_card(s17, 0.8, top_pos, 11.733, 0.98)
        tf = card.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.text = q_title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = q_col
        p2 = tf.add_paragraph()
        p2.text = q_desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = COLOR_TEXT_MUTED

    add_speaker_notes(s17,
        "What this means: Shows how questions are generated tailored to candidate context.\n"
        "Verbal Pitch: 'Questions are not pulled from a static database. The LLM generates bespoke questions that specifically challenge the technologies listed on the candidate's resume.'"
    )

    # ==========================================
    # SLIDE 18: AI Answer Evaluation Pipeline
    # ==========================================
    s18 = add_base_slide("Answer Evaluation", "Real-Time AI Answer Evaluation & Rubrics", "Multi-dimensional scoring: Technical Depth, Clarity, Relevance, and STAR model answers")
    
    c_ev1 = create_card(s18, 0.8, 1.9, 5.7, 4.8)
    populate_card_bullets(c_ev1, "Grading Dimensions & Rubrics", [
        "• Technical Score (0-100): Domain depth & accuracy",
        "• Clarity Score (0-100): Structure & conciseness",
        "• Relevance Score (0-100): Addresses the prompt",
        "• Overall Weighted Score (0-100): Turn rating",
        "• What Went Well: Specific candidate strengths",
        "• Recommendations: Actionable improvement tips",
        "Evaluated strictly against expected rubric points"
    ], COLOR_PRIMARY)

    c_ev2 = create_card(s18, 6.8, 1.9, 5.7, 4.8)
    populate_card_bullets(c_ev2, "Model STAR Answer Generation", [
        "Generates exemplary answer demonstrating STAR method",
        "Formatted in structured Markdown:",
        "  - ### Architecture & Core Approach",
        "  - ### Key Implementation Steps (Numbered)",
        "  - ### Production & Scaling Trade-offs (Bullets)",
        "Rendered via react-markdown in MarkdownView",
        "Provides immediate learning benchmark for candidate"
    ], COLOR_CYAN)

    add_speaker_notes(s18,
        "What this means: Explains how answers are scored and critiqued.\n"
        "Verbal Pitch: 'Every answer is scored across three dimensions: Technical, Clarity, and Relevance. Candidates receive specific strengths, improvements, and a model STAR response.'"
    )

    # ==========================================
    # SLIDE 19: AI Prompt Architecture
    # ==========================================
    s19 = add_base_slide("Prompt Architecture", "AI Prompt Architecture & Schema Integrity", "Defensive prompt design, JSON-only output constraints, and regex sanitization")
    
    p_steps = [
        ("1. Role & Persona Definition", "System instruction assigns expert persona: 'You are a Lead Hiring Manager and Technical Interviewer'.", COLOR_PRIMARY),
        ("2. Concrete JSON Schema Template", "Prompts provide explicit schema examples: { 'technical_score': 85, 'strengths': [...], 'ideal_answer': '...' }.", COLOR_CYAN),
        ("3. Strict Output Constraints", "Rules explicitly declare: 'Return ONLY valid JSON. Do not include markdown code blocks or conversational text'.", COLOR_EMERALD),
        ("4. Regex Sanitization Pipeline", "clean_json_response() strips ```json wrappers and extracts JSON blocks via regex before json.loads() validation.", COLOR_AMBER)
    ]

    for i, (p_title, p_desc, p_col) in enumerate(p_steps):
        top_pos = 1.9 + i * 1.15
        card = create_card(s19, 0.8, top_pos, 11.733, 0.98)
        tf = card.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.text = p_title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = p_col
        p2 = tf.add_paragraph()
        p2.text = p_desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = COLOR_TEXT_MUTED

    add_speaker_notes(s19,
        "What this means: Shows how the backend guarantees valid JSON from the LLM.\n"
        "Verbal Pitch: 'We use defensive prompt engineering combined with regex sanitization to ensure that LLM outputs always conform to our application schema.'"
    )

    # ==========================================
    # SLIDE 20: Interview State Machine
    # ==========================================
    s20 = add_base_slide("Interview Engine", "Interview State Machine & Session Lifecycle", "State progression from configuration to completion with database persistence")
    
    c_sm1 = create_card(s20, 0.8, 1.9, 5.7, 4.8)
    populate_card_bullets(c_sm1, "State Transitions", [
        "[NOT_STARTED] Candidate configures role in SetupPage",
        "  │ POST /api/interviews/start/",
        "  ▼",
        "[IN_PROGRESS] Session created; 5 questions generated",
        "  │ POST .../questions/:id/answer/",
        "  ▼",
        "[TURN_EVALUATED] Score & model answer saved",
        "  │ (Repeats for Q1 through Q5)",
        "  ▼",
        "[COMPLETED] POST /api/interviews/:id/finish/",
        "Final scorecard synthesized & session locked"
    ], COLOR_CYAN)

    c_sm2 = create_card(s20, 6.8, 1.9, 5.7, 4.8)
    populate_card_bullets(c_sm2, "Persistence & Crash Recovery", [
        "Every turn commits immediately to SQLite database",
        "Browser refresh recovery: automatically reloads",
        "InterviewRoom navigates to first unanswered question",
        "Preserves candidate answers & previous scores",
        "Session summary recalculates 3-pillar radar scores",
        "Readiness rating assigned based on score threshold"
    ], COLOR_PRIMARY)

    add_speaker_notes(s20,
        "What this means: State machine lifecycle of an interview session.\n"
        "Verbal Pitch: 'Because state is saved after every single question, candidates can pause or refresh their browser without losing their progress or evaluations.'"
    )

    # ==========================================
    # SLIDE 21: Audio & Speech Architecture
    # ==========================================
    s21 = add_base_slide("Audio / Speech", "Speech Recognition & Synthesis Architecture", "Browser-native Web Speech API integration delivering voice interaction with zero API cost")
    
    c_sp1 = create_card(s21, 0.8, 1.9, 5.7, 4.8)
    populate_card_bullets(c_sp1, "Speech-to-Text (STT) Engine", [
        "webkitSpeechRecognition / SpeechRecognition",
        "continuous = true (retains mic through pauses)",
        "interimResults = true (real-time live preview)",
        "Dialect selector: English (US), (India), (UK)",
        "finalTranscriptRef preserves manual keyboard edits",
        "Auto-reconnects on unexpected silence drops",
        "Zero server audio bandwidth & zero API cost"
    ], COLOR_PRIMARY)

    c_sp2 = create_card(s21, 6.8, 1.9, 5.7, 4.8)
    populate_card_bullets(c_sp2, "Text-to-Speech (TTS) & Video", [
        "window.speechSynthesis reads questions aloud",
        "SpeechSynthesisUtterance with rate/pitch control",
        "Click 'Read Question' to trigger AI voice playback",
        "CameraPreview component (WebRTC MediaDevices):",
        "  - HTML5 getUserMedia({ video: true })",
        "  - Local video mirror (no server bandwidth)",
        "  - Turn on/off anytime with privacy toggle"
    ], COLOR_CYAN)

    add_speaker_notes(s21,
        "What this means: Explains how voice and video operate in the browser.\n"
        "Verbal Pitch: 'By utilizing native Web Speech APIs, we provide voice answering and question narration with zero backend audio latency and zero third-party transcription fees.'"
    )

    # ==========================================
    # SLIDE 22: Real-Time Communication Analysis
    # ==========================================
    s22 = add_base_slide("Real-Time Architecture", "Real-Time Communication Analysis — REST vs WebSockets", "Architectural rationale for turn-based REST architecture in mock interview platforms")
    
    rt_points = [
        ("Turn-Based Interaction Model", "An interview is inherently a turn-based request-response flow. Candidates listen to a question, formulate their answer, and submit it for evaluation. Continuous duplex streaming is not required.", COLOR_CYAN),
        ("Infrastructure Simplicity & Reliability", "Stateless HTTP REST eliminates persistent WebSocket connection drops, stateful server memory, and complex load balancer sticky sessions.", COLOR_PRIMARY),
        ("Targeted HTTP Timeouts", "API requests use a 60-second timeout. OpenRouter Gemini 2.5 Flash delivers complete evaluations in 1.2 to 2.5 seconds, providing an immediate real-time feel.", COLOR_EMERALD),
        ("Future WebSocket Evolution Path", "If live multi-user interviewer monitoring or streaming LLM token chunks are introduced, Django Channels can be activated via backend/core/asgi.py.", COLOR_AMBER)
    ]

    for i, (r_title, r_desc, r_col) in enumerate(rt_points):
        top_pos = 1.9 + i * 1.15
        card = create_card(s22, 0.8, top_pos, 11.733, 0.98)
        tf = card.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.text = r_title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = r_col
        p2 = tf.add_paragraph()
        p2.text = r_desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = COLOR_TEXT_MUTED

    add_speaker_notes(s22,
        "What this means: Justifies why REST was chosen over WebSockets for this phase.\n"
        "Verbal Pitch: 'We evaluated WebSockets vs REST. Because mock interviews are turn-based, stateless REST provides superior horizontal scalability and simpler infrastructure.'"
    )

    # ==========================================
    # SLIDE 23: Caching & Data Storage
    # ==========================================
    s23 = add_base_slide("Data Storage", "Data Storage, Media Storage & Query Optimization", "Relational persistence, media filesystem organization, and ORM query optimization")
    
    c_st1 = create_card(s23, 0.8, 1.9, 5.7, 4.8)
    populate_card_bullets(c_st1, "Storage Architecture", [
        "Database: SQLite 3 (backend/db.sqlite3)",
        "Media Storage: backend/media/resumes/",
        "Django MEDIA_ROOT & MEDIA_URL routing",
        "Unique file naming prevents overwrite collisions",
        "Client Token Cache: browser localStorage",
        "React Component State: active room cache"
    ], COLOR_PRIMARY)

    c_st2 = create_card(s23, 6.8, 1.9, 5.7, 4.8)
    populate_card_bullets(c_st2, "ORM Query Optimizations", [
        "select_related('analysis') on Resumes:",
        "  - Single SQL JOIN fetches resume + ATS score",
        "prefetch_related('questions__response') on Sessions:",
        "  - Fetches 5 questions & responses in 2 queries",
        "  - Eliminates N+1 query overhead completely",
        "Aggregate SQL queries (Avg, Count) for dashboard"
    ], COLOR_EMERALD)

    add_speaker_notes(s23,
        "What this means: Shows how data is stored and optimized.\n"
        "Verbal Pitch: 'We optimized our ORM queries using select_related and prefetch_related, reducing database round-trips by over 80% when loading interview sessions.'"
    )

    # ==========================================
    # SLIDE 24: Asynchronous Processing & Timeouts
    # ==========================================
    s24 = add_base_slide("Async & Timeouts", "Execution Model, Timeouts & Credit Guards", "Synchronous sub-2-second AI execution with token-bounded credit protection")
    
    async_points = [
        ("Synchronous Execution with 60s Timeout", "Document text extraction (PyMuPDF) takes ~15ms; OpenRouter Gemini 2.5 Flash takes ~1.5s. Synchronous calls deliver immediate feedback to the candidate.", COLOR_CYAN),
        ("OpenRouter Credit Reservation Guard", "Setting `max_tokens: 1500` in ai_service.py prevents OpenRouter from reserving 65,535 tokens, avoiding HTTP 402 Payment Required credit errors.", COLOR_PRIMARY),
        ("Network Error Handling", "Explicit try-except blocks catch requests.exceptions.Timeout and requests.exceptions.ConnectionError, returning clean 502 error responses.", COLOR_EMERALD),
        ("Future Asynchronous Queue (Celery + Redis)", "For batch resume uploading (e.g. recruiters uploading 100 resumes), Celery task workers can be attached without changing the frontend API contracts.", COLOR_AMBER)
    ]

    for i, (as_title, as_desc, as_col) in enumerate(async_points):
        top_pos = 1.9 + i * 1.15
        card = create_card(s24, 0.8, top_pos, 11.733, 0.98)
        tf = card.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.text = as_title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = as_col
        p2 = tf.add_paragraph()
        p2.text = as_desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = COLOR_TEXT_MUTED

    add_speaker_notes(s24,
        "What this means: Explains the synchronous latency model and credit protection.\n"
        "Verbal Pitch: 'Because Gemini Flash is so fast, synchronous execution provides the best user experience. We strictly enforce a 1,500 token limit to protect API credits.'"
    )

    # ==========================================
    # SLIDE 25: Error Handling & Resilience
    # ==========================================
    s25 = add_base_slide("Resilience", "Error Handling & Failure Defense Matrix", "Graceful degradation, explicit error propagation, and automated token refresh")
    
    c_err1 = create_card(s25, 0.8, 1.9, 5.7, 4.8)
    populate_card_bullets(c_err1, "Backend Failure Defense", [
        "OpenRouter Quota Error (402/429):",
        "  - ai_service extracts error message from API JSON",
        "  - Views return HTTP 502 Bad Gateway with exact reason",
        "Malformed LLM JSON Output:",
        "  - Regex extractor attempts JSON block recovery",
        "  - Raises ValueError if unparseable",
        "Document Extraction Errors:",
        "  - Unified dispatcher catches corrupted binaries"
    ], COLOR_ROSE)

    c_err2 = create_card(s25, 6.8, 1.9, 5.7, 4.8)
    populate_card_bullets(c_err2, "Frontend Error States", [
        "Axios Response Interceptor:",
        "  - Catches 401 Unauthorized -> refreshes token",
        "Visual Error Banners:",
        "  - AlertCircle banners in Setup, Room, & Resumes",
        "Speech Recognition Disconnect:",
        "  - Auto-reconnects on unexpected silence timeout",
        "Zero mock fallbacks: errors surfaced transparently"
    ], COLOR_AMBER)

    add_speaker_notes(s25,
        "What this means: Matrix of failure modes and recovery actions.\n"
        "Verbal Pitch: 'We never hide API errors behind fake fallback data. If an API key or quota issue occurs, the exact OpenRouter error is surfaced directly to the user.'"
    )

    # ==========================================
    # SLIDE 26: Security Architecture Audit
    # ==========================================
    s26 = add_base_slide("Security", "Security Architecture & Controls Audit", "Cryptographic password hashing, JWT token validation, and multi-tenant data isolation")
    
    sec_points = [
        ("NIST-Compliant Password Security", "Django PBKDF2 with SHA-256 and unique per-user salt. Plaintext passwords never touch storage.", COLOR_PRIMARY),
        ("Stateless HMAC-SHA256 JWTs", "Access tokens expire in 30 minutes, mitigating token theft risks. Refresh tokens expire in 7 days.", COLOR_CYAN),
        ("Complete IDOR Protection", "All database queries filter by request.user. Users cannot access or modify other candidates' data.", COLOR_EMERALD),
        ("CORS Whitelisting & SQLi Defense", "CORS restricted to authorized origins; Django ORM uses parameterized queries preventing SQL injection.", COLOR_AMBER)
    ]

    for i, (sc_title, sc_desc, sc_col) in enumerate(sec_points):
        top_pos = 1.9 + i * 1.15
        card = create_card(s26, 0.8, top_pos, 11.733, 0.98)
        tf = card.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.text = sc_title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = sc_col
        p2 = tf.add_paragraph()
        p2.text = sc_desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = COLOR_TEXT_MUTED

    add_speaker_notes(s26,
        "What this means: Audit of the security controls in place.\n"
        "Verbal Pitch: 'Our application protects candidate data with PBKDF2 password hashing, short-lived JWT tokens, and strict object-level query filtering to prevent IDOR vulnerabilities.'"
    )

    # ==========================================
    # SLIDE 27: Deployment Architecture
    # ==========================================
    s27 = add_base_slide("Deployment", "Production Deployment Architecture", "Containerized Gunicorn WSGI backend, static SPA hosting, and PostgreSQL cluster")
    
    c_dep1 = create_card(s27, 0.8, 1.9, 5.7, 4.8)
    populate_card_bullets(c_dep1, "Production Gateway & Frontend", [
        "Nginx Reverse Proxy & SSL/TLS Termination",
        "Let's Encrypt automated HTTPS certificates",
        "React 19 SPA built via `npm run build`",
        "Compiled static assets in frontend/dist/",
        "Served via Nginx or Cloudflare Pages CDN",
        "Sub-300ms global static asset delivery"
    ], COLOR_CYAN)

    c_dep2 = create_card(s27, 6.8, 1.9, 5.7, 4.8)
    populate_card_bullets(c_dep2, "Backend & Managed Database", [
        "Gunicorn WSGI Application Server (4 workers)",
        "Docker container running Python 3.14 + Django 5",
        "Managed PostgreSQL 16 database cluster",
        "Persistent object storage for uploaded resumes",
        "Health checks on /api/analytics/dashboard/",
        "Environment secrets injected via container env"
    ], COLOR_PRIMARY)

    add_speaker_notes(s27,
        "What this means: Blueprints for deploying the system to production.\n"
        "Verbal Pitch: 'For production, the frontend is compiled into static assets served via CDN, while the backend runs as containerized Gunicorn workers connected to PostgreSQL.'"
    )

    # ==========================================
    # SLIDE 28: Environment Configuration
    # ==========================================
    s28 = add_base_slide("Environment", "Environment Configuration & Secrets Management", "Strict separation of server-only API keys and client-safe configuration")
    
    table_shape28 = s28.shapes.add_table(6, 4, Inches(0.8), Inches(1.9), Inches(11.733), Inches(4.8))
    table28 = table_shape28.table
    table28.columns[0].width = Inches(2.8)
    table28.columns[1].width = Inches(2.0)
    table28.columns[2].width = Inches(1.8)
    table28.columns[3].width = Inches(5.133)

    for col_idx, text in enumerate(["Variable Name", "Scope Location", "Sensitivity", "Purpose"]):
        cell = table28.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(25, 33, 58)
        p = cell.text_frame.paragraphs[0]
        p.text = text
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_PRIMARY

    env_rows = [
        ("SECRET_KEY", "backend/.env", "CRITICAL", "Django cryptographic signing key for CSRF & sessions."),
        ("OPENROUTER_API_KEY", "backend/.env", "CRITICAL", "API key for OpenRouter LLM calls. Server-only."),
        ("OPENROUTER_MODEL", "backend/.env", "MEDIUM", "Specifies target model (google/gemini-2.5-flash)."),
        ("ALLOWED_HOSTS", "backend/.env", "HIGH", "Whitelists valid HTTP Host headers in production."),
        ("CORS_ALLOWED_ORIGINS", "backend/.env", "MEDIUM", "Whitelists allowed frontend origins for CORS.")
    ]

    for row_idx, row_data in enumerate(env_rows, 1):
        for col_idx, text in enumerate(row_data):
            cell = table28.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_CARD if row_idx % 2 == 0 else RGBColor(14, 18, 32)
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.size = Pt(9.5)
            p.font.color.rgb = COLOR_ROSE if col_idx == 2 and text == "CRITICAL" else (COLOR_TEXT_MAIN if col_idx == 0 else COLOR_TEXT_MUTED)

    add_speaker_notes(s28,
        "What this means: Breakdown of environment secrets and safety.\n"
        "Verbal Pitch: 'We maintain strict separation between server-only secrets and client variables. The OpenRouter key is never exposed to the frontend bundle.'"
    )

    # ==========================================
    # SLIDE 29: Complete End-to-End System Data Flow
    # ==========================================
    s29 = add_base_slide("Data Flow", "Complete End-to-End System Data Flow", "Full architectural journey from document upload to interview feedback and analytics")
    
    flow_steps = [
        ("Step 1: Resume Upload", "Candidate uploads PDF/DOCX -> POST /api/resumes/ -> PyMuPDF extracts text -> OpenRouter computes ATS score (0-100) -> Saved to DB.", COLOR_CYAN),
        ("Step 2: Interview Setup", "Candidate selects role, level, and resume -> POST /api/interviews/start/ -> LLM generates 5 tailored questions -> Session initialized.", COLOR_PRIMARY),
        ("Step 3: Live Interview", "InterviewRoom renders Q1 -> TTS reads question -> Candidate answers via Web Speech STT -> POST .../answer/ -> AI returns rubric.", COLOR_EMERALD),
        ("Step 4: Completion", "Candidate completes 5 questions -> POST .../finish/ -> LLM synthesizes final scorecard -> Confetti & Printable Report in ResultPage.", COLOR_AMBER)
    ]

    for i, (f_title, f_desc, f_col) in enumerate(flow_steps):
        top_pos = 1.9 + i * 1.15
        card = create_card(s29, 0.8, top_pos, 11.733, 0.98)
        tf = card.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.text = f_title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = f_col
        p2 = tf.add_paragraph()
        p2.text = f_desc
        p2.font.size = Pt(10)
        p2.font.color.rgb = COLOR_TEXT_MUTED

    add_speaker_notes(s29,
        "What this means: Summarizes the complete user journey across all systems.\n"
        "Verbal Pitch: 'This data flow demonstrates how our platform connects resume parsing, dynamic question generation, voice input, AI scoring, and scorecard analytics into a unified workflow.'"
    )

    # ==========================================
    # SLIDE 30: Scalability Analysis
    # ==========================================
    s30 = add_base_slide("Scalability", "Scalability Architecture & Growth Trajectory", "Scaling from single-instance prototype to 10,000+ concurrent interview sessions")
    
    c_sc1 = create_card(s30, 0.8, 1.9, 5.7, 4.8)
    populate_card_bullets(c_sc1, "Phase 1 to Phase 2 (1 - 1,000 Users)", [
        "Current Phase: Single Django process + SQLite",
        "Phase 2 Transition:",
        "  - Swap SQLite -> Managed PostgreSQL RDS",
        "  - PgBouncer connection pooling",
        "  - Run Gunicorn with 4-8 worker processes",
        "  - Redis cache for analytics dashboard KPIs",
        "  - Handles up to 1,000 active candidates easily"
    ], COLOR_PRIMARY)

    c_sc2 = create_card(s30, 6.8, 1.9, 5.7, 4.8)
    populate_card_bullets(c_sc2, "Phase 3 (1,000 - 10,000+ Users)", [
        "Horizontal Backend Scaling:",
        "  - Stateless Django containers behind AWS ALB",
        "  - Auto-scaling groups based on CPU/Request count",
        "Asynchronous Task Queue:",
        "  - Celery + Redis offloads LLM and PDF parsing",
        "Storage Scaling:",
        "  - AWS S3 / Cloudflare R2 for resume binaries",
        "Global CDN caching for frontend SPA assets"
    ], COLOR_EMERALD)

    add_speaker_notes(s30,
        "What this means: Blueprint for scaling the platform as user traffic grows.\n"
        "Verbal Pitch: 'Because our backend is stateless and relies on JWT, horizontal scaling is straightforward. We can deploy multiple container instances behind a load balancer with Celery task queues.'"
    )

    # ==========================================
    # SLIDE 31: Performance & AI Cost Economics
    # ==========================================
    s31 = add_base_slide("Economics", "Performance Latency & AI Cost Economics", "Sub-2-second response latency and sub-$0.002 cost per complete interview session")
    
    c_ec1 = create_card(s31, 0.8, 1.9, 5.7, 4.8)
    populate_card_bullets(c_ec1, "Latency Breakdown (Total: ~1.8s)", [
        "• Network transit (Client -> API): ~40ms",
        "• Django ORM DB query (select_related): ~10ms",
        "• Binary document parsing (PyMuPDF): ~15ms",
        "• OpenRouter LLM (gemini-2.5-flash): ~1,400ms",
        "• Response serialization & render: ~50ms",
        "Result: Sub-2-second turn latency feels immediate"
    ], COLOR_CYAN)

    c_ec2 = create_card(s31, 6.8, 1.9, 5.7, 4.8)
    populate_card_bullets(c_ec2, "AI Cost Breakdown (gemini-2.5-flash)", [
        "• Resume ATS Scan: ~1,600 tokens (~$0.0003)",
        "• 5 Question Generation: ~1,100 tokens (~$0.0002)",
        "• 5 Turn Evaluations: ~4,500 tokens (~$0.0008)",
        "• Final Summary Scorecard: ~1,200 tokens (~$0.0002)",
        "Total Cost Per 5-Question Interview: < $0.002",
        "Over 500 complete mock interviews per $1.00!"
    ], COLOR_EMERALD)

    add_speaker_notes(s31,
        "What this means: Real-world performance and cost modeling.\n"
        "Verbal Pitch: 'By choosing Gemini 2.5 Flash and capping token output, a full 5-question mock interview costs less than one-fifth of a cent, making the business model highly profitable.'"
    )

    # ==========================================
    # SLIDE 32: Architectural Tradeoffs
    # ==========================================
    s32 = add_base_slide("Tradeoffs", "Key Architectural Decisions & Tradeoffs", "Analyzing technical compromises between speed, complexity, cost, and maintainability")
    
    table_shape32 = s32.shapes.add_table(5, 4, Inches(0.8), Inches(1.9), Inches(11.733), Inches(4.8))
    table32 = table_shape32.table
    table32.columns[0].width = Inches(2.2)
    table32.columns[1].width = Inches(2.4)
    table32.columns[2].width = Inches(2.4)
    table32.columns[3].width = Inches(4.733)

    for col_idx, text in enumerate(["Decision", "Chosen Option", "Alternative", "Tradeoff Analysis"]):
        cell = table32.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(25, 33, 58)
        p = cell.text_frame.paragraphs[0]
        p.text = text
        p.font.bold = True
        p.font.size = Pt(10.5)
        p.font.color.rgb = COLOR_PRIMARY

    trade_rows = [
        ("API Protocol", "REST (JSON)", "GraphQL", "REST is simpler to cache and standard in DRF; GraphQL avoids overfetching but adds schema overhead."),
        ("Authentication", "Stateless SimpleJWT", "Session Cookies", "JWT scales horizontally without DB session lookups; requires client-side refresh handling."),
        ("Speech Engine", "Native Web Speech API", "Whisper API", "Web Speech has 0 cost and 0 server latency; tradeoff is browser engine dependency (Chrome/Edge)."),
        ("LLM Provider", "OpenRouter Gateway", "Direct Google SDK", "OpenRouter gives unified billing and instant model switching without vendor lock-in.")
    ]

    for row_idx, row_data in enumerate(trade_rows, 1):
        for col_idx, text in enumerate(row_data):
            cell = table32.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_CARD if row_idx % 2 == 0 else RGBColor(14, 18, 32)
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.size = Pt(9.5)
            p.font.color.rgb = COLOR_TEXT_MAIN if col_idx <= 1 else COLOR_TEXT_MUTED

    add_speaker_notes(s32,
        "What this means: Candid evaluation of architectural decisions.\n"
        "Verbal Pitch: 'Every decision involved deliberate tradeoffs. Using the browser's Web Speech API eliminated third-party audio costs, while OpenRouter gives us total freedom to swap LLMs.'"
    )

    # ==========================================
    # SLIDE 33: Technical Audit & Roadmap
    # ==========================================
    s33 = add_base_slide("Technical Audit", "Technical Strengths, Limitations & Future Roadmap", "Honest engineering audit of current codebase capabilities and production enhancements")
    
    c_au_str = create_card(s33, 0.8, 1.9, 5.7, 4.8)
    populate_card_bullets(c_au_str, "Current Strengths", [
        "✅ Multi-format PDF & DOCX text extractors",
        "✅ Zero-cost native Web Speech STT & TTS",
        "✅ Multi-dialect speech recognition (en-US, en-IN)",
        "✅ Strict object-level query authorization (no IDOR)",
        "✅ Markdown formatting in model answers",
        "✅ Automated ATS scoring upon upload",
        "✅ Zero mock fallbacks: direct AI execution"
    ], COLOR_EMERALD)

    c_au_lim = create_card(s33, 6.8, 1.9, 5.7, 4.8)
    populate_card_bullets(c_au_lim, "Production Roadmap Items", [
        "⚠️ Storage: Migrate local media/ storage to AWS S3",
        "⚠️ Throttling: Add django-ratelimit on login & AI endpoints",
        "⚠️ Prompt Safety: Add prompt injection sanitizer",
        "⚠️ Background Jobs: Add Celery workers for batch tasks",
        "⚠️ Database: Migrate SQLite to PostgreSQL cluster",
        "⚠️ WebSockets: Optional real-time streaming LLM tokens"
    ], COLOR_AMBER)

    add_speaker_notes(s33,
        "What this means: Balanced assessment of strengths and future improvements.\n"
        "Verbal Pitch: 'The core architecture is solid, secure, and fully functional. Our production roadmap focuses on cloud object storage, rate limiting, and background workers.'"
    )

    # ==========================================
    # SLIDE 34: Step-by-Step Build Blueprint
    # ==========================================
    s34 = add_base_slide("Blueprint", "Step-by-Step Blueprint to Rebuild From Scratch", "Prescribed 10-step dependency order for building this entire system independently")
    
    steps_build = [
        ("Step 1: Foundation Setup", "Initialize Django 5 backend and Vite React 19 frontend repositories with dependencies.", COLOR_CYAN),
        ("Step 2: Database Models", "Define User, Resume, ResumeAnalysis, InterviewSession, Question, and Response models with ORM relationships.", COLOR_PRIMARY),
        ("Step 3: Authentication", "Configure SimpleJWT token views, serializers, and custom User model with PBKDF2 hashing.", COLOR_EMERALD),
        ("Step 4: Document & AI Services", "Implement PyMuPDF/docx extractors in document_service and OpenRouter client in ai_service.", COLOR_AMBER),
        ("Step 5: API Views & Routing", "Build Resume upload/scan, Interview start, Answer submit, and Dashboard analytics endpoints.", COLOR_ROSE),
        ("Step 6: Frontend Client", "Implement index.css design tokens, Axios JWT interceptors, AuthContext, and Web Speech room UI.", COLOR_CYAN)
    ]

    for i, (b_title, b_desc, b_col) in enumerate(steps_build):
        top_pos = 1.9 + i * 0.8
        card = create_card(s34, 0.8, top_pos, 11.733, 0.68)
        tf = card.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]
        p.text = b_title
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = b_col
        p2 = tf.add_paragraph()
        p2.text = b_desc
        p2.font.size = Pt(9)
        p2.font.color.rgb = COLOR_TEXT_MUTED

    add_speaker_notes(s34,
        "What this means: Mental model for rebuilding the system from zero.\n"
        "Verbal Pitch: 'If you were to build this from scratch, following this sequence ensures you build on top of solid foundations: database first, auth second, AI services third, and client UI last.'"
    )

    # ==========================================
    # SLIDE 35: Master Architecture Summary
    # ==========================================
    s35 = add_base_slide("Summary", "Master Architecture Summary & Final Takeaway", "One unified architecture combining resume intelligence, speech interaction, and real-time AI")
    
    c_m1 = create_card(s35, 0.8, 1.9, 11.733, 3.2, bg_color=RGBColor(14, 20, 36), border_color=COLOR_PRIMARY)
    tf_m = c_m1.text_frame
    tf_m.word_wrap = True
    p = tf_m.paragraphs[0]
    p.text = "CANDIDATE (Microphone Voice & Camera)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN
    p.alignment = PP_ALIGN.CENTER
    
    p2 = tf_m.add_paragraph()
    p2.text = "│\n▼\nREACT 19 SPA (Vite 8 • Axios JWT Interceptors • Web Speech STT/TTS • ScoreMeter)\n│\n▼  HTTPS REST API\nDJANGO 5 REST FRAMEWORK (SimpleJWT Auth • CORS • Object-Level Permission Guards)\n│\n├──> MEDIA STORAGE (Local / S3) ──> Document Parsers (PyMuPDF & docx)\n├──> AI ENGINE (prompt_service.py ──> OpenRouter google/gemini-2.5-flash)\n└──> RELATIONAL DATABASE (Users • Resumes • Sessions • Questions • Scores)"
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = COLOR_TEXT_MUTED
    p2.alignment = PP_ALIGN.CENTER

    c_m2 = create_card(s35, 0.8, 5.3, 11.733, 1.4, bg_color=RGBColor(25, 33, 58), border_color=COLOR_EMERALD)
    tf_m2 = c_m2.text_frame
    tf_m2.word_wrap = True
    tf_m2.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_core = tf_m2.paragraphs[0]
    p_core.text = "SYSTEM ESSENCE IN ONE SENTENCE:"
    p_core.font.size = Pt(11)
    p_core.font.bold = True
    p_core.font.color.rgb = COLOR_EMERALD
    p_core.alignment = PP_ALIGN.CENTER
    
    p_core2 = tf_m2.add_paragraph()
    p_core2.text = "\"A decoupled, voice-assisted full-stack platform that extracts resume intelligence, generates contextual mock interviews, and evaluates candidate responses in real time using generative AI and browser-native speech processing.\""
    p_core2.font.size = Pt(11)
    p_core2.font.bold = True
    p_core2.font.color.rgb = COLOR_TEXT_MAIN
    p_core2.alignment = PP_ALIGN.CENTER
    p_core2.space_before = Pt(4)

    add_speaker_notes(s35,
        "What this means: Concluding architectural summary slide.\n"
        "Verbal Pitch: 'To conclude: this platform combines decoupled React 19 and Django REST architectures with OpenRouter generative AI and native Web Speech APIs to deliver a comprehensive, low-cost, and scalable technical interview preparation platform. Thank you, and I am now open to your questions.'"
    )

    # Save presentation
    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    out_file = "/Users/pranav1718/Resume Projects/AI-Interview-Platform/AI_Interview_Platform_Architecture.pptx"
    create_deck(out_file)
