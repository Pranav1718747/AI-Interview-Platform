import React from 'react';
import ReactMarkdown from 'react-markdown';

export default function MarkdownView({ content }) {
  if (!content) return null;

  return (
    <div className="markdown-content" style={{ fontSize: '0.95rem', lineHeight: 1.7, color: 'var(--text-main)' }}>
      <ReactMarkdown
        components={{
          h3: ({ node, ...props }) => (
            <h3 style={{ fontSize: '1.08rem', color: 'var(--accent-cyan)', marginTop: '16px', marginBottom: '8px', fontWeight: 700 }} {...props} />
          ),
          h4: ({ node, ...props }) => (
            <h4 style={{ fontSize: '1rem', color: '#a5b4fc', marginTop: '14px', marginBottom: '6px', fontWeight: 600 }} {...props} />
          ),
          p: ({ node, ...props }) => (
            <p style={{ marginBottom: '12px', color: 'var(--text-muted)' }} {...props} />
          ),
          ul: ({ node, ...props }) => (
            <ul style={{ paddingLeft: '22px', marginBottom: '14px', color: 'var(--text-muted)' }} {...props} />
          ),
          ol: ({ node, ...props }) => (
            <ol style={{ paddingLeft: '22px', marginBottom: '14px', color: 'var(--text-muted)' }} {...props} />
          ),
          li: ({ node, ...props }) => (
            <li style={{ marginBottom: '6px' }} {...props} />
          ),
          strong: ({ node, ...props }) => (
            <strong style={{ color: 'var(--text-main)', fontWeight: 700 }} {...props} />
          ),
          code: ({ node, inline, ...props }) => (
            <code style={{
              background: 'rgba(255, 255, 255, 0.08)',
              padding: '2px 6px',
              borderRadius: '4px',
              fontSize: '0.85em',
              color: '#38bdf8'
            }} {...props} />
          ),
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}
