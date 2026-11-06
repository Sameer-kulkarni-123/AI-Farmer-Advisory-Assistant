import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Clock, MessageSquare, Trash2, ArrowRight, Calendar, Layers } from 'lucide-react';
import { api } from '../services/api';

export default function ConversationHistory() {
  const navigate = useNavigate();
  const [conversations, setConversations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadConversations();
  }, []);

  const loadConversations = async () => {
    setLoading(true);
    try {
      const data = await api.getConversations();
      setConversations(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id, e) => {
    e.stopPropagation();
    if (window.confirm('Delete this conversation history?')) {
      try {
        await api.deleteConversation(id);
        setConversations((prev) => prev.filter((c) => c.id !== id));
      } catch (err) {
        alert('Failed to delete session.');
      }
    }
  };

  const handleOpenConversation = (id) => {
    navigate('/chat', { state: { resumeId: id } });
  };

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* Title */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 flex items-center space-x-3">
          <Clock className="w-8 h-8 text-emerald-600" />
          <span>Farming Advisory History</span>
        </h1>
        <p className="text-sm text-slate-500 mt-1">
          Review and continue previous agricultural advisory conversations stored persistently in SQLite.
        </p>
      </div>

      {loading ? (
        <div className="py-20 text-center text-slate-400 text-sm">
          Loading conversation logs...
        </div>
      ) : conversations.length === 0 ? (
        <div className="py-20 text-center bg-white border border-slate-200 rounded-3xl p-8 space-y-3">
          <div className="w-12 h-12 rounded-2xl bg-slate-100 text-slate-400 flex items-center justify-center mx-auto">
            <MessageSquare className="w-6 h-6" />
          </div>
          <h3 className="font-bold text-slate-700">No Advisory Sessions Found</h3>
          <p className="text-xs text-slate-400 max-w-sm mx-auto">
            Conversations you start in the AI Assistant will appear here automatically.
          </p>
        </div>
      ) : (
        <div className="space-y-3">
          {conversations.map((conv) => (
            <div
              key={conv.id}
              onClick={() => handleOpenConversation(conv.id)}
              className="bg-white border border-slate-200 hover:border-emerald-300 rounded-2xl p-5 shadow-sm hover:shadow-md transition-all cursor-pointer flex items-center justify-between group"
            >
              <div className="space-y-1.5 flex-1 pr-4">
                <div className="flex items-center space-x-2">
                  <span className="px-2 py-0.5 text-[10px] font-bold rounded uppercase bg-emerald-50 text-emerald-800 border border-emerald-200">
                    {conv.crop || 'General Advisory'}
                  </span>
                  <span className="text-xs text-slate-400">
                    Language: <strong className="text-slate-600 uppercase">{conv.language}</strong>
                  </span>
                  <span className="text-xs text-slate-400">• {conv.message_count} messages</span>
                </div>

                <h3 className="font-bold text-slate-900 text-sm sm:text-base group-hover:text-emerald-700 transition-colors">
                  {conv.title}
                </h3>

                <div className="text-[11px] text-slate-400 flex items-center space-x-1">
                  <Calendar className="w-3.5 h-3.5" />
                  <span>{new Date(conv.updated_at).toLocaleString()}</span>
                </div>
              </div>

              <div className="flex items-center space-x-2">
                <button
                  onClick={(e) => handleDelete(conv.id, e)}
                  className="p-2 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-xl transition-colors"
                  title="Delete Session"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
                <div className="w-8 h-8 rounded-xl bg-slate-50 group-hover:bg-emerald-600 group-hover:text-white text-slate-400 flex items-center justify-center transition-colors">
                  <ArrowRight className="w-4 h-4" />
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

