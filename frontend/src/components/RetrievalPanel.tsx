"use client";

import { FileText, ExternalLink, Database } from "lucide-react";
import { RetrievedDoc } from "@/types";

interface RetrievalPanelProps {
  docs: RetrievedDoc[];
  confidence?: number;
}

export default function RetrievalPanel({ docs, confidence }: RetrievalPanelProps) {
  return (
    <div className="bg-white/5 border border-white/10 rounded-3xl p-6 shadow-2xl">
      <div className="flex items-center justify-between mb-8">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-purple-600/20 rounded-xl flex items-center justify-center text-purple-400">
            <Database size={20} />
          </div>
          <div>
            <h2 className="font-semibold text-lg">Semantic Retrieval (RAG)</h2>
            <p className="text-xs text-white/40">Grounded documentation sources</p>
          </div>
        </div>
      </div>

      {docs.length === 0 ? (
        <div className="py-12 text-center border-2 border-dashed border-white/5 rounded-2xl text-white/20 italic text-sm">
          No relevant documents retrieved for this query.
        </div>
      ) : (
        <div className="grid grid-cols-2 gap-6">
          {docs.map((doc, idx) => (
            <div 
              key={idx} 
              className="group bg-white/[0.03] border border-white/10 p-5 rounded-2xl hover:border-purple-500/40 hover:bg-white/[0.05] transition-all relative overflow-hidden flex flex-col h-full shadow-lg"
            >
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 bg-purple-500/10 rounded-lg flex items-center justify-center">
                    <FileText className="text-purple-400" size={16} />
                  </div>
                  <span className="text-sm font-bold text-white/90 truncate max-w-[140px]">{doc.filename}</span>
                </div>
              </div>
              
              <p className="text-[13px] text-white/60 leading-relaxed line-clamp-4 mb-6 flex-1">
                {doc.content}
              </p>

              <div className="flex items-center justify-between mt-auto pt-4 border-t border-white/5">
                <span className="text-[10px] text-white/30 uppercase tracking-widest font-bold">Ref: {doc.source}</span>
                <button className="w-7 h-7 rounded-lg bg-white/5 flex items-center justify-center text-purple-400 hover:bg-purple-500/20 transition-colors">
                  <ExternalLink size={14} />
                </button>
              </div>
              
              <div className="absolute inset-0 bg-gradient-to-br from-purple-600/5 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none" />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
