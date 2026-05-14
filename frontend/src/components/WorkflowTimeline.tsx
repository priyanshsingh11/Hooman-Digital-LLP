"use client";

import { CheckCircle2, Circle, Clock, Loader2, Search, Brain, Zap, Sparkles } from "lucide-react";
import { cn } from "@/lib/utils";

interface WorkflowTimelineProps {
  loading: boolean;
  loadingStep: string;
  result: any;
}

export default function WorkflowTimeline({ loading, loadingStep, result }: WorkflowTimelineProps) {
  const steps = [
    { id: "classify", label: "Analyze Intent", icon: <Brain size={16} />, status: getStatus("Analyzing Intent...", "Analyzing Intent...") },
    { id: "retrieve", label: "Retrieve Knowledge", icon: <Search size={16} />, status: getStatus("Retrieving Knowledge...", "Retrieving Knowledge...") },
    { id: "decide", label: "Select Action", icon: <Zap size={16} />, status: getStatus("Generating Grounded Response...", "Generating Grounded Response...") },
    { id: "generate", label: "Generate Reply", icon: <Sparkles size={16} />, status: result ? "complete" : "pending" },
  ];

  function getStatus(stepLabel: string, currentStep: string) {
    if (result) return "complete";
    if (!loading) return "pending";
    if (loadingStep === stepLabel) return "active";
    // If we are past this step in the mock sequence
    return "complete"; 
  }

  return (
    <div className="bg-white/5 border border-white/10 rounded-3xl p-6 shadow-xl">
      <h3 className="text-xs font-bold uppercase tracking-widest text-white/30 mb-6 flex items-center gap-2">
        <Clock size={14} />
        Live Execution Timeline
      </h3>

      <div className="space-y-4">
        {steps.map((step, idx) => (
          <div key={step.id} className="flex items-center gap-4 relative">
            {idx < steps.length - 1 && (
              <div className={cn(
                "absolute left-[11px] top-6 w-[1px] h-6 bg-white/10",
                step.status === "complete" && "bg-blue-500/40"
              )} />
            )}
            
            <div className={cn(
              "w-6 h-6 rounded-full flex items-center justify-center transition-all duration-500",
              step.status === "complete" ? "bg-emerald-500/20 text-emerald-400" :
              step.status === "active" ? "bg-blue-500/20 text-blue-400 animate-pulse" :
              "bg-white/5 text-white/20"
            )}>
              {step.status === "complete" ? <CheckCircle2 size={14} /> : 
               step.status === "active" ? <Loader2 size={14} className="animate-spin" /> : 
               <Circle size={8} className="fill-current" />}
            </div>

            <div className="flex-1 flex items-center justify-between">
              <span className={cn(
                "text-sm font-medium transition-colors",
                step.status === "complete" ? "text-white/80" :
                step.status === "active" ? "text-blue-400" : "text-white/20"
              )}>
                {step.label}
              </span>
              {step.status === "active" && (
                <span className="text-[10px] font-bold text-blue-400/60 animate-pulse">In Progress...</span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
