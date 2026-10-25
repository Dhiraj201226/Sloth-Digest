import React, { useState } from 'react';
import {
  Sparkles,
  Copy,
  Check,
  ChevronDown,
  ChevronUp,
  ShieldAlert,
  FileText,
  MessageSquare,
} from 'lucide-react';
import type { DigestResponse } from '../api';

interface MorningDigestProps {
  digest: DigestResponse;
  onOpenChatView?: () => void;
}

export const MorningDigest: React.FC<MorningDigestProps> = ({
  digest,
  onOpenChatView,
}) => {
  const [copied, setCopied] = useState(false);
  const [showDetailed, setShowDetailed] = useState(true);

  const handleCopy = () => {
    let md = `**Sloth Digest: ${digest.chat_name}**\n\n`;
    md += `*Overall Classification: ${digest.overall_classification.toUpperCase()}*\n\n`;
    md += `*Two-Line Executive Digest:*\n${digest.two_line_summary}\n\n`;
    if (digest.detailed_summary) {
      md += `*Detailed Summary Breakdown:*\n${digest.detailed_summary}\n\n`;
    }
    if (digest.action_items.length > 0) {
      md += `*Action Items:*\n`;
      digest.action_items.forEach((a) => {
        md += `- [ ] (${a.assignee_target}): ${a.description} [Line ${a.source.line_number}]\n`;
      });
      md += `\n`;
    }
    if (digest.deadlines.length > 0) {
      md += `*Dates & Deadlines:*\n`;
      digest.deadlines.forEach((d) => {
        md += `- 📅 ${d.date_mentioned}: ${d.event_description}\n`;
      });
    }

    navigator.clipboard.writeText(md);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const lines = digest.two_line_summary.split('\n').filter((l) => l.trim().length > 0);

  const getClassificationBadge = () => {
    switch (digest.overall_classification) {
      case 'important':
        return {
          icon: <Sparkles className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />,
          label: 'Classified: High Priority / Action-Heavy',
          badgeClass:
            'bg-emerald-50 text-emerald-800 border-emerald-200 dark:bg-emerald-950/50 dark:text-emerald-300 dark:border-emerald-800',
        };
      case 'spam':
        return {
          icon: <ShieldAlert className="w-3.5 h-3.5 text-amber-600 dark:text-amber-400" />,
          label: 'Classified: Mostly Spam & Casual Banter',
          badgeClass:
            'bg-amber-50 text-amber-800 border-amber-200 dark:bg-amber-950/50 dark:text-amber-300 dark:border-amber-800',
        };
      case 'balanced':
      default:
        return {
          icon: <FileText className="w-3.5 h-3.5 text-[#4A6B53] dark:text-[#A8D1B2]" />,
          label: 'Classified: Balanced Discussion',
          badgeClass:
            'bg-[#EBF2ED] text-[#304736] border-[#D0E2D5] dark:bg-[#202E24] dark:text-[#A8D1B2] dark:border-[#2E4233]',
        };
    }
  };

  const badge = getClassificationBadge();

  return (
    <article
      className="bg-white dark:bg-[#22201E] border border-[#EBE5DC] dark:border-[#34302C] rounded-2xl p-6 shadow-sm space-y-5"
      aria-labelledby="morning-digest-heading"
    >
      {/* Top Header Row with Title, Classification Pill, and Copy Action */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div className="flex flex-wrap items-center gap-2">
          <div className="flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-[#4A6B53]" />
            <h3
              id="morning-digest-heading"
              className="text-sm font-semibold tracking-wide uppercase text-[#4A6B53]"
            >
              Executive Morning Digest
            </h3>
          </div>

          {/* Classification Pill */}
          <span
            className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold border ${badge.badgeClass}`}
          >
            {badge.icon}
            <span>{badge.label}</span>
          </span>
        </div>

        <div className="flex items-center gap-2">
          {onOpenChatView && (
            <button
              onClick={onOpenChatView}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium text-[#304736] bg-[#EBF2ED] hover:bg-[#E1ECE3] dark:bg-[#222B24] dark:text-[#A8D1B2] border border-[#D0E2D5] dark:border-[#2E4233] transition-colors"
            >
              <MessageSquare className="w-3.5 h-3.5" />
              <span>View Chat ({digest.total_messages})</span>
            </button>
          )}

          <button
            onClick={handleCopy}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium text-gray-700 bg-gray-50 hover:bg-gray-100 dark:bg-gray-800 dark:text-gray-300 border border-gray-200 dark:border-gray-700 transition-colors"
            aria-label="Copy entire morning digest to clipboard"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
            {copied ? 'Copied' : 'Copy Digest'}
          </button>
        </div>
      </div>

      {/* Two-Line Summary Quotes */}
      <div className="space-y-2.5 text-base sm:text-lg leading-relaxed text-[#2D2A26] dark:text-[#E6E2DC] font-normal border-l-4 border-[#4A6B53] pl-4">
        {lines.map((line, idx) => (
          <p key={idx} className="tracking-tight font-medium">
            {line}
          </p>
        ))}
      </div>

      {/* Metric Counters Strip */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2">
        <div className="p-3 rounded-xl bg-[#FAF8F5] dark:bg-[#1A1918] border border-[#EBE5DC] dark:border-[#302D2A]">
          <span className="text-[11px] text-gray-500 block">Total Messages</span>
          <span className="text-lg font-bold text-[#1E1D1B] dark:text-[#E6E2DC]">
            {digest.total_messages}
          </span>
        </div>
        <div className="p-3 rounded-xl bg-emerald-50/70 dark:bg-emerald-950/20 border border-emerald-200 dark:border-emerald-900/50">
          <span className="text-[11px] text-emerald-800 dark:text-emerald-400 font-medium block">
            ⭐ Important
          </span>
          <span className="text-lg font-bold text-emerald-900 dark:text-emerald-200">
            {digest.important_count}
          </span>
        </div>
        <div className="p-3 rounded-xl bg-amber-50/70 dark:bg-amber-950/20 border border-amber-200 dark:border-amber-900/50">
          <span className="text-[11px] text-amber-800 dark:text-amber-400 font-medium block">
            🛡️ Spam / Filtered
          </span>
          <span className="text-lg font-bold text-amber-900 dark:text-amber-200">
            {digest.spam_count}
          </span>
        </div>
        <div className="p-3 rounded-xl bg-[#FAF8F5] dark:bg-[#1A1918] border border-[#EBE5DC] dark:border-[#302D2A]">
          <span className="text-[11px] text-gray-500 block">Safe to Ignore</span>
          <span className="text-lg font-bold text-[#9C6528] dark:text-[#D1A066]">
            {digest.safe_to_ignore_count}
          </span>
        </div>
      </div>

      {/* Expandable Detailed Summary Breakdown */}
      {digest.detailed_summary && (
        <div className="pt-2 border-t border-[#EBE5DC] dark:border-[#34302C]">
          <button
            onClick={() => setShowDetailed(!showDetailed)}
            className="w-full flex items-center justify-between py-2 text-xs font-semibold text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors"
          >
            <div className="flex items-center gap-1.5">
              <FileText className="w-4 h-4 text-[#4A6B53]" />
              <span>Detailed Discussion Breakdown</span>
            </div>
            {showDetailed ? (
              <ChevronUp className="w-4 h-4" />
            ) : (
              <ChevronDown className="w-4 h-4" />
            )}
          </button>

          {showDetailed && (
            <div className="mt-3 p-4 rounded-xl bg-[#FAF8F5] dark:bg-[#1A1918] border border-[#EBE5DC] dark:border-[#302D2A] text-xs sm:text-sm text-[#3E3A35] dark:text-[#D8D3CC] leading-relaxed space-y-3">
              {digest.detailed_summary.split('\n\n').map((paragraph, pIdx) => {
                // If paragraph has bold title e.g. **Title**: content
                if (paragraph.startsWith('**') && paragraph.includes('**:')) {
                  const colonIdx = paragraph.indexOf('**:');
                  const heading = paragraph.slice(2, colonIdx);
                  const body = paragraph.slice(colonIdx + 3);
                  return (
                    <div key={pIdx} className="space-y-1">
                      <h4 className="font-bold text-[#1E1D1B] dark:text-[#EAE5DC] text-xs tracking-wide uppercase text-[#4A6B53]">
                        {heading}
                      </h4>
                      <p>{body.trim()}</p>
                    </div>
                  );
                }
                return <p key={pIdx}>{paragraph}</p>;
              })}
            </div>
          )}
        </div>
      )}
    </article>
  );
};
