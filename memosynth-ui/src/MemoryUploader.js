import React, { useState } from 'react';
import axios from 'axios';

function MemoryUploader() {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [status, setStatus] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;
    setUploading(true);
    setStatus('Uploading...');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await axios.post('http://127.0.0.1:8000/upload-memory', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      setStatus(res.data.message);
    } catch (err) {
      setStatus('Upload failed.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div style={{
      marginTop: '2rem',
      background: 'rgba(255, 255, 255, 0.08)',
      padding: '1rem',
      borderRadius: '12px',
      color: '#fff'
    }}>
      <h2 style={{ marginBottom: '1rem' }}>📄 Upload Memory File</h2>
      <input type="file" onChange={handleFileChange} style={{ marginBottom: '1rem' }} />
      <br />
      <button onClick={handleUpload} disabled={uploading} style={{
        padding: '0.5rem 1rem',
        background: '#00c2ff',
        border: 'none',
        borderRadius: '6px',
        color: '#000',
        fontWeight: 'bold',
        cursor: 'pointer'
      }}>
        {uploading ? 'Uploading...' : 'Upload'}
      </button>
      <p>{status}</p>
    </div>
  );
}

export default MemoryUploader;
