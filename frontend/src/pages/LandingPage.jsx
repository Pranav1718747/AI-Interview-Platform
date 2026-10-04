import React from 'react';
import { Link } from 'react-router-dom';
import { Sparkles, FileText, Video, Award, ArrowRight, ShieldCheck, Zap, BarChart3, MessageSquare } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function LandingPage() {
  const { user } = useAuth();

  return (
    <div style={{ paddingBottom: '80px' }}>
      {/* Hero Section */}
      <section style={{
        padding: '100px 0 60px',
        textAlign: 'center',
        position: 'relative',
      }}>
        <div className="container" style={{ maxWidth: '900px' }}>
          <div className="badge badge-primary" style={{ marginBottom: '20px', padding: '6px 16px' }}>
            <Sparkles size={14} /> Next-Gen AI Interview Prep & ATS Intelligence
          </div>

          <h1 style={{
            fontSize: 'clamp(2.5rem, 5vw, 4.2rem)',
            fontWeight: 800,
            lineHeight: 1.15,
            marginBottom: '24px',
          }}>
            Ace Your Next Tech Interview with <span className="gradient-text">Real-Time AI</span>
          </h1>

          <p style={{
            fontSize: '1.2rem',
            color: 'var(--text-muted)',
            marginBottom: '36px',
            lineHeight: 1.6,
          }}>
            Upload your resume for instant ATS scoring, personalized skill gap analysis, and practice with voice-enabled AI mock interviews that provide live feedback, question-by-question scoring, and ideal model answers.
          </p>

          <div style={{ display: 'flex', gap: '16px', justifyContent: 'center', flexWrap: 'wrap' }}>
            {user ? (
              <Link to="/dashboard" className="btn btn-primary" style={{ padding: '14px 32px', fontSize: '1.05rem' }}>
                Go to Dashboard <ArrowRight size={18} />
              </Link>
            ) : (
              <>
                <Link to="/register" className="btn btn-primary" style={{ padding: '14px 32px', fontSize: '1.05rem' }}>
                  Start Free Practice <ArrowRight size={18} />
                </Link>
                <Link to="/login" className="btn btn-secondary" style={{ padding: '14px 32px', fontSize: '1.05rem' }}>
                  Sign In
                </Link>
              </>
            )}
          </div>

          {/* Highlights Row */}
          <div style={{
            display: 'flex',
            justifyContent: 'center',
            gap: '32px',
            marginTop: '50px',
            color: 'var(--text-dim)',
            fontSize: '0.9rem',
            flexWrap: 'wrap',
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Zap size={16} color="var(--primary)" /> Instant ATS Scoring
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <MessageSquare size={16} color="var(--accent-cyan)" /> Voice & Speech Recognition
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <ShieldCheck size={16} color="var(--accent-emerald)" /> Real-Time AI Grading
            </div>
          </div>
        </div>
      </section>

      {/* Feature Cards Grid */}
      <section className="container" style={{ marginTop: '40px' }}>
        <div style={{ textAlign: 'center', marginBottom: '48px' }}>
          <h2 style={{ fontSize: '2rem', marginBottom: '12px' }}>Complete Career Acceleration Platform</h2>
          <p style={{ color: 'var(--text-muted)' }}>Everything you need to turn applications into high-paying offers.</p>
        </div>

        <div className="grid-3">
          {/* Card 1 */}
          <div className="glass-card" style={{ padding: '32px' }}>
            <div style={{
              width: '48px',
              height: '48px',
              borderRadius: '12px',
              background: 'rgba(99, 102, 241, 0.15)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              marginBottom: '20px',
              color: 'var(--primary)',
            }}>
              <FileText size={24} />
            </div>
            <h3 style={{ fontSize: '1.25rem', marginBottom: '12px' }}>Deep ATS Resume Review</h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem', lineHeight: 1.6 }}>
              Extracts technical and soft skills from PDF and DOCX resumes, checks keyword matching, and computes a recruiter-grade ATS compatibility score with actionable strengths and weaknesses.
            </p>
          </div>

          {/* Card 2 */}
          <div className="glass-card" style={{ padding: '32px', border: '1px solid var(--border-glow)' }}>
            <div style={{
              width: '48px',
              height: '48px',
              borderRadius: '12px',
              background: 'rgba(6, 182, 212, 0.15)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              marginBottom: '20px',
              color: 'var(--accent-cyan)',
            }}>
              <Video size={24} />
            </div>
            <h3 style={{ fontSize: '1.25rem', marginBottom: '12px' }}>Interactive AI Interview Room</h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem', lineHeight: 1.6 }}>
              Simulate realistic interviews for roles like Frontend, Backend, Fullstack, or DevOps. Speak naturally with real-time speech-to-text input, listen to questions via AI speech synthesis, and receive instant rubric feedback.
            </p>
          </div>

          {/* Card 3 */}
          <div className="glass-card" style={{ padding: '32px' }}>
            <div style={{
              width: '48px',
              height: '48px',
              borderRadius: '12px',
              background: 'rgba(16, 185, 129, 0.15)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              marginBottom: '20px',
              color: 'var(--accent-emerald)',
            }}>
              <BarChart3 size={24} />
            </div>
            <h3 style={{ fontSize: '1.25rem', marginBottom: '12px' }}>Scorecards & Analytics</h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.95rem', lineHeight: 1.6 }}>
              Track your readiness trajectory over time with breakdown radar scores across Technical Mastery, Communication Clarity, and Problem Solving.
            </p>
          </div>
        </div>
      </section>

      {/* CTA Box */}
      <section className="container" style={{ marginTop: '80px' }}>
        <div className="glass-card-glow" style={{
          padding: '48px 32px',
          textAlign: 'center',
          background: 'linear-gradient(135deg, rgba(18, 24, 38, 0.9) 0%, rgba(30, 41, 67, 0.9) 100%)',
        }}>
          <h2 style={{ fontSize: '2.2rem', marginBottom: '16px' }}>Ready to Experience Smarter Interview Prep?</h2>
          <p style={{ color: 'var(--text-muted)', maxWidth: '600px', margin: '0 auto 28px', fontSize: '1.05rem' }}>
            Join candidates sharpening their technical narrative, building confidence, and landing top roles.
          </p>
          <Link to={user ? "/interviews/setup" : "/register"} className="btn btn-primary" style={{ padding: '14px 36px', fontSize: '1.05rem' }}>
            Start Your First Mock Interview <ArrowRight size={18} />
          </Link>
        </div>
      </section>
    </div>
  );
}
