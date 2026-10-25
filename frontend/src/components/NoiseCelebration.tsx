import React from 'react';
import { Coffee } from 'lucide-react';

interface NoiseCelebrationProps {
  safeCount: number;
  totalMessages: number;
  chatName: string;
  durationSec: number;
}

export const NoiseCelebration: React.FC<NoiseCelebrationProps> = ({
  safeCount,
  totalMessages,
  chatName,
  durationSec,
}) => {
  const noisePercent = totalMessages > 0 ? Math.round((safeCount / totalMessages) * 100) : 0;

  return (
    <div className="relative overflow-hidden bg-gradient-to-r from-[#F4E9D8]/60 via-[#FDFBF7] to-[#E1ECE3]/60 dark:from-[#2A2724] dark:via-[#181716] dark:to-[#222B24] border border-[#EBE5DC] dark:border-[#34302C] rounded-2xl p-6 shadow-sm">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-start gap-4">
          <div className="p-3 bg-[#FAF5ED] dark:bg-[#2C2620] border border-[#EADFCF] dark:border-[#3E362E] rounded-2xl text-[#9C6528]">
            <Coffee className="w-8 h-8" />
          </div>
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="text-xs uppercase tracking-wider font-semibold text-[#4A6B53]">
                Slow & Steady Reward
              </span>
              <span className="text-xs text-gray-400">·</span>
              <span className="text-xs text-gray-500 font-medium">{chatName}</span>
            </div>
            <h2 className="text-xl sm:text-2xl font-bold tracking-tight text-[#1E1D1B] dark:text-[#E6E2DC]">
              Good morning. You safely bypassed{' '}
              <span className="text-[#9C6528] underline decoration-[#9C6528]/30 underline-offset-4">
                {safeCount.toLocaleString()} messages
              </span>
              .
            </h2>
            <p className="text-sm text-[#6B665F] dark:text-[#A09A90]">
              {noisePercent}% of the conversation was pure chatter, memes, or logistics you didn't have to read.
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3 self-start md:self-auto pt-2 md:pt-0">
          <div className="px-3.5 py-2 rounded-xl bg-white/80 dark:bg-[#22201E]/80 border border-[#EBE5DC] dark:border-[#34302C] text-center">
            <span className="block text-xs text-gray-400">Total Read</span>
            <span className="text-sm font-semibold text-[#1E1D1B] dark:text-[#E6E2DC]">{totalMessages}</span>
          </div>
          <div className="px-3.5 py-2 rounded-xl bg-white/80 dark:bg-[#22201E]/80 border border-[#EBE5DC] dark:border-[#34302C] text-center">
            <span className="block text-xs text-gray-400">Time Taken</span>
            <span className="text-sm font-semibold text-[#1E1D1B] dark:text-[#E6E2DC]">{durationSec}s</span>
          </div>
        </div>
      </div>
    </div>
  );
};
