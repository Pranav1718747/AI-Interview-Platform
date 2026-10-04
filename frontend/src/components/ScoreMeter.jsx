import React from 'react';

export default function ScoreMeter({ score = 0, size = 120, strokeWidth = 10, label = "Score" }) {
  const normalizedScore = Math.min(100, Math.max(0, Math.round(score)));
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (normalizedScore / 100) * circumference;

  let color = '#ef4444'; // Red
  if (normalizedScore >= 80) {
    color = '#10b981'; // Green
  } else if (normalizedScore >= 65) {
    color = '#6366f1'; // Indigo
  } else if (normalizedScore >= 50) {
    color = '#f59e0b'; // Amber
  }

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      position: 'relative',
      width: `${size}px`,
      height: `${size}px`,
    }}>
      <svg width={size} height={size} style={{ transform: 'rotate(-90deg)' }}>
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="rgba(255, 255, 255, 0.08)"
          strokeWidth={strokeWidth}
          fill="transparent"
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke={color}
          strokeWidth={strokeWidth}
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          strokeLinecap="round"
          fill="transparent"
          style={{ transition: 'stroke-dashoffset 1s ease-in-out, stroke 0.5s ease' }}
        />
      </svg>
      <div style={{
        position: 'absolute',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
      }}>
        <span style={{ fontSize: `${size * 0.26}px`, fontWeight: 800, color: 'var(--text-main)', lineHeight: 1 }}>
          {normalizedScore}
        </span>
        {label && (
          <span style={{ fontSize: `${size * 0.1}px`, fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', marginTop: '3px' }}>
            {label}
          </span>
        )}
      </div>
    </div>
  );
}
