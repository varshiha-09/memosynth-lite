// frontend/src/App.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';

function App() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');
  const [memories, setMemories] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!message.trim()) return;
    setLoading(true);
    setResponse('');
    try {
      const res = await axios.post('http://127.0.0.1:8000/chat', {
        message
      });
      setResponse(res.data.response);
      setMemories(res.data.relevant_memories || []);
    } catch (err) {
      setResponse("Something went wrong. Please try again later.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      minHeight: '100vh',
      background: 'linear-gradient(to bottom, #1f0027, #3a0058, #6a0d78)',
      fontFamily: 'Segoe UI, sans-serif',
      padding: '1rem'
    }}>
      <div style={{
        width: '100%',
        maxWidth: '600px',
        background: 'rgba(255, 255, 255, 0.08)',
        padding: '2rem',
        borderRadius: '16px',
        boxShadow: '0 8px 24px rgba(0, 0, 0, 0.4)',
        backdropFilter: 'blur(10px)',
        border: '1px solid rgba(255, 255, 255, 0.2)'
      }}>
        <h1 style={{
          fontSize: '2rem',
          fontWeight: 'bold',
          marginBottom: '1.5rem',
          textAlign: 'center',
          color: '#ffffff'
        }}>💬 Chat with Memory</h1>

        <textarea
          rows="3"
          style={{
            width: '100%',
            padding: '0.75rem',
            fontSize: '1rem',
            border: '1px solid #aaa',
            borderRadius: '8px',
            outline: 'none',
            resize: 'none',
            background: '#f3f3f3',
            boxShadow: 'inset 0 1px 3px rgba(0,0,0,0.1)'
          }}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Ask something cool..."
        ></textarea>

        <button
          onClick={handleSend}
          style={{
            marginTop: '1rem',
            padding: '0.75rem 1.5rem',
            background: 'linear-gradient(to right, #ff007f, #a200ff)',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            fontWeight: 'bold',
            cursor: 'pointer',
            transition: 'transform 0.1s ease-in-out'
          }}
          onMouseOver={e => e.currentTarget.style.transform = 'scale(1.05)'}
          onMouseOut={e => e.currentTarget.style.transform = 'scale(1)'}
        >
           🚀 Send
        </button>

        {loading && (
          <div style={{
            marginTop: '1.5rem',
            fontStyle: 'italic',
            color: '#d1d5db',
            animation: 'pulse 2s infinite'
          }}>
            🤖 Thinking...
          </div>
        )}

        {!loading && response && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            style={{
              marginTop: '2rem',
              background: 'rgba(255, 255, 255, 0.1)',
              padding: '1rem',
              borderRadius: '8px',
              borderLeft: '5px solid #ff00ff',
              boxShadow: '0 2px 10px rgba(0,0,0,0.3)',
              color: '#fefefe'
            }}
          >
            <h2 style={{ fontSize: '1.2rem', fontWeight: 'bold', marginBottom: '0.5rem', color: '#ff99ff' }}>🤖 Response</h2>
            <p style={{ whiteSpace: 'pre-line' }}>{response}</p>
          </motion.div>
        )}
      </div>
    </div>
  );
}

export default App;