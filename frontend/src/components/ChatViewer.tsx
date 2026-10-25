import React, { useState, useMemo, useEffect, useRef } from 'react';
import {
  MessageSquare,
  Sparkles,
  ShieldAlert,
  Search,
  Copy,
  Check,
  Filter,
  Hash,
} from 'lucide-react';
import type { ClassifiedMessage, SourceCitation } from '../api';

interface ChatViewerProps {
  messages: ClassifiedMessage[];
  chatName: string;
  highlightedLine?: number | null;
  onSelectCitation?: (citation: SourceCitation) => void;
}

// Deterministic pastel color generator for avatar initials based on sender name
const getAvatarColor = (sender: string): { bg: string; text: string } => {
  const colors = [
    { bg: 'bg-emerald-100 dark:bg-emerald-950/60', text: 'text-emerald-800 dark:text-emerald-300' },
    { bg: 'bg-amber-100 dark:bg-amber-950/60', text: 'text-amber-800 dark:text-amber-300' },
    { bg: 'bg-blue-100 dark:bg-blue-950/60', text: 'text-blue-800 dark:text-blue-300' },
    { bg: 'bg-purple-100 dark:bg-purple-950/60', text: 'text-purple-800 dark:text-purple-300' },
    { bg: 'bg-rose-100 dark:bg-rose-950/60', text: 'text-rose-800 dark:text-rose-300' },
    { bg: 'bg-teal-100 dark:bg-teal-950/60', text: 'text-teal-800 dark:text-teal-300' },
    { bg: 'bg-indigo-100 dark:bg-indigo-950/60', text: 'text-indigo-800 dark:text-indigo-300' },
    { bg: 'bg-orange-100 dark:bg-orange-950/60', text: 'text-orange-800 dark:text-orange-300' },
  ];
  let hash = 0;
  for (let i = 0; i < sender.length; i++) {
    hash = sender.charCodeAt(i) + ((hash << 5) - hash);
  }
  const index = Math.abs(hash) % colors.length;
  return colors[index];
};

const getInitials = (name: string): string => {
  if (!name) return '?';
  const parts = name.trim().split(/\s+/);
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase();
  }
  return name.slice(0, 2).toUpperCase();
};

export const ChatViewer: React.FC<ChatViewerProps> = ({
  messages,
  chatName,
  highlightedLine,
  onSelectCitation,
}) => {
  const [filter, setFilter] = useState<'all' | 'important' | 'spam' | 'normal'>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const messageRefs = useRef<{ [key: number]: HTMLDivElement | null }>({});

  const importantCount = useMemo(
    () => messages.filter((m) => m.classification === 'important').length,
    [messages]
  );
  const spamCount = useMemo(
    () => messages.filter((m) => m.classification === 'spam').length,
    [messages]
  );
  const normalCount = useMemo(
    () => messages.filter((m) => m.classification === 'normal').length,
    [messages]
  );

  const filteredMessages = useMemo(() => {
    return messages.filter((m) => {
      // Classification filter
      if (filter !== 'all' && m.classification !== filter) {
        return false;
      }
      // Search query filter
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        const matchesSender = m.sender.toLowerCase().includes(q);
        const matchesText = m.text.toLowerCase().includes(q);
        const matchesReason = m.classification_reason?.toLowerCase().includes(q);
        return matchesSender || matchesText || matchesReason;
      }
      return true;
    });
  }, [messages, filter, searchQuery]);

  // Scroll to highlighted line if provided
  useEffect(() => {
    if (highlightedLine && messageRefs.current[highlightedLine]) {
      messageRefs.current[highlightedLine]?.scrollIntoView({
        behavior: 'smooth',
        block: 'center',
      });
    }
  }, [highlightedLine]);

  const handleCopyMessage = (m: ClassifiedMessage) => {
    const textToCopy = `[${m.timestamp}] ${m.sender}: ${m.text}`;
    navigator.clipboard.writeText(textToCopy);
    setCopiedId(m.message_id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  return (
    <div className="bg-white dark:bg-[#22201E] border border-[#EBE5DC] dark:border-[#34302C] rounded-2xl shadow-sm overflow-hidden flex flex-col h-[750px]">
      {/* Top Controls Toolbar */}
      <div className="p-4 border-b border-[#EBE5DC] dark:border-[#34302C] bg-[#FAF8F5]/80 dark:bg-[#1E1C1A]/80 backdrop-blur space-y-3">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <MessageSquare className="w-5 h-5 text-[#4A6B53]" />
            <div>
              <h2 className="text-sm font-bold tracking-tight text-[#2D2A26] dark:text-[#E6E2DC]">
                {chatName}
              </h2>
              <p className="text-[11px] text-[#6B665F] dark:text-[#A09A90]">
                {messages.length} messages parsed · Local AI classified
              </p>
            </div>
          </div>

          {/* Search Bar */}
          <div className="relative w-full sm:w-64">
            <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
            <input
              type="text"
              placeholder="Filter by sender or keyword..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-9 pr-3 py-1.5 text-xs rounded-xl bg-white dark:bg-[#181716] border border-gray-200 dark:border-gray-700 text-[#2D2A26] dark:text-[#E6E2DC] placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#4A6B53]/50 transition-shadow"
            />
            {searchQuery && (
              <button
                onClick={() => setSearchQuery('')}
                className="absolute right-2.5 top-1/2 -translate-y-1/2 text-[10px] text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 font-semibold"
              >
                ✕
              </button>
            )}
          </div>
        </div>

        {/* Filter Pills */}
        <div className="flex flex-wrap items-center gap-1.5 pt-1">
          <button
            onClick={() => setFilter('all')}
            className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-medium transition-all ${
              filter === 'all'
                ? 'bg-[#4A6B53] text-white shadow-sm'
                : 'bg-gray-100 hover:bg-gray-200 text-gray-700 dark:bg-gray-800 dark:text-gray-300'
            }`}
          >
            <Filter className="w-3 h-3" />
            <span>All Messages</span>
            <span className="text-[10px] opacity-75 font-mono">({messages.length})</span>
          </button>

          <button
            onClick={() => setFilter('important')}
            className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-medium transition-all ${
              filter === 'important'
                ? 'bg-emerald-600 text-white shadow-sm'
                : 'bg-emerald-50 hover:bg-emerald-100 text-emerald-800 dark:bg-emerald-950/40 dark:text-emerald-300 border border-emerald-200/60 dark:border-emerald-900/60'
            }`}
          >
            <Sparkles className="w-3 h-3" />
            <span>Important Only</span>
            <span className="text-[10px] opacity-75 font-mono">({importantCount})</span>
          </button>

          <button
            onClick={() => setFilter('spam')}
            className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-medium transition-all ${
              filter === 'spam'
                ? 'bg-amber-600 text-white shadow-sm'
                : 'bg-amber-50 hover:bg-amber-100 text-amber-800 dark:bg-amber-950/40 dark:text-amber-300 border border-amber-200/60 dark:border-amber-900/60'
            }`}
          >
            <ShieldAlert className="w-3 h-3" />
            <span>Spam / Chatter</span>
            <span className="text-[10px] opacity-75 font-mono">({spamCount})</span>
          </button>

          <button
            onClick={() => setFilter('normal')}
            className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-medium transition-all ${
              filter === 'normal'
                ? 'bg-slate-700 text-white shadow-sm'
                : 'bg-slate-100 hover:bg-slate-200 text-slate-700 dark:bg-slate-800 dark:text-slate-300'
            }`}
          >
            <span>Normal Context</span>
            <span className="text-[10px] opacity-75 font-mono">({normalCount})</span>
          </button>
        </div>
      </div>

      {/* Messages Scrollable Body */}
      <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-4 bg-[#F8F6F2] dark:bg-[#181716] font-sans">
        {filteredMessages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center p-8 text-gray-500 dark:text-gray-400 space-y-2">
            <Filter className="w-8 h-8 opacity-40 text-[#4A6B53]" />
            <p className="text-sm font-medium">No messages matched the selected filter.</p>
            <button
              onClick={() => {
                setFilter('all');
                setSearchQuery('');
              }}
              className="text-xs text-[#4A6B53] dark:text-[#A8D1B2] underline font-semibold"
            >
              Reset filters
            </button>
          </div>
        ) : (
          filteredMessages.map((m) => {
            const isHighlighted = highlightedLine === m.line_number;
            const isImportant = m.classification === 'important';
            const isSpam = m.classification === 'spam';
            const avatar = getAvatarColor(m.sender);

            // System messages (e.g. encryption notice, group creation)
            if (m.is_system) {
              return (
                <div
                  key={m.message_id}
                  ref={(el) => {
                    messageRefs.current[m.line_number] = el;
                  }}
                  className="flex justify-center my-3"
                >
                  <div className="inline-flex items-center gap-1.5 px-4 py-1.5 rounded-full bg-[#EAE5DC]/80 dark:bg-[#2C2926] text-[#716C64] dark:text-[#A8A29A] text-[11px] font-medium shadow-xs border border-[#DFD8CE] dark:border-[#383430] max-w-lg text-center">
                    <span>🛡️</span>
                    <span>{m.text}</span>
                    <span className="opacity-60 text-[10px]">#L{m.line_number}</span>
                  </div>
                </div>
              );
            }

            return (
              <div
                key={m.message_id}
                ref={(el) => {
                  messageRefs.current[m.line_number] = el;
                }}
                className={`group flex items-start gap-3 transition-all rounded-2xl p-2.5 ${
                  isHighlighted
                    ? 'ring-2 ring-emerald-500 bg-emerald-50/60 dark:bg-emerald-950/30'
                    : 'hover:bg-black/[0.02] dark:hover:bg-white/[0.02]'
                }`}
              >
                {/* Sender Avatar */}
                <div
                  className={`w-9 h-9 rounded-full shrink-0 flex items-center justify-center font-bold text-xs shadow-xs ${avatar.bg} ${avatar.text}`}
                  title={m.sender}
                >
                  {getInitials(m.sender)}
                </div>

                {/* Message Bubble Container */}
                <div className="flex-1 max-w-2xl">
                  {/* Bubble Header */}
                  <div className="flex items-center justify-between gap-2 mb-1">
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-bold text-[#1E1D1B] dark:text-[#EAE5DC]">
                        {m.sender}
                      </span>
                      <span className="text-[10px] text-gray-400 dark:text-gray-500">
                        {m.timestamp}
                      </span>
                    </div>

                    <div className="flex items-center gap-1.5">
                      {/* Classification Badge */}
                      {isImportant && (
                        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[10px] font-semibold bg-emerald-100 text-emerald-800 dark:bg-emerald-900/60 dark:text-emerald-200 border border-emerald-300 dark:border-emerald-800">
                          <Sparkles className="w-2.5 h-2.5" />
                          Important
                        </span>
                      )}
                      {isSpam && (
                        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[10px] font-semibold bg-amber-100 text-amber-800 dark:bg-amber-950/60 dark:text-amber-200 border border-amber-300 dark:border-amber-800">
                          <ShieldAlert className="w-2.5 h-2.5" />
                          Spam / Noise
                        </span>
                      )}

                      {/* Line Number Pill */}
                      <span className="inline-flex items-center text-[10px] font-mono text-gray-400 dark:text-gray-500">
                        <Hash className="w-2.5 h-2.5" />
                        {m.line_number}
                      </span>

                      {/* Quick Copy Button */}
                      <button
                        onClick={() => handleCopyMessage(m)}
                        className="opacity-0 group-hover:opacity-100 p-1 rounded hover:bg-gray-200 dark:hover:bg-gray-700 text-gray-500 transition-opacity"
                        title="Copy message line"
                        aria-label={`Copy message from ${m.sender}`}
                      >
                        {copiedId === m.message_id ? (
                          <Check className="w-3 h-3 text-emerald-600" />
                        ) : (
                          <Copy className="w-3 h-3" />
                        )}
                      </button>
                    </div>
                  </div>

                  {/* Message Bubble Body */}
                  <div
                    className={`rounded-2xl rounded-tl-sm p-3.5 text-xs sm:text-sm leading-relaxed shadow-xs transition-colors ${
                      isImportant
                        ? 'bg-white dark:bg-[#252825] border-2 border-emerald-500/40 dark:border-emerald-600/40 text-[#1E1D1B] dark:text-[#E6E2DC]'
                        : isSpam
                        ? 'bg-[#EFECE6]/70 dark:bg-[#22201E]/60 border border-[#E3DED5] dark:border-[#383430] text-gray-600 dark:text-gray-400'
                        : 'bg-white dark:bg-[#252220] border border-[#EBE5DC] dark:border-[#36322E] text-[#2D2A26] dark:text-[#E6E2DC]'
                    }`}
                  >
                    <p className="whitespace-pre-wrap break-words">{m.text}</p>

                    {/* Classification Reason Tag */}
                    {m.classification_reason && (
                      <div className="mt-2 pt-2 border-t border-black/5 dark:border-white/5 flex items-center justify-between text-[11px]">
                        <span
                          className={`font-medium ${
                            isImportant
                              ? 'text-emerald-700 dark:text-emerald-400'
                              : isSpam
                              ? 'text-amber-700 dark:text-amber-400'
                              : 'text-gray-500 dark:text-gray-400'
                          }`}
                        >
                          ✦ {m.classification_reason}
                        </span>

                        {onSelectCitation && isImportant && (
                          <button
                            onClick={() =>
                              onSelectCitation({
                                message_id: m.message_id,
                                line_number: m.line_number,
                                sender: m.sender,
                                timestamp: m.timestamp,
                                raw_text: m.text,
                              })
                            }
                            className="text-[10px] text-[#4A6B53] dark:text-[#A8D1B2] hover:underline font-semibold"
                          >
                            Inspect citation →
                          </button>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            );
          })
        )}
      </div>

      {/* Footer Status Bar */}
      <div className="px-4 py-2.5 border-t border-[#EBE5DC] dark:border-[#34302C] bg-[#FAF8F5] dark:bg-[#1E1C1A] flex items-center justify-between text-[11px] text-[#6B665F] dark:text-[#A09A90]">
        <span>
          Showing {filteredMessages.length} of {messages.length} messages
        </span>
        <div className="flex items-center gap-3">
          <span className="inline-flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-emerald-500"></span> Important ({importantCount})
          </span>
          <span className="inline-flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-amber-500"></span> Spam / Chatter ({spamCount})
          </span>
        </div>
      </div>
    </div>
  );
};
