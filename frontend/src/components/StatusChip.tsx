import React, { useState } from 'react';
import { ShieldCheck, X, RefreshCw } from 'lucide-react';
import type { SystemHealth } from '../api';

interface StatusChipProps {
  health: SystemHealth | null;
  onRefresh: () => void;
}

export const StatusChip: React.FC<StatusChipProps> = ({ health, onRefresh }) => {
  const [modalOpen, setModalOpen] = useState(false);

  const modelTag = health?.active_model || 'qwen2.5:1.5b';
  const isReady = health?.status === 'ready';

  return (
    <>
      <button
        onClick={() => setModalOpen(true)}
        className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-medium bg-[#EBF2ED] text-[#304736] border border-[#CDE0D2] hover:bg-[#E1ECE3] transition-colors focus:ring-2 focus:ring-[#4A6B53] focus:ring-offset-1"
        aria-label={`Offline status: Nothing leaves this machine. Model: ${modelTag}. Click for diagnostics.`}
      >
        <span className={`w-2 h-2 rounded-full ${isReady ? 'bg-emerald-600' : 'bg-amber-600 animate-pulse'}`} />
        <span className="font-semibold">Offline · nothing leaves this machine</span>
        <span className="text-gray-500 font-mono">[{modelTag}]</span>
      </button>

      {modalOpen && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm"
          role="dialog"
          aria-modal="true"
          aria-labelledby="diagnostics-title"
        >
          <div className="bg-[#FFFFFF] dark:bg-[#22201E] border border-[#EBE5DC] dark:border-[#34302C] rounded-2xl max-w-md w-full p-6 shadow-xl space-y-4">
            <div className="flex items-center justify-between border-b border-[#EBE5DC] dark:border-[#34302C] pb-3">
              <div className="flex items-center gap-2">
                <ShieldCheck className="w-5 h-5 text-[#4A6B53]" />
                <h3 id="diagnostics-title" className="text-base font-semibold text-[#1E1D1B] dark:text-[#E6E2DC]">
                  Local Offline Diagnostics
                </h3>
              </div>
              <button
                onClick={() => setModalOpen(false)}
                className="p-1 rounded-lg text-gray-400 hover:text-gray-600 hover:bg-gray-100 dark:hover:bg-gray-800"
                aria-label="Close diagnostics dialog"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-3 text-sm">
              <div className="flex justify-between py-1 border-b border-gray-100 dark:border-gray-800">
                <span className="text-gray-500">Airgap Guarantee:</span>
                <span className="font-medium text-emerald-700 dark:text-emerald-400">100% Localhost Only</span>
              </div>
              <div className="flex justify-between py-1 border-b border-gray-100 dark:border-gray-800">
                <span className="text-gray-500">Ollama Connection:</span>
                <span className="font-mono text-xs">{health?.ollama_connected ? 'Connected (127.0.0.1:11434)' : 'Unreachable'}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-gray-100 dark:border-gray-800">
                <span className="text-gray-500">Active Model:</span>
                <span className="font-mono text-xs font-semibold">{modelTag}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-gray-100 dark:border-gray-800">
                <span className="text-gray-500">System Status:</span>
                <span className="capitalize font-medium">{health?.status || 'Unknown'}</span>
              </div>

              {health?.available_models && health.available_models.length > 0 && (
                <div className="pt-2">
                  <span className="text-xs text-gray-500 block mb-1">Installed Local Models:</span>
                  <div className="flex flex-wrap gap-1">
                    {health.available_models.map((m) => (
                      <span key={m} className="px-2 py-0.5 text-xs bg-gray-100 dark:bg-gray-800 rounded font-mono">
                        {m}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {health?.error_message && (
                <div className="p-3 bg-amber-50 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-800 rounded-lg text-xs text-amber-800 dark:text-amber-200">
                  {health.error_message}
                </div>
              )}
            </div>

            <div className="flex justify-end gap-2 pt-2">
              <button
                onClick={onRefresh}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-300"
              >
                <RefreshCw className="w-3.5 h-3.5" /> Re-check
              </button>
              <button
                onClick={() => setModalOpen(false)}
                className="px-4 py-1.5 rounded-lg text-xs font-medium text-white bg-[#4A6B53] hover:bg-[#3D5944]"
              >
                Done
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};
