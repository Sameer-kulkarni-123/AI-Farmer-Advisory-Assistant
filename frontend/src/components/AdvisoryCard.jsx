import React, { useState } from 'react';
import { 
  CheckCircle2, AlertTriangle, MapPin, Sparkles, Copy, Check, 
  HelpCircle, ChevronRight, BookmarkCheck, FileText, Info
} from 'lucide-react';
import CitationBadge from './CitationBadge';

export default function AdvisoryCard({ advisory, modelUsed, latencySeconds, language }) {
  const [copied, setCopied] = useState(false);

  if (!advisory) return null;

  const handleCopy = () => {
    const textToCopy = `
Krishi Mitra Advisory: ${advisory.crop || ''}
-----------------------------------------------
Recommendation:
${advisory.recommendation}

Why this is recommended:
${advisory.why_recommended}

Practical Steps:
${(advisory.practical_steps || []).map((s, i) => `${i + 1}. ${s}`).join('\n')}

Important Precautions:
${(advisory.important_precautions || []).map(p => `• ${p}`).join('\n')}

Regional Considerations:
${advisory.regional_considerations || 'Applicable for Indian conditions.'}

Sources:
${(advisory.sources || []).map(s => `- ${s.title} (${s.source})`).join('\n')}

Evidence Level: ${advisory.confidence_level}
Model: ${modelUsed || 'AgriParam'}
-----------------------------------------------
${advisory.disclaimer || ''}
    `.trim();

    navigator.clipboard.writeText(textToCopy);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const isInsufficient = advisory.confidence_level === 'Insufficient';

  return (
    <div className={`rounded-2xl border transition-all shadow-sm ${
      isInsufficient 
        ? 'border-amber-200 bg-amber-50/30' 
        : 'border-slate-200 bg-white'
    }`}>
      {/* Top Banner with Badges & Copy Button */}
      <div className="flex flex-wrap items-center justify-between gap-3 px-5 py-4 border-b border-slate-100 bg-slate-50/50 rounded-t-2xl">
        <div className="flex items-center space-x-2">
          {advisory.crop && advisory.crop !== 'All' && (
            <span className="px-2.5 py-1 text-xs font-semibold rounded-md bg-emerald-100 text-emerald-800 border border-emerald-200">
              Crop: {advisory.crop}
            </span>
          )}
          {advisory.topic && (
            <span className="px-2.5 py-1 text-xs font-medium rounded-md bg-slate-100 text-slate-700 capitalize">
              {advisory.topic.replace('_', ' ')}
            </span>
          )}
          <span className={`px-2.5 py-1 text-xs font-medium rounded-md border ${
            advisory.confidence_level === 'Strong'
              ? 'bg-green-50 text-green-700 border-green-200'
              : advisory.confidence_level === 'Limited'
              ? 'bg-blue-50 text-blue-700 border-blue-200'
              : 'bg-amber-50 text-amber-700 border-amber-200'
          }`}>
            Evidence: {advisory.confidence_level}
          </span>
        </div>

        <div className="flex items-center space-x-2 text-xs text-slate-500">
          {latencySeconds && <span>⏱ {latencySeconds}s</span>}
          <button
            onClick={handleCopy}
            className="flex items-center space-x-1 px-2.5 py-1 rounded-md text-xs font-medium text-slate-600 bg-white border border-slate-200 hover:bg-slate-100 transition-colors"
          >
            {copied ? (
              <>
                <Check className="w-3.5 h-3.5 text-emerald-600" />
                <span className="text-emerald-600">Copied</span>
              </>
            ) : (
              <>
                <Copy className="w-3.5 h-3.5 text-slate-500" />
                <span>Copy</span>
              </>
            )}
          </button>
        </div>
      </div>

      <div className="p-5 sm:p-6 space-y-6">
        {/* 1. Core Recommendation */}
        <div>
          <h4 className="text-xs font-bold uppercase tracking-wider text-emerald-700 flex items-center space-x-1.5 mb-2">
            <Sparkles className="w-4 h-4 text-emerald-600" />
            <span>Recommendation</span>
          </h4>
          <p className="text-base sm:text-lg font-medium text-slate-900 leading-relaxed">
            {advisory.recommendation}
          </p>
        </div>

        {/* 2. Why this is recommended */}
        {advisory.why_recommended && (
          <div className="bg-slate-50 border border-slate-200/80 rounded-xl p-4">
            <h5 className="text-xs font-semibold uppercase tracking-wider text-slate-600 flex items-center space-x-1.5 mb-1">
              <Info className="w-3.5 h-3.5 text-slate-500" />
              <span>Scientific & Agronomic Rationale</span>
            </h5>
            <p className="text-sm text-slate-700 leading-relaxed">
              {advisory.why_recommended}
            </p>
          </div>
        )}

        {/* 3. Practical Steps */}
        {advisory.practical_steps && advisory.practical_steps.length > 0 && (
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center space-x-1.5 mb-3">
              <BookmarkCheck className="w-4 h-4 text-emerald-600" />
              <span>Practical Actionable Steps</span>
            </h4>
            <div className="space-y-2">
              {advisory.practical_steps.map((step, idx) => (
                <div key={idx} className="flex items-start space-x-3 text-sm text-slate-700 bg-slate-50/60 p-2.5 rounded-lg border border-slate-100">
                  <span className="w-5 h-5 rounded-full bg-emerald-100 text-emerald-800 font-bold text-xs flex items-center justify-center flex-shrink-0 mt-0.5">
                    {idx + 1}
                  </span>
                  <span>{step}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* 4. Important Precautions */}
        {advisory.important_precautions && advisory.important_precautions.length > 0 && (
          <div className="bg-amber-50/70 border border-amber-200 rounded-xl p-4">
            <h4 className="text-xs font-bold uppercase tracking-wider text-amber-900 flex items-center space-x-1.5 mb-2">
              <AlertTriangle className="w-4 h-4 text-amber-600" />
              <span>Critical Precautions & Safety</span>
            </h4>
            <ul className="space-y-1.5 text-xs sm:text-sm text-amber-950">
              {advisory.important_precautions.map((prec, idx) => (
                <li key={idx} className="flex items-start space-x-2">
                  <span className="text-amber-500 font-bold">•</span>
                  <span>{prec}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* 5. Regional Considerations */}
        {advisory.regional_considerations && (
          <div className="flex items-start space-x-2.5 text-xs text-slate-600 bg-slate-50 p-3 rounded-lg border border-slate-200">
            <MapPin className="w-4 h-4 text-slate-400 flex-shrink-0 mt-0.5" />
            <div>
              <span className="font-semibold text-slate-700">Regional Nuance: </span>
              {advisory.regional_considerations}
            </div>
          </div>
        )}

        {/* 6. Citations & Supporting Sources */}
        {advisory.sources && advisory.sources.length > 0 && (
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center space-x-1.5 mb-2.5">
              <FileText className="w-4 h-4 text-slate-500" />
              <span>Verified Agricultural Citations ({advisory.sources.length})</span>
            </h4>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
              {advisory.sources.map((src, i) => (
                <CitationBadge key={i} citation={src} />
              ))}
            </div>
          </div>
        )}

        {/* Footer Model Attribution & Disclaimer */}
        <div className="pt-3 border-t border-slate-100 flex flex-col sm:flex-row items-start sm:items-center justify-between text-[11px] text-slate-400 gap-2">
          <span>Engine: <strong className="text-slate-600">{modelUsed || 'AgriParam Grounded Adapter'}</strong></span>
          <span className="italic">{advisory.disclaimer}</span>
        </div>
      </div>
    </div>
  );
}

