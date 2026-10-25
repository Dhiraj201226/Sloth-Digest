import React, { useState, useEffect } from 'react';
import { FolderCheck, X, Check, ArrowRight, Sparkles } from 'lucide-react';
import type { TidySuggestion } from '../api';
import { fetchTidierSuggestions, applyTidierSuggestions } from '../api';

interface TidierModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const TidierModal: React.FC<TidierModalProps> = ({ isOpen, onClose }) => {
  const [suggestions, setSuggestions] = useState<TidySuggestion[]>([]);
  const [loading, setLoading] = useState(false);
  const [applied, setApplied] = useState(false);

  useEffect(() => {
    if (isOpen) {
      setLoading(true);
      setApplied(false);
      fetchTidierSuggestions()
        .then((data) => setSuggestions(data))
        .catch(() => setSuggestions([]))
        .finally(() => setLoading(false));
    }
  }, [isOpen]);

  const handleApply = async () => {
    setLoading(true);
    try {
      await applyTidierSuggestions(suggestions);
      setApplied(true);
      const updated = await fetchTidierSuggestions();
      setSuggestions(updated);
    } catch (e) {
      alert('Failed to apply tidy suggestions');
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm"
      role="dialog"
      aria-modal="true"
      aria-labelledby="tidier-title"
    >
      <div className="bg-white dark:bg-[#22201E] border border-[#EBE5DC] dark:border-[#34302C] rounded-2xl max-w-xl w-full p-6 shadow-2xl space-y-4">
        <div className="flex items-center justify-between border-b border-[#EBE5DC] dark:border-[#34302C] pb-3">
          <div className="flex items-center gap-2">
            <span className="p-1.5 rounded-lg bg-[#FAF5ED] text-[#9C6528]">
              <FolderCheck className="w-5 h-5" />
            </span>
            <h3 id="tidier-title" className="text-base font-semibold text-[#1E1D1B] dark:text-[#E6E2DC]">
              File & Inbox Tidier (Lazy Mode)
            </h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-gray-400 hover:text-gray-600 hover:bg-gray-100 dark:hover:bg-gray-800"
            aria-label="Close tidier dialog"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {applied && (
          <div className="p-3 bg-[#EBF2ED] text-[#304736] border border-[#CDE0D2] rounded-xl text-xs flex items-center gap-2">
            <Check className="w-4 h-4" /> All selected suggestions have been applied cleanly.
          </div>
        )}

        <p className="text-xs text-[#6B665F] dark:text-[#A09A90]">
          Clean your chat exports folder with zero effort. Sloth standardizes chaotic WhatsApp export filenames and moves stale chats into an archive folder.
        </p>

        {loading ? (
          <div className="py-8 text-center text-xs text-gray-500">Scanning chat files...</div>
        ) : suggestions.length === 0 ? (
          <div className="py-8 text-center space-y-2">
            <Sparkles className="w-8 h-8 mx-auto text-emerald-600 opacity-80" />
            <p className="text-sm font-semibold text-gray-700 dark:text-gray-300">
              Your chat directory is completely tidy!
            </p>
            <p className="text-xs text-gray-500">No messy filenames or stale chats detected.</p>
          </div>
        ) : (
          <div className="space-y-2.5 max-h-64 overflow-y-auto pr-1">
            {suggestions.map((s, idx) => (
              <div
                key={idx}
                className="p-3 bg-[#FAF5ED]/50 dark:bg-[#2A2724]/40 border border-[#EBE5DC] dark:border-[#34302C] rounded-xl flex items-center justify-between gap-3 text-xs"
              >
                <div className="space-y-1">
                  <div className="flex items-center gap-1.5 font-medium text-gray-700 dark:text-gray-300">
                    <span className="font-mono line-through text-gray-400">{s.original_name}</span>
                    <ArrowRight className="w-3 h-3 text-[#4A6B53]" />
                    <span className="font-mono text-[#304736] dark:text-[#A8D1B2] font-semibold">
                      {s.suggested_name}
                    </span>
                  </div>
                  <span className="text-gray-500 block">{s.reason}</span>
                </div>
                <span className="px-2 py-0.5 rounded text-[11px] font-semibold uppercase tracking-wider bg-[#EBF2ED] text-[#304736]">
                  {s.action}
                </span>
              </div>
            ))}
          </div>
        )}

        <div className="flex justify-between items-center pt-3 border-t border-[#EBE5DC] dark:border-[#34302C]">
          <span className="text-xs text-gray-400">
            {suggestions.length > 0 ? `${suggestions.length} suggestion(s)` : ''}
          </span>
          <div className="flex gap-2">
            <button
              onClick={onClose}
              className="px-3.5 py-1.5 rounded-xl text-xs font-medium text-gray-600 hover:bg-gray-100 dark:text-gray-300 dark:hover:bg-gray-800"
            >
              Cancel
            </button>
            {suggestions.length > 0 && (
              <button
                onClick={handleApply}
                disabled={loading}
                className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-semibold text-white bg-[#4A6B53] hover:bg-[#3D5944] transition-colors"
              >
                <Check className="w-3.5 h-3.5" /> Apply All (Lazy Mode)
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
