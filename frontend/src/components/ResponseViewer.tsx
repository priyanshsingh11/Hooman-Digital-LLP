"use client";

import { useState } from "react";
import { Sparkles, Copy, Check, MessageSquare, Info } from "lucide-react";
import { cn } from "@/lib/utils";

interface ResponseViewerProps {
  response: string;
  summary: string;
}

export default function ResponseViewer({ response, summary }: ResponseViewerProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(response);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="bg-white/5 border border-white/10 rounded-3xl p-8 shadow-2xl relative overflow-hidden">
      <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600" />
      
      <div className="flex items-center justify-between mb-8">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-emerald-600/20 rounded-xl flex items-center justify-center text-emerald-400">
            <Sparkles size={20} />
          </div>
          <div>
            <h2 className="font-semibold text-lg">AI Generated Response</h2>
            <p className="text-xs text-white/40">Professional & grounded support reply</p>
          </div>
        </div>

        <button
          onClick={handleCopy}
          className="flex items-center gap-2 px-4 py-2 bg-white/5 hover:bg-white/10 rounded-xl border border-white/10 text-sm font-medium transition-all active:scale-95"
        >
          {copied ? <Check size={16} className="text-emerald-400" /> : <Copy size={16} />}
          {copied ? "Copied" : "Copy Response"}
        </button>
      </div>

      <div className="bg-black/40 border border-white/5 rounded-2xl p-6 relative">
        <div className="absolute -top-3 left-6 px-3 py-1 bg-blue-600 rounded-lg text-[10px] font-bold uppercase tracking-widest shadow-lg shadow-blue-600/20">
          Draft Response
        </div>
        <p className="text-white/90 leading-relaxed font-medium whitespace-pre-wrap">
          {response}
        </p>
      </div>

      <div className="mt-8 flex items-start gap-4 p-4 bg-blue-600/5 border border-blue-500/20 rounded-2xl">
        <div className="text-blue-400 mt-1">
          <Info size={18} />
        </div>
        <div>
          <h4 className="text-xs font-bold text-blue-400 uppercase tracking-widest mb-1">Workflow Summary</h4>
          <p className="text-sm text-white/60 leading-relaxed">
            {summary}
          </p>
        </div>
      </div>
    </div>
  );
}
