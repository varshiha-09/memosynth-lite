// frontend/src/App.js
import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');

  const handleSend = async () => {
    try {
      const res = await axios.post('http://127.0.0.1:8000/chat', {
        message
      });
      setResponse(res.data.response);
    } catch (err) {
      alert("Error: " + err.message);
    }
  };

  return (
    <div style={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      minHeight: '100vh',
      background: 'linear-gradient(to right, #4facfe, #00f2fe)',
      fontFamily: 'Segoe UI, sans-serif'
    }}>
      <div style={{
        width: '100%',
        maxWidth: '600px',
        background: 'white',
        padding: '2rem',
        borderRadius: '16px',
        boxShadow: '0 8px 24px rgba(0, 0, 0, 0.15)',
        transition: 'transform 0.2s ease-in-out'
      }}>
        <h1 style={{
          fontSize: '2rem',
          fontWeight: 'bold',
          marginBottom: '1.5rem',
          textAlign: 'center',
          color: '#1e3a8a'
        }}>💬 Chat with Memory</h1>

        <textarea
          rows="3"
          style={{
            width: '100%',
            padding: '0.75rem',
            fontSize: '1rem',
            border: '1px solid #ccc',
            borderRadius: '8px',
            outline: 'none',
            resize: 'none',
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
            background: 'linear-gradient(to right, #667eea, #764ba2)',
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

        {response && (
          <div style={{
            marginTop: '2rem',
            background: '#f0f4ff',
            padding: '1rem',
            borderRadius: '8px',
            borderLeft: '5px solid #6366f1'
          }}>
            <h2 style={{ fontSize: '1.2rem', fontWeight: 'bold', marginBottom: '0.5rem' }}>🤖 Response</h2>
            <p>{response}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
