import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Sprout, MessageSquare, BookOpen, Clock, Activity, ShieldCheck, Compass } from 'lucide-react';
import { api } from '../services/api';

export default function Navbar({ currentLang, onLangChange }) {
  const location = useLocation();
  const [health, setHealth] = useState(null);
  const [languages, setLanguages] = useState([]);

  useEffect(() => {
    api.getHealth()
      .then(data => setHealth(data))
      .catch(() => setHealth({ status: 'offline', agriparam_engine: 'Standby' }));

    api.getLanguages()
      .then(langs => setLanguages(langs))
      .catch(() => setLanguages([
        { code: 'en', name: 'English', native: 'English' },
        { code: 'hi', name: 'Hindi', native: 'हिन्दी' },
        { code: 'kn', name: 'Kannada', native: 'ಕನ್ನಡ' },
        { code: 'ta', name: 'Tamil', native: 'தமிழ்' },
        { code: 'te', name: 'Telugu', native: 'తెలుగు' },
        { code: 'bn', name: 'Bengali', native: 'বাংলা' },
        { code: 'mr', name: 'Marathi', native: 'मराठी' }
      ]));
  }, []);

  const navItems = [
    { label: 'Dashboard', path: '/', icon: Compass },
    { label: 'AI Assistant', path: '/chat', icon: MessageSquare },
    { label: 'Crop Advisory', path: '/advisory', icon: Sprout },
    { label: 'Knowledge Sources', path: '/sources', icon: BookOpen },
    { label: 'History', path: '/history', icon: Clock },
  ];

  return (
    <header className="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b border-slate-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Brand */}
          <Link to="/" className="flex items-center space-x-3 group">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-600 to-green-500 flex items-center justify-center text-white shadow-md shadow-emerald-200 group-hover:scale-105 transition-transform">
              <Sprout className="w-6 h-6" />
            </div>
            <div>
              <span className="text-lg font-bold tracking-tight text-slate-900 group-hover:text-emerald-700 transition-colors">
                Krishi Mitra AI
              </span>
              <span className="hidden sm:inline-block ml-2 px-2 py-0.5 text-xs font-semibold bg-emerald-100 text-emerald-800 rounded-full border border-emerald-200">
                AgriParam RAG
              </span>
            </div>
          </Link>

          {/* Navigation links */}
          <nav className="hidden md:flex items-center space-x-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center space-x-2 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                    isActive
                      ? 'bg-emerald-50 text-emerald-700 font-semibold'
                      : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                  }`}
                >
                  <Icon className={`w-4 h-4 ${isActive ? 'text-emerald-600' : 'text-slate-400'}`} />
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </nav>

          {/* Right Controls: Language Selector & Engine Badge */}
          <div className="flex items-center space-x-3">
            {/* Language Selector */}
            <select
              value={currentLang}
              onChange={(e) => onLangChange(e.target.value)}
              className="text-xs sm:text-sm font-medium bg-slate-50 border border-slate-300 rounded-lg px-2.5 py-1.5 text-slate-700 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
            >
              {languages.map((l) => (
                <option key={l.code} value={l.code}>
                  {l.native} ({l.name})
                </option>
              ))}
            </select>

            {/* Status Pill */}
            <div className="hidden lg:flex items-center space-x-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              <span title={health?.agriparam_engine || 'Checking...'}>
                {health?.status === 'healthy' ? 'Model Active' : 'Connecting...'}
              </span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}

