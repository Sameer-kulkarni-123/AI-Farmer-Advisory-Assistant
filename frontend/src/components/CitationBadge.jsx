import React, { useState } from 'react';
import { BookOpen, ExternalLink, CheckCircle, ChevronDown, ChevronUp } from 'lucide-react';

export default function CitationBadge({ citation }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="border border-emerald-200 bg-emerald-50/60 rounded-xl p-3 text-xs text-slate-700 transition-all hover:bg-emerald-50">
      <div className="flex items-start justify-between gap-2">
        <div className="flex items-start space-x-2">
          <BookOpen className="w-4 h-4 text-emerald-600 flex-shrink-0 mt-0.5" />
          <div>
            <div className="font-semibold text-emerald-950 flex items-center space-x-1.5">
              <span>{citation.title}</span>
              <span className="inline-flex items-center px-1.5 py-0.2 rounded text-[10px] font-medium bg-emerald-100 text-emerald-800">
                <CheckCircle className="w-2.5 h-2.5 mr-0.5 text-emerald-600" /> Verified
              </span>
            </div>
            <div className="text-slate-500 text-[11px] mt-0.5">
              {citation.source} {citation.similarity_score ? `• Similarity: ${(citation.similarity_score * 100).toFixed(0)}%` : ''}
            </div>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          {citation.source_url && (
            <a
              href={citation.source_url}
              target="_blank"
              rel="noreferrer"
              title="Open Official Publication"
              className="p-1 rounded hover:bg-emerald-100 text-emerald-700"
            >
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
          )}
          {citation.excerpt && (
            <button
              onClick={() => setExpanded(!expanded)}
              className="p-1 rounded hover:bg-emerald-100 text-emerald-700"
            >
              {expanded ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
            </button>
          )}
        </div>
      </div>

      {expanded && citation.excerpt && (
        <div className="mt-2.5 pt-2 border-t border-emerald-200/80 text-[11px] text-slate-600 italic bg-white/70 p-2 rounded">
          "{citation.excerpt}"
        </div>
      )}
    </div>
  );
}

