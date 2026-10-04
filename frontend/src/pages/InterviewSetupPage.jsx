import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import client from '../api/client';
import { Video, Sparkles, AlertCircle, ArrowRight, Brain, Briefcase, Layers } from 'lucide-react';

const COMMON_ROLES = [
  'Full Stack Software Engineer',
  'Python / Django Backend Engineer',
  'Frontend React Developer',
  'Senior DevOps & Cloud Architect',
  'Machine Learning / AI Engineer',
  'Data Engineer / SQL Specialist',
];

export default function InterviewSetupPage() {
  const location = useLocation();
  const navigate = useNavigate();

  const [resumes, setResumes] = useState([]);
  const [roleTitle, setRoleTitle] = useState('');
  const [difficulty, setDifficulty] = useState('MID');
  const [interviewType, setInterviewType] = useState('MIXED');
  const [selectedResumeId, setSelectedResumeId] = useState(
    location.state?.selectedResumeId || ''
  );
  const [jobDescription, setJobDescription] = useState('');
  const [questionCount, setQuestionCount] = useState(5);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchResumes = async () => {
      try {
        const res = await client.get('/api/resumes/');
        setResumes(res.data);
      } catch (err) {
        console.error('Failed to load resumes:', err);
      }
    };
    fetchResumes();
  }, []);

  const handleStart = async (e) => {
    e.preventDefault();
    if (!roleTitle.trim()) {
      setError('Please specify the target job role.');
      return;
    }

    setError('');
    setLoading(true);

    try {
      const payload = {
        role_title: roleTitle.trim(),
        difficulty,
        interview_type: interviewType,
        resume_id: selectedResumeId ? parseInt(selectedResumeId) : null,
        job_description: jobDescription.trim(),
        question_count: questionCount,
      };

      const res = await client.post('/api/interviews/start/', payload);
      navigate(`/interviews/${res.data.id}`);
    } catch (err) {
      setError(
        err.response?.data?.error ||
        err.response?.data?.detail ||
        'Failed to generate interview. Please try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container" style={{ padding: '40px 24px 80px', maxWidth: '840px' }}>
      <div style={{ marginBottom: '32px', textAlign: 'center' }}>
        <div className="badge badge-primary" style={{ marginBottom: '12px' }}>
          <Sparkles size={14} /> AI Mock Interview Setup
        </div>
        <h1 style={{ fontSize: '2.4rem', marginBottom: '8px' }}>
          Configure Your <span className="gradient-text">Interview Simulation</span>
        </h1>
        <p style={{ color: 'var(--text-muted)' }}>
          Customize the target role, seniority level, and question focus for a tailored practice session.
        </p>
      </div>

      <div className="glass-card" style={{ padding: '36px' }}>
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
            marginBottom: '24px',
          }}>
            <AlertCircle size={18} />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleStart}>
          {/* Target Role Input */}
          <div className="form-group">
            <label className="form-label" style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <Briefcase size={16} color="var(--primary)" /> Target Job Title / Position
            </label>
            <input
              type="text"
              className="form-control"
              placeholder="e.g. Senior Backend Engineer"
              value={roleTitle}
              onChange={(e) => setRoleTitle(e.target.value)}
              required
            />
            {/* Quick Select Role Pills */}
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginTop: '8px' }}>
              {COMMON_ROLES.map((role) => (
                <button
                  key={role}
                  type="button"
                  onClick={() => setRoleTitle(role)}
                  className="pill"
                  style={{
                    cursor: 'pointer',
                    fontSize: '0.78rem',
                    background: roleTitle === role ? 'rgba(99, 102, 241, 0.2)' : 'rgba(255, 255, 255, 0.03)',
                    borderColor: roleTitle === role ? 'var(--primary)' : 'var(--border-color)',
                    color: roleTitle === role ? '#fff' : 'var(--text-muted)',
                  }}
                >
                  {role}
                </button>
              ))}
            </div>
          </div>

          {/* Difficulty & Interview Type (2-Column) */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginTop: '16px' }}>
            <div className="form-group">
              <label className="form-label">Experience & Seniority</label>
              <select
                className="form-control"
                value={difficulty}
                onChange={(e) => setDifficulty(e.target.value)}
              >
                <option value="ENTRY">Entry-Level / Junior (0 - 2 yrs)</option>
                <option value="MID">Mid-Level (2 - 5 yrs)</option>
                <option value="SENIOR">Senior (5 - 8+ yrs)</option>
                <option value="LEAD">Staff / Lead / Principal</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">Interview Style</label>
              <select
                className="form-control"
                value={interviewType}
                onChange={(e) => setInterviewType(e.target.value)}
              >
                <option value="MIXED">Mixed (Technical & Behavioral)</option>
                <option value="TECHNICAL">Pure Technical & Architecture</option>
                <option value="BEHAVIORAL">Behavioral & Cultural (STAR)</option>
                <option value="SYSTEM_DESIGN">System Design & Scale</option>
              </select>
            </div>
          </div>

          {/* Resume Picker */}
          <div className="form-group" style={{ marginTop: '8px' }}>
            <label className="form-label">Link Resume Context (Optional)</label>
            <select
              className="form-control"
              value={selectedResumeId}
              onChange={(e) => setSelectedResumeId(e.target.value)}
            >
              <option value="">-- Practice without specific resume --</option>
              {resumes.map((r) => (
                <option key={r.id} value={r.id}>
                  {r.title} {r.analysis ? `(ATS Score: ${r.analysis.ats_score})` : ''}
                </option>
              ))}
            </select>
            <span style={{ fontSize: '0.78rem', color: 'var(--text-dim)', marginTop: '4px' }}>
              The AI interviewer will customize technical questions based on projects and skills listed in your resume.
            </span>
          </div>

          {/* Job Description Optional Box */}
          <div className="form-group" style={{ marginTop: '12px' }}>
            <label className="form-label">Specific Job Posting / Description (Optional)</label>
            <textarea
              className="form-control"
              placeholder="Paste specific job requirements or responsibilities here to simulate an interview for that exact company..."
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              rows={3}
            />
          </div>

          {/* Question Count */}
          <div className="form-group" style={{ marginTop: '12px' }}>
            <label className="form-label">Question Count</label>
            <div style={{ display: 'flex', gap: '12px' }}>
              {[3, 5, 7].map((num) => (
                <button
                  key={num}
                  type="button"
                  onClick={() => setQuestionCount(num)}
                  className={`btn ${questionCount === num ? 'btn-primary' : 'btn-secondary'}`}
                  style={{ flex: 1, padding: '10px' }}
                >
                  {num} Questions ({num * 3} mins)
                </button>
              ))}
            </div>
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            className="btn btn-primary"
            style={{ width: '100%', marginTop: '24px', padding: '14px', fontSize: '1.05rem' }}
            disabled={loading}
          >
            {loading ? (
              <>
                <Sparkles size={18} className="pulse-animation" /> Crafting Personalized Questions with AI...
              </>
            ) : (
              <>
                <Video size={18} /> Launch AI Interview Simulation <ArrowRight size={16} />
              </>
            )}
          </button>
        </form>
      </div>
    </div>
  );
}
