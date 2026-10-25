import React, { useRef, useState } from 'react';
import { UploadCloud, FileText, Zap } from 'lucide-react';
import type { SyntheticSample } from '../api';

interface DropzoneProps {
  onFileSelect: (file: File) => void;
  onSampleSelect: (sampleId: string) => void;
  samples: SyntheticSample[];
  disabled: boolean;
}

export const Dropzone: React.FC<DropzoneProps> = ({
  onFileSelect,
  onSampleSelect,
  samples,
  disabled,
}) => {
  const [isDragOver, setIsDragOver] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (disabled) return;
    if (e.type === 'dragover') setIsDragOver(true);
    else if (e.type === 'dragleave') setIsDragOver(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(false);
    if (disabled) return;

    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const file = e.dataTransfer.files[0];
      const ext = file.name.split('.').pop()?.toLowerCase();
      if (ext === 'txt' || ext === 'zip') {
        onFileSelect(file);
      } else {
        alert('Please drop a WhatsApp export (.txt or .zip)');
      }
    }
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      onFileSelect(e.target.files[0]);
    }
  };

  return (
    <div className="bg-white dark:bg-[#22201E] border border-[#EBE5DC] dark:border-[#34302C] rounded-2xl p-6 shadow-sm space-y-4">
      <div
        onDragOver={handleDrag}
        onDragLeave={handleDrag}
        onDrop={handleDrop}
        onClick={() => !disabled && fileInputRef.current?.click()}
        className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all ${
          isDragOver
            ? 'border-[#4A6B53] bg-[#EBF2ED]/50 dark:bg-[#222B24]/40 scale-[1.008]'
            : 'border-[#EBE5DC] dark:border-[#34302C] hover:border-[#4A6B53]/60 hover:bg-[#FAF5ED]/40 dark:hover:bg-[#2A2724]/30'
        } ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
        role="button"
        tabIndex={0}
        aria-label="Upload WhatsApp chat export file (.txt or .zip)"
        onKeyDown={(e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            fileInputRef.current?.click();
          }
        }}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".txt,.zip"
          onChange={handleFileInput}
          className="hidden"
          disabled={disabled}
        />
        <div className="flex flex-col items-center gap-2">
          <div className="p-3 bg-[#FAF5ED] dark:bg-[#2C2620] text-[#4A6B53] rounded-2xl">
            <UploadCloud className="w-8 h-8" />
          </div>
          <p className="text-base font-semibold text-[#1E1D1B] dark:text-[#E6E2DC]">
            Drop your exported WhatsApp chat here
          </p>
          <p className="text-xs text-[#6B665F] dark:text-[#A09A90] max-w-sm">
            Supports exported <strong>.txt</strong> or <strong>.zip</strong> archives. Everything is processed 100% locally on your machine.
          </p>
          <button
            type="button"
            className="mt-2 px-4 py-2 rounded-xl text-xs font-semibold text-white bg-[#4A6B53] hover:bg-[#3D5944] transition-colors focus:ring-2 focus:ring-[#4A6B53]"
            disabled={disabled}
          >
            Browse Chat File
          </button>
        </div>
      </div>

      {samples.length > 0 && (
        <div className="pt-2 border-t border-[#EBE5DC] dark:border-[#34302C] flex flex-wrap items-center justify-between gap-2">
          <span className="text-xs text-gray-500 font-medium flex items-center gap-1.5">
            <Zap className="w-3.5 h-3.5 text-[#9C6528]" />
            Or try pre-bundled synthetic sample:
          </span>
          <div className="flex flex-wrap gap-2">
            {samples.map((s) => (
              <button
                key={s.id}
                onClick={() => onSampleSelect(s.id)}
                disabled={disabled}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium text-[#304736] bg-[#EBF2ED] hover:bg-[#E1ECE3] dark:bg-[#222B24] dark:text-[#A8D1B2] transition-colors disabled:opacity-50"
                aria-label={`Test with sample: ${s.filename}`}
              >
                <FileText className="w-3 h-3" />
                <span>{s.filename.replace('.txt', '').replace('sample_', '')}</span>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
