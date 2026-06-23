"use client";

import React from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { 
  Users, ShieldAlert, Home, Landmark, ShoppingBag, Briefcase, 
  FileText, ShieldCheck, HeartCrack, Scale, ArrowRight 
} from "lucide-react";

const legalCategories = [
  {
    name: "Family Laws",
    icon: Users,
    desc: "Marriage registration, divorce, Khula (dissolution), dower (Haq Mehr), child support maintenance, and physical custody of minors under the Muslim Family Laws Ordinance 1961.",
    stats: "2.4k inquiries this month",
    law: "Muslim Family Laws Ordinance 1961, Guardians and Wards Act 1890"
  },
  {
    name: "Criminal Laws",
    icon: ShieldAlert,
    desc: "First Information Report (FIR) registration, bail applications, police detention rules, theft, mischief, forgery, and murder offenses under the PPC.",
    stats: "5.5k inquiries this month",
    law: "Pakistan Penal Code (PPC) 1860, Code of Criminal Procedure (CrPC) 1898"
  },
  {
    name: "Civil Laws",
    icon: Landmark,
    desc: "Specific performance of contracts, declaratory lawsuits, perpetual injunction stay orders, breach of contracts, and indemnity frameworks.",
    stats: "1.8k inquiries this month",
    law: "Specific Relief Act 1877, Contract Act 1872"
  },
  {
    name: "Property Laws",
    icon: Home,
    desc: "Registered sale deeds, gift deeds (Hiba), land records verification (Fard/Mutation), and remedies against qabza mafia and encroachment.",
    stats: "3.2k inquiries this month",
    law: "Transfer of Property Act 1882, Illegal Dispossession Act 2005"
  },
  {
    name: "Labour Laws",
    icon: Briefcase,
    desc: "Worker wage limits, delayed salaries, wrongful termination, gratuity calculation, and workplace inquiry defense under Standing Orders.",
    stats: "2.0k inquiries this month",
    law: "Payment of Wages Act 1936, Industrial & Commercial Employment Ordinance 1968"
  },
  {
    name: "Tax Laws",
    icon: FileText,
    desc: "Annual income tax return filing, FBR assessments, default surcharge penalties, sales tax credit refunds, and FBR tax audit appeals.",
    stats: "1.2k inquiries this month",
    law: "Income Tax Ordinance 2001, Sales Tax Act 1990"
  },
  {
    name: "Consumer Protection Laws",
    icon: ShoppingBag,
    desc: "Defective online and physical products, deficient services, mental agony damages, 15-day mandatory legal notice, and Consumer Court filings.",
    stats: "1.1k inquiries this month",
    law: "Provincial Consumer Protection Acts (e.g. Punjab Consumer Protection Act 2005)"
  },
  {
    name: "Constitutional Laws",
    icon: Scale,
    desc: "Fundamental rights enforcement, security of person, right to fair trial and due process, and writ petitions in High Court under Article 199.",
    stats: "1.9k inquiries this month",
    law: "Constitution of the Islamic Republic of Pakistan, 1973 (Part II)"
  }
];

export default function CategoriesPage() {
  return (
    <div className="w-full min-h-screen bg-brand-black pt-24 pb-20 relative">
      {/* Background gradients */}
      <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-primary/10 rounded-full blur-[100px] opacity-40 pointer-events-none" />
      <div className="absolute bottom-0 left-0 w-[400px] h-[400px] bg-secondary/10 rounded-full blur-[120px] opacity-40 pointer-events-none" />

      <div className="container relative z-10 mx-auto px-4 md:px-6">
        {/* Header */}
        <div className="text-center max-w-3xl mx-auto mb-16">
          <motion.h1 
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="text-4xl md:text-5xl font-extrabold tracking-tight mb-4"
          >
            Explore Pakistani Legal Categories
          </motion.h1>
          <motion.p 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.15 }}
            className="text-lg text-foreground/60 leading-relaxed"
          >
            Learn about your legal rights and the governing laws in Pakistan. Select a category below to launch a targeted consultation session with our AI advisor.
          </motion.p>
        </div>

        {/* Categories Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 lg:gap-8">
          {legalCategories.map((cat, i) => {
            const Icon = cat.icon;
            return (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: i * 0.05 }}
                className="glass p-6 md:p-8 rounded-2xl border border-white/10 hover:border-primary/40 relative overflow-hidden group hover:shadow-2xl hover:shadow-primary/5 transition-all"
              >
                {/* Glow Accent */}
                <div className="absolute top-0 right-0 w-24 h-24 bg-primary/10 rounded-full blur-[30px] opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none" />
                
                <div className="flex gap-4 md:gap-6 items-start">
                  <div className="w-12 h-12 md:w-14 md:h-14 rounded-xl bg-primary/10 border border-primary/20 flex items-center justify-center shrink-0 group-hover:scale-110 transition-transform">
                    <Icon className="w-6 h-6 md:w-7 md:h-7 text-primary" />
                  </div>
                  
                  <div className="space-y-3 flex-1">
                    <div className="flex justify-between items-center">
                      <h3 className="text-xl font-bold text-white group-hover:text-primary transition-colors">{cat.name}</h3>
                      <span className="text-[10px] text-primary bg-primary/10 px-2 py-0.5 rounded-full font-medium">{cat.stats}</span>
                    </div>
                    
                    <p className="text-xs md:text-sm text-foreground/60 leading-relaxed">{cat.desc}</p>
                    
                    <div className="border-t border-white/5 pt-3 mt-3 flex flex-col gap-2 sm:flex-row sm:items-center justify-between">
                      <div className="text-[10px] text-foreground/40 font-mono">
                        <span className="font-semibold text-foreground/50">Primary Law:</span> {cat.law}
                      </div>
                      
                      <Link 
                        href={`/chat?category=${encodeURIComponent(cat.name)}`}
                        className="inline-flex items-center gap-1 text-xs font-semibold text-primary group-hover:text-white transition-colors mt-2 sm:mt-0"
                      >
                        Ask AI Chatbot <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
                      </Link>
                    </div>
                  </div>
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
