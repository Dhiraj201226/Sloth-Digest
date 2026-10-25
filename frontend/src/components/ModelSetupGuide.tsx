import React, { useState } from 'react';
import { Terminal, RefreshCw, Check, Copy } from 'lucide-react';

interface ModelSetupGuideProps {
  activeModel: string;
  onRetry: () => void;
}

export const ModelSetupGuide: React.FC<ModelSetupGuideProps> = ({ activeModel, onRetry }) => {
  const [copied, setCopied] = useState(false);
  const command = `ollama pull ${activeModel}`;

  const handleCopy = () => {
    navigator.clipboard.writeText(command);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="bg-[#FAF5ED] dark:bg-[#2C2620] border border-[#EADFCF] dark:border-[#3E362E] rounded-2xl p-6 shadow-sm space-y-5">
      <div className="flex items-center gap-3">
        <div className="p-2.5 bg-[#F4E9D8] dark:bg-[#3E362E] text-[#9C6528] rounded-xl">
          <Terminal className="w-6 h-6" />
        </div>
        <div>
          <h3 className="text-base font-bold text-[#1E1D1B] dark:text-[#E6E2DC]">
            First-Run Guide: Setup Your Local Model
          </h3>
          <p className="text-xs text-[#6B665F] dark:text-[#A09A90]">
            Sloth Digest needs a local open-weight model to read chats privately without the cloud.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs sm:text-sm">
        <div className="bg-white dark:bg-[#22201E] border border-[#EBE5DC] dark:border-[#34302C] rounded-xl p-4 space-y-2">
          <div className="flex items-center gap-2 font-bold text-[#4A6B53]">
            <span className="w-5 h-5 rounded-full bg-[#EBF2ED] flex items-center justify-center text-xs">1</span>
            <span>Install Ollama</span>
          </div>
          <p className="text-gray-600 dark:text-gray-400 text-xs">
            Download the free, open-source Ollama runtime from{' '}
            <a
              href="https://ollama.com"
              target="_blank"
              rel="noreferrer"
              className="text-[#4A6B53] underline font-medium"
            >
              ollama.com
            </a>.
          </p>
        </div>

        <div className="bg-white dark:bg-[#22201E] border border-[#EBE5DC] dark:border-[#34302C] rounded-xl p-4 space-y-2">
          <div className="flex items-center gap-2 font-bold text-[#4A6B53]">
            <span className="w-5 h-5 rounded-full bg-[#EBF2ED] flex items-center justify-center text-xs">2</span>
            <span>Pull {activeModel}</span>
          </div>
          <p className="text-gray-600 dark:text-gray-400 text-xs">Run this in your terminal:</p>
          <div className="flex items-center justify-between bg-gray-100 dark:bg-black/40 px-2 py-1.5 rounded-lg font-mono text-xs">
            <span>{command}</span>
            <button
              onClick={handleCopy}
              className="p-1 text-gray-500 hover:text-gray-800 dark:hover:text-gray-200"
              aria-label="Copy ollama pull command"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
            </button>
          </div>
        </div>

        <div className="bg-white dark:bg-[#22201E] border border-[#EBE5DC] dark:border-[#34302C] rounded-xl p-4 space-y-2 flex flex-col justify-between">
          <div className="space-y-1">
            <div className="flex items-center gap-2 font-bold text-[#4A6B53]">
              <span className="w-5 h-5 rounded-full bg-[#EBF2ED] flex items-center justify-center text-xs">3</span>
              <span>Verify & Relax</span>
            </div>
            <p className="text-gray-600 dark:text-gray-400 text-xs">
              Once downloaded, click check to start reading offline.
            </p>
          </div>
          <button
            onClick={onRetry}
            className="w-full mt-2 inline-flex items-center justify-center gap-2 px-3 py-2 rounded-xl text-xs font-semibold text-white bg-[#4A6B53] hover:bg-[#3D5944] transition-colors"
          >
            <RefreshCw className="w-3.5 h-3.5" /> Check Connection
          </button>
        </div>
      </div>
    </div>
  );
};
