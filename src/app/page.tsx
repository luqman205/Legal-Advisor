"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { ArrowRight, MessageSquare, BookOpen, Globe, Mic, FileText, Clock, Shield, Scale, ChevronRight } from "lucide-react";

const features = [
  { icon: MessageSquare, title: "AI Legal Chatbot", desc: "Instant legal answers in simple terms." },
  { icon: BookOpen, title: "Pakistani Law Knowledge", desc: "Trained on constitution and civil/criminal laws." },
  { icon: Globe, title: "Urdu + English Support", desc: "Ask questions in your preferred language." },
  { icon: Mic, title: "Voice Assistant", desc: "Speak your legal problems naturally." },
  { icon: FileText, title: "PDF Legal Analysis", desc: "Upload legal documents for quick summaries." },
  { icon: Clock, title: "24/7 AI Assistance", desc: "Legal help available around the clock." },
  { icon: Shield, title: "Secure Conversations", desc: "Your legal queries are private and encrypted." },
  { icon: Scale, title: "Legal Rights Awareness", desc: "Know your rights as a Pakistani citizen." },
];

const categories = [
  "Family Laws", "Criminal Laws", "Civil Laws", "Property Laws", 
  "Labour Laws", "Tax Laws", "Consumer Protection Laws", "Constitutional Laws"
];

export default function Home() {
  return (
    <div className="flex flex-col w-full items-center">
      {/* Hero Section */}
      <section className="relative w-full overflow-hidden bg-background pt-24 md:pt-32 lg:pt-40 pb-20">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-primary/20 rounded-full blur-[120px] opacity-50 pointer-events-none" />
        <div className="absolute top-0 right-0 w-[400px] h-[400px] bg-accent/20 rounded-full blur-[100px] opacity-40 pointer-events-none" />
        
        <div className="container relative z-10 mx-auto px-4 md:px-6 text-center flex flex-col items-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-sm font-medium mb-8 text-primary"
          >
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-primary"></span>
            </span>
            Pakistan's First AI Legal Advisor
          </motion.div>
          
          <motion.h1 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="text-4xl md:text-6xl lg:text-7xl font-extrabold tracking-tight max-w-4xl bg-clip-text text-transparent bg-gradient-to-r from-white via-white/90 to-white/50 mb-6"
          >
            AI-Powered Pakistani Legal Advisor
          </motion.h1>
          
          <motion.p 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="text-lg md:text-xl text-foreground/60 max-w-2xl mb-10"
          >
            Get intelligent legal guidance instantly using advanced AI trained on Pakistani laws and rights. Understand your legal standing in simple English or Urdu.
          </motion.p>
          
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="flex flex-col sm:flex-row gap-4 w-full sm:w-auto"
          >
            <Link href="/chat" className="inline-flex items-center justify-center gap-2 px-8 py-4 rounded-xl bg-primary text-white font-medium hover:bg-primary/90 transition-all shadow-[0_0_30px_-5px_rgba(124,58,237,0.4)] hover:shadow-[0_0_40px_-5px_rgba(124,58,237,0.6)]">
              Start Chat <ArrowRight className="w-5 h-5" />
            </Link>
            <Link href="/categories" className="inline-flex items-center justify-center gap-2 px-8 py-4 rounded-xl bg-white/5 border border-white/10 text-white font-medium hover:bg-white/10 transition-all">
              Explore Services
            </Link>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="w-full py-24 bg-brand-black border-y border-white/5 relative z-10">
        <div className="container mx-auto px-4 md:px-6">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Powerful Features</h2>
            <p className="text-foreground/60 max-w-2xl mx-auto">Everything you need to understand your legal rights and navigate the Pakistani justice system.</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature, i) => (
              <motion.div 
                key={i}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.4, delay: i * 0.1 }}
                className="glass p-6 rounded-2xl group hover:border-primary/50 transition-colors"
              >
                <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform">
                  <feature.icon className="w-6 h-6 text-primary" />
                </div>
                <h3 className="text-lg font-semibold mb-2">{feature.title}</h3>
                <p className="text-sm text-foreground/60">{feature.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Categories Section */}
      <section className="w-full py-24 relative overflow-hidden">
        <div className="absolute top-0 left-0 w-full h-full bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-secondary/10 via-background to-background pointer-events-none" />
        
        <div className="container relative z-10 mx-auto px-4 md:px-6">
          <div className="flex flex-col md:flex-row md:items-end justify-between mb-12 gap-4">
            <div>
              <h2 className="text-3xl md:text-4xl font-bold mb-4">Legal Categories</h2>
              <p className="text-foreground/60 max-w-xl">Explore specific areas of law to get targeted advice and understand how the legal system applies to your situation.</p>
            </div>
            <Link href="/categories" className="inline-flex items-center text-primary font-medium hover:text-primary/80 transition-colors">
              View All <ChevronRight className="w-4 h-4 ml-1" />
            </Link>
          </div>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
            {categories.map((cat, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, scale: 0.95 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ duration: 0.3, delay: i * 0.05 }}
              >
                <Link href={`/chat?category=${encodeURIComponent(cat)}`} className="block w-full h-full p-5 rounded-xl border border-white/10 bg-white/5 hover:bg-white/10 hover:border-primary/50 transition-all group">
                  <div className="flex justify-between items-center">
                    <span className="font-medium group-hover:text-primary transition-colors">{cat}</span>
                    <ArrowRight className="w-4 h-4 opacity-0 group-hover:opacity-100 -translate-x-2 group-hover:translate-x-0 transition-all text-primary" />
                  </div>
                </Link>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="w-full py-24 bg-gradient-to-t from-brand-black to-background relative z-10">
        <div className="container mx-auto px-4 md:px-6 text-center">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="max-w-3xl mx-auto glass p-10 md:p-16 rounded-3xl border-primary/20 relative overflow-hidden"
          >
            <div className="absolute inset-0 bg-primary/10 blur-[50px]" />
            <div className="relative z-10">
              <h2 className="text-3xl md:text-5xl font-bold mb-6">Ready to get legal clarity?</h2>
              <p className="text-lg text-foreground/70 mb-8">
                Start your conversation with the AI legal advisor now. It's completely free, confidential, and available 24/7.
              </p>
              <Link href="/chat" className="inline-flex items-center justify-center gap-2 px-8 py-4 rounded-xl bg-white text-black font-semibold hover:bg-gray-200 transition-all shadow-lg hover:shadow-xl">
                Start Free Consultation
              </Link>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  );
}
