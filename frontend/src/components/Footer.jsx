import React from 'react';
import { ShieldAlert, ExternalLink, Heart } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="bg-white border-t border-slate-200 mt-auto py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Safety Disclaimer Banner */}
        <div className="bg-amber-50 border border-amber-200 rounded-xl p-4 mb-6 flex items-start space-x-3 text-amber-900 text-xs sm:text-sm">
          <ShieldAlert className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
          <div>
            <span className="font-semibold">Agricultural Safety Disclaimer:</span> All advisories are evidence-grounded syntheses of published ICAR, KVK, and DAC&FW bulletins. Chemical dosages, pesticide interventions, and major irrigation investments should be validated against local soil test results and with your nearest Krishi Vigyan Kendra (KVK) officer.
          </div>
        </div>

        <div className="flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 gap-4">
          <div>
            Krishi Mitra AI — CS3235 Capstone Project using BharatGen AgriParam & AI4Bharat IndicTrans2.
          </div>
          <div className="flex items-center space-x-4">
            <a href="https://icar.org.in" target="_blank" rel="noreferrer" className="hover:text-emerald-700 flex items-center space-x-1">
              <span>ICAR</span>
              <ExternalLink className="w-3 h-3" />
            </a>
            <a href="https://agriwelfare.gov.in" target="_blank" rel="noreferrer" className="hover:text-emerald-700 flex items-center space-x-1">
              <span>AgriWelfare</span>
              <ExternalLink className="w-3 h-3" />
            </a>
            <a href="https://pmkisan.gov.in" target="_blank" rel="noreferrer" className="hover:text-emerald-700 flex items-center space-x-1">
              <span>PM-KISAN</span>
              <ExternalLink className="w-3 h-3" />
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}

