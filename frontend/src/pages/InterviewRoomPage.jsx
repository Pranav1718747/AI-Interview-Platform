import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import client from '../api/client';
import CameraPreview from '../components/CameraPreview';
import ScoreMeter from '../components/ScoreMeter';
import MarkdownView from '../components/MarkdownView';
import {
  Sparkles,
  Mic,
  MicOff,
  Volume2,
  VolumeX,
  Send,
  ArrowRight,
  ArrowLeft,
  CheckCircle2,
  AlertCircle,
  Clock,
  Award,
  BookOpen,
  HelpCircle,
  Globe,
  Radio
} from 'lucide-react';

const SPEECH_LANGUAGES = [
  { code: 'en-US', label: 'English (US)' },
  { code: 'en-IN', label: 'English (India)' },
  { code: 'en-GB', label: 'English (UK)' },
];

export default function InterviewRoomPage() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [session, setSession] = useState(null);
  const [currentIdx, setCurrentIdx] = useState(0);
  const [answerText, setAnswerText] = useState('');
  const [selectedLang, setSelectedLang] = useState('en-US');
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [finishing, setFinishing] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showKeyPoints, setShowKeyPoints] = useState(false);

  const recognitionRef = useRef(null);
  const finalTranscriptRef = useRef('');
  const isListeningRef = useRef(false);

  const fetchSession = async () => {
    try {
      const res = await client.get(`/api/interviews/${id}/`);
      setSession(res.data);
      const questions = res.data.questions || [];
      const firstUnanswered = questions.findIndex((q) => !q.response);
      if (firstUnanswered !== -1) {
        setCurrentIdx(firstUnanswered);
      } else if (questions.length > 0) {
        setCurrentIdx(0);
      }
    } catch (err) {
      setError('Failed to load interview session.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSession();
  }, [id]);

  const questions = session?.questions || [];
  const currentQuestion = questions[currentIdx] || null;

  // Sync answer textarea when switching questions
  useEffect(() => {
    if (currentQuestion?.response) {
      const existingAns = currentQuestion.response.candidate_answer || '';
      setAnswerText(existingAns);
      finalTranscriptRef.current = existingAns;
    } else {
      setAnswerText('');
      finalTranscriptRef.current = '';
    }
    setShowKeyPoints(false);
    if (isListening && recognitionRef.current) {
      recognitionRef.current.stop();
      setIsListening(false);
      isListeningRef.current = false;
    }
  }, [currentIdx, currentQuestion]);

  // Handle manual typing in textarea to keep final transcript in sync
  const handleAnswerChange = (e) => {
    const val = e.target.value;
    setAnswerText(val);
    finalTranscriptRef.current = val;
  };

  // High-accuracy Speech Recognition Setup
  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      const recognition = new SpeechRecognition();
      recognition.continuous = true;
      recognition.interimResults = true;
      recognition.lang = selectedLang;
      recognition.maxAlternatives = 1;

      recognition.onresult = (event) => {
        let interimTranscript = '';
        for (let i = event.resultIndex; i < event.results.length; ++i) {
          const transcriptPiece = event.results[i][0].transcript;
          if (event.results[i].isFinal) {
            // Append final recognized sentence cleanly
            finalTranscriptRef.current += (finalTranscriptRef.current ? ' ' : '') + transcriptPiece.trim();
          } else {
            interimTranscript += transcriptPiece;
          }
        }
        
        const combined = finalTranscriptRef.current + (interimTranscript ? ` ${interimTranscript}` : '');
        setAnswerText(combined);
      };

      recognition.onerror = (event) => {
        console.warn('Speech recognition warning:', event.error);
        if (event.error === 'no-speech') {
          // ignore transient silence
          return;
        }
        setIsListening(false);
        isListeningRef.current = false;
      };

      recognition.onend = () => {
        // Auto-restart if user hasn't explicitly stopped listening
        if (isListeningRef.current) {
          try {
            recognition.start();
          } catch (e) {
            setIsListening(false);
            isListeningRef.current = false;
          }
        } else {
          setIsListening(false);
        }
      };

      recognitionRef.current = recognition;
    }

    return () => {
      if (recognitionRef.current) {
        try {
          recognitionRef.current.stop();
        } catch (e) {}
      }
    };
  }, [selectedLang]);

  const toggleListening = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert('Speech Recognition is not supported in this browser. Please use Google Chrome or Microsoft Edge.');
      return;
    }

    if (isListening) {
      isListeningRef.current = false;
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
      setIsListening(false);
    } else {
      try {
        isListeningRef.current = true;
        if (recognitionRef.current) {
          recognitionRef.current.lang = selectedLang;
          recognitionRef.current.start();
          setIsListening(true);
        }
      } catch (err) {
        console.error('Failed to start speech recognition:', err);
        setIsListening(false);
        isListeningRef.current = false;
      }
    }
  };

  // Text to Speech for Question
  const speakQuestion = () => {
    if (!('speechSynthesis' in window) || !currentQuestion) return;

    if (isSpeaking) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
      return;
    }

    const utterance = new SpeechSynthesisUtterance(currentQuestion.question_text);
    utterance.rate = 1.0;
    utterance.pitch = 1.0;
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);

    setIsSpeaking(true);
    window.speechSynthesis.speak(utterance);
  };

  const handleSubmitAnswer = async () => {
    if (!answerText.trim() || !currentQuestion) return;

    if (isListening && recognitionRef.current) {
      isListeningRef.current = false;
      recognitionRef.current.stop();
      setIsListening(false);
    }

    setSubmitting(true);
    setError('');

    try {
      const res = await client.post(
        `/api/interviews/${session.id}/questions/${currentQuestion.id}/answer/`,
        { candidate_answer: answerText.trim() }
      );

      setSession((prev) => ({
        ...prev,
        questions: prev.questions.map((q) =>
          q.id === currentQuestion.id ? res.data : q
        ),
      }));
    } catch (err) {
      setError(
        err.response?.data?.error ||
        err.response?.data?.detail ||
        'OpenRouter LLM failed to evaluate answer. Please verify your connection or API key.'
      );
    } finally {
      setSubmitting(false);
    }
  };

  const handleFinishInterview = async () => {
    setFinishing(true);
    try {
      await client.post(`/api/interviews/${session.id}/finish/`);
      navigate(`/interviews/${session.id}/result`);
    } catch (err) {
      setError(
        err.response?.data?.error ||
        'OpenRouter LLM failed to generate the final interview summary.'
      );
    } finally {
      setFinishing(false);
    }
  };

  if (loading) {
    return (
      <div className="container" style={{ padding: '80px 0', textAlign: 'center' }}>
        <p style={{ color: 'var(--text-muted)' }}>Loading AI Interview Session...</p>
      </div>
    );
  }

  if (!session || questions.length === 0) {
    return (
      <div className="container" style={{ padding: '80px 0', textAlign: 'center' }}>
        <h2>Session not found</h2>
        <button onClick={() => navigate('/dashboard')} className="btn btn-primary" style={{ marginTop: '16px' }}>
          Back to Dashboard
        </button>
      </div>
    );
  }

  const allAnswered = questions.every((q) => !!q.response);
  const isLastQuestion = currentIdx === questions.length - 1;

  return (
    <div className="container" style={{ padding: '32px 24px 80px' }}>
      {/* Top Session Status Bar */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '16px 24px',
        background: 'rgba(18, 24, 38, 0.8)',
        borderRadius: 'var(--radius-md)',
        border: '1px solid var(--border-color)',
        marginBottom: '28px',
        flexWrap: 'wrap',
        gap: '16px',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{
            width: '10px',
            height: '10px',
            borderRadius: '50%',
            background: 'var(--accent-emerald)',
            boxShadow: '0 0 10px #10b981',
          }} />
          <div>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700 }}>{session.role_title}</h3>
            <span style={{ fontSize: '0.8rem', color: 'var(--text-dim)' }}>
              {session.difficulty} Level • {session.interview_type} Focus
            </span>
          </div>
        </div>

        {/* Question Step Indicators */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          {questions.map((q, idx) => (
            <button
              key={q.id}
              onClick={() => setCurrentIdx(idx)}
              style={{
                width: '32px',
                height: '32px',
                borderRadius: '8px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '0.85rem',
                fontWeight: 700,
                cursor: 'pointer',
                border: idx === currentIdx ? '2px solid var(--primary)' : '1px solid var(--border-color)',
                background: q.response
                  ? 'rgba(16, 185, 129, 0.2)'
                  : idx === currentIdx
                  ? 'var(--primary)'
                  : 'rgba(255, 255, 255, 0.04)',
                color: q.response ? '#6ee7b7' : '#fff',
                transition: 'all 0.2s ease',
              }}
              title={`Question ${idx + 1}`}
            >
              {idx + 1}
            </button>
          ))}
        </div>

        {/* Finish Action */}
        <div>
          {allAnswered ? (
            <button
              onClick={handleFinishInterview}
              className="btn btn-primary"
              style={{ padding: '8px 18px', fontSize: '0.9rem' }}
              disabled={finishing}
            >
              <Award size={16} /> {finishing ? 'Generating Scorecard...' : 'Complete & View Scorecard'}
            </button>
          ) : (
            <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
              Question {currentIdx + 1} of {questions.length}
            </span>
          )}
        </div>
      </div>

      {error && (
        <div style={{
          background: 'rgba(244, 63, 94, 0.1)',
          border: '1px solid rgba(244, 63, 94, 0.3)',
          borderRadius: 'var(--radius-sm)',
          padding: '12px 16px',
          display: 'flex',
          alignItems: 'center',
          gap: '10px',
          color: '#fda4af',
          fontSize: '0.875rem',
          marginBottom: '20px',
        }}>
          <AlertCircle size={18} />
          <span>{error}</span>
        </div>
      )}

      {/* Main Interview Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 340px', gap: '24px' }}>
        {/* Left Column: Question, Answer Box & Live AI Feedback */}
        <div>
          {/* Question Card */}
          <div className="glass-card" style={{ padding: '32px', marginBottom: '24px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
              <span className="badge badge-primary">{currentQuestion.category}</span>

              <button
                onClick={speakQuestion}
                className="btn btn-secondary"
                style={{ padding: '6px 12px', fontSize: '0.8rem' }}
                title="Listen to question"
              >
                {isSpeaking ? <><VolumeX size={14} /> Stop Audio</> : <><Volume2 size={14} /> Read Question</>}
              </button>
            </div>

            <h2 style={{ fontSize: '1.4rem', fontWeight: 600, lineHeight: 1.5, marginBottom: '20px' }}>
              {currentQuestion.question_text}
            </h2>

            {/* Expected Key Points toggle */}
            {currentQuestion.expected_key_points?.length > 0 && (
              <div>
                <button
                  type="button"
                  onClick={() => setShowKeyPoints(!showKeyPoints)}
                  style={{
                    background: 'transparent',
                    border: 'none',
                    color: 'var(--primary)',
                    fontSize: '0.85rem',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '6px',
                    fontWeight: 600,
                  }}
                >
                  <HelpCircle size={14} /> {showKeyPoints ? 'Hide Key Concepts' : 'Show Key Concepts / Hint'}
                </button>

                {showKeyPoints && (
                  <div style={{
                    marginTop: '12px',
                    padding: '12px 16px',
                    background: 'rgba(99, 102, 241, 0.08)',
                    borderRadius: 'var(--radius-sm)',
                    border: '1px solid rgba(99, 102, 241, 0.2)',
                    fontSize: '0.85rem',
                    color: 'var(--text-muted)',
                  }}>
                    <strong>Ideal concepts to cover:</strong>
                    <ul style={{ paddingLeft: '18px', marginTop: '6px' }}>
                      {currentQuestion.expected_key_points.map((pt, i) => (
                        <li key={i}>{pt}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Answer Input Section */}
          <div className="glass-card" style={{ padding: '28px', marginBottom: '24px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px', flexWrap: 'wrap', gap: '10px' }}>
              <span className="form-label" style={{ marginBottom: 0 }}>Your Response</span>

              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                {/* Speech Language Selector */}
                <div style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                  <Globe size={14} />
                  <select
                    value={selectedLang}
                    onChange={(e) => setSelectedLang(e.target.value)}
                    style={{
                      background: 'rgba(255, 255, 255, 0.05)',
                      border: '1px solid var(--border-color)',
                      color: 'var(--text-main)',
                      padding: '4px 8px',
                      borderRadius: 'var(--radius-sm)',
                      fontSize: '0.8rem',
                      outline: 'none',
                    }}
                  >
                    {SPEECH_LANGUAGES.map((lang) => (
                      <option key={lang.code} value={lang.code} style={{ background: '#121826' }}>
                        {lang.label}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Speech Recognition Toggle */}
                <button
                  type="button"
                  onClick={toggleListening}
                  className={`btn ${isListening ? 'btn-danger' : 'btn-secondary'}`}
                  style={{
                    padding: '6px 14px',
                    fontSize: '0.82rem',
                    boxShadow: isListening ? '0 0 15px rgba(244, 63, 94, 0.4)' : 'none',
                  }}
                >
                  {isListening ? (
                    <>
                      <Radio size={14} className="pulse-animation" /> Live Microphone Active... (Click to Stop)
                    </>
                  ) : (
                    <>
                      <Mic size={14} color="var(--primary)" /> Speak Answer (Mic)
                    </>
                  )}
                </button>
              </div>
            </div>

            {/* Listening Visual Indicator */}
            {isListening && (
              <div style={{
                background: 'rgba(244, 63, 94, 0.08)',
                border: '1px dashed rgba(244, 63, 94, 0.3)',
                padding: '10px 14px',
                borderRadius: 'var(--radius-sm)',
                marginBottom: '12px',
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                fontSize: '0.8rem',
                color: '#fda4af',
              }}>
                <div style={{
                  width: '8px',
                  height: '8px',
                  borderRadius: '50%',
                  background: 'var(--accent-rose)',
                  animation: 'pulseGlow 1s infinite',
                }} />
                <span>Transcribing your speech in real-time ({selectedLang}). Speak clearly into your microphone...</span>
              </div>
            )}

            <textarea
              className="form-control"
              rows={6}
              placeholder="Speak using the microphone button above, or type your structured technical explanation here..."
              value={answerText}
              onChange={handleAnswerChange}
              style={{ fontSize: '0.95rem', lineHeight: 1.6 }}
            />

            <div style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              marginTop: '16px',
            }}>
              <span style={{ fontSize: '0.8rem', color: 'var(--text-dim)' }}>
                {answerText.trim().split(/\s+/).filter(Boolean).length} words
              </span>

              <button
                type="button"
                onClick={handleSubmitAnswer}
                className="btn btn-primary"
                disabled={submitting || !answerText.trim()}
              >
                {submitting ? (
                  <>
                    <Sparkles size={16} className="pulse-animation" /> Evaluating Answer with AI...
                  </>
                ) : (
                  <>
                    <Send size={16} /> {currentQuestion.response ? 'Re-Evaluate Answer' : 'Submit for AI Grading'}
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Real-Time AI Feedback Panel with Structured Markdown */}
          {currentQuestion.response && (
            <div className="glass-card-glow" style={{ padding: '28px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                  <Sparkles size={20} color="var(--primary)" />
                  <h3 style={{ fontSize: '1.2rem' }}>AI Real-Time Evaluation</h3>
                </div>
                <span className={`badge ${currentQuestion.response.overall_score >= 80 ? 'badge-success' : 'badge-warning'}`}>
                  Score: {currentQuestion.response.overall_score}/100
                </span>
              </div>

              {/* Breakdown Metric Chips */}
              <div style={{ display: 'flex', gap: '12px', marginBottom: '20px', flexWrap: 'wrap' }}>
                <div className="pill" style={{ background: 'rgba(6, 182, 212, 0.1)', borderColor: 'rgba(6, 182, 212, 0.3)', color: '#67e8f9' }}>
                  Technical Depth: {currentQuestion.response.technical_score}%
                </div>
                <div className="pill" style={{ background: 'rgba(16, 185, 129, 0.1)', borderColor: 'rgba(16, 185, 129, 0.3)', color: '#6ee7b7' }}>
                  Clarity: {currentQuestion.response.clarity_score}%
                </div>
                <div className="pill" style={{ background: 'rgba(99, 102, 241, 0.1)', borderColor: 'rgba(99, 102, 241, 0.3)', color: '#a5b4fc' }}>
                  Relevance: {currentQuestion.response.relevance_score}%
                </div>
              </div>

              {/* Structured AI Feedback Text */}
              <div style={{ marginBottom: '20px' }}>
                <MarkdownView content={currentQuestion.response.ai_feedback} />
              </div>

              {/* Strengths & Improvements */}
              <div className="grid-2" style={{ marginBottom: '20px' }}>
                <div style={{ background: 'rgba(16, 185, 129, 0.05)', border: '1px solid rgba(16, 185, 129, 0.2)', padding: '16px', borderRadius: 'var(--radius-sm)' }}>
                  <h4 style={{ color: '#6ee7b7', fontSize: '0.9rem', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <CheckCircle2 size={16} /> What Went Well
                  </h4>
                  <ul style={{ paddingLeft: '18px', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                    {currentQuestion.response.strengths?.map((str, i) => (
                      <li key={i}>{str}</li>
                    ))}
                  </ul>
                </div>

                <div style={{ background: 'rgba(244, 63, 94, 0.05)', border: '1px solid rgba(244, 63, 94, 0.2)', padding: '16px', borderRadius: 'var(--radius-sm)' }}>
                  <h4 style={{ color: '#fda4af', fontSize: '0.9rem', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <AlertCircle size={16} /> Recommendation
                  </h4>
                  <ul style={{ paddingLeft: '18px', color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                    {currentQuestion.response.improvements?.map((imp, i) => (
                      <li key={i}>{imp}</li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* Model / Exemplary Answer with Structured Markdown */}
              {currentQuestion.response.ideal_answer && (
                <div style={{
                  background: 'rgba(255, 255, 255, 0.02)',
                  border: '1px solid var(--border-color)',
                  padding: '20px',
                  borderRadius: 'var(--radius-sm)',
                }}>
                  <h4 style={{ color: 'var(--accent-cyan)', fontSize: '0.95rem', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <BookOpen size={16} /> Model Exemplary Response:
                  </h4>
                  <MarkdownView content={currentQuestion.response.ideal_answer} />
                </div>
              )}

              {/* Next Step Action */}
              <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '20px' }}>
                {!isLastQuestion ? (
                  <button
                    onClick={() => setCurrentIdx(currentIdx + 1)}
                    className="btn btn-primary"
                  >
                    Next Question <ArrowRight size={16} />
                  </button>
                ) : (
                  <button
                    onClick={handleFinishInterview}
                    className="btn btn-primary"
                    disabled={finishing}
                  >
                    {finishing ? 'Generating Final Scorecard...' : 'Complete Interview & View Scorecard'} <Award size={16} />
                  </button>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Right Column: Camera & Session Controls */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          <CameraPreview />

          {/* Session Progress Card */}
          <div className="glass-card" style={{ padding: '24px' }}>
            <h4 style={{ fontSize: '1rem', marginBottom: '14px' }}>Interview Progress</h4>
            <div style={{ width: '100%', height: '8px', background: 'rgba(255, 255, 255, 0.08)', borderRadius: '4px', overflow: 'hidden', marginBottom: '12px' }}>
              <div style={{
                width: `${(questions.filter((q) => !!q.response).length / questions.length) * 100}%`,
                height: '100%',
                background: 'var(--primary)',
                borderRadius: '4px',
                transition: 'width 0.5s ease',
              }} />
            </div>
            <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
              {questions.filter((q) => !!q.response).length} of {questions.length} Questions Answered
            </span>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', marginTop: '20px' }}>
              {questions.map((q, i) => (
                <div
                  key={q.id}
                  onClick={() => setCurrentIdx(i)}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    padding: '8px 12px',
                    borderRadius: 'var(--radius-sm)',
                    background: i === currentIdx ? 'rgba(99, 102, 241, 0.15)' : 'rgba(255, 255, 255, 0.02)',
                    cursor: 'pointer',
                    fontSize: '0.85rem',
                  }}
                >
                  <span style={{ color: i === currentIdx ? 'var(--text-main)' : 'var(--text-muted)' }}>
                    Q{i + 1}: {q.category}
                  </span>
                  {q.response ? (
                    <span style={{ color: 'var(--accent-emerald)', fontWeight: 700, fontSize: '0.8rem' }}>
                      {q.response.overall_score}%
                    </span>
                  ) : (
                    <span style={{ color: 'var(--text-dim)', fontSize: '0.75rem' }}>Pending</span>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
