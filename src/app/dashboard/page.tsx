"use client";

import React from "react";
import { motion } from "framer-motion";
import { 
  MessageSquare, FileText, Landmark, Clock, Activity, 
  ArrowRight, ShieldCheck, Scale, Award, TrendingUp 
} from "lucide-react";
import Link from "next/link";

const stats = [
  { label: "Total Consultations", value: "14", icon: MessageSquare, gradient: "from-primary to-purple-800" },
  { label: "Documents Analyzed", value: "3", icon: FileText, gradient: "from-secondary to-blue-800" },
  { label: "Active Legal Categories", value: "8", icon: Scale, gradient: "from-accent to-cyan-800" },
  { label: "AI Response Quality", value: "98%", icon: ShieldCheck, gradient: "from-green-500 to-emerald-800" }
];

const recentChats = [
  { id: "1", title: "Property possession dispute under Illegal Dispossession Act", category: "Property Laws", date: "May 18, 2026", status: "Completed" },
  { id: "2", title: "Process of registering an FIR under Section 154 CrPC", category: "Criminal Laws", date: "May 16, 2026", status: "Completed" },
  { id: "3", title: "Khula and maintenance claims suit procedure", category: "Family Laws", date: "May 12, 2026", status: "Completed" }
];

const categoriesDistribution = [
  { name: "Criminal Laws", count: 5, percentage: "25%" },
  { name: "Property Laws", count: 4, percentage: "20%" },
  { name: "Family Laws", count: 3, percentage: "15%" },
  { name: "Constitutional Laws", count: 2, percentage: "10%" },
  { name: "Labour Laws", count: 2, percentage: "10%" },
  { name: "Tax Laws", count: 2, percentage: "10%" },
  { name: "Consumer Protection Laws", count: 1, percentage: "5%" },
  { name: "Civil Laws", count: 1, percentage: "5%" }
];

export default function DashboardPage() {
  return (
    <div className="w-full min-h-screen bg-brand-black pt-24 pb-20 relative">
      <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-primary/10 rounded-full blur-[100px] opacity-40 pointer-events-none" />
      
      <div className="container relative z-10 mx-auto px-4 md:px-6 max-w-6xl space-y-12">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight mb-2">Legal Advisor Dashboard</h1>
            <p className="text-sm text-foreground/50">Manage your consultations, analyze case files, and track your active inquiries.</p>
          </div>
          
          <Link 
            href="/chat"
            className="inline-flex items-center gap-2 px-5 py-3 rounded-xl bg-primary hover:bg-primary/95 text-white font-bold transition-all text-sm w-max shadow-md shadow-primary/20"
          >
            Start New Consultation <ArrowRight className="w-4 h-4" />
          </Link>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {stats.map((stat, i) => {
            const Icon = stat.icon;
            return (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: i * 0.05 }}
                className="glass p-6 rounded-2xl border-white/10 flex items-center justify-between group hover:border-white/20 transition-all"
              >
                <div className="space-y-1">
                  <span className="text-xs text-foreground/50 font-medium block">{stat.label}</span>
                  <span className="text-3xl font-extrabold text-white">{stat.value}</span>
                </div>
                <div className={`w-12 h-12 rounded-xl bg-gradient-to-tr ${stat.gradient} flex items-center justify-center text-white shrink-0 shadow-lg`}>
                  <Icon className="w-6 h-6" />
                </div>
              </motion.div>
            );
          })}
        </div>

        {/* Analytics and Categories Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Mock Activity Graph Card */}
          <div className="glass p-6 rounded-2xl border-white/10 lg:col-span-2 space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-bold text-white text-lg">AI Consultation Activity</h3>
                <p className="text-xs text-foreground/50">Number of messages sent over the past week</p>
              </div>
              <span className="text-xs font-semibold text-primary flex items-center gap-1">
                <TrendingUp className="w-3.5 h-3.5" /> +24% this week
              </span>
            </div>

            {/* Simulated Line Graph with SVG */}
            <div className="h-48 w-full flex items-end pt-4">
              <svg className="w-full h-full text-primary" viewBox="0 0 100 30" preserveAspectRatio="none">
                <defs>
                  <linearGradient id="chartGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="var(--color-primary)" stopOpacity="0.4" />
                    <stop offset="100%" stopColor="var(--color-primary)" stopOpacity="0" />
                  </linearGradient>
                </defs>
                <path
                  d="M 0 25 Q 15 20, 30 15 T 60 10 T 90 5 T 100 2 L 100 30 L 0 30 Z"
                  fill="url(#chartGradient)"
                />
                <path
                  d="M 0 25 Q 15 20, 30 15 T 60 10 T 90 5 T 100 2"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="0.8"
                />
              </svg>
            </div>
            
            {/* Graph labels */}
            <div className="flex justify-between text-[10px] text-foreground/40 font-semibold px-2">
              <span>Mon</span>
              <span>Tue</span>
              <span>Wed</span>
              <span>Thu</span>
              <span>Fri</span>
              <span>Sat</span>
              <span>Sun</span>
            </div>
          </div>

          {/* Legal Categories Distribution */}
          <div className="glass p-6 rounded-2xl border-white/10 space-y-6">
            <div>
              <h3 className="font-bold text-white text-lg">Category Distribution</h3>
              <p className="text-xs text-foreground/50">Your highly consulted sectors</p>
            </div>
            
            <div className="space-y-4">
              {categoriesDistribution.map((cat, i) => (
                <div key={i} className="space-y-1.5">
                  <div className="flex justify-between text-xs font-medium">
                    <span className="text-foreground/75">{cat.name}</span>
                    <span className="text-white font-bold">{cat.percentage}</span>
                  </div>
                  <div className="w-full bg-white/5 h-2 rounded-full overflow-hidden">
                    <div 
                      className="bg-primary h-full rounded-full" 
                      style={{ width: cat.percentage }} 
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Recent consultations */}
        <div className="glass p-6 md:p-8 rounded-2xl border-white/10 space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="font-bold text-white text-lg">Recent Consultations</h3>
              <p className="text-xs text-foreground/50 font-medium">View the summary of active legal inquiries</p>
            </div>
          </div>

          <div className="overflow-x-auto w-full">
            <table className="w-full text-left text-xs md:text-sm">
              <thead className="text-[10px] uppercase font-bold text-foreground/40 tracking-wider border-b border-white/5">
                <tr>
                  <th className="pb-3 pr-4">Case Title / Topic</th>
                  <th className="pb-3 pr-4">Focus Category</th>
                  <th className="pb-3 pr-4">Consultation Date</th>
                  <th className="pb-3 pr-4">Status</th>
                  <th className="pb-3 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {recentChats.map((chat) => (
                  <tr key={chat.id} className="text-foreground/80 hover:text-white transition-colors group">
                    <td className="py-4 pr-4 font-bold text-white/90 max-w-[200px] truncate">{chat.title}</td>
                    <td className="py-4 pr-4">
                      <span className="bg-primary/10 border border-primary/20 text-primary text-[10px] px-2 py-0.5 rounded-full font-semibold">
                        {chat.category}
                      </span>
                    </td>
                    <td className="py-4 pr-4 text-foreground/60">{chat.date}</td>
                    <td className="py-4 pr-4 text-emerald-400 font-semibold">{chat.status}</td>
                    <td className="py-4 text-right">
                      <Link 
                        href="/chat"
                        className="inline-flex items-center gap-1 text-xs text-primary font-bold hover:text-white transition-colors"
                      >
                        Reopen Chat <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
