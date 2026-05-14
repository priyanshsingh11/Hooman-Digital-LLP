"use client";

import { useState } from "react";
import { Send, Mail, Type, Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";

interface EmailInputFormProps {
  onAnalyze: (subject: string, body: string) => void;
  isLoading: boolean;
}

export default function EmailInputForm({ onAnalyze, isLoading }: EmailInputFormProps) {
  const [subject, setSubject] = useState("");
  const [body, setBody] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (subject.trim() && body.trim()) {
      onAnalyze(subject, body);
    }
  };

  return (
    <div className="bg-white/5 border border-white/10 p-6 rounded-3xl backdrop-blur-sm shadow-xl">
      <div className="flex items-center gap-3 mb-6">
        <div className="w-10 h-10 bg-blue-600/20 rounded-xl flex items-center justify-center text-blue-400">
          <Mail size={20} />
        </div>
        <div>
          <h2 className="font-semibold">Email Simulator</h2>
          <p className="text-xs text-white/40">Test the orchestration logic</p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="space-y-1.5">
          <label className="text-[10px] font-bold uppercase tracking-wider text-white/30 ml-1">Subject</label>
          <div className="relative group">
            <Type className="absolute left-3 top-1/2 -translate-y-1/2 text-white/20 group-focus-within:text-blue-500 transition-colors" size={16} />
            <input
              type="text"
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
              placeholder="Refund request..."
              className="w-full bg-black/40 border border-white/5 rounded-xl py-3 pl-10 pr-4 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:bg-black/60 transition-all placeholder:text-white/20"
            />
          </div>
        </div>

        <div className="space-y-1.5">
          <label className="text-[10px] font-bold uppercase tracking-wider text-white/30 ml-1">Message Body</label>
          <textarea
            value={body}
            onChange={(e) => setBody(e.target.value)}
            placeholder="Hi, I was charged twice..."
            rows={8}
            className="w-full bg-black/40 border border-white/5 rounded-2xl p-4 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:bg-black/60 transition-all placeholder:text-white/20 resize-none custom-scrollbar"
          />
        </div>

        <button
          type="submit"
          disabled={isLoading || !subject.trim() || !body.trim()}
          className={cn(
            "w-full py-3 rounded-xl font-bold text-sm flex items-center justify-center gap-2 transition-all duration-300 shadow-lg",
            isLoading 
              ? "bg-blue-600/50 cursor-not-allowed" 
              : "bg-blue-600 hover:bg-blue-500 active:scale-[0.98] shadow-blue-600/20"
          )}
        >
          {isLoading ? (
            <Loader2 className="w-5 h-5 animate-spin" />
          ) : (
            <>
              Analyze Email
              <Send size={16} className="transition-transform group-hover:translate-x-1" />
            </>
          )}
        </button>
      </form>
    </div>
  );
}
