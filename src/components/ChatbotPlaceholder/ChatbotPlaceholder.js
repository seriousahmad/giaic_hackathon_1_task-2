import React, { useState, useRef, useEffect } from 'react';
import './ChatbotPlaceholder.css';

const ChatbotPlaceholder = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef(null);
  const chatContainerRef = useRef(null);

  // Function to get selected text
  const getSelectedText = () => {
    const selectedText = window.getSelection().toString().trim();
    if (selectedText) {
      setInputValue(selectedText);
    }
    return selectedText;
  };

  // Handle sending a message
  const handleSendMessage = async () => {
    if (inputValue.trim() !== '') {
      const newMessage = {
        id: Date.now(),
        text: inputValue,
        sender: 'user',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };

      setMessages(prev => [...prev, newMessage]);

      try {
        // Call the backend API
        const response = await fetch('http://localhost:8000/api/ask', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ question: inputValue })
        });

        if (response.ok) {
          const data = await response.json();
          const botResponse = {
            id: Date.now() + 1,
            text: data.answer,
            sender: 'bot',
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
          };
          setMessages(prev => [...prev, botResponse]);
        } else {
          const errorResponse = {
            id: Date.now() + 1,
            text: 'Sorry, I encountered an error processing your request. Please try again.',
            sender: 'bot',
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
          };
          setMessages(prev => [...prev, errorResponse]);
        }
      } catch (error) {
        console.error('Error calling backend API:', error);
        const errorResponse = {
          id: Date.now() + 1,
          text: 'Sorry, I\'m having trouble connecting to the textbook AI. Please make sure the backend server is running.',
          sender: 'bot',
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        };
        setMessages(prev => [...prev, errorResponse]);
      }

      setInputValue('');
    }
  };

  // Handle Enter key press
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  // Scroll to bottom of messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Add click handler to document to close chat when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (chatContainerRef.current && !chatContainerRef.current.contains(event.target) && isOpen) {
        // Don't close if clicking on the toggle button
        if (!event.target.closest('.chatbot-toggle')) {
          setIsOpen(false);
        }
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen]);

  return (
    <div className="chatbot-container" ref={chatContainerRef}>
      {/* Chatbot toggle button */}
      <button
        className={`chatbot-toggle ${isOpen ? 'open' : ''}`}
        onClick={() => setIsOpen(!isOpen)}
        aria-label={isOpen ? 'Close chatbot' : 'Open chatbot'}
      >
        <div className="chatbot-icon">🤖</div>
        {isOpen && <span className="chatbot-label">Textbook AI</span>}
      </button>

      {/* Chatbot panel */}
      {isOpen && (
        <div className="chatbot-panel">
          <div className="chatbot-header">
            <h3>Textbook AI Assistant</h3>
            <button
              className="chatbot-close"
              onClick={() => setIsOpen(false)}
              aria-label="Close chat"
            >
              ×
            </button>
          </div>

          <div className="chatbot-messages">
            {messages.length === 0 ? (
              <div className="chatbot-welcome">
                <p>Hello! I'm your textbook AI assistant.</p>
                <p>Select text on any page and click the button below to ask about it:</p>
                <button
                  className="select-text-btn"
                  onClick={getSelectedText}
                >
                  Use Selected Text
                </button>
              </div>
            ) : (
              messages.map((message) => (
                <div
                  key={message.id}
                  className={`message ${message.sender}`}
                >
                  <div className="message-content">
                    {message.text}
                  </div>
                  <div className="message-timestamp">
                    {message.timestamp}
                  </div>
                </div>
              ))
            )}
            <div ref={messagesEndRef} />
          </div>

          <div className="chatbot-input-area">
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask about the textbook content..."
              rows="2"
              className="chatbot-input"
            />
            <button
              className="chatbot-send-btn"
              onClick={handleSendMessage}
              disabled={!inputValue.trim()}
            >
              Send
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatbotPlaceholder;