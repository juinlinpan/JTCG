import React, { useState, useEffect, useRef } from 'react';
import './App.css';
import api from './services/api';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    // 載入歷史消息
    fetchMessages();
  }, []);

  useEffect(() => {
    // 消息列表滾動到底部
    scrollToBottom();
  }, [messages]);

  const fetchMessages = async () => {
    try {
      const response = await api.getMessages();
      setMessages(response.data);
    } catch (error) {
      console.error('無法載入消息:', error);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (input.trim() === '') return;

    const userMessage = {
      content: input,
      role: 'user'
    };

    setMessages([...messages, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await api.sendMessage(userMessage);
      setMessages(prevMessages => [...prevMessages, response.data]);
    } catch (error) {
      console.error('發送消息失敗:', error);
      alert('發送消息時發生錯誤，請稍後再試。');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = async () => {
    try {
      await api.resetMessages();
      setMessages([]);
    } catch (error) {
      console.error('重置對話失敗:', error);
    }
  };

  return (
    <div className="app-container">
      <div className="chat-container">
        <header className="chat-header">
          <h1>旅遊顧問聊天室</h1>
          <button className="reset-button" onClick={handleReset}>重置對話</button>
        </header>

        <div className="messages-container">
          {messages.length === 0 ? (
            <div className="empty-state">發送一條消息開始對話吧!</div>
          ) : (
            messages.map((message, index) => (
              <div
                key={index}
                className={`message ${message.role === 'user' ? 'user-message' : 'assistant-message'}`}
              >
                <div className="message-content">{message.content}</div>
              </div>
            ))
          )}
          {loading && (
            <div className="message assistant-message">
              <div className="loading-indicator">思考中...</div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <form className="input-form" onSubmit={handleSendMessage}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="輸入您的問題..."
            disabled={loading}
          />
          <button type="submit" disabled={loading || input.trim() === ''}>
            發送
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;
