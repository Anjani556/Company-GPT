import React, { useState } from 'react';
import './App.css';

interface Message {
  question: string;
  answer: string;
}

const App = (): React.JSX.Element => {
  const [question, setQuestion] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  const [uploading, setUploading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState('');

  const askQuestion = async () => {
    if (!question.trim()) return;
    const currentQuestion = question;
    setQuestion('');
    setLoading(true);

    try {
      const res = await fetch('http://127.0.0.1:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: currentQuestion }),
      });
      const data = await res.json();
      setMessages((prev) => [...prev, { question: currentQuestion, answer: data.answer }]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { question: currentQuestion, answer: 'Error connecting to backend.' },
      ]);
    }
    setLoading(false);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      askQuestion();
    }
  };

  const uploadFile = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    setUploadMessage('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch('http://127.0.0.1:8000/upload', {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      setUploadMessage(data.message);
    } catch (err) {
      setUploadMessage('Upload failed. Check backend connection.');
    }
    setUploading(false);
    e.target.value = '';
  };

  return (
    <div className="app-container">
      <h1>Company GPT</h1>

      <div className="upload-section">
        <input type="file" accept=".pdf" onChange={uploadFile} disabled={uploading} />
        {uploading && <p className="upload-status">Uploading...</p>}
        {uploadMessage && <p className="upload-status">{uploadMessage}</p>}
      </div>

      <div className="chat-window">
        {messages.map((msg, index) => (
          <div key={index} className="message-pair">
            <p className="user-msg">{msg.question}</p>
            <p className="bot-msg">{msg.answer}</p>
          </div>
        ))}
        {loading && <p className="bot-msg">Thinking...</p>}
      </div>

      <div className="input-row">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask a question about company policy..."
        />
        <button onClick={askQuestion} disabled={loading}>
          Ask
        </button>
      </div>
    </div>
  );
};

export default App;