import React, { useState } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';

function App() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [tab, setTab] = useState('chat');
  const [manualSummaries, setManualSummaries] = useState('');
  const [uploadStatus, setUploadStatus] = useState('');

  const handleSend = async () => {
    if (!message.trim()) return;
    setLoading(true);
    setResponse('');
    try {
      const res = await axios.post('http://127.0.0.1:8000/chat', { message });
      setResponse(res.data.response);
    } catch (err) {
      setResponse("Something went wrong. Please try again later.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleManualSubmit = async () => {
    const summaries = manualSummaries
      .split('\n')
      .map(s => s.trim())
      .filter(s => s.length > 0);

    if (summaries.length === 0) return;

    try {
      const res = await axios.post('http://127.0.0.1:8000/add_memories', { summaries });
      setUploadStatus(`Added ${res.data.memories_created} memory items.`);
      setManualSummaries('');
    } catch (err) {
      setUploadStatus("Failed to upload memories.");
      console.error(err);
    }
  };

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      minHeight: '100vh',
      background: 'linear-gradient(to bottom, #1f0027, #3a0058, #6a0d78)',
      fontFamily: 'Segoe UI, sans-serif',
      padding: '1rem'
    }}>
      <div style={{ display: 'flex', gap: '1rem', marginBottom: '2rem' }}>
        <button onClick={() => setTab('chat')} style={tabStyle(tab === 'chat')}>Chat with Memory</button>
        <button onClick={() => setTab('upload')} style={tabStyle(tab === 'upload')}>What should I remember?</button>
      </div>

      {tab === 'chat' && (
        <div style={cardStyle}>
          <h1 style={headerStyle}>Chat with Memory</h1>
          <textarea
            rows="3"
            style={textAreaStyle}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Ask something..."
          />
          <button onClick={handleSend} style={buttonStyle}>Send</button>

          {loading && <div style={thinkingStyle}>Thinking...</div>}

          {!loading && response && (
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }} style={responseStyle}>
              <h2 style={responseHeaderStyle}> Response</h2>
              <p style={{ whiteSpace: 'pre-line' }}>{response}</p>
            </motion.div>
          )}
        </div>
      )}

      {tab === 'upload' && (
        <div style={cardStyle}>
          <h2 style={{ textAlign: 'center', marginBottom: '1rem', color: 'white' }}>What should I remember?</h2>
          <textarea
            rows="6"
            style={textAreaStyle}
            placeholder="Enter one memory summary per line..."
            value={manualSummaries}
            onChange={(e) => setManualSummaries(e.target.value)}
          />
          <button onClick={handleManualSubmit} style={buttonStyle}>Save Memories</button>
          {uploadStatus && <p style={{ marginTop: '1rem', color: 'lightgreen' }}>{uploadStatus}</p>}
        </div>
      )}
    </div>
  );
}

const tabStyle = (active) => ({
  padding: '0.5rem 1rem',
  background: active ? '#a200ff' : '#444',
  color: 'white',
  border: 'none',
  borderRadius: '8px',
  cursor: 'pointer'
});

const cardStyle = {
  width: '100%',
  maxWidth: '600px',
  background: 'rgba(255, 255, 255, 0.08)',
  padding: '2rem',
  borderRadius: '16px',
  boxShadow: '0 8px 24px rgba(0, 0, 0, 0.4)',
  backdropFilter: 'blur(10px)',
  border: '1px solid rgba(255, 255, 255, 0.2)',
  color: 'white'
};

const headerStyle = {
  fontSize: '2rem',
  fontWeight: 'bold',
  marginBottom: '1.5rem',
  textAlign: 'center',
  color: '#ffffff'
};

const textAreaStyle = {
  width: '100%',
  padding: '0.75rem',
  fontSize: '1rem',
  border: '1px solid #aaa',
  borderRadius: '8px',
  outline: 'none',
  resize: 'none',
  background: '#f3f3f3',
  boxShadow: 'inset 0 1px 3px rgba(0,0,0,0.1)'
};

const buttonStyle = {
  marginTop: '1rem',
  padding: '0.75rem 1.5rem',
  background: 'linear-gradient(to right, #ff007f, #a200ff)',
  color: 'white',
  border: 'none',
  borderRadius: '8px',
  fontWeight: 'bold',
  cursor: 'pointer',
  transition: 'transform 0.1s ease-in-out'
};

const thinkingStyle = {
  marginTop: '1.5rem',
  fontStyle: 'italic',
  color: '#d1d5db',
  animation: 'pulse 2s infinite'
};

const responseStyle = {
  marginTop: '2rem',
  background: 'rgba(255, 255, 255, 0.1)',
  padding: '1rem',
  borderRadius: '8px',
  borderLeft: '5px solid #ff00ff',
  boxShadow: '0 2px 10px rgba(0,0,0,0.3)',
  color: '#fefefe'
};

const responseHeaderStyle = {
  fontSize: '1.2rem',
  fontWeight: 'bold',
  marginBottom: '0.5rem',
  color: '#ff99ff'
};

export default App;
