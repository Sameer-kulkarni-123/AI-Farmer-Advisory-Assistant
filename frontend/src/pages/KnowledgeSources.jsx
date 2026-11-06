import React, { useState, useEffect } from 'react';
import { BookOpen, ExternalLink, CheckCircle, Search, Filter, FileText, X } from 'lucide-react';
import { api } from '../services/api';

export default function KnowledgeSources() {
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCrop, setSelectedCrop] = useState('All');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [activeDoc, setActiveDoc] = useState(null);

  useEffect(() => {
    loadSources();
  }, [selectedCrop, selectedCategory]);

  const loadSources = async () => {
    setLoading(true);
    try {
      const params = {};
      if (selectedCrop !== 'All') params.crop = selectedCrop;
      if (selectedCategory !== 'All') params.category = selectedCategory;

      const data = await api.getSources(params);
      setSources(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const filteredSources = sources.filter((s) => {
    if (!searchTerm) return true;
    const term = searchTerm.toLowerCase();
    return (
      s.title.toLowerCase().includes(term) ||
      s.source.toLowerCase().includes(term) ||
      s.crop.toLowerCase().includes(term)
    );
  });

  const crops = ['All', 'Rice', 'Wheat', 'Maize', 'Cotton', 'Sugarcane', 'Tomato', 'Potato', 'Groundnut', 'Soybean', 'Pulses'];
  const categories = ['All', 'cultivation', 'irrigation', 'fertilizer_management', 'pest_management', 'soil_health', 'organic_farming', 'government_schemes'];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 flex items-center space-x-3">
            <BookOpen className="w-8 h-8 text-emerald-600" />
            <span>Agricultural Knowledge Corpus</span>
          </h1>
          <p className="text-sm text-slate-500 mt-1">
            Authoritative publications and official guidelines ingested into ChromaDB for evidence-grounded RAG.
          </p>
        </div>

        <div className="flex items-center space-x-2 text-xs font-semibold text-emerald-800 bg-emerald-50 px-3 py-1.5 rounded-xl border border-emerald-200">
          <CheckCircle className="w-4 h-4 text-emerald-600" />
          <span>{sources.length} Official ICAR/KVK Documents Indexed</span>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm flex flex-col md:flex-row gap-3">
        {/* Search */}
        <div className="flex-1 relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
          <input
            type="text"
            placeholder="Search by title, organization or crop keyword..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-9 pr-3 py-2 text-sm bg-slate-50 border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-500"
          />
        </div>

        {/* Crop Filter */}
        <div className="w-full md:w-48">
          <select
            value={selectedCrop}
            onChange={(e) => setSelectedCrop(e.target.value)}
            className="w-full py-2 px-3 text-sm font-medium bg-slate-50 border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-500"
          >
            {crops.map((c) => (
              <option key={c} value={c}>Crop: {c}</option>
            ))}
          </select>
        </div>

        {/* Category Filter */}
        <div className="w-full md:w-56">
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="w-full py-2 px-3 text-sm font-medium bg-slate-50 border border-slate-300 rounded-xl focus:ring-2 focus:ring-emerald-500"
          >
            {categories.map((cat) => (
              <option key={cat} value={cat}>Category: {cat.replace('_', ' ')}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Sources Grid */}
      {loading ? (
        <div className="py-20 text-center text-slate-400 text-sm">
          Loading verified agricultural documents...
        </div>
      ) : filteredSources.length === 0 ? (
        <div className="py-20 text-center bg-white border border-slate-200 rounded-2xl p-8 space-y-2">
          <p className="font-semibold text-slate-700">No documents match your query.</p>
          <p className="text-xs text-slate-400">Try clearing your search keyword or selecting "All".</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredSources.map((doc) => (
            <div
              key={doc.document_id}
              className="bg-white border border-slate-200 hover:border-emerald-300 rounded-2xl p-5 shadow-sm transition-all hover:shadow-md flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between gap-2 mb-2">
                  <span className="px-2 py-0.5 text-[10px] font-bold rounded-md uppercase bg-emerald-50 text-emerald-800 border border-emerald-200">
                    {doc.crop}
                  </span>
                  <span className="text-[11px] text-slate-400 capitalize">
                    {doc.category.replace('_', ' ')}
                  </span>
                </div>

                <h3 className="font-bold text-slate-900 text-sm leading-snug mb-1 line-clamp-2">
                  {doc.title}
                </h3>

                <p className="text-xs font-medium text-emerald-800 mb-2">
                  {doc.source}
                </p>

                <p className="text-xs text-slate-500 line-clamp-3 leading-relaxed mb-4">
                  {doc.content_preview}
                </p>
              </div>

              <div className="pt-3 border-t border-slate-100 flex items-center justify-between">
                <button
                  onClick={() => setActiveDoc(doc)}
                  className="text-xs font-semibold text-emerald-700 hover:text-emerald-800 flex items-center space-x-1"
                >
                  <FileText className="w-3.5 h-3.5" />
                  <span>Inspect Passage</span>
                </button>

                {doc.source_url && (
                  <a
                    href={doc.source_url}
                    target="_blank"
                    rel="noreferrer"
                    className="text-xs text-slate-400 hover:text-slate-700 flex items-center space-x-1"
                  >
                    <span>Official Link</span>
                    <ExternalLink className="w-3 h-3" />
                  </a>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Document Detail Modal */}
      {activeDoc && (
        <div className="fixed inset-0 z-50 bg-slate-900/40 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl max-w-2xl w-full p-6 shadow-2xl space-y-4 max-h-[85vh] flex flex-col">
            <div className="flex items-start justify-between">
              <div>
                <span className="px-2 py-0.5 text-xs font-semibold rounded bg-emerald-100 text-emerald-800">
                  {activeDoc.crop} • {activeDoc.category}
                </span>
                <h3 className="text-base font-bold text-slate-900 mt-2">
                  {activeDoc.title}
                </h3>
                <p className="text-xs text-emerald-700 font-medium">
                  {activeDoc.source}
                </p>
              </div>
              <button
                onClick={() => setActiveDoc(null)}
                className="p-1 rounded-lg hover:bg-slate-100 text-slate-400 hover:text-slate-600"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="flex-1 overflow-y-auto text-xs sm:text-sm text-slate-700 leading-relaxed bg-slate-50 p-4 rounded-xl border border-slate-200">
              {activeDoc.content_preview}
            </div>

            <div className="flex items-center justify-between pt-2 text-xs text-slate-500">
              <span>Region: {activeDoc.region}</span>
              {activeDoc.source_url && (
                <a
                  href={activeDoc.source_url}
                  target="_blank"
                  rel="noreferrer"
                  className="font-semibold text-emerald-700 hover:underline flex items-center space-x-1"
                >
                  <span>Open Official Document URL</span>
                  <ExternalLink className="w-3.5 h-3.5" />
                </a>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

