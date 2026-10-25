import React, { useState, useEffect } from 'react';
import {
  FolderCheck,
  Upload,
  AlertCircle,
} from 'lucide-react';
import type {
  DigestResponse,
  SystemHealth,
  ProgressEvent,
  SourceCitation,
  SyntheticSample,
} from './api';
import {
  fetchHealth,
  fetchLatestDigest,
  uploadChat,
  fetchSyntheticSamples,
  digestSyntheticSample,
} from './api';

import { StatusChip } from './components/StatusChip';
import { NoiseCelebration } from './components/NoiseCelebration';
import { MorningDigest } from './components/MorningDigest';
import { ActionItemList } from './components/ActionItemList';
import { DatesTimeline } from './components/DatesTimeline';
import { SourceDrawer } from './components/SourceDrawer';
import { Dropzone } from './components/Dropzone';
import { StreamingProgress } from './components/StreamingProgress';
import { ModelSetupGuide } from './components/ModelSetupGuide';
import { TidierModal } from './components/TidierModal';

export const App: React.FC = () => {
  const [health, setHealth] = useState<SystemHealth | null>(null);
  const [digest, setDigest] = useState<DigestResponse | null>(null);
  const [samples, setSamples] = useState<SyntheticSample[]>([]);
  const [loading, setLoading] = useState(false);
  const [loadingChatName, setLoadingChatName] = useState<string>('Chat Export');
  const [progress, setProgress] = useState<ProgressEvent | null>(null);
  const [selectedCitation, setSelectedCitation] = useState<SourceCitation | null>(null);
  const [tidierOpen, setTidierOpen] = useState(false);
  const [showUploader, setShowUploader] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const loadInitialData = async () => {
    try {
      const h = await fetchHealth();
      setHealth(h);
    } catch {
      setHealth(null);
    }

    try {
      const d = await fetchLatestDigest();
      if (d) setDigest(d);
    } catch {
      // No previous digest yet
    }

    try {
      const s = await fetchSyntheticSamples();
      setSamples(s);
    } catch {
      setSamples([]);
    }
  };

  useEffect(() => {
    loadInitialData();
  }, []);

  const handleFileUpload = async (file: File) => {
    setLoading(true);
    setLoadingChatName(file.name);
    setErrorMessage(null);
    setProgress({
      task_id: 'init',
      status: 'parsing',
      current_chunk: 0,
      total_chunks: 0,
      percent: 10,
      elapsed_sec: 0.1,
      estimated_remaining_sec: 12.0,
      message: 'Parsing chat structure and slicing into temporal chunks...',
    });

    try {
      const result = await uploadChat(file, health?.active_model);
      setDigest(result);
      setShowUploader(false);
    } catch (err: any) {
      setErrorMessage(err.message || 'Failed to process chat.');
    } finally {
      setLoading(false);
      setProgress(null);
    }
  };

  const handleSampleSelect = async (sampleId: string) => {
    setLoading(true);
    setLoadingChatName(sampleId.replace('sample_', '').replace(/_/g, ' '));
    setErrorMessage(null);
    setProgress({
      task_id: 'init',
      status: 'parsing',
      current_chunk: 0,
      total_chunks: 0,
      percent: 15,
      elapsed_sec: 0.1,
      estimated_remaining_sec: 8.0,
      message: 'Digesting synthetic benchmark sample locally...',
    });

    try {
      const result = await digestSyntheticSample(sampleId);
      setDigest(result);
      setShowUploader(false);
    } catch (err: any) {
      setErrorMessage(err.message || 'Failed to process synthetic sample.');
    } finally {
      setLoading(false);
      setProgress(null);
    }
  };

  const isModelMissing = health && (!health.ollama_connected || health.status === 'model_missing');

  return (
    <div className="min-h-screen bg-[#FDFBF7] dark:bg-[#181716] text-[#2D2A26] dark:text-[#E6E2DC] flex flex-col selection:bg-[#EBF2ED] selection:text-[#304736]">
      {/* Header */}
      <header className="border-b border-[#EBE5DC] dark:border-[#34302C] bg-[#FFFFFF]/90 dark:bg-[#22201E]/90 backdrop-blur-md sticky top-0 z-40">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="text-2xl" role="img" aria-label="Sloth logo">
              🦥
            </span>
            <div>
              <h1 className="text-lg font-bold tracking-tight text-[#1E1D1B] dark:text-[#E6E2DC]">
                Sloth Digest
              </h1>
              <p className="hidden sm:block text-[11px] text-[#6B665F] dark:text-[#A09A90]">
                Slow & steady · rewards laziness
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={() => setTidierOpen(true)}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
              aria-label="Open chat folder tidier"
            >
              <FolderCheck className="w-3.5 h-3.5 text-[#9C6528]" />
              <span className="hidden md:inline">Inbox Tidier</span>
            </button>

            <StatusChip health={health} onRefresh={loadInitialData} />
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1 max-w-6xl w-full mx-auto px-4 sm:px-6 py-6 sm:py-8 space-y-6">
        {/* Model Missing / First Run Alert Banner */}
        {isModelMissing && (
          <ModelSetupGuide
            activeModel={health?.active_model || 'qwen2.5:1.5b'}
            onRetry={loadInitialData}
          />
        )}

        {/* Error Alert */}
        {errorMessage && (
          <div
            className="p-4 bg-red-50 dark:bg-red-950/40 border border-red-200 dark:border-red-900 rounded-2xl flex items-center justify-between gap-3 text-xs sm:text-sm text-red-800 dark:text-red-200"
            role="alert"
          >
            <div className="flex items-center gap-2">
              <AlertCircle className="w-5 h-5 text-red-600 shrink-0" />
              <span>{errorMessage}</span>
            </div>
            <button
              onClick={() => setErrorMessage(null)}
              className="px-3 py-1 rounded-lg bg-red-100 dark:bg-red-900 text-xs font-semibold hover:bg-red-200"
            >
              Dismiss
            </button>
          </div>
        )}

        {/* Loading / Inference State */}
        {loading && (
          <StreamingProgress progress={progress} chatName={loadingChatName} />
        )}

        {/* Digest View or Empty Welcome Screen */}
        {!loading && digest && (
          <div className="space-y-6 animate-in fade-in duration-200">
            {/* 1. Safe Noise Avoided Celebration */}
            <NoiseCelebration
              safeCount={digest.safe_to_ignore_count}
              totalMessages={digest.total_messages}
              chatName={digest.chat_name}
              durationSec={digest.processing_duration_sec}
            />

            {/* 2. Two-Line Executive Morning Digest */}
            <MorningDigest digest={digest} />

            {/* 3 & 4: Action Items (Who is waiting) + Dates & Deadlines */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-start">
              <ActionItemList
                items={digest.action_items}
                onSelectCitation={setSelectedCitation}
              />
              <DatesTimeline
                items={digest.deadlines}
                onSelectCitation={setSelectedCitation}
              />
            </div>

            {/* Secondary Action: Digest another chat */}
            <div className="pt-6 border-t border-[#EBE5DC] dark:border-[#34302C] flex items-center justify-between">
              <span className="text-xs text-gray-400">
                Processed via {digest.model_used} at {digest.created_at}
              </span>
              <button
                onClick={() => setShowUploader(!showUploader)}
                className="inline-flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-semibold text-[#304736] bg-[#EBF2ED] hover:bg-[#E1ECE3] dark:bg-[#222B24] dark:text-[#A8D1B2] transition-colors"
              >
                <Upload className="w-3.5 h-3.5" />
                {showUploader ? 'Hide Uploader' : 'Digest Another Chat'}
              </button>
            </div>

            {showUploader && (
              <Dropzone
                onFileSelect={handleFileUpload}
                onSampleSelect={handleSampleSelect}
                samples={samples}
                disabled={loading}
              />
            )}
          </div>
        )}

        {/* Empty State: First Visit */}
        {!loading && !digest && (
          <div className="space-y-6 max-w-2xl mx-auto py-8 text-center">
            <div className="space-y-3">
              <div className="w-16 h-16 mx-auto bg-[#FAF5ED] dark:bg-[#2C2620] text-[#9C6528] rounded-3xl flex items-center justify-center text-3xl shadow-inner">
                🦥
              </div>
              <h2 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-[#1E1D1B] dark:text-[#E6E2DC]">
                Sleep peacefully. Wake up informed.
              </h2>
              <p className="text-sm text-[#6B665F] dark:text-[#A09A90] max-w-lg mx-auto">
                Stop doom-scrolling busy group chats. Sloth Digest reads them overnight on your local machine, pulling out action items, deadlines, and a two-line morning summary.
              </p>
            </div>

            <Dropzone
              onFileSelect={handleFileUpload}
              onSampleSelect={handleSampleSelect}
              samples={samples}
              disabled={loading}
            />
          </div>
        )}
      </main>

      {/* Hallucination Guard Source Citation Modal/Drawer */}
      <SourceDrawer
        citation={selectedCitation}
        onClose={() => setSelectedCitation(null)}
      />

      {/* Stretch Goal: Tidier Modal */}
      <TidierModal
        isOpen={tidierOpen}
        onClose={() => setTidierOpen(false)}
      />

      {/* Footer */}
      <footer className="border-t border-[#EBE5DC] dark:border-[#34302C] py-6 text-center text-xs text-[#6B665F] dark:text-[#A09A90]">
        <div className="max-w-6xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
          <span>
            Sloth Digest · Built for Dev.to Hacktoberfest (Week 3: Slow & Steady)
          </span>
          <span className="font-mono text-[11px] text-gray-400">
            100% Localhost · Zero Cloud Telemetry
          </span>
        </div>
      </footer>
    </div>
  );
};

export default App;
