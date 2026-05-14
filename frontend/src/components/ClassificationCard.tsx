"use client";

import { AlertCircle, CheckCircle2, ShieldAlert, Tag, Zap, MessageSquare, Target } from "lucide-react";
import { Classification } from "@/types";
import { cn } from "@/lib/utils";

interface ClassificationCardProps {
  classification: Classification;
  action: string;
  systemConfidence?: number;
}

export default function ClassificationCard({ classification, action, systemConfidence }: ClassificationCardProps) {
  const getUrgencyColor = (urgency: string) => {
    switch (urgency.toLowerCase()) {
      case "high": return "text-rose-400 bg-rose-400/10 border-rose-400/20 shadow-rose-400/10";
      case "medium": return "text-amber-400 bg-amber-400/10 border-amber-400/20 shadow-amber-400/10";
      default: return "text-emerald-400 bg-emerald-400/10 border-emerald-400/20 shadow-emerald-400/10";
    }
  };

  const getActionIcon = (action: string) => {
    if (action.includes("human")) return <ShieldAlert size={18} />;
    if (action.includes("reply")) return <CheckCircle2 size={18} />;
    if (action.includes("billing")) return <Zap size={18} />;
    return <Tag size={18} />;
  };

  const formatLabel = (label: string) => {
    return label.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
  };

  return (
    <div className="bg-white/5 border border-white/10 rounded-3xl p-6 shadow-2xl relative overflow-hidden group">
      <div className="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity">
        <MessageSquare size={120} />
      </div>

      <div className="flex items-start justify-between mb-8 relative">
        <div className="flex items-center gap-4">
          <div>
            <h2 className="text-xl font-bold mb-1">AI Classification</h2>
            <p className="text-sm text-white/40">Real-time intent analysis</p>
          </div>
        </div>
        <div className={cn(
          "px-4 py-2 rounded-xl border text-sm font-bold flex items-center gap-2 shadow-lg backdrop-blur-md",
          getUrgencyColor(classification.urgency)
        )}>
          <AlertCircle size={16} />
          {classification.urgency.toUpperCase()} PRIORITY
        </div>
      </div>

      <div className="grid grid-cols-3 gap-6 relative">
        <Metric label="Category" value={formatLabel(classification.category)} icon={<Tag size={14} />} color="text-blue-400" />
        <Metric label="Sentiment" value={formatLabel(classification.sentiment)} icon={<MessageSquare size={14} />} color="text-purple-400" />
        <Metric label="Workflow Action" value={formatLabel(action)} icon={getActionIcon(action)} color="text-emerald-400" />
      </div>

      <div className="mt-8 pt-6 border-t border-white/5 relative">
        <h4 className="text-[10px] font-bold uppercase tracking-widest text-white/30 mb-3">Analysis Reasoning</h4>
        <p className="text-sm text-white/70 leading-relaxed italic">
          "{classification.reasoning}"
        </p>
      </div>
    </div>
  );
}

function Metric({ label, value, icon, color }: any) {
  return (
    <div className="space-y-2">
      <p className="text-[10px] font-bold uppercase tracking-widest text-white/30 ml-1">{label}</p>
      <div className="bg-white/5 rounded-2xl p-3 border border-white/5 flex items-center gap-3 hover:bg-white/10 transition-colors cursor-default">
        <div className={cn("w-7 h-7 rounded-lg flex items-center justify-center bg-white/5", color)}>
          {icon}
        </div>
        <span className="text-sm font-semibold">{value}</span>
      </div>
    </div>
  );
}
