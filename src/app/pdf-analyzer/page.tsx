"use client";

import React, { useState, useRef } from "react";
import { motion } from "framer-motion";
import { Upload, FileText, CheckCircle2, AlertTriangle, Play, RefreshCw, BookOpen, Scale } from "lucide-react";
import Link from "next/link";

export default function PdfAnalyzerPage() {
  const [dragActive, setDragActive] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [progress, setProgress] = useState(0);
  const [isUploading, setIsUploading] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [result, setResult] = useState<any | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const droppedFile = e.dataTransfer.files[0];
      if (droppedFile.type === "application/pdf") {
        handleUpload(droppedFile);
      } else {
        alert("Please upload a PDF document only.");
      }
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleUpload(e.target.files[0]);
    }
  };

  const handleUpload = (file: File) => {
    setFile(file);
    setIsUploading(true);
    setProgress(0);
    
    // Simulate upload progress
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval);
          setIsUploading(false);
          analyzeDocument();
          return 100;
        }
        return prev + 10;
      });
    }, 150);
  };

  const analyzeDocument = () => {
    setIsAnalyzing(true);
    
    // Simulate AI document analysis
    setTimeout(() => {
      setIsAnalyzing(false);
      setResult({
        title: file?.name || "Legal Document",
        type: "First Information Report (FIR) / Legal Grievance",
        clauses: [
          { number: "PPC Section 379", title: "Theft", summary: "Accuses the perpetrator of dishonestly taking moveable property out of the possession of the complainant without consent." },
          { number: "PPC Section 427", title: "Mischief causing damage", summary: "Deals with committing mischief and thereby causing damage or loss to the amount of fifty rupees or upwards." }
        ],
        summary: "This document is a formal police complaint (FIR) filed under the Pakistan Penal Code. It accuses the designated accused parties of committing theft (Section 379) and damage to personal property (Section 427). The incident is reported to have occurred within the jurisdiction of Punjab Police.",
        simpleExplanation: "In simple words, the complainant alleges that someone stole their belongings and caused physical damage to their property. The police are legally bound to investigate the theft and assess the damages.",
        recommendations: [
          "Ensure that the police issue an officially stamped copy of the registered FIR.",
          "Collect proof of ownership/valuation of the stolen property to support the investigation.",
          "Seek the assistance of a criminal advocate to draft statements under Section 161 of CrPC."
        ]
      });
    }, 2500);
  };

  const resetAnalyzer = () => {
    setFile(null);
    setProgress(0);
    setResult(null);
  };

  return (
    <div className="w-full min-h-screen bg-brand-black pt-24 pb-20 relative">
      <div className="absolute top-0 left-0 w-[500px] h-[500px] bg-primary/10 rounded-full blur-[100px] opacity-40 pointer-events-none" />
      
      <div className="container relative z-10 mx-auto px-4 md:px-6 max-w-4xl">
        {/* Header */}
        <div className="text-center mb-12">
          <motion.h1 
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-4xl font-extrabold tracking-tight mb-4"
          >
            PDF Legal Document Analyzer
          </motion.h1>
          <motion.p 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-lg text-foreground/60 leading-relaxed"
          >
            Upload FIRs, rent agreements, court summons, or contract documents. Our AI will extract key terms, summarize them, and explain Pakistani legal jargon in simple words.
          </motion.p>
        </div>

        {/* Upload Zone & States */}
        {!file ? (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            onDragEnter={handleDrag}
            onDragOver={handleDrag}
            onDragLeave={handleDrag}
            onDrop={handleDrop}
            className={`glass border-2 border-dashed rounded-3xl p-12 text-center flex flex-col items-center justify-center cursor-pointer transition-all ${
              dragActive ? "border-primary bg-primary/5" : "border-white/10 hover:border-primary/50"
            }`}
            onClick={() => fileInputRef.current?.click()}
          >
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleChange}
              accept=".pdf"
              className="hidden"
            />
            
            <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center mb-6">
              <Upload className="w-8 h-8 text-primary" />
            </div>
            
            <h3 className="text-xl font-bold text-white mb-2">Drag & drop your PDF here</h3>
            <p className="text-sm text-foreground/50 mb-6">or click to browse from files</p>
            <span className="text-[10px] uppercase bg-white/5 border border-white/10 text-foreground/60 px-3 py-1 rounded-full font-semibold">
              Supports PDF documents up to 10MB
            </span>
          </motion.div>
        ) : (
          <div className="space-y-8">
            {/* File status card */}
            <div className="glass p-6 rounded-2xl border-white/10 flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-xl bg-primary/10 border border-primary/20 flex items-center justify-center text-primary">
                  <FileText className="w-6 h-6" />
                </div>
                <div>
                  <h4 className="font-bold text-white max-w-[200px] sm:max-w-xs md:max-w-md truncate">{file.name}</h4>
                  <span className="text-xs text-foreground/40">{(file.size / (1024 * 1024)).toFixed(2)} MB</span>
                </div>
              </div>
              
              {!isUploading && !isAnalyzing && (
                <button 
                  onClick={resetAnalyzer}
                  className="p-2 rounded-lg bg-white/5 hover:bg-white/10 hover:text-red-400 text-foreground/60 transition-colors cursor-pointer"
                >
                  Remove
                </button>
              )}
            </div>

            {/* Upload progress state */}
            {isUploading && (
              <div className="glass p-8 rounded-2xl border-white/10 text-center space-y-4">
                <RefreshCw className="w-8 h-8 text-primary animate-spin mx-auto" />
                <h4 className="font-bold text-white text-lg">Uploading document...</h4>
                <div className="w-full bg-white/5 h-2 rounded-full overflow-hidden">
                  <div className="bg-primary h-full transition-all duration-150" style={{ width: `${progress}%` }} />
                </div>
                <span className="text-xs text-foreground/50">{progress}% completed</span>
              </div>
            )}

            {/* Analysis Loading state */}
            {isAnalyzing && (
              <div className="glass p-8 rounded-2xl border-white/10 text-center space-y-4">
                <Scale className="w-8 h-8 text-primary animate-bounce mx-auto" />
                <h4 className="font-bold text-white text-lg">AI Legal Engine is analyzing document clauses...</h4>
                <p className="text-sm text-foreground/60 max-w-sm mx-auto">
                  Applying NLP and matching document statements against active articles of Pakistan Penal Code (PPC) and CrPC.
                </p>
                <div className="w-32 bg-white/5 h-1.5 rounded-full overflow-hidden mx-auto">
                  <div className="bg-primary h-full w-1/2 animate-[shimmer_1.5s_infinite]" style={{ transform: "translateX(100%)" }} />
                </div>
              </div>
            )}

            {/* Analysis results */}
            {result && (
              <motion.div
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                className="space-y-6"
              >
                {/* AI Summary Banner */}
                <div className="glass p-6 md:p-8 rounded-2xl border-primary/20 bg-primary/5 space-y-4">
                  <div className="flex items-center gap-2 text-primary">
                    <CheckCircle2 className="w-5 h-5" />
                    <span className="font-bold uppercase tracking-wider text-xs">AI Extraction Success</span>
                  </div>
                  
                  <div>
                    <span className="text-[10px] text-primary-foreground font-semibold px-2 py-0.5 rounded-full bg-primary/10">Document Type: {result.type}</span>
                    <h3 className="text-xl font-bold text-white mt-2">Executive Summary</h3>
                  </div>
                  <p className="text-sm text-foreground/75 leading-relaxed">{result.summary}</p>
                </div>

                {/* Explanation Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {/* Simple Explanation */}
                  <div className="glass p-6 rounded-2xl border-white/10 space-y-3">
                    <h4 className="font-bold text-white text-md flex items-center gap-2">
                      <BookOpen className="w-4 h-4 text-primary" /> Plain English / Urdu Explanation
                    </h4>
                    <p className="text-xs md:text-sm text-foreground/70 leading-relaxed">{result.simpleExplanation}</p>
                  </div>

                  {/* Recommendations */}
                  <div className="glass p-6 rounded-2xl border-white/10 space-y-3">
                    <h4 className="font-bold text-white text-md flex items-center gap-2">
                      <Scale className="w-4 h-4 text-primary" /> Advised Next Actions
                    </h4>
                    <ul className="space-y-2">
                      {result.recommendations.map((rec: string, idx: number) => (
                        <li key={idx} className="text-xs text-foreground/70 flex gap-2">
                          <span className="text-primary font-bold shrink-0">{idx + 1}.</span>
                          <span>{rec}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>

                {/* Clauses & Sections */}
                <div className="glass p-6 md:p-8 rounded-2xl border-white/10 space-y-6">
                  <h4 className="font-bold text-white text-lg">Identified Penal/Civil Sections</h4>
                  
                  <div className="space-y-4">
                    {result.clauses.map((clause: any, idx: number) => (
                      <div key={idx} className="p-4 rounded-xl bg-white/5 border border-white/5 space-y-2">
                        <div className="flex justify-between items-center">
                          <span className="text-xs font-mono font-bold text-primary">{clause.number}</span>
                          <span className="text-xs font-semibold text-white">{clause.title}</span>
                        </div>
                        <p className="text-xs text-foreground/60 leading-relaxed">{clause.summary}</p>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Action CTA */}
                <div className="flex gap-4">
                  <Link 
                    href={`/chat?query=I want to consult about my uploaded FIR relating to PPC sections`}
                    className="flex-1 text-center py-4 rounded-xl bg-primary text-white font-bold hover:bg-primary/95 transition-all shadow-md shadow-primary/20"
                  >
                    Start Chat Consultation on this PDF
                  </Link>
                  
                  <button 
                    onClick={resetAnalyzer}
                    className="px-6 py-4 rounded-xl bg-white/5 border border-white/10 hover:bg-white/10 text-white transition-all text-sm font-semibold"
                  >
                    Upload Another PDF
                  </button>
                </div>
              </motion.div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
