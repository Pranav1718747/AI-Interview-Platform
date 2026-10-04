import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import client from '../api/client';
import ScoreMeter from '../components/ScoreMeter';
import {
  BarChart3,
  TrendingUp,
  Award,
  Calendar,
  FileText,
  Video,
  ArrowRight,
  Sparkles,
  CheckCircle2
} from 'lucide-react';

export default function AnalyticsPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const res = await client.get('/api/analytics/dashboard/');
        setData(res.data);
      } catch (err) {
        console.error('Failed to load analytics:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchAnalytics();
  }, []);

  if (loading) {
    return (
      <div className="container" style={{ padding: '80px 0', textAlign: 'center' }}>
        <p style={{ color: 'var(--text-muted)' }}>Loading analytics intelligence...</p>
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
    score_history = [],
  } = data || {};

  return (
    <div className="container" style={{ padding: '40px 24px 80px' }}>
      {/* Header */}
      <div style={{ marginBottom: '32px' }}>
        <div className="badge badge-primary" style={{ marginBottom: '8px' }}>
          <BarChart3 size={14} /> Analytics & Growth Trajectory
        </div>
        <h1 style={{ fontSize: '2.4rem', marginBottom: '8px' }}>
          Interview Performance <span className="gradient-text">Insights</span>
        </h1>
        <p style={{ color: 'var(--text-muted)' }}>
          Review aggregate metrics, score progression across sessions, and skill readiness.
        </p>
      </div>

      {/* Top Metrics Row */}
      <div className="grid-3" style={{ marginBottom: '32px' }}>
        <div className="glass-card" style={{ padding: '28px', display: 'flex', alignItems: 'center', gap: '20px' }}>
          <ScoreMeter score={avg_interview_score} size={90} strokeWidth={9} label="Avg Score" />
          <div>
            <h4 style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>Interview Mastery</h4>
            <h2 style={{ fontSize: '1.8rem', marginTop: '4px' }}>{avg_interview_score || '--'}%</h2>
            <span style={{ fontSize: '0.8rem', color: 'var(--accent-emerald)' }}>
              Across {completed_interviews} completed sessions
            </span>
          </div>
        </div>

        <div className="glass-card" style={{ padding: '28px', display: 'flex', alignItems: 'center', gap: '20px' }}>
          <ScoreMeter score={avg_ats_score} size={90} strokeWidth={9} label="Avg ATS" />
          <div>
            <h4 style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>Resume ATS Index</h4>
            <h2 style={{ fontSize: '1.8rem', marginTop: '4px' }}>{avg_ats_score || '--'}%</h2>
            <span style={{ fontSize: '0.8rem', color: 'var(--primary)' }}>
              {total_resumes} resumes analyzed
            </span>
          </div>
        </div>

        <div className="glass-card" style={{ padding: '28px', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
          <h4 style={{ fontSize: '0.9rem', color: 'var(--text-muted)', marginBottom: '8px' }}>Practice Completion Rate</h4>
          <h2 style={{ fontSize: '2rem' }}>
            {total_interviews > 0 ? Math.round((completed_interviews / total_interviews) * 100) : 0}%
          </h2>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-dim)', marginTop: '4px' }}>
            {completed_interviews} finished out of {total_interviews} started
          </span>
        </div>
      </div>

      {/* Historical Progression Table */}
      <div className="glass-card" style={{ padding: '32px', marginBottom: '36px' }}>
        <h3 style={{ fontSize: '1.25rem', marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <TrendingUp size={20} color="var(--primary)" /> Session Performance History
        </h3>

        {score_history.length === 0 ? (
          <p style={{ color: 'var(--text-dim)', textAlign: 'center', padding: '32px 0' }}>
            Complete your first AI mock interview to generate performance history.
          </p>
        ) : (
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.9rem' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid var(--border-color)', color: 'var(--text-muted)' }}>
                  <th style={{ padding: '12px 16px' }}>Session / Role</th>
                  <th style={{ padding: '12px 16px' }}>Date</th>
                  <th style={{ padding: '12px 16px' }}>Technical</th>
                  <th style={{ padding: '12px 16px' }}>Communication</th>
                  <th style={{ padding: '12px 16px' }}>Problem Solving</th>
                  <th style={{ padding: '12px 16px' }}>Overall Score</th>
                  <th style={{ padding: '12px 16px', textAlign: 'right' }}>Action</th>
                </tr>
              </thead>
              <tbody>
                {score_history.map((s) => (
                  <tr key={s.id} style={{ borderBottom: '1px solid var(--border-color)' }}>
                    <td style={{ padding: '14px 16px', fontWeight: 600 }}>
                      {s.role_title} <span className="badge badge-primary" style={{ fontSize: '0.7rem', marginLeft: '6px' }}>{s.difficulty}</span>
                    </td>
                    <td style={{ padding: '14px 16px', color: 'var(--text-muted)' }}>{s.date}</td>
                    <td style={{ padding: '14px 16px', color: 'var(--accent-cyan)' }}>{s.technical}%</td>
                    <td style={{ padding: '14px 16px', color: 'var(--accent-emerald)' }}>{s.communication}%</td>
                    <td style={{ padding: '14px 16px', color: 'var(--accent-amber)' }}>{s.problem_solving}%</td>
                    <td style={{ padding: '14px 16px' }}>
                      <span className={`badge ${s.overall_score >= 80 ? 'badge-success' : 'badge-warning'}`}>
                        {s.overall_score}%
                      </span>
                    </td>
                    <td style={{ padding: '14px 16px', textAlign: 'right' }}>
                      <Link to={`/interviews/${s.id}/result`} className="btn btn-secondary" style={{ padding: '6px 12px', fontSize: '0.8rem' }}>
                        View Scorecard <ArrowRight size={12} />
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
