import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Dashboard from './pages/Dashboard';
import ChatAssistant from './pages/ChatAssistant';
import CropAdvisoryPage from './pages/CropAdvisoryPage';
import KnowledgeSources from './pages/KnowledgeSources';
import ConversationHistory from './pages/ConversationHistory';

export default function App() {
  const [currentLang, setCurrentLang] = useState('en');

  return (
    <Router>
      <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900">
        <Navbar currentLang={currentLang} onLangChange={setCurrentLang} />
        <main className="flex-1">
          <Routes>
            <Route path="/" element={<Dashboard currentLang={currentLang} />} />
            <Route path="/chat" element={<ChatAssistant currentLang={currentLang} onLangChange={setCurrentLang} />} />
            <Route path="/advisory" element={<CropAdvisoryPage currentLang={currentLang} />} />
            <Route path="/sources" element={<KnowledgeSources />} />
            <Route path="/history" element={<ConversationHistory />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

