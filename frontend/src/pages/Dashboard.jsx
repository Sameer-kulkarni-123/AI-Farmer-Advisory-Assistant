import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Sprout, Droplets, FlaskConical, Bug, Landmark, ShieldCheck, 
  ArrowRight, Sparkles, MessageSquare, BookOpen, Layers
} from 'lucide-react';
import { api } from '../services/api';

export default function Dashboard({ currentLang }) {
  const navigate = useNavigate();
  const [quickQuery, setQuickQuery] = useState('');
  const [recentConversations, setRecentConversations] = useState([]);
  const [sourcesCount, setSourcesCount] = useState(20);

  useEffect(() => {
    api.getConversations()
      .then(convs => setRecentConversations(convs.slice(0, 4)))
      .catch(() => setRecentConversations([]));

    api.getSources()
      .then(docs => setSourcesCount(docs.length))
      .catch(() => setSourcesCount(20));
  }, []);

  const handleQuickSubmit = (e) => {
    e.preventDefault();
    if (quickQuery.trim()) {
      navigate('/chat', { state: { initialQuery: quickQuery } });
    }
  };

  const handleSuggestedClick = (question) => {
    navigate('/chat', { state: { initialQuery: question } });
  };

  const categories = [
    { title: 'Crop Cultivation', desc: 'Sowing dates, seed rates & land preparation', icon: Sprout, color: 'emerald', cat: 'cultivation' },
    { title: 'Smart Irrigation', desc: 'Critical stages, AWD & water saving', icon: Droplets, color: 'blue', cat: 'irrigation' },
    { title: 'Fertilizer & Soil', desc: 'NPK, Neem-coated Urea & Soil Health', icon: FlaskConical, color: 'amber', cat: 'fertilizer' },
    { title: 'Pest & Disease IPM', desc: 'Biological controls, pheromone traps & warnings', icon: Bug, color: 'rose', cat: 'pest_management' },
    { title: 'Government Schemes', desc: 'PM-KISAN, PMFBY & Soil Health Card eligibility', icon: Landmark, color: 'indigo', cat: 'government_schemes' },
    { title: 'Organic Farming', desc: 'Jeevamrit, Beejamrit & natural inputs', icon: ShieldCheck, color: 'teal', cat: 'organic_farming' },
  ];

  const suggestedQuestions = [
    "Which fertilizer should I use for growing paddy?",
    "How frequently should I irrigate my tomato crop?",
    "What are the symptoms and IPM control for pink bollworm in cotton?",
    "When is the Crown Root Initiation (CRI) stage in wheat?",
    "Why is gypsum mandatory for groundnut at pegging stage?",
    "What is the financial benefit and eligibility under PM-KISAN?",
    "धान की बुवाई के लिए अनुशंसित बीज दर क्या है?",
    "ಭತ್ತದ ಬೆಳೆಗೆ ಎಷ್ಟು ನೀರು ಬೇಕು?"
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-10">
      {/* Hero Section */}
      <section className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-emerald-900 via-emerald-800 to-teal-950 text-white p-8 sm:p-12 shadow-xl shadow-emerald-950/20">
        <div className="relative z-10 max-w-3xl space-y-4">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/20 text-emerald-300 border border-emerald-400/30 backdrop-blur">
            <Sparkles className="w-3.5 h-3.5" />
            <span>BharatGen AgriParam + AI4Bharat IndicTrans2</span>
          </div>

          <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight leading-tight">
            Evidence-Backed AI Advisory for Indian Farmers
          </h1>

          <p className="text-sm sm:text-base text-emerald-100/90 leading-relaxed">
            Get practical, reliable agricultural recommendations grounded in verified ICAR bulletins, 
            KVK packages of practices, and Ministry guidelines in 7 Indian languages.
          </p>

          {/* Quick Query Bar */}
          <form onSubmit={handleQuickSubmit} className="pt-2 flex flex-col sm:flex-row gap-2 max-w-2xl">
            <input
              type="text"
              placeholder="Ask a farming question (e.g. fertilizer for paddy, tomato blight, PM-KISAN)..."
              value={quickQuery}
              onChange={(e) => setQuickQuery(e.target.value)}
              className="flex-1 px-4 py-3.5 rounded-xl text-sm bg-white text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-emerald-400 shadow-md"
            />
            <button
              type="submit"
              className="px-6 py-3.5 rounded-xl font-semibold text-sm bg-emerald-500 hover:bg-emerald-400 text-emerald-950 transition-colors shadow-md flex items-center justify-center space-x-2"
            >
              <span>Ask Krishi Mitra</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </form>
        </div>

        {/* Decorative background glow */}
        <div className="absolute -right-20 -bottom-20 w-80 h-80 rounded-full bg-emerald-500/20 blur-3xl pointer-events-none"></div>
      </section>

      {/* Suggested Questions Grid */}
      <section className="space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-bold text-slate-900 flex items-center space-x-2">
            <MessageSquare className="w-5 h-5 text-emerald-600" />
            <span>Frequently Asked Agricultural Questions</span>
          </h2>
          <span className="text-xs text-slate-500">Click to run query with RAG</span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2.5">
          {suggestedQuestions.map((q, idx) => (
            <button
              key={idx}
              onClick={() => handleSuggestedClick(q)}
              className="text-left p-3 rounded-xl bg-white border border-slate-200 hover:border-emerald-300 hover:bg-emerald-50/40 text-xs sm:text-sm text-slate-700 transition-all shadow-sm group flex flex-col justify-between"
            >
              <span className="font-medium group-hover:text-emerald-900 line-clamp-2">{q}</span>
              <span className="text-[11px] text-emerald-600 font-semibold mt-2 flex items-center space-x-1">
                <span>Ask Advisory</span>
                <ArrowRight className="w-3 h-3 group-hover:translate-x-0.5 transition-transform" />
              </span>
            </button>
          ))}
        </div>
      </section>

      {/* Agricultural Domains */}
      <section className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-bold text-slate-900 flex items-center space-x-2">
            <Layers className="w-5 h-5 text-emerald-600" />
            <span>Explore Agricultural Advisory Domains</span>
          </h2>
          <span className="text-xs text-slate-500">Based on ICAR & KVK Taxonomy</span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {categories.map((c, i) => {
            const Icon = c.icon;
            return (
              <div
                key={i}
                onClick={() => navigate('/advisory', { state: { category: c.cat } })}
                className="p-5 rounded-2xl bg-white border border-slate-200 hover:border-emerald-300 hover:shadow-md transition-all cursor-pointer group"
              >
                <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-700 flex items-center justify-center mb-3 group-hover:bg-emerald-600 group-hover:text-white transition-colors">
                  <Icon className="w-5 h-5" />
                </div>
                <h3 className="font-bold text-slate-900 group-hover:text-emerald-800 transition-colors">
                  {c.title}
                </h3>
                <p className="text-xs text-slate-500 mt-1 leading-relaxed">
                  {c.desc}
                </p>
              </div>
            );
          })}
        </div>
      </section>

      {/* Trust & Knowledge Base Stats Banner */}
      <section className="rounded-2xl bg-slate-900 text-white p-6 sm:p-8 flex flex-col sm:flex-row items-center justify-between gap-6">
        <div>
          <div className="text-xs font-semibold text-emerald-400 uppercase tracking-wider mb-1">
            Authoritative Evidence Base
          </div>
          <h3 className="text-xl sm:text-2xl font-bold">
            {sourcesCount} Verified Publications from ICAR, KVK & DAC&FW
          </h3>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            Persistent ChromaDB vector index with domain entity extraction and anti-hallucination abstention.
          </p>
        </div>
        <button
          onClick={() => navigate('/sources')}
          className="px-5 py-2.5 rounded-xl text-xs font-semibold bg-emerald-500 hover:bg-emerald-400 text-slate-950 transition-colors flex items-center space-x-2 flex-shrink-0"
        >
          <BookOpen className="w-4 h-4" />
          <span>Browse Knowledge Base</span>
        </button>
      </section>
    </div>
  );
}

