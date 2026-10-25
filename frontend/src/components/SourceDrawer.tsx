import React, { useEffect } from 'react';
import { X, CheckCircle } from 'lucide-react';
import type { SourceCitation } from '../api';

interface SourceDrawerProps {
  citation: SourceCitation | null;
  onClose: () => void;
}

export const SourceDrawer: React.FC<SourceDrawerProps> = ({ citation, onClose }) => {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onClose]);

  if (!citation) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm transition-opacity"
      role="dialog"
      aria-modal="true"
      aria-labelledby="source-drawer-title"
    >
      <div className="bg-white dark:bg-[#22201E] border border-[#EBE5DC] dark:border-[#34302C] rounded-2xl max-w-lg w-full p-6 shadow-2xl space-y-4 animate-in fade-in zoom-in-95 duration-150">
        <div className="flex items-center justify-between border-b border-[#EBE5DC] dark:border-[#34302C] pb-3">
          <div className="flex items-center gap-2">
            <span className="p-1.5 rounded-lg bg-[#EBF2ED] text-[#304736]">
              <CheckCircle className="w-4 h-4" />
            </span>
            <h3 id="source-drawer-title" className="text-base font-semibold text-[#1E1D1B] dark:text-[#E6E2DC]">
              Hallucination Guard: Source Citation
            </h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-gray-400 hover:text-gray-600 hover:bg-gray-100 dark:hover:bg-gray-800"
            aria-label="Close source drawer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="space-y-3">
          <div className="flex items-center justify-between text-xs text-gray-500 pb-1">
            <div className="flex items-center gap-1.5">
              <span className="font-semibold text-gray-700 dark:text-gray-300">{citation.sender}</span>
              <span>·</span>
              <span className="font-mono">{citation.timestamp}</span>
            </div>
            <span className="px-2 py-0.5 rounded bg-gray-100 dark:bg-gray-800 font-mono text-gray-600 dark:text-gray-400">
              Line {citation.line_number}
            </span>
          </div>

          <div className="p-4 bg-[#FDFBF7] dark:bg-[#1A1918] border border-[#EBE5DC] dark:border-[#34302C] rounded-xl font-mono text-xs sm:text-sm text-gray-800 dark:text-gray-200 whitespace-pre-wrap leading-relaxed">
            {citation.raw_text}
          </div>

          <p className="text-xs text-[#6B665F] dark:text-[#A09A90] italic">
            ✓ Verified Grounding: Extracted directly from the original raw chat export without LLM fabrication.
          </p>
        </div>

        <div className="flex justify-end pt-2">
          <button
            onClick={onClose}
            className="px-4 py-2 rounded-xl text-xs font-semibold text-white bg-[#4A6B53] hover:bg-[#3D5944] focus:ring-2 focus:ring-[#4A6B53] focus:ring-offset-2"
          >
            Dismiss
          </button>
        </div>
      </div>
    </div>
  );
};
