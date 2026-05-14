"use client";

import { useEffect, useState } from "react";
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from "recharts";
import { Activity, Target, Zap } from "lucide-react";

export default function MetricsDashboard({ stats }: { stats: any }) {
  const [chartData, setChartData] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/api/chart-data")
      .then(res => res.json())
      .then(data => setChartData(data))
      .catch(err => console.error("Failed to fetch chart data", err));
  }, []);

  if (chartData.length === 0) return null;

  return (
    <div className="bg-white/5 border border-white/10 rounded-3xl p-8 shadow-2xl">
      <div className="flex items-center justify-between mb-10">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-blue-600/20 rounded-xl flex items-center justify-center text-blue-400">
            <Activity size={20} />
          </div>
          <div>
            <h2 className="text-xl font-bold">System Performance</h2>
            <p className="text-sm text-white/40">Accuracy and retrieval trends over time</p>
          </div>
        </div>
        
        <div className="flex gap-4">
          <LegendItem color="#3b82f6" label="Accuracy" />
          <LegendItem color="#a855f7" label="Retrieval Hit Rate" />
        </div>
      </div>

      <div className="h-[350px] w-full">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData}>
            <defs>
              <linearGradient id="colorAcc" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
              </linearGradient>
              <linearGradient id="colorHit" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#a855f7" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#a855f7" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
            <XAxis 
              dataKey="name" 
              axisLine={false} 
              tickLine={false} 
              tick={{fill: 'rgba(255,255,255,0.4)', fontSize: 12}}
              dy={10}
            />
            <YAxis 
              hide 
              domain={[80, 100]}
            />
            <Tooltip 
              contentStyle={{ 
                backgroundColor: '#18181b', 
                border: '1px solid rgba(255,255,255,0.1)',
                borderRadius: '16px',
                boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.5)'
              }}
              itemStyle={{ fontSize: '12px', fontWeight: 'bold' }}
            />
            <Area 
              type="monotone" 
              dataKey="accuracy" 
              stroke="#3b82f6" 
              strokeWidth={3}
              fillOpacity={1} 
              fill="url(#colorAcc)" 
              animationDuration={2000}
            />
            <Area 
              type="monotone" 
              dataKey="hitRate" 
              stroke="#a855f7" 
              strokeWidth={3}
              fillOpacity={1} 
              fill="url(#colorHit)" 
              animationDuration={2000}
              animationDelay={500}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      <div className="grid grid-cols-3 gap-6 mt-10">
        <SmallMetric label="Peak Accuracy" value={stats?.accuracy || "91.2%"} icon={<Target size={14} />} />
        <SmallMetric label="Avg. Confidence" value={stats?.avg_confidence || "0%"} icon={<Zap size={14} />} />
        <SmallMetric label="Automation Rate" value={stats?.automation_rate || "0%"} icon={<Zap size={14} />} />
      </div>
    </div>
  );
}

function LegendItem({ color, label }: { color: string, label: string }) {
  return (
    <div className="flex items-center gap-2">
      <div className="w-3 h-3 rounded-full" style={{ backgroundColor: color }} />
      <span className="text-xs font-medium text-white/60">{label}</span>
    </div>
  );
}

function SmallMetric({ label, value, icon }: any) {
  return (
    <div className="bg-white/5 border border-white/5 p-4 rounded-2xl flex items-center justify-between hover:bg-white/10 transition-colors">
      <div>
        <p className="text-[10px] font-bold uppercase tracking-widest text-white/30 mb-1">{label}</p>
        <p className="text-lg font-bold">{value}</p>
      </div>
      <div className="w-8 h-8 bg-white/5 rounded-lg flex items-center justify-center text-white/40">
        {icon}
      </div>
    </div>
  );
}
