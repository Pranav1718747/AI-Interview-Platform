import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import client from '../api/client';
import ScoreMeter from '../components/ScoreMeter';
import {
  FileText,
  Upload,
  Trash2,
  RefreshCw,
  CheckCircle,
  AlertCircle,
  Sparkles,
  Video,
  X,
  Plus,
  Tag,
  Briefcase
} from 'lucide-react';

export default function ResumeManagerPage() {
  const [resumes, setResumes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [selectedAnalysis, setSelectedAnalysis] = useState(null);
  const [title, setTitle] = useState('');
  const [file, setFile] = useState(null);
  const [error, setError] = useState('');
  const fileInputRef = useRef(null);
  const navigate = useNavigate();

  const fetchResumes = async () => {
    try {
      const res = await client.get('/api/resumes/');
      setResumes(res.data);
    } catch (err) {
      console.error('Failed to load resumes:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchResumes();
  }, []);

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (selected) {
      setFile(selected);
      if (!title) {
        // Auto-fill title from filename
        const cleanName = selected.name.replace(/\.[^/.]+$/, '').replace(/[_-]/g, ' ');
        setTitle(cleanName);
      }
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a resume file (.pdf, .docx, .txt)');
      return;
    }

    setError('');
    setUploading(true);

    const formData = new FormData();
    formData.append('title', title || file.name);
    formData.append('resume', file);

    try {
      const res = await client.post('/api/resumes/', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setTitle('');
      setFile(null);
      if (fileInputRef.current) fileInputRef.current.value = '';
      await fetchResumes();
      
      if (res.data.warning) {
        setError(res.data.warning);
      } else if (res.data.analysis) {
        setSelectedAnalysis(res.data);
      }
    } catch (err) {
      setError(
        err.response?.data?.error ||
        err.response?.data?.resume?.[0] ||
        'Upload failed. Please verify the file.'
      );
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (id, e) => {
    e.stopPropagation();
    if (window.confirm('Are you sure you want to delete this resume?')) {
      try {
        await client.delete(`/api/resumes/${id}/`);
        setResumes(resumes.filter((r) => r.id !== id));
        if (selectedAnalysis?.id === id) setSelectedAnalysis(null);
      } catch (err) {
        console.error('Failed to delete resume:', err);
      }
    }
  };

  const handleReanalyze = async (id, e) => {
    e.stopPropagation();
    setError('');
    try {
      const res = await client.post(`/api/resumes/${id}/analyze/`);
      setResumes(resumes.map((r) => (r.id === id ? res.data : r)));
      if (selectedAnalysis?.id === id) {
        setSelectedAnalysis(res.data);
      }
    } catch (err) {
      setError(
        err.response?.data?.error ||
        'OpenRouter LLM failed to analyze resume. Check your API key/credits.'
      );
    }
  };

  const startInterviewWithResume = (resumeId) => {
    navigate('/interviews/setup', { state: { selectedResumeId: resumeId } });
  };

  return (
    <div className="container" style={{ padding: '40px 24px 80px' }}>
      {/* Header */}
      <div style={{ marginBottom: '32px' }}>
        <h1 style={{ fontSize: '2.2rem', marginBottom: '8px' }}>
          Resume <span className="gradient-text">ATS Intelligence</span>
        </h1>
        <p style={{ color: 'var(--text-muted)' }}>
          Upload your resume to extract skills, compute ATS matching score, and detect strengths and keyword gaps.
        </p>
      </div>

      {/* Upload Box */}
      <div className="glass-card" style={{ padding: '32px', marginBottom: '40px' }}>
        <h3 style={{ fontSize: '1.2rem', marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Upload size={20} color="var(--primary)" /> Upload New Resume
        </h3>

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

        <form onSubmit={handleUpload}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr auto', gap: '16px', alignItems: 'end' }}>
            <div className="form-group" style={{ marginBottom: 0 }}>
              <label className="form-label">Resume Title / Label</label>
              <input
                type="text"
                className="form-control"
                placeholder="e.g. Senior Backend Python Resume"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
              />
            </div>

            <div className="form-group" style={{ marginBottom: 0 }}>
              <label className="form-label">Select File (.pdf, .docx, .txt)</label>
              <input
                type="file"
                ref={fileInputRef}
                className="form-control"
                accept=".pdf,.docx,.doc,.txt"
                onChange={handleFileChange}
                required
              />
            </div>

            <button
              type="submit"
              className="btn btn-primary"
              style={{ height: '46px', padding: '0 24px' }}
              disabled={uploading}
            >
              {uploading ? (
                <>
                  <RefreshCw size={16} className="pulse-animation" /> Scanning ATS...
                </>
              ) : (
                <>
                  <Sparkles size={16} /> Upload & Analyze
                </>
              )}
            </button>
          </div>
        </form>
      </div>

      {/* Resumes List */}
      <div>
        <h2 style={{ fontSize: '1.4rem', marginBottom: '20px' }}>Your Uploaded Resumes ({resumes.length})</h2>

        {loading ? (
          <p style={{ color: 'var(--text-muted)' }}>Loading resumes...</p>
        ) : resumes.length === 0 ? (
          <div className="glass-card" style={{ padding: '48px 24px', textAlign: 'center', color: 'var(--text-dim)' }}>
            <FileText size={48} style={{ marginBottom: '12px', opacity: 0.4 }} />
            <p style={{ fontSize: '1rem', marginBottom: '12px' }}>No resumes uploaded yet.</p>
            <p style={{ fontSize: '0.85rem' }}>Upload your first resume above to get automated ATS scoring and skill extraction.</p>
          </div>
        ) : (
          <div className="grid-2">
            {resumes.map((resume) => {
              const analysis = resume.analysis;
              const atsScore = analysis?.ats_score || 0;

              return (
                <div
                  key={resume.id}
                  className="glass-card"
                  style={{
                    padding: '24px',
                    cursor: 'pointer',
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'space-between',
                  }}
                  onClick={() => setSelectedAnalysis(resume)}
                >
                  <div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '16px' }}>
                      <div style={{ display: 'flex', gap: '14px', alignItems: 'center' }}>
                        <div style={{
                          width: '44px',
                          height: '44px',
                          borderRadius: '10px',
                          background: 'rgba(99, 102, 241, 0.15)',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          color: 'var(--primary)',
                        }}>
                          <FileText size={24} />
                        </div>
                        <div>
                          <h3 style={{ fontSize: '1.1rem', fontWeight: 700 }}>{resume.title}</h3>
                          <span style={{ fontSize: '0.8rem', color: 'var(--text-dim)' }}>
                            Uploaded {new Date(resume.uploaded_at).toLocaleDateString()}
                          </span>
                        </div>
                      </div>

                      {analysis ? (
                        <ScoreMeter score={atsScore} size={64} strokeWidth={6} label="ATS" />
                      ) : (
                        <span className="badge badge-warning">Pending</span>
                      )}
                    </div>

                    {analysis?.summary && (
                      <p style={{
                        fontSize: '0.875rem',
                        color: 'var(--text-muted)',
                        lineHeight: 1.5,
                        marginBottom: '16px',
                        display: '-webkit-box',
                        WebkitLineClamp: 2,
                        WebkitBoxOrient: 'vertical',
                        overflow: 'hidden',
                      }}>
                        {analysis.summary}
                      </p>
                    )}

                    {/* Skill Pills preview */}
                    {analysis?.skills && analysis.skills.length > 0 && (
                      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', marginBottom: '20px' }}>
                        {analysis.skills.slice(0, 5).map((skill, i) => (
                          <span key={i} className="pill" style={{ fontSize: '0.75rem', padding: '3px 8px' }}>
                            {skill}
                          </span>
                        ))}
                        {analysis.skills.length > 5 && (
                          <span className="pill" style={{ fontSize: '0.75rem', padding: '3px 8px', color: 'var(--primary)' }}>
                            +{analysis.skills.length - 5} more
                          </span>
                        )}
                      </div>
                    )}
                  </div>

                  {/* Actions Footer */}
                  <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    paddingTop: '16px',
                    borderTop: '1px solid var(--border-color)',
                  }}>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        startInterviewWithResume(resume.id);
                      }}
                      className="btn btn-primary"
                      style={{ padding: '6px 14px', fontSize: '0.8rem' }}
                    >
                      <Video size={14} /> Practice Mock
                    </button>

                    <div style={{ display: 'flex', gap: '8px' }}>
                      <button
                        onClick={(e) => handleReanalyze(resume.id, e)}
                        className="btn btn-secondary"
                        style={{ padding: '6px 10px', fontSize: '0.8rem' }}
                        title="Re-run AI Analysis"
                      >
                        <RefreshCw size={14} />
                      </button>
                      <button
                        onClick={(e) => handleDelete(resume.id, e)}
                        className="btn btn-danger"
                        style={{ padding: '6px 10px', fontSize: '0.8rem' }}
                        title="Delete resume"
                      >
                        <Trash2 size={14} />
                      </button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Full ATS Analysis Modal */}
      {selectedAnalysis && (
        <div className="modal-backdrop" onClick={() => setSelectedAnalysis(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
              <div>
                <span className="badge badge-primary" style={{ marginBottom: '6px' }}>ATS Audit Report</span>
                <h2 style={{ fontSize: '1.5rem' }}>{selectedAnalysis.title}</h2>
              </div>
              <button
                onClick={() => setSelectedAnalysis(null)}
                style={{
                  background: 'transparent',
                  border: 'none',
                  color: 'var(--text-muted)',
                  cursor: 'pointer',
                  padding: '4px',
                }}
              >
                <X size={24} />
              </button>
            </div>

            {selectedAnalysis.analysis ? (
              <div>
                {/* Score & Summary Top Grid */}
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '24px',
                  background: 'rgba(255, 255, 255, 0.02)',
                  padding: '20px',
                  borderRadius: 'var(--radius-md)',
                  border: '1px solid var(--border-color)',
                  marginBottom: '24px',
                  flexWrap: 'wrap',
                }}>
                  <ScoreMeter score={selectedAnalysis.analysis.ats_score} size={110} strokeWidth={10} label="ATS Score" />
                  <div style={{ flex: 1, minWidth: '240px' }}>
                    <h4 style={{ fontSize: '1rem', color: 'var(--text-muted)', marginBottom: '6px' }}>Executive Summary</h4>
                    <p style={{ fontSize: '0.95rem', lineHeight: 1.6 }}>{selectedAnalysis.analysis.summary}</p>
                  </div>
                </div>

                {/* Suggested Roles */}
                {selectedAnalysis.analysis.suggested_roles?.length > 0 && (
                  <div style={{ marginBottom: '24px' }}>
                    <h4 style={{ fontSize: '0.95rem', color: 'var(--accent-cyan)', marginBottom: '10px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                      <Briefcase size={16} /> Recommended Matching Roles
                    </h4>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                      {selectedAnalysis.analysis.suggested_roles.map((role, i) => (
                        <span key={i} className="badge badge-primary" style={{ textTransform: 'none', fontSize: '0.85rem' }}>
                          {role}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Technical Skills */}
                <div style={{ marginBottom: '24px' }}>
                  <h4 style={{ fontSize: '0.95rem', color: 'var(--text-muted)', marginBottom: '10px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <Tag size={16} /> Verified Technical Skills
                  </h4>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                    {selectedAnalysis.analysis.skills.map((skill, i) => (
                      <span key={i} className="pill" style={{ background: 'rgba(99, 102, 241, 0.1)', borderColor: 'rgba(99, 102, 241, 0.3)', color: '#a5b4fc' }}>
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Strengths & Weaknesses 2-Column Grid */}
                <div className="grid-2" style={{ marginBottom: '28px' }}>
                  {/* Strengths */}
                  <div style={{
                    background: 'rgba(16, 185, 129, 0.05)',
                    border: '1px solid rgba(16, 185, 129, 0.2)',
                    padding: '20px',
                    borderRadius: 'var(--radius-md)',
                  }}>
                    <h4 style={{ color: '#6ee7b7', fontSize: '1rem', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <CheckCircle size={18} /> Key Strengths
                    </h4>
                    <ul style={{ paddingLeft: '20px', color: 'var(--text-muted)', fontSize: '0.9rem', lineHeight: 1.6 }}>
                      {selectedAnalysis.analysis.strengths.map((str, i) => (
                        <li key={i} style={{ marginBottom: '6px' }}>{str}</li>
                      ))}
                    </ul>
                  </div>

                  {/* Weaknesses / Improvements */}
                  <div style={{
                    background: 'rgba(244, 63, 94, 0.05)',
                    border: '1px solid rgba(244, 63, 94, 0.2)',
                    padding: '20px',
                    borderRadius: 'var(--radius-md)',
                  }}>
                    <h4 style={{ color: '#fda4af', fontSize: '1rem', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px' }}>
                      <AlertCircle size={18} /> Gaps & Improvement Areas
                    </h4>
                    <ul style={{ paddingLeft: '20px', color: 'var(--text-muted)', fontSize: '0.9rem', lineHeight: 1.6 }}>
                      {selectedAnalysis.analysis.weaknesses.map((weak, i) => (
                        <li key={i} style={{ marginBottom: '6px' }}>{weak}</li>
                      ))}
                    </ul>
                  </div>
                </div>

                {/* Missing Keywords */}
                {selectedAnalysis.analysis.missing_keywords?.length > 0 && (
                  <div style={{
                    background: 'rgba(245, 158, 11, 0.05)',
                    border: '1px solid rgba(245, 158, 11, 0.2)',
                    padding: '16px 20px',
                    borderRadius: 'var(--radius-md)',
                    marginBottom: '28px',
                  }}>
                    <h4 style={{ color: '#fcd34d', fontSize: '0.9rem', marginBottom: '8px' }}>
                      High-Value Missing Keywords for ATS Optimization:
                    </h4>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                      {selectedAnalysis.analysis.missing_keywords.map((kw, i) => (
                        <span key={i} className="pill" style={{ borderColor: 'rgba(245, 158, 11, 0.3)', color: '#fcd34d', fontSize: '0.8rem' }}>
                          + {kw}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Modal CTA */}
                <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '12px' }}>
                  <button onClick={() => setSelectedAnalysis(null)} className="btn btn-secondary">
                    Close
                  </button>
                  <button
                    onClick={() => {
                      startInterviewWithResume(selectedAnalysis.id);
                    }}
                    className="btn btn-primary"
                  >
                    <Video size={16} /> Launch Mock Interview for this Resume
                  </button>
                </div>
              </div>
            ) : (
              <div style={{ textAlign: 'center', padding: '32px 0' }}>
                <p style={{ color: 'var(--text-muted)', marginBottom: '16px' }}>No analysis generated yet.</p>
                <button
                  onClick={() => handleReanalyze(selectedAnalysis.id)}
                  className="btn btn-primary"
                >
                  <Sparkles size={16} /> Run ATS Analysis
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
