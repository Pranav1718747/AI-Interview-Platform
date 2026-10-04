import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import client from '../api/client';
import { useAuth } from '../context/AuthContext';
import ScoreMeter from '../components/ScoreMeter';
import {
  FileText,
  Video,
  Sparkles,
  ArrowRight,
  Plus,
  Clock,
  CheckCircle2,
  TrendingUp,
  Brain,
  MessageSquare,
  Award
} from 'lucide-react';

export default function DashboardPage() {
  const { user } = useAuth();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const res = await client.get('/api/analytics/dashboard/');
        setData(res.data);
      } catch (err) {
        console.error('Error fetching dashboard data:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchDashboard();
  }, []);

  if (loading) {
    return (
      <div className="container" style={{ padding: '60px 0', textAlign: 'center' }}>
        <p style={{ color: 'var(--text-muted)' }}>Loading your dashboard analytics...</p>
      </div>
    );
  }

  const {
    total_resumes = 0,
    avg_ats_score = 0,
    total_interviews = 0,
    completed_interviews = 0,
    avg_interview_score = 0,
    skill_metrics = {},
    recent_resumes = [],
    recent_interviews = [],
  } = data || {};

  return (
    <div className="container" style={{ padding: '40px 24px 80px' }}>
      {/* Welcome Header */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: '36px',
        flexWrap: 'wrap',
        gap: '20px',
      }}>
        <div>
          <h1 style={{ fontSize: '2.2rem', marginBottom: '6px' }}>
            Welcome back, <span className="gradient-text">{user?.first_name || user?.username}</span> 👋
          </h1>
          <p style={{ color: 'var(--text-muted)' }}>
            Track your ATS matching readiness and mock interview milestones.
          </p>
        </div>

        <div style={{ display: 'flex', gap: '12px' }}>
          <Link to="/resumes" className="btn btn-secondary">
            <FileText size={16} /> Manage Resumes
          </Link>
          <Link to="/interviews/setup" className="btn btn-primary">
            <Video size={16} /> New Mock Interview
          </Link>
        </div>
      </div>

      {/* Top Metrics Row */}
      <div className="grid-4" style={{ marginBottom: '32px' }}>
        <div className="glass-card" style={{ padding: '24px', display: 'flex', alignItems: 'center', gap: '20px' }}>
          <ScoreMeter score={avg_ats_score} size={84} strokeWidth={8} label="ATS" />
          <div>
            <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: 600 }}>Avg. ATS Score</span>
            <h3 style={{ fontSize: '1.6rem', marginTop: '4px' }}>{avg_ats_score}%</h3>
            <span style={{ fontSize: '0.75rem', color: 'var(--accent-emerald)' }}>Resume Readiness</span>
          </div>
        </div>

        <div className="glass-card" style={{ padding: '24px', display: 'flex', alignItems: 'center', gap: '20px' }}>
          <ScoreMeter score={avg_interview_score} size={84} strokeWidth={8} label="Interview" />
          <div>
            <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: 600 }}>Avg. Interview Score</span>
            <h3 style={{ fontSize: '1.6rem', marginTop: '4px' }}>{avg_interview_score || '--'}</h3>
            <span style={{ fontSize: '0.75rem', color: 'var(--primary)' }}>Evaluation Performance</span>
          </div>
        </div>

        <div className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
            <FileText size={20} color="var(--accent-cyan)" />
            <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: 600 }}>Resumes Uploaded</span>
          </div>
          <h3 style={{ fontSize: '1.8rem' }}>{total_resumes}</h3>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-dim)', marginTop: '4px' }}>Ready for AI role matching</span>
        </div>

        <div className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
            <Award size={20} color="var(--accent-amber)" />
            <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: 600 }}>Completed Sessions</span>
          </div>
          <h3 style={{ fontSize: '1.8rem' }}>{completed_interviews} <span style={{ fontSize: '1rem', color: 'var(--text-dim)' }}>/ {total_interviews}</span></h3>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-dim)', marginTop: '4px' }}>Mock practice rounds</span>
        </div>
      </div>

      {/* Skill Performance Breakdown */}
      <div className="glass-card" style={{ padding: '28px', marginBottom: '36px' }}>
        <h3 style={{ fontSize: '1.2rem', marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <TrendingUp size={20} color="var(--primary)" /> Core Competency Scores
        </h3>
        <div className="grid-3">
          <div style={{ background: 'rgba(255, 255, 255, 0.02)', padding: '16px 20px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-color)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
              <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: 600 }}>Technical Mastery</span>
              <span style={{ fontWeight: 700, color: 'var(--accent-cyan)' }}>{skill_metrics.technical_mastery || 0}%</span>
            </div>
            <div style={{ width: '100%', height: '8px', background: 'rgba(255, 255, 255, 0.08)', borderRadius: '4px', overflow: 'hidden' }}>
              <div style={{ width: `${skill_metrics.technical_mastery || 0}%`, height: '100%', background: 'linear-gradient(90deg, #6366f1, #06b6d4)', borderRadius: '4px', transition: 'width 0.8s ease' }} />
            </div>
          </div>

          <div style={{ background: 'rgba(255, 255, 255, 0.02)', padding: '16px 20px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-color)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
              <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: 600 }}>Communication Clarity</span>
              <span style={{ fontWeight: 700, color: 'var(--accent-emerald)' }}>{skill_metrics.communication_clarity || 0}%</span>
            </div>
            <div style={{ width: '100%', height: '8px', background: 'rgba(255, 255, 255, 0.08)', borderRadius: '4px', overflow: 'hidden' }}>
              <div style={{ width: `${skill_metrics.communication_clarity || 0}%`, height: '100%', background: 'linear-gradient(90deg, #10b981, #34d399)', borderRadius: '4px', transition: 'width 0.8s ease' }} />
            </div>
          </div>

          <div style={{ background: 'rgba(255, 255, 255, 0.02)', padding: '16px 20px', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-color)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
              <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)', fontWeight: 600 }}>Problem Solving</span>
              <span style={{ fontWeight: 700, color: 'var(--accent-amber)' }}>{skill_metrics.problem_solving || 0}%</span>
            </div>
            <div style={{ width: '100%', height: '8px', background: 'rgba(255, 255, 255, 0.08)', borderRadius: '4px', overflow: 'hidden' }}>
              <div style={{ width: `${skill_metrics.problem_solving || 0}%`, height: '100%', background: 'linear-gradient(90deg, #f59e0b, #fbbf24)', borderRadius: '4px', transition: 'width 0.8s ease' }} />
            </div>
          </div>
        </div>
      </div>

      {/* Two Column Grid for Recent Activity */}
      <div className="grid-2">
        {/* Recent Resumes */}
        <div className="glass-card" style={{ padding: '28px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
            <h3 style={{ fontSize: '1.15rem' }}>Recent Resumes</h3>
            <Link to="/resumes" style={{ color: 'var(--primary)', fontSize: '0.85rem', textDecoration: 'none', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '4px' }}>
              View All <ArrowRight size={14} />
            </Link>
          </div>

          {recent_resumes.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '32px 0', color: 'var(--text-dim)' }}>
              <FileText size={36} style={{ marginBottom: '8px', opacity: 0.5 }} />
              <p style={{ fontSize: '0.9rem' }}>No resumes uploaded yet.</p>
              <Link to="/resumes" className="btn btn-secondary" style={{ marginTop: '12px', fontSize: '0.85rem' }}>
                <Plus size={14} /> Upload Resume
              </Link>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {recent_resumes.map((resume) => (
                <div key={resume.id} style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '12px 16px',
                  background: 'rgba(255, 255, 255, 0.03)',
                  borderRadius: 'var(--radius-sm)',
                  border: '1px solid var(--border-color)',
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <FileText size={20} color="var(--primary)" />
                    <div>
                      <h4 style={{ fontSize: '0.95rem', fontWeight: 600 }}>{resume.title}</h4>
                      <span style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>{resume.uploaded_at}</span>
                    </div>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    {resume.ats_score !== null ? (
                      <span className={`badge ${resume.ats_score >= 80 ? 'badge-success' : 'badge-warning'}`}>
                        {resume.ats_score} ATS
                      </span>
                    ) : (
                      <span className="badge badge-primary">Processing</span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Recent Interviews */}
        <div className="glass-card" style={{ padding: '28px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
            <h3 style={{ fontSize: '1.15rem' }}>Recent Interviews</h3>
            <Link to="/interviews/setup" style={{ color: 'var(--primary)', fontSize: '0.85rem', textDecoration: 'none', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '4px' }}>
              Start Interview <ArrowRight size={14} />
            </Link>
          </div>

          {recent_interviews.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '32px 0', color: 'var(--text-dim)' }}>
              <Video size={36} style={{ marginBottom: '8px', opacity: 0.5 }} />
              <p style={{ fontSize: '0.9rem' }}>No mock interviews recorded yet.</p>
              <Link to="/interviews/setup" className="btn btn-primary" style={{ marginTop: '12px', fontSize: '0.85rem' }}>
                <Sparkles size={14} /> Start AI Session
              </Link>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {recent_interviews.map((session) => (
                <div key={session.id} style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '12px 16px',
                  background: 'rgba(255, 255, 255, 0.03)',
                  borderRadius: 'var(--radius-sm)',
                  border: '1px solid var(--border-color)',
                }}>
                  <div>
                    <h4 style={{ fontSize: '0.95rem', fontWeight: 600 }}>{session.role_title}</h4>
                    <span style={{ fontSize: '0.75rem', color: 'var(--text-dim)' }}>
                      {session.difficulty} • {session.date}
                    </span>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    {session.status === 'COMPLETED' ? (
                      <Link to={`/interviews/${session.id}/result`} className="btn btn-secondary" style={{ padding: '6px 12px', fontSize: '0.8rem' }}>
                        Score: {session.overall_score || 0}% <ArrowRight size={12} />
                      </Link>
                    ) : (
                      <Link to={`/interviews/${session.id}`} className="btn btn-primary" style={{ padding: '6px 12px', fontSize: '0.8rem' }}>
                        Continue
                      </Link>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
