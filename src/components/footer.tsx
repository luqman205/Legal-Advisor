"use client";

import Link from "next/link";
import { Scale } from "lucide-react";
import { usePathname } from "next/navigation";

export function Footer() {
  const pathname = usePathname();
  if (pathname === "/chat") return null;

  return (
    <footer className="border-t border-white/10 bg-brand-black py-12 md:py-16 lg:py-20">
      <div className="container mx-auto px-4 md:px-6">
        <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-4">
          <div className="space-y-4">
            <Link href="/" className="flex items-center gap-2">
              <Scale className="h-6 w-6 text-primary" />
              <span className="font-bold text-lg tracking-tight">Legal Advisor AI</span>
            </Link>
            <p className="text-sm text-foreground/60 leading-relaxed max-w-xs">
              Empowering citizens with accessible, AI-driven legal guidance based on Pakistani laws.
            </p>
          </div>
          <div>
            <h3 className="mb-4 text-sm font-semibold uppercase tracking-wider text-foreground/80">Services</h3>
            <ul className="space-y-2 text-sm text-foreground/60">
              <li><Link href="/chat" className="hover:text-primary transition-colors">AI Chatbot</Link></li>
              <li><Link href="/pdf-analyzer" className="hover:text-primary transition-colors">PDF Document Analysis</Link></li>
              <li><Link href="/categories" className="hover:text-primary transition-colors">Legal Categories</Link></li>
            </ul>
          </div>
          <div>
            <h3 className="mb-4 text-sm font-semibold uppercase tracking-wider text-foreground/80">Company</h3>
            <ul className="space-y-2 text-sm text-foreground/60">
              <li><Link href="#" className="hover:text-primary transition-colors">About Us</Link></li>
              <li><Link href="#" className="hover:text-primary transition-colors">Contact</Link></li>
              <li><Link href="#" className="hover:text-primary transition-colors">Privacy Policy</Link></li>
            </ul>
          </div>
          <div>
            <h3 className="mb-4 text-sm font-semibold uppercase tracking-wider text-foreground/80">Disclaimer</h3>
            <p className="text-xs text-foreground/50 leading-relaxed">
              This AI chatbot provides informational legal guidance only and is not a substitute for professional legal advice. Always consult a qualified lawyer for critical matters.
            </p>
          </div>
        </div>
        <div className="mt-12 border-t border-white/10 pt-8 text-center text-sm text-foreground/60">
          <p>© {new Date().getFullYear()} Pakistani Legal Advisor AI. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}
