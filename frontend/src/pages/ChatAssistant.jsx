import React, { useState, useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import { 
  Send, RotateCcw, Sparkles, Sprout, User, Bot, AlertCircle, 
  HelpCircle, ChevronDown, Check, SlidersHorizontal
} from 'lucide-react';
import { api } from '../services/api';
import AdvisoryCard from '../components/AdvisoryCard';

export default function ChatAssistant({ currentLang, onLangChange }) {
  const location = useLocation();
  const [messages, setMessages] = useState([]);
  const [inputQuery, setInputQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState(null);
  const [error, setError] = useState(null);

  // Optional Context drawer
  const [showFilters, setShowFilters] = useState(false);
  const [crop, setCrop] = useState('');
  const [region, setRegion] = useState('');
  const [soilType, setSoilType] = useState('');
  const [growthStage, setGrowthStage] = useState('');

  const chatEndRef = useRef(null);

  // Load initial query if passed from Dashboard
  useEffect(() => {
    if (location.state?.initialQuery) {
      handleSendMessage(location.state.initialQuery);
    }
  }, [location.state]);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const handleSendMessage = async (textToSend) => {
    const query = textToSend || inputQuery;
    if (!query.trim() || loading) return;

    setError(null);
    const userMsg = {
      role: 'user',
      content: query,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputQuery('');
    setLoading(true);

    try {
      const data = await api.sendChatMessage({
        message: query,
        conversationId,
        language: currentLang,
        crop: crop || undefined,
        region: region || undefined,
        soilType: soilType || undefined,
        growthStage: growthStage || undefined,
      });

      setConversationId(data.conversation_id);

      const assistantMsg = {
        role: 'assistant',
        advisory: data.advisory,
        modelUsed: data.model_used,
        latencySeconds: data.latency_seconds,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };

      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err) {
      console.error(err);
      setError('Unable to fetch agricultural advisory from backend. Please ensure the FastAPI server is running on port 8000.');
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setMessages([]);
    setConversationId(null);
    setError(null);
  };

  const quickPrompts = [
    "Which fertilizer should I use for paddy?",
    "How frequently should I irrigate tomato?",
    "Control pests affecting cotton with IPM",
    "Symptoms of nitrogen deficiency in wheat",
    "PM-KISAN eligibility criteria"
  ];

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 py-6 h-[calc(100vh-5rem)] flex flex-col">
      {/* Header Bar */}
      <div className="flex items-center justify-between pb-4 border-b border-slate-200">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-emerald-600 text-white flex items-center justify-center shadow-md shadow-emerald-200">
            <Bot className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-slate-900">
              Krishi Mitra AI Assistant
            </h2>
            <p className="text-xs text-slate-500">
              Evidence-Grounded Multilingual Agricultural Advisory
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={() => setShowFilters(!showFilters)}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium border flex items-center space-x-1.5 transition-colors ${
              showFilters ? 'bg-emerald-50 border-emerald-300 text-emerald-800' : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-50'
            }`}
          >
            <SlidersHorizontal className="w-3.5 h-3.5" />
            <span>Farm Context</span>
          </button>

          <button
            onClick={handleClear}
            className="p-1.5 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-lg transition-colors"
            title="Clear Chat"
          >
            <RotateCcw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Optional Context Drawer */}
      {showFilters && (
        <div className="mt-3 p-3.5 rounded-xl bg-slate-50 border border-slate-200 grid grid-cols-2 sm:grid-cols-4 gap-2.5 text-xs">
          <div>
            <label className="block text-slate-600 font-medium mb-1">Crop</label>
            <input
              type="text"
              placeholder="e.g. Rice, Wheat"
              value={crop}
              onChange={(e) => setCrop(e.target.value)}
              className="w-full px-2.5 py-1.5 bg-white border border-slate-300 rounded-md"
            />
          </div>
          <div>
            <label className="block text-slate-600 font-medium mb-1">State / Region</label>
            <input
              type="text"
              placeholder="e.g. Karnataka, Punjab"
              value={region}
              onChange={(e) => setRegion(e.target.value)}
              className="w-full px-2.5 py-1.5 bg-white border border-slate-300 rounded-md"
            />
          </div>
          <div>
            <label className="block text-slate-600 font-medium mb-1">Soil Type</label>
            <input
              type="text"
              placeholder="e.g. Black soil, Loam"
              value={soilType}
              onChange={(e) => setSoilType(e.target.value)}
              className="w-full px-2.5 py-1.5 bg-white border border-slate-300 rounded-md"
            />
          </div>
          <div>
            <label className="block text-slate-600 font-medium mb-1">Growth Stage</label>
            <input
              type="text"
              placeholder="e.g. Flowering, Tillering"
              value={growthStage}
              onChange={(e) => setGrowthStage(e.target.value)}
              className="w-full px-2.5 py-1.5 bg-white border border-slate-300 rounded-md"
            />
          </div>
        </div>
      )}

      {/* Messages Stream */}
      <div className="flex-1 overflow-y-auto py-6 space-y-6 pr-1">
        {messages.length === 0 && (
          <div className="h-full flex flex-col items-center justify-center text-center max-w-md mx-auto space-y-4">
            <div className="w-16 h-16 rounded-2xl bg-emerald-100 text-emerald-700 flex items-center justify-center shadow-inner">
              <Sprout className="w-8 h-8" />
            </div>
            <div>
              <h3 className="text-base font-bold text-slate-800">
                Namaste! How can I help your farm today?
              </h3>
              <p className="text-xs text-slate-500 mt-1">
                Ask any question about crop cultivation, irrigation scheduling, fertilizer doses, pest management, or government schemes.
              </p>
            </div>

            {/* Quick Prompt Pills */}
            <div className="flex flex-wrap justify-center gap-1.5 pt-2">
              {quickPrompts.map((p, i) => (
                <button
                  key={i}
                  onClick={() => handleSendMessage(p)}
                  className="px-3 py-1.5 rounded-full text-xs bg-white border border-slate-200 hover:border-emerald-300 hover:bg-emerald-50 text-slate-600 transition-colors"
                >
                  {p}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((m, idx) => (
          <div
            key={idx}
            className={`flex items-start space-x-3 ${
              m.role === 'user' ? 'justify-end' : 'justify-start'
            }`}
          >
            {m.role === 'assistant' && (
              <div className="w-8 h-8 rounded-lg bg-emerald-700 text-white flex items-center justify-center flex-shrink-0 mt-1">
                <Bot className="w-5 h-5" />
              </div>
            )}

            <div className={`max-w-3xl ${m.role === 'user' ? 'w-auto' : 'w-full'}`}>
              {m.role === 'user' ? (
                <div className="bg-emerald-600 text-white px-4 py-2.5 rounded-2xl rounded-tr-sm text-sm shadow-sm">
                  {m.content}
                </div>
              ) : (
                <AdvisoryCard
                  advisory={m.advisory}
                  modelUsed={m.modelUsed}
                  latencySeconds={m.latencySeconds}
                  language={currentLang}
                />
              )}
              <div className={`text-[10px] text-slate-400 mt-1 px-1 ${m.role === 'user' ? 'text-right' : 'text-left'}`}>
                {m.timestamp}
              </div>
            </div>

            {m.role === 'user' && (
              <div className="w-8 h-8 rounded-lg bg-slate-200 text-slate-700 flex items-center justify-center flex-shrink-0 mt-1">
                <User className="w-4 h-4" />
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="flex items-start space-x-3">
            <div className="w-8 h-8 rounded-lg bg-emerald-700 text-white flex items-center justify-center flex-shrink-0">
              <Bot className="w-5 h-5" />
            </div>
            <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm space-y-2 max-w-sm">
              <div className="flex items-center space-x-2 text-xs font-semibold text-emerald-800">
                <span className="w-2 h-2 rounded-full bg-emerald-600 animate-ping"></span>
                <span>Synthesizing ICAR Evidence & Advisory...</span>
              </div>
              <div className="h-1.5 w-full bg-slate-100 rounded-full overflow-hidden">
                <div className="h-full bg-emerald-500 rounded-full animate-pulse w-3/4"></div>
              </div>
            </div>
          </div>
        )}

        {error && (
          <div className="p-4 rounded-xl bg-red-50 border border-red-200 text-xs text-red-700 flex items-start space-x-2">
            <AlertCircle className="w-4 h-4 flex-shrink-0 mt-0.5" />
            <span>{error}</span>
          </div>
        )}

        <div ref={chatEndRef} />
      </div>

      {/* Input Bar */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleSendMessage();
        }}
        className="pt-2 border-t border-slate-200"
      >
        <div className="flex items-center space-x-2 bg-white border border-slate-300 rounded-2xl px-3 py-2 shadow-sm focus-within:ring-2 focus-within:ring-emerald-500 focus-within:border-emerald-500">
          <input
            type="text"
            placeholder="Type your agricultural question in English, Hindi, Kannada, etc..."
            value={inputQuery}
            onChange={(e) => setInputQuery(e.target.value)}
            disabled={loading}
            className="flex-1 text-sm bg-transparent border-0 focus:outline-none text-slate-900 placeholder:text-slate-400"
          />
          <button
            type="submit"
            disabled={loading || !inputQuery.trim()}
            className="w-9 h-9 rounded-xl bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-white flex items-center justify-center transition-colors shadow-sm"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
        <div className="text-[11px] text-slate-400 text-center mt-1.5">
          Recommendations generated using ICAR & KVK documents. Verify critical decisions with local experts.
        </div>
      </form>
    </div>
  );
}

