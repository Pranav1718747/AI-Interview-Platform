import React, { useRef, useEffect, useState } from 'react';
import { Camera, CameraOff, Mic, MicOff } from 'lucide-react';

export default function CameraPreview() {
  const videoRef = useRef(null);
  const [isVideoOn, setIsVideoOn] = useState(false);
  const [stream, setStream] = useState(null);
  const [hasPermissionError, setHasPermissionError] = useState(false);

  const startCamera = async () => {
    try {
      setHasPermissionError(false);
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: true,
        audio: false,
      });
      setStream(mediaStream);
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
      setIsVideoOn(true);
    } catch (err) {
      console.warn("Camera access denied or unavailable:", err);
      setHasPermissionError(true);
      setIsVideoOn(false);
    }
  };

  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach((track) => track.stop());
      setStream(null);
    }
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
    setIsVideoOn(false);
  };

  const toggleCamera = () => {
    if (isVideoOn) {
      stopCamera();
    } else {
      startCamera();
    }
  };

  useEffect(() => {
    return () => {
      if (stream) {
        stream.getTracks().forEach((track) => track.stop());
      }
    };
  }, [stream]);

  return (
    <div style={{
      position: 'relative',
      width: '100%',
      aspectRatio: '16 / 10',
      background: 'rgba(0, 0, 0, 0.4)',
      borderRadius: 'var(--radius-md)',
      overflow: 'hidden',
      border: '1px solid var(--border-color)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
    }}>
      <video
        ref={videoRef}
        autoPlay
        playsInline
        muted
        style={{
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          display: isVideoOn ? 'block' : 'none',
          transform: 'scaleX(-1)', // mirror view
        }}
      />

      {!isVideoOn && (
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: '8px',
          color: 'var(--text-dim)',
          textAlign: 'center',
          padding: '20px',
        }}>
          <CameraOff size={36} />
          <span style={{ fontSize: '0.85rem' }}>
            {hasPermissionError ? 'Camera access not available' : 'Camera is off (Optional)'}
          </span>
        </div>
      )}

      {/* Floating control */}
      <div style={{
        position: 'absolute',
        bottom: '12px',
        right: '12px',
        zIndex: 10,
      }}>
        <button
          onClick={toggleCamera}
          className="btn btn-secondary"
          style={{
            padding: '6px 12px',
            fontSize: '0.8rem',
            background: 'rgba(10, 13, 20, 0.8)',
            backdropFilter: 'blur(8px)',
          }}
          type="button"
        >
          {isVideoOn ? <><CameraOff size={14} /> Turn Off</> : <><Camera size={14} /> Turn On</>}
        </button>
      </div>
    </div>
  );
}
