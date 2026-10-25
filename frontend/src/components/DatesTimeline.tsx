import React from 'react';
import { Calendar, Eye, Clock } from 'lucide-react';
import type { DeadlineItem, SourceCitation } from '../api';

interface DatesTimelineProps {
  items: DeadlineItem[];
  onSelectCitation: (citation: SourceCitation) => void;
}

export const DatesTimeline: React.FC<DatesTimelineProps> = ({ items, onSelectCitation }) => {
  return (
    <section className="space-y-3" aria-labelledby="deadlines-heading">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Calendar className="w-5 h-5 text-[#4A6B53]" />
          <h3 id="deadlines-heading" className="text-base font-bold text-[#1E1D1B] dark:text-[#E6E2DC]">
            Dates & Deadlines Mentioned ({items.length})
          </h3>
        </div>
        <span className="text-xs text-gray-400">Chronological</span>
      </div>

      {items.length === 0 ? (
        <div className="bg-white dark:bg-[#22201E] border border-[#EBE5DC] dark:border-[#34302C] rounded-2xl p-6 text-center text-sm text-gray-500">
          <Clock className="w-8 h-8 mx-auto text-gray-400 mb-2 opacity-60" />
          No specific dates or deadlines were mentioned in this chat.
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
                    <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-[#EBF2ED] text-[#304736] dark:bg-[#222B24] dark:text-[#A8D1B2]">
                      📅 {item.date_mentioned}
                    </span>
                  </div>
                  <p className="text-sm font-medium text-[#2D2A26] dark:text-[#E6E2DC] leading-snug">
                    {item.event_description}
                  </p>
                </div>

                <button
                  onClick={() => onSelectCitation(item.source)}
                  className="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg text-xs font-medium text-[#4A6B53] bg-[#EBF2ED] hover:bg-[#E1ECE3] dark:bg-[#222B24] dark:text-[#A8D1B2] transition-colors shrink-0 focus:ring-2 focus:ring-[#4A6B53]"
                  aria-label={`View source message for date: ${item.date_mentioned}`}
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
