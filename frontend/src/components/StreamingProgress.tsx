import React from 'react';
import { Moon } from 'lucide-react';
import type { ProgressEvent } from '../api';

interface StreamingProgressProps {
  progress: ProgressEvent | null;
  chatName: string;
}

export const StreamingProgress: React.FC<StreamingProgressProps> = ({ progress, chatName }) => {
  const percent = progress ? progress.percent : 10;
  const message = progress ? progress.message : 'Waking up local model...';
  const eta = progress ? progress.estimated_remaining_sec : 15;
  const chunkInfo = progress && progress.total_chunks > 0 ? `Chunk ${progress.current_chunk} of ${progress.total_chunks}` : 'Preparing slices';

  return (
    <div
      className="bg-white dark:bg-[#22201E] border border-[#EBE5DC] dark:border-[#34302C] rounded-2xl p-8 shadow-sm space-y-6 text-center animate-calm-pulse"
      role="status"
      aria-live="polite"
    >
      <div className="flex flex-col items-center gap-3">
        <div className="p-3.5 bg-[#FAF5ED] dark:bg-[#2C2620] text-[#4A6B53] rounded-full">
          <Moon className="w-8 h-8 animate-pulse text-[#4A6B53]" />
        </div>
        <div className="space-y-1">
          <h3 className="text-lg font-bold text-[#1E1D1B] dark:text-[#E6E2DC]">
            Sloth is reading "{chatName}" while you relax...
          </h3>
          <p className="text-xs text-[#6B665F] dark:text-[#A09A90]">
            Running 100% locally on localhost. No data leaves this device.
          </p>
        </div>
      </div>

      <div className="space-y-2 max-w-md mx-auto">
        <div className="flex justify-between text-xs text-gray-500 font-medium">
          <span>{chunkInfo}</span>
          <span className="font-mono">~{eta}s remaining</span>
        </div>
        <div className="w-full bg-[#EBE5DC] dark:bg-[#34302C] rounded-full h-3 overflow-hidden">
          <div
            className="bg-[#4A6B53] h-full rounded-full transition-all duration-300 ease-out"
            style={{ width: `${percent}%` }}
          />
        </div>
        <p className="text-xs text-gray-600 dark:text-gray-400 italic pt-1">
          {message}
        </p>
      </div>
    </div>
  );
};
