"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { 
  LayoutDashboard, 
  Mail, 
  BarChart3, 
  Settings, 
  Search, 
  Bell,
  User,
  Zap,
  Activity
} from "lucide-react";
import { cn } from "@/lib/utils";
import EmailInputForm from "@/components/EmailInputForm";
import ClassificationCard from "@/components/ClassificationCard";
import RetrievalPanel from "@/components/RetrievalPanel";
import ResponseViewer from "@/components/ResponseViewer";
import MetricsDashboard from "@/components/MetricsDashboard";
import ActivityLogs from "@/components/ActivityLogs";
import WorkflowTimeline from "@/components/WorkflowTimeline";
import { WorkflowResult } from "@/types";

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState("overview");
  const [loading, setLoading] = useState(false);
  const [loadingStep, setLoadingStep] = useState<string>("");
  const [result, setResult] = useState<WorkflowResult | null>(null);
  const [logs, setLogs] = useState<any[]>([]);
  const [stats, setStats] = useState<any>(null);

  // Correct way to fetch on mount
  useEffect(() => {
    fetch("http://localhost:8000/api/stats")
      .then(res => res.json())
      .then(data => setStats(data))
      .catch(err => console.error("Failed to fetch stats", err));
  }, []);

  const handleAnalyze = async (subject: string, body: string) => {
    setLoading(true);
    setResult(null);
    setLoadingStep("Analyzing Intent...");
    
    try {
      // Step-by-step loading simulation for better UX (actual steps happen in parallel/sequence on backend)
      const loadingSequence = [
        { label: "Analyzing Intent...", delay: 0 },
        { label: "Retrieving Knowledge...", delay: 800 },
        { label: "Generating Grounded Response...", delay: 2000 },
      ];

      loadingSequence.forEach(step => {
        setTimeout(() => { if (loading) setLoadingStep(step.label); }, step.delay);
      });

      const response = await fetch("http://localhost:8000/api/process-email", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ subject, body }),
      });

      if (!response.ok) throw new Error("Failed to connect to AI Backend");

      const data = await response.json();
      setResult(data);
      setLogs(prev => [
        { 
          id: Date.now(), 
          type: "success", 
          message: `Orchestration Success (${data.latency?.total}s)`, 
          time: new Date().toISOString() 
        },
        ...prev
      ]);
    } catch (error: any) {
      console.error(error);
      setLogs(prev => [
        { id: Date.now(), type: "error", message: `Error: ${error.message}`, time: new Date().toISOString() },
        ...prev
      ]);
    } finally {
      setLoading(false);
      setLoadingStep("");
    }
  };

  return (
    <div className="flex h-screen bg-[#09090b] text-white font-sans selection:bg-blue-500/30">
      {/* Sidebar */}
      <aside className="w-64 border-r border-white/5 bg-[#09090b] flex flex-col">
        <div className="p-6 flex items-center gap-3">
          <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
            <Zap className="w-5 h-5 text-white fill-current" />
          </div>
          <span className="font-bold text-xl tracking-tight">Lumen AI</span>
        </div>

        <nav className="flex-1 px-4 space-y-2 mt-4">
          <SidebarItem 
            icon={<LayoutDashboard size={20} />} 
            label="Overview" 
            active={activeTab === "overview"} 
            onClick={() => setActiveTab("overview")} 
          />
          <SidebarItem 
            icon={<Mail size={20} />} 
            label="Simulator" 
            active={activeTab === "simulator"} 
            onClick={() => setActiveTab("simulator")} 
          />
          <SidebarItem 
            icon={<BarChart3 size={20} />} 
            label="Metrics" 
            active={activeTab === "metrics"} 
            onClick={() => setActiveTab("metrics")} 
          />
          <SidebarItem 
            icon={<Activity size={20} />} 
            label="Activity" 
            active={activeTab === "activity"} 
            onClick={() => setActiveTab("activity")} 
          />
        </nav>

        <div className="p-4 border-t border-white/5">
          <SidebarItem icon={<Settings size={20} />} label="Settings" />
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col overflow-hidden bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-blue-900/10 via-transparent to-transparent">
        {/* Header */}
        <header className="h-16 border-b border-white/5 flex items-center justify-between px-8 bg-black/20 backdrop-blur-md">
          <h1 className="text-lg font-medium text-white/80 capitalize">{activeTab}</h1>
          <div className="flex items-center gap-6">
            <div className="relative group">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-white/40 group-focus-within:text-blue-400 transition-colors" size={18} />
              <input 
                type="text" 
                placeholder="Search..." 
                className="bg-white/5 border border-white/10 rounded-full py-1.5 pl-10 pr-4 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500/50 w-64 transition-all"
              />
            </div>
            <button className="text-white/60 hover:text-white transition-colors relative">
              <Bell size={20} />
              <span className="absolute top-0 right-0 w-2 h-2 bg-blue-500 rounded-full border border-[#09090b]"></span>
            </button>
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-xs font-bold ring-2 ring-white/10">
              PS
            </div>
          </div>
        </header>

        {/* Content Area */}
        <div className="flex-1 overflow-y-auto p-8 custom-scrollbar">
          <AnimatePresence mode="wait">
            {activeTab === "overview" && (
              <motion.div 
                key="overview"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="space-y-8"
              >
                <div className="grid grid-cols-4 gap-6">
                  <StatCard label="Total Tickets" value={stats?.total_tickets ?? "..."} change="+12%" />
                  <StatCard label="Avg. Latency" value={stats?.avg_latency || "..."} change="-5%" />
                  <StatCard label="Accuracy" value={stats?.accuracy || "..."} change="+2.1%" />
                  <StatCard label="Automation" value={stats?.automation_rate || "..."} change="+15%" />
                </div>
                <MetricsDashboard stats={stats} />
              </motion.div>
            )}

            {activeTab === "simulator" && (
              <motion.div 
                key="simulator"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                className="grid grid-cols-12 gap-8"
              >
                <div className="col-span-4 space-y-6">
                  <EmailInputForm onAnalyze={handleAnalyze} isLoading={loading} />
                  <WorkflowTimeline loading={loading} loadingStep={loadingStep} result={result} />
                  <ActivityLogs logs={logs} />
                </div>
                
                <div className="col-span-8 space-y-6">
                  {!result && !loading && (
                    <div className="h-full flex flex-col items-center justify-center border-2 border-dashed border-white/5 rounded-3xl p-12 text-center">
                      <div className="w-16 h-16 bg-white/5 rounded-2xl flex items-center justify-center mb-4 text-white/20">
                        <Mail size={32} />
                      </div>
                      <h3 className="text-xl font-medium text-white/60">No Analysis Yet</h3>
                      <p className="text-white/40 mt-2 max-w-sm">
                        Enter an email on the left to start the AI support orchestration workflow.
                      </p>
                    </div>
                  )}

                  {loading && (
                    <div className="space-y-8 py-12 flex flex-col items-center justify-center">
                      <div className="relative">
                        <div className="w-24 h-24 border-4 border-blue-500/20 border-t-blue-500 rounded-full animate-spin" />
                        <div className="absolute inset-0 flex items-center justify-center">
                          <Zap className="text-blue-500 animate-pulse" size={32} />
                        </div>
                      </div>
                      <div className="text-center space-y-2">
                        <h3 className="text-xl font-bold text-white/90 animate-pulse-soft">{loadingStep}</h3>
                        <p className="text-sm text-white/30 max-w-xs mx-auto">
                          Orchestrating Llama 3.1 and ChromaDB to process your request...
                        </p>
                      </div>
                    </div>
                  )}

                  {result && !loading && (
                    <div className="space-y-6 pb-12">
                      <ClassificationCard classification={result.classification} action={result.action} />
                      <RetrievalPanel docs={result.retrieved_docs} confidence={result.retrieval_confidence} />
                      <ResponseViewer response={result.generated_response} summary={result.workflow_summary} />
                    </div>
                  )}
                </div>
              </motion.div>
            )}

            {activeTab === "metrics" && (
               <motion.div key="metrics" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                 <MetricsDashboard stats={stats} />
               </motion.div>
            )}

            {activeTab === "activity" && (
               <motion.div key="activity" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
                 <ActivityLogs logs={logs} fullWidth />
               </motion.div>
            )}
          </AnimatePresence>
        </div>
      </main>
    </div>
  );
}

function SidebarItem({ icon, label, active = false, onClick }: any) {
  return (
    <button 
      onClick={onClick}
      className={cn(
        "w-full flex items-center gap-3 px-4 py-2.5 rounded-xl text-sm font-medium transition-all duration-200",
        active 
          ? "bg-blue-600/10 text-blue-400 ring-1 ring-blue-500/20 shadow-[0_0_20px_-5px_rgba(59,130,246,0.3)]" 
          : "text-white/50 hover:text-white hover:bg-white/5"
      )}
    >
      <span className={cn("transition-transform duration-200", active && "scale-110")}>{icon}</span>
      {label}
    </button>
  );
}

function StatCard({ label, value, change }: any) {
  const isPositive = change.startsWith("+");
  return (
    <div className="bg-white/5 border border-white/10 p-6 rounded-3xl hover:bg-white/[0.07] transition-all group overflow-hidden relative">
      <div className="absolute -right-4 -top-4 w-24 h-24 bg-blue-600/5 rounded-full blur-2xl group-hover:bg-blue-600/10 transition-colors" />
      <p className="text-sm font-medium text-white/40 mb-1">{label}</p>
      <div className="flex items-baseline gap-3">
        <h3 className="text-2xl font-bold">{value}</h3>
        <span className={cn("text-xs font-medium", isPositive ? "text-emerald-400" : "text-rose-400")}>
          {change}
        </span>
      </div>
    </div>
  );
}
