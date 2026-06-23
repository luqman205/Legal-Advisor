"use client";

import React, { useState } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { Scale, Mail, Lock, ArrowRight, Eye, EyeOff } from "lucide-react";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setTimeout(() => {
      setIsLoading(false);
      window.location.href = "/dashboard";
    }, 1500);
  };

  return (
    <div className="w-full min-h-screen bg-brand-black flex items-center justify-center pt-20 pb-16 relative px-4">
      <div className="absolute top-1/4 left-1/4 w-[350px] h-[350px] bg-primary/20 rounded-full blur-[100px] opacity-40 pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/4 w-[350px] h-[350px] bg-secondary/10 rounded-full blur-[100px] opacity-40 pointer-events-none" />

      <motion.div 
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-md glass p-8 rounded-3xl border border-white/10 relative z-10 flex flex-col items-center"
      >
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2 mb-8 group">
          <Scale className="h-7 w-7 text-primary group-hover:rotate-12 transition-transform" />
          <span className="font-extrabold text-lg tracking-wider text-white">Legal Advisor AI</span>
        </Link>

        {/* Title */}
        <div className="text-center mb-8">
          <h2 className="text-2xl font-bold text-white mb-2">Welcome Back</h2>
          <p className="text-xs text-foreground/50">Log in to access your secure legal consultations dashboard</p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="w-full space-y-5">
          {/* Email */}
          <div className="space-y-1.5">
            <label className="text-[10px] font-bold uppercase tracking-wider text-foreground/50 block">Email Address</label>
            <div className="relative">
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="name@example.com"
                className="w-full bg-white/5 border border-white/10 rounded-xl py-3 pl-10 pr-4 text-xs text-white focus:outline-none focus:border-primary placeholder:text-foreground/20 transition-colors"
              />
              <Mail className="absolute left-3.5 top-3.5 h-4.5 w-4.5 text-foreground/35" />
            </div>
          </div>

          {/* Password */}
          <div className="space-y-1.5">
            <div className="flex justify-between items-center">
              <label className="text-[10px] font-bold uppercase tracking-wider text-foreground/50 block">Password</label>
              <Link href="#" className="text-[10px] text-primary hover:text-primary/80 transition-colors">Forgot Password?</Link>
            </div>
            <div className="relative">
              <input
                type={showPassword ? "text" : "password"}
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full bg-white/5 border border-white/10 rounded-xl py-3 pl-10 pr-10 text-xs text-white focus:outline-none focus:border-primary placeholder:text-foreground/20 transition-colors"
              />
              <Lock className="absolute left-3.5 top-3.5 h-4.5 w-4.5 text-foreground/35" />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-3 text-foreground/40 hover:text-white"
              >
                {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>
          </div>

          {/* Button */}
          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-3.5 rounded-xl bg-primary text-white font-bold hover:bg-primary/95 transition-all shadow-md shadow-primary/20 flex items-center justify-center gap-2 cursor-pointer mt-4"
          >
            {isLoading ? "Signing in..." : "Log In"} <ArrowRight className="w-4 h-4" />
          </button>
        </form>

        {/* Signup CTA */}
        <p className="mt-8 text-xs text-foreground/55 text-center">
          Don't have a secure account?{" "}
          <Link href="/signup" className="text-primary hover:text-primary/80 font-semibold transition-colors">
            Create an Account
          </Link>
        </p>
      </motion.div>
    </div>
  );
}
