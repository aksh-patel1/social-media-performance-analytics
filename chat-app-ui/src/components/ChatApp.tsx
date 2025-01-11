import React, { useState, useEffect, useRef } from 'react';
import { MessageCircle, Send, Loader2 } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from "remark-gfm";
import "../styles/markdown-table.css"

// Message type definition
type Message = {
  text: string;
  sender: 'user' | 'ai';
  timestamp: string;
};

const ChatApp = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage: Message = {
      text: input,
      sender: 'user',
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: input }),
      });

      const data = await response.json();

      const aiMessage: Message = {
        text: data.text,
        sender: 'ai',
        timestamp: data.timestamp,
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error:', error);
      const errorMessage: Message = {
        text: 'Sorry, I encountered an error. Please try again.',
        sender: 'ai',
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Custom styles for markdown elements
  const markdownStyles = {
    p: 'mb-2 last:mb-0',
    h1: 'text-2xl font-bold mb-4',
    h2: 'text-xl font-bold mb-3',
    h3: 'text-lg font-bold mb-2',
    ul: 'list-disc pl-4 mb-2',
    ol: 'list-decimal pl-4 mb-2',
    li: 'mb-1',
    pre: 'bg-gray-800 text-white p-3 rounded-md mb-2 overflow-x-auto',
    code: 'bg-gray-800 text-white px-1 py-0.5 rounded',
    blockquote: 'border-l-4 border-gray-300 pl-4 italic mb-2',
    a: 'text-blue-500 hover:underline',
    table: 'border-collapse table-auto w-full mb-2',
    th: 'border border-gray-300 px-4 py-2 bg-gray-100',
    td: 'border border-gray-300 px-4 py-2',
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-blue-500 text-white p-4 shadow-md flex items-center justify-between">
        <div className="flex items-center gap-2">
          <MessageCircle className="text-white" />
          <h1 className="text-lg font-semibold">Social Media Performance Analyzer</h1>
        </div>
      </header>

      {/* Chat Container */}
      <div className="flex flex-1 overflow-hidden">
        <main className="flex-1 flex flex-col p-4 bg-gray-100">
          <div className="flex-1 overflow-y-auto space-y-4">
            {messages.map((message, index) => (
              <div
                key={index}
                className={`flex ${
                  message.sender === 'user' ? 'justify-end' : 'justify-start'
                }`}
              >
                <div
                  className={`max-w-[75%] rounded-lg p-4 ${
                    message.sender === 'user'
                      ? 'bg-blue-500 text-white'
                      : 'bg-white text-gray-800'
                  } shadow-md`}
                >
                  {message.sender === 'user' ? (
                    <p className="whitespace-pre-wrap">{message.text}</p>
                  ) : (
                    <ReactMarkdown
                      className="prose prose-sm max-w-none"
                      remarkPlugins={[remarkGfm]}
                      components={{
                        p: ({ children }) => <p className={markdownStyles.p}>{children}</p>,
                        h1: ({ children }) => <h1 className={markdownStyles.h1}>{children}</h1>,
                        h2: ({ children }) => <h2 className={markdownStyles.h2}>{children}</h2>,
                        h3: ({ children }) => <h3 className={markdownStyles.h3}>{children}</h3>,
                        ul: ({ children }) => <ul className={markdownStyles.ul}>{children}</ul>,
                        ol: ({ children }) => <ol className={markdownStyles.ol}>{children}</ol>,
                        li: ({ children }) => <li className={markdownStyles.li}>{children}</li>,
                        pre: ({ children }) => <pre className={markdownStyles.pre}>{children}</pre>,
                        code: ({ children }) => <code className={markdownStyles.code}>{children}</code>,
                        blockquote: ({ children }) => (
                          <blockquote className={markdownStyles.blockquote}>{children}</blockquote>
                        ),
                        a: ({ href, children }) => (
                          <a href={href} className={markdownStyles.a} target="_blank" rel="noopener noreferrer">
                            {children}
                          </a>
                        ),
                      }}
                    >
                      {message.text}
                    </ReactMarkdown>
                  )}
                  <p className="text-xs mt-2 opacity-70">
                    {new Date(message.timestamp).toLocaleTimeString()}
                  </p>
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-white rounded-lg p-4 shadow flex items-center gap-2">
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <p>Thinking...</p>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Form */}
          <form onSubmit={handleSubmit} className="mt-4">
            <div className="flex items-center gap-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Type your message..."
                className="flex-1 border border-gray-300 rounded-lg px-4 py-2 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                disabled={isLoading}
              />
              <button
                type="submit"
                disabled={isLoading || !input.trim()}
                className="bg-blue-500 text-white rounded-lg px-4 py-2 hover:bg-blue-600 disabled:opacity-50 flex items-center gap-2"
              >
                <Send className="w-4 h-4" />
                Send
              </button>
            </div>
          </form>
        </main>

        {/* Embedded Chat Section */}
        <langflow-chat
          window_title="Basic Prompting"
          flow_id="2e80e619-11e1-4576-a3c0-6ceb1c62f9c6"
          host_url="http://localhost:7860"
        ></langflow-chat>
      </div>
    </div>
  );
};

export default ChatApp;