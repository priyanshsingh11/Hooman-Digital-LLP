"use client";

import { Activity, Clock, Terminal, ChevronRight, Timer } from "lucide-react";
import { cn, formatDate } from "@/lib/utils";

interface ActivityLogsProps {
  logs: any[];
  fullWidth?: boolean;
}

export default function ActivityLogs({ logs, fullWidth }: ActivityLogsProps) {
  return (
    <div className={cn(
      "bg-white/5 border border-white/10 rounded-3xl p-6 shadow-2xl flex flex-col overflow-hidden",
      fullWidth ? "h-[600px]" : "h-[400px]"
    )}>
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-amber-600/20 rounded-xl flex items-center justify-center text-amber-400">
            <Activity size={20} />
          </div>
          <div>
            <h2 className="font-semibold text-lg">Activity Logs</h2>
            <p className="text-xs text-white/40">Execution timeline</p>
          </div>
        </div>
        <div className="w-8 h-8 rounded-lg bg-white/5 flex items-center justify-center text-white/40 hover:bg-white/10 transition-colors cursor-pointer">
          <Terminal size={16} />
        </div>
      </div>

      <div className="flex-1 overflow-y-auto space-y-3 custom-scrollbar pr-2">
        {logs.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center p-8 opacity-20">
            <Clock size={40} className="mb-4" />
            <p className="text-sm font-medium">Waiting for activity...</p>
          </div>
        ) : (
          logs.map((log) => (
            <div 
              key={log.id} 
              className="bg-black/40 border border-white/5 p-4 rounded-xl flex items-start gap-4 hover:border-white/10 transition-colors group cursor-default"
            >
              <div className={cn(
                "w-2 h-2 rounded-full mt-2 shrink-0",
                log.type === "success" ? "bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.5)]" : "bg-rose-500 shadow-[0_0_8px_rgba(244,63,94,0.5)]"
              )} />
              <div className="flex-1">
                <div className="flex items-center justify-between gap-4 mb-2">
                  <p className="text-[13px] font-semibold text-white/90 leading-tight">{log.message}</p>
                  <span className="text-[10px] text-white/20 font-bold whitespace-nowrap">{formatDate(log.time)}</span>
                </div>
                
                {log.latency && (
                  <div className="grid grid-cols-3 gap-2 mt-3 pt-3 border-t border-white/5">
                    <LatencyItem label="Class" time={log.latency.classification} />
                    <LatencyItem label="RAG" time={log.latency.retrieval} />
                    <LatencyItem label="Gen" time={log.latency.generation} />
                  </div>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

function LatencyItem({ label, time }: { label: string, time: number }) {
  return (
    <div className="flex flex-col gap-0.5">
      <span className="text-[9px] font-bold text-white/20 uppercase tracking-widest">{label}</span>
      <span className="text-xs font-mono text-amber-400/80">{time}s</span>
    </div>
  );
}
