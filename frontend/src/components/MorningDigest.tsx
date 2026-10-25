import React, { useState } from 'react';
import { Sparkles, Copy, Check } from 'lucide-react';
import type { DigestResponse } from '../api';

interface MorningDigestProps {
  digest: DigestResponse;
}

export const MorningDigest: React.FC<MorningDigestProps> = ({ digest }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    let md = `**Sloth Digest: ${digest.chat_name}**\n\n`;
    md += `*Summary:*\n${digest.two_line_summary}\n\n`;
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

  return (
    <article
      className="bg-white dark:bg-[#22201E] border border-[#EBE5DC] dark:border-[#34302C] rounded-2xl p-6 shadow-sm space-y-4"
      aria-labelledby="morning-digest-heading"
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Sparkles className="w-5 h-5 text-[#4A6B53]" />
          <h3 id="morning-digest-heading" className="text-sm font-semibold tracking-wide uppercase text-[#4A6B53]">
            Two-Line Executive Digest
          </h3>
        </div>
        <button
          onClick={handleCopy}
          className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium text-gray-700 bg-gray-50 hover:bg-gray-100 dark:bg-gray-800 dark:text-gray-300 border border-gray-200 dark:border-gray-700 transition-colors"
          aria-label="Copy entire morning digest to clipboard"
        >
          {copied ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
          {copied ? 'Copied' : 'Copy Digest'}
        </button>
      </div>

      <div className="space-y-2.5 text-base sm:text-lg leading-relaxed text-[#2D2A26] dark:text-[#E6E2DC] font-normal border-l-4 border-[#4A6B53] pl-4">
        {lines.map((line, idx) => (
          <p key={idx} className="tracking-tight">
            {line}
          </p>
        ))}
      </div>
    </article>
  );
};
