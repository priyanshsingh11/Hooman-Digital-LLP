"use client";

import { useState, useEffect } from "react";
import { Sparkles, Copy, Check, MessageSquare, Info, Edit3, Send, CheckCircle } from "lucide-react";
import { cn } from "@/lib/utils";

interface ResponseViewerProps {
  response: string;
  summary: string;
  ticketId?: string;
  onApprove?: (id: string, finalizedResponse: string) => void;
}

export default function ResponseViewer({ response: initialResponse, summary, ticketId, onApprove }: ResponseViewerProps) {
  const [copied, setCopied] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [editedResponse, setEditedResponse] = useState(initialResponse);
  const [isApproved, setIsApproved] = useState(false);

  useEffect(() => {
    setEditedResponse(initialResponse);
    setIsApproved(false);
    setIsEditing(false);
  }, [initialResponse]);

  const handleCopy = () => {
    navigator.clipboard.writeText(editedResponse);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleApprove = async () => {
    if (ticketId && onApprove) {
      await onApprove(ticketId, editedResponse);
      setIsApproved(true);
      setIsEditing(false);
    }
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

        <div className="flex items-center gap-3">
          <button
            onClick={() => setIsEditing(!isEditing)}
            disabled={isApproved}
            className={cn(
              "flex items-center gap-2 px-4 py-2 rounded-xl border text-sm font-medium transition-all active:scale-95",
              isEditing ? "bg-blue-600/20 border-blue-500/40 text-blue-400" : "bg-white/5 border-white/10 text-white/60 hover:bg-white/10"
            )}
          >
            <Edit3 size={16} />
            {isEditing ? "Cancel Edit" : "Edit Draft"}
          </button>
          
          <button
            onClick={handleCopy}
            className="flex items-center gap-2 px-4 py-2 bg-white/5 hover:bg-white/10 rounded-xl border border-white/10 text-sm font-medium transition-all active:scale-95"
          >
            {copied ? <Check size={16} className="text-emerald-400" /> : <Copy size={16} />}
            {copied ? "Copied" : "Copy"}
          </button>
        </div>
      </div>

      <div className="bg-black/40 border border-white/5 rounded-2xl p-6 relative group">
        <div className={cn(
          "absolute -top-3 left-6 px-3 py-1 rounded-lg text-[10px] font-bold uppercase tracking-widest shadow-lg transition-all",
          isApproved ? "bg-emerald-600 shadow-emerald-600/20" : "bg-blue-600 shadow-blue-600/20"
        )}>
          {isApproved ? "Approved & Finalized" : isEditing ? "Editing Mode" : "Draft Response"}
        </div>
        
        {isEditing ? (
          <textarea 
            value={editedResponse}
            onChange={(e) => setEditedResponse(e.target.value)}
            className="w-full bg-transparent text-white/90 leading-relaxed font-medium min-h-[200px] focus:outline-none resize-none"
            spellCheck={false}
          />
        ) : (
          <p className={cn(
            "text-white/90 leading-relaxed font-medium whitespace-pre-wrap transition-opacity",
            isApproved && "opacity-50"
          )}>
            {editedResponse || "No response generated."}
          </p>
        )}
      </div>

      {!isApproved && (
        <div className="mt-6">
          <button
            onClick={handleApprove}
            className="w-full py-4 bg-emerald-600 hover:bg-emerald-500 text-white font-bold rounded-2xl transition-all shadow-lg shadow-emerald-600/20 flex items-center justify-center gap-2 group"
          >
            <CheckCircle size={20} className="group-hover:scale-110 transition-transform" />
            Approve & Send Final Response
          </button>
        </div>
      )}

      <div className="mt-8 flex items-start gap-4 p-4 bg-blue-600/5 border border-blue-500/20 rounded-2xl">
        <div className="text-blue-400 mt-1">
          <Info size={18} />
        </div>
        <div>
          <h4 className="text-xs font-bold text-blue-400 uppercase tracking-widest mb-1">Workflow Summary</h4>
          <p className="text-sm text-white/60 leading-relaxed">
            {summary || "Calculating workflow impact..."}
          </p>
        </div>
      </div>
    </div>
  );
}
