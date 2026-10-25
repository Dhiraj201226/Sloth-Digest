import React from 'react';
import { UserCheck, Eye, CheckCircle2 } from 'lucide-react';
import type { ActionItem, SourceCitation } from '../api';

interface ActionItemListProps {
  items: ActionItem[];
  onSelectCitation: (citation: SourceCitation) => void;
}

export const ActionItemList: React.FC<ActionItemListProps> = ({ items, onSelectCitation }) => {
  return (
    <section className="space-y-3" aria-labelledby="action-items-heading">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <UserCheck className="w-5 h-5 text-[#9C6528]" />
          <h3 id="action-items-heading" className="text-base font-bold text-[#1E1D1B] dark:text-[#E6E2DC]">
            Who is Waiting on You ({items.length})
          </h3>
        </div>
        <span className="text-xs text-gray-400">Zero-guilt triage</span>
      </div>

      {items.length === 0 ? (
        <div className="bg-white dark:bg-[#22201E] border border-[#EBE5DC] dark:border-[#34302C] rounded-2xl p-6 text-center text-sm text-gray-500">
          <CheckCircle2 className="w-8 h-8 mx-auto text-emerald-600 mb-2 opacity-80" />
          No one is waiting on you! Enjoy your coffee and stay lazy.
        </div>
      ) : (
        <div className="space-y-2.5">
          {items.map((item) => (
            <article
              key={item.id}
              className="bg-white dark:bg-[#22201E] border border-[#EBE5DC] dark:border-[#34302C] rounded-xl p-4 shadow-sm hover:border-[#CDE0D2] transition-colors space-y-2.5"
            >
              <div className="flex items-start justify-between gap-3">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="px-2 py-0.5 rounded-full text-xs font-semibold bg-[#F4E9D8] text-[#835420] dark:bg-[#3E362E] dark:text-[#F4E9D8]">
                      {item.assignee_target}
                    </span>
                    <span className="text-xs text-gray-400">waiting on</span>
                  </div>
                  <p className="text-sm font-medium text-[#2D2A26] dark:text-[#E6E2DC] leading-snug">
                    {item.description}
                  </p>
                </div>

                <button
                  onClick={() => onSelectCitation(item.source)}
                  className="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg text-xs font-medium text-[#4A6B53] bg-[#EBF2ED] hover:bg-[#E1ECE3] dark:bg-[#222B24] dark:text-[#A8D1B2] transition-colors shrink-0 focus:ring-2 focus:ring-[#4A6B53]"
                  aria-label={`View source message for action: ${item.description}`}
                >
                  <Eye className="w-3.5 h-3.5" />
                  <span>View Source</span>
                </button>
              </div>
            </article>
          ))}
        </div>
      )}
    </section>
  );
};
