import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import client from '../api/client';
import ScoreMeter from '../components/ScoreMeter';
import MarkdownView from '../components/MarkdownView';
import confetti from 'canvas-confetti';
import {
  Award,
  Sparkles,
  CheckCircle2,
  AlertCircle,
  ArrowRight,
  TrendingUp,
  FileText,
  RotateCcw,
  BookOpen,
  Printer
} from 'lucide-react';

export default function InterviewResultPage() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchResult = async () => {
      try {
        const res = await client.get(`/api/interviews/${id}/`);
        setSession(res.data);
        if (res.data.overall_score && res.data.overall_score >= 75) {
          confetti({
            particleCount: 80,
            spread: 70,
            origin: { y: 0.6 },
          });
        }
      } catch (err) {
        console.error('Failed to load interview report:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchResult();
  }, [id]);

  if (loading) {
    return (
      <div className="container" style={{ padding: '80px 0', textAlign: 'center' }}>
        <p style={{ color: 'var(--text-muted)' }}>Generating comprehensive scorecard...</p>
      </div>
    );
  }

  if (!session) {
    return (
      <div className="container" style={{ padding: '80px 0', textAlign: 'center' }}>
        <h2>Report not found</h2>
        <Link to="/dashboard" className="btn btn-primary" style={{ marginTop: '16px' }}>
          Back to Dashboard
        </Link>
      </div>
    );
  }

  const {
    role_title,
    difficulty,
    interview_type,
    overall_score = 0,
    technical_mastery = 0,
    communication_clarity = 0,
    problem_solving = 0,
    readiness_rating = 'Completed',
    key_takeaways = [],
    actionable_recommendations = [],
    detailed_summary = '',
    questions = [],
  } = session;

  return (
    <div className="container" style={{ padding: '40px 24px 80px', maxWidth: '1000px' }}>
      {/* Header Bar */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '32px',
        flexWrap: 'wrap',
        gap: '16px',
      }}>
        <div>
          <div className="badge badge-success" style={{ marginBottom: '8px' }}>
            <Award size={14} /> Evaluation Completed
          </div>
          <h1 style={{ fontSize: '2.4rem' }}>{role_title} Scorecard</h1>
          <p style={{ color: 'var(--text-muted)' }}>
            {difficulty} Level • {questions.length} Questions Evaluated
          </p>
        </div>

        <div style={{ display: 'flex', gap: '12px' }}>
          <button
            onClick={() => window.print()}
            className="btn btn-secondary"
            style={{ padding: '10px 18px' }}
          >
            <Printer size={16} /> Print Report
          </button>
          <Link to="/interviews/setup" className="btn btn-primary" style={{ padding: '10px 20px' }}>
            <RotateCcw size={16} /> Practice Another
          </Link>
        </div>
      </div>

      {/* Main Score & Readiness Card */}
      <div className="glass-card-glow" style={{ padding: '36px', marginBottom: '32px' }}>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '32px',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '28px', flexWrap: 'wrap' }}>
            <ScoreMeter score={overall_score || 0} size={140} strokeWidth={12} label="Overall Score" />
            <div>
              <span style={{ fontSize: '0.9rem', color: 'var(--text-muted)', fontWeight: 600 }}>Readiness Assessment</span>
              <h2 style={{ fontSize: '1.8rem', color: 'var(--accent-emerald)', marginTop: '4px', marginBottom: '8px' }}>
                {readiness_rating || 'Good Candidate'}
              </h2>
              <p style={{ fontSize: '0.95rem', color: 'var(--text-muted)', maxWidth: '440px', lineHeight: 1.5 }}>
                {detailed_summary || 'Detailed performance summary calculated by AI evaluator.'}
              </p>
            </div>
          </div>

          {/* 3 Pillars */}
          <div style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '12px',
            minWidth: '240px',
            background: 'rgba(0, 0, 0, 0.25)',
            padding: '20px',
            borderRadius: 'var(--radius-md)',
            border: '1px solid var(--border-color)',
          }}>
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '4px' }}>
                <span style={{ color: 'var(--text-muted)' }}>Technical Mastery</span>
                <span style={{ fontWeight: 700, color: 'var(--accent-cyan)' }}>{technical_mastery}%</span>
              </div>
              <div style={{ width: '100%', height: '6px', background: 'rgba(255, 255, 255, 0.1)', borderRadius: '3px', overflow: 'hidden' }}>
                <div style={{ width: `${technical_mastery}%`, height: '100%', background: 'var(--accent-cyan)' }} />
              </div>
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '4px' }}>
                <span style={{ color: 'var(--text-muted)' }}>Communication Clarity</span>
                <span style={{ fontWeight: 700, color: 'var(--accent-emerald)' }}>{communication_clarity}%</span>
              </div>
              <div style={{ width: '100%', height: '6px', background: 'rgba(255, 255, 255, 0.1)', borderRadius: '3px', overflow: 'hidden' }}>
                <div style={{ width: `${communication_clarity}%`, height: '100%', background: 'var(--accent-emerald)' }} />
              </div>
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '4px' }}>
                <span style={{ color: 'var(--text-muted)' }}>Problem Solving</span>
                <span style={{ fontWeight: 700, color: 'var(--accent-amber)' }}>{problem_solving}%</span>
              </div>
              <div style={{ width: '100%', height: '6px', background: 'rgba(255, 255, 255, 0.1)', borderRadius: '3px', overflow: 'hidden' }}>
                <div style={{ width: `${problem_solving}%`, height: '100%', background: 'var(--accent-amber)' }} />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Strengths & Actionable Recommendations Grid */}
      <div className="grid-2" style={{ marginBottom: '40px' }}>
        <div className="glass-card" style={{ padding: '28px', background: 'rgba(16, 185, 129, 0.05)', borderColor: 'rgba(16, 185, 129, 0.2)' }}>
          <h3 style={{ fontSize: '1.15rem', color: '#6ee7b7', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <CheckCircle2 size={20} /> Candidate Strengths & Highlights
          </h3>
          <ul style={{ paddingLeft: '20px', color: 'var(--text-muted)', lineHeight: 1.7, fontSize: '0.92rem' }}>
            {key_takeaways.map((item, i) => (
              <li key={i}>{item}</li>
            ))}
          </ul>
        </div>

        <div className="glass-card" style={{ padding: '28px', background: 'rgba(244, 63, 94, 0.05)', borderColor: 'rgba(244, 63, 94, 0.2)' }}>
          <h3 style={{ fontSize: '1.15rem', color: '#fda4af', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <AlertCircle size={20} /> Targeted Improvement Plan
          </h3>
          <ul style={{ paddingLeft: '20px', color: 'var(--text-muted)', lineHeight: 1.7, fontSize: '0.92rem' }}>
            {actionable_recommendations.map((item, i) => (
              <li key={i}>{item}</li>
            ))}
          </ul>
        </div>
      </div>

      {/* Question-by-Question Deep Dive */}
      <div>
        <h2 style={{ fontSize: '1.5rem', marginBottom: '24px' }}>Question Breakdown & Transcripts</h2>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          {questions.map((q, idx) => (
            <div key={q.id} className="glass-card" style={{ padding: '28px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px' }}>
                <span className="badge badge-primary">
                  Question {idx + 1} • {q.category}
                </span>
                {q.response ? (
                  <span className={`badge ${q.response.overall_score >= 80 ? 'badge-success' : 'badge-warning'}`}>
                    Score: {q.response.overall_score}/100
                  </span>
                ) : (
                  <span className="badge badge-danger">Unanswered</span>
                )}
              </div>

              <h3 style={{ fontSize: '1.15rem', marginBottom: '16px' }}>{q.question_text}</h3>

              {q.response && (
                <div>
                  {/* Candidate Answer */}
                  <div style={{
                    background: 'rgba(255, 255, 255, 0.02)',
                    padding: '14px 18px',
                    borderRadius: 'var(--radius-sm)',
                    border: '1px solid var(--border-color)',
                    marginBottom: '14px',
                    fontSize: '0.9rem',
                  }}>
                    <strong style={{ color: 'var(--text-muted)', display: 'block', marginBottom: '4px' }}>Your Response:</strong>
                    <p style={{ color: 'var(--text-main)', lineHeight: 1.6 }}>{q.response.candidate_answer}</p>
                  </div>

                  {/* AI Feedback */}
                  <div style={{
                    background: 'rgba(99, 102, 241, 0.05)',
                    padding: '14px 18px',
                    borderRadius: 'var(--radius-sm)',
                    border: '1px solid rgba(99, 102, 241, 0.2)',
                    marginBottom: '14px',
                    fontSize: '0.9rem',
                  }}>
                    <strong style={{ color: 'var(--primary)', display: 'block', marginBottom: '8px' }}>AI Assessment:</strong>
                    <MarkdownView content={q.response.ai_feedback} />
                  </div>

                  {/* Model Answer */}
                  {q.response.ideal_answer && (
                    <div style={{
                      background: 'rgba(6, 182, 212, 0.05)',
                      padding: '14px 18px',
                      borderRadius: 'var(--radius-sm)',
                      border: '1px solid rgba(6, 182, 212, 0.2)',
                      fontSize: '0.9rem',
                    }}>
                      <strong style={{ color: 'var(--accent-cyan)', display: 'block', marginBottom: '8px' }}>Model Ideal Answer:</strong>
                      <MarkdownView content={q.response.ideal_answer} />
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
