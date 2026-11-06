import React, { useState } from 'react';
import { Sprout, Filter, Sparkles, AlertCircle } from 'lucide-react';
import { api } from '../services/api';
import AdvisoryCard from '../components/AdvisoryCard';

export default function CropAdvisoryPage({ currentLang }) {
  const [crop, setCrop] = useState('Rice');
  const [category, setCategory] = useState('cultivation');
  const [state, setState] = useState('Karnataka');
  const [district, setDistrict] = useState('');
  const [soilType, setSoilType] = useState('Clay Loam');
  const [growthStage, setGrowthStage] = useState('Vegetative');

  const [loading, setLoading] = useState(false);
  const [advisoryResult, setAdvisoryResult] = useState(null);
  const [error, setError] = useState(null);

  const cropsList = [
    'Rice', 'Wheat', 'Maize', 'Cotton', 'Sugarcane',
    'Tomato', 'Potato', 'Groundnut', 'Soybean', 'Pulses'
  ];

  const categories = [
    { value: 'cultivation', label: 'Land Prep & Cultivation' },
    { value: 'irrigation', label: 'Irrigation & Water Schedule' },
    { value: 'fertilizer', label: 'Fertilizer & Nutrient Schedule' },
    { value: 'pest_management', label: 'Pest & Disease IPM' }
  ];

  const statesList = [
    'Karnataka', 'Tamil Nadu', 'Andhra Pradesh', 'Telangana', 'Maharashtra',
    'Punjab', 'Haryana', 'Uttar Pradesh', 'Madhya Pradesh', 'Gujarat', 'West Bengal', 'Rajasthan'
  ];

  const soilTypes = [
    'Clay Loam', 'Deep Black Soil (Vertisol)', 'Red Sandy Loam', 'Alluvial Silt Loam', 'Saline / Alkaline Soil'
  ];

  const growthStages = [
    'Land Preparation & Nursery', 'Sowing & Germination', 'Vegetative & Tillering',
    'Crown Root Initiation (CRI)', 'Flowering & Pegging', 'Grain / Fruit Formation', 'Maturity & Pre-Harvest'
  ];

  const handleFetchAdvisory = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const data = await api.getCropAdvisory({
        crop,
        category,
        state,
        district: district || undefined,
        soilType,
        growthStage,
        language: currentLang
      });

      setAdvisoryResult(data);
    } catch (err) {
      console.error(err);
      setError('Failed to fetch structured crop advisory. Please ensure backend is reachable.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Title */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 flex items-center space-x-3">
          <Sprout className="w-8 h-8 text-emerald-600" />
          <span>Regional Crop Advisory Matrix</span>
        </h1>
        <p className="text-sm text-slate-500 mt-1">
          Select crop, agro-climatic region, soil properties, and growth phase to retrieve calibrated ICAR/KVK guidance.
        </p>
      </div>

      {/* Advisory Configuration Form */}
      <form onSubmit={handleFetchAdvisory} className="bg-white border border-slate-200 rounded-3xl p-6 shadow-sm space-y-6">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {/* Crop Selector */}
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-600 mb-1.5">
              Target Crop *
            </label>
            <select
              value={crop}
              onChange={(e) => setCrop(e.target.value)}
              className="w-full text-sm font-medium bg-slate-50 border border-slate-300 rounded-xl px-3 py-2.5 text-slate-800 focus:ring-2 focus:ring-emerald-500"
            >
              {cropsList.map((c) => (
                <option key={c} value={c}>{c}</option>
              ))}
            </select>
          </div>

          {/* Advisory Category */}
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-600 mb-1.5">
              Advisory Focus *
            </label>
            <select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="w-full text-sm font-medium bg-slate-50 border border-slate-300 rounded-xl px-3 py-2.5 text-slate-800 focus:ring-2 focus:ring-emerald-500"
            >
              {categories.map((cat) => (
                <option key={cat.value} value={cat.value}>{cat.label}</option>
              ))}
            </select>
          </div>

          {/* State */}
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-600 mb-1.5">
              State / Region *
            </label>
            <select
              value={state}
              onChange={(e) => setState(e.target.value)}
              className="w-full text-sm font-medium bg-slate-50 border border-slate-300 rounded-xl px-3 py-2.5 text-slate-800 focus:ring-2 focus:ring-emerald-500"
            >
              {statesList.map((s) => (
                <option key={s} value={s}>{s}</option>
              ))}
            </select>
          </div>

          {/* District */}
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-600 mb-1.5">
              District (Optional)
            </label>
            <input
              type="text"
              placeholder="e.g. Mandya, Karnal, Ludhiana"
              value={district}
              onChange={(e) => setDistrict(e.target.value)}
              className="w-full text-sm bg-slate-50 border border-slate-300 rounded-xl px-3 py-2 text-slate-800 focus:ring-2 focus:ring-emerald-500"
            />
          </div>

          {/* Soil Type */}
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-600 mb-1.5">
              Soil Type
            </label>
            <select
              value={soilType}
              onChange={(e) => setSoilType(e.target.value)}
              className="w-full text-sm font-medium bg-slate-50 border border-slate-300 rounded-xl px-3 py-2.5 text-slate-800 focus:ring-2 focus:ring-emerald-500"
            >
              {soilTypes.map((st) => (
                <option key={st} value={st}>{st}</option>
              ))}
            </select>
          </div>

          {/* Growth Stage */}
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-600 mb-1.5">
              Current Growth Stage
            </label>
            <select
              value={growthStage}
              onChange={(e) => setGrowthStage(e.target.value)}
              className="w-full text-sm font-medium bg-slate-50 border border-slate-300 rounded-xl px-3 py-2.5 text-slate-800 focus:ring-2 focus:ring-emerald-500"
            >
              {growthStages.map((gs) => (
                <option key={gs} value={gs}>{gs}</option>
              ))}
            </select>
          </div>
        </div>

        <div className="pt-2 flex justify-end">
          <button
            type="submit"
            disabled={loading}
            className="px-6 py-3 rounded-xl font-semibold text-sm bg-emerald-600 hover:bg-emerald-500 text-white flex items-center space-x-2 transition-colors shadow-sm disabled:opacity-50"
          >
            <Sparkles className="w-4 h-4" />
            <span>{loading ? 'Synthesizing Advisory...' : 'Generate Regional Advisory'}</span>
          </button>
        </div>
      </form>

      {/* Error state */}
      {error && (
        <div className="p-4 rounded-xl bg-red-50 border border-red-200 text-sm text-red-700 flex items-center space-x-2">
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Advisory Result Render */}
      {advisoryResult && (
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-base font-bold text-slate-900">
              Generated Advisory for {advisoryResult.crop} ({advisoryResult.state})
            </h3>
            <span className="text-xs text-slate-500">
              Execution latency: {advisoryResult.latency_seconds}s
            </span>
          </div>

          <AdvisoryCard
            advisory={advisoryResult.advisory}
            modelUsed={advisoryResult.model_used}
            latencySeconds={advisoryResult.latency_seconds}
            language={currentLang}
          />
        </div>
      )}
    </div>
  );
}

