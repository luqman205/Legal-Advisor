"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Scale, Menu, X } from "lucide-react";
import { useState } from "react";

export function Navbar() {
  const pathname = usePathname();
  const [isOpen, setIsOpen] = useState(false);

  // Don't show navbar on chat page for full-screen experience
  if (pathname === "/chat") return null;

  const links = [
    { href: "/", label: "Home" },
    { href: "/categories", label: "Legal Categories" },
    { href: "/pdf-analyzer", label: "PDF Analyzer" },
    { href: "/dashboard", label: "Dashboard" },
  ];

  return (
    <header className="sticky top-0 z-50 w-full border-b border-white/10 bg-background/80 backdrop-blur-md">
      <div className="container mx-auto flex h-16 items-center justify-between px-4 md:px-6">
        <Link href="/" className="flex items-center gap-2 transition-colors hover:text-primary">
          <Scale className="h-6 w-6 text-primary" />
          <span className="font-bold tracking-tight">Pakistani Legal Advisor AI</span>
        </Link>
        <nav className="hidden md:flex items-center gap-6 text-sm font-medium">
          {links.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className={`transition-colors hover:text-primary ${
                pathname === link.href ? "text-primary" : "text-foreground/80"
              }`}
            >
              {link.label}
            </Link>
          ))}
          <Link
            href="/login"
            className="rounded-md bg-white/5 px-4 py-2 text-sm font-medium border border-white/10 hover:bg-white/10 transition-colors"
          >
            Log In
          </Link>
          <Link
            href="/chat"
            className="rounded-md bg-primary px-4 py-2 text-sm font-medium text-white shadow hover:bg-primary/90 transition-colors shadow-primary/20"
          >
            Start Chat
          </Link>
        </nav>
        <button
          className="md:hidden p-2 text-foreground/80"
          onClick={() => setIsOpen(!isOpen)}
        >
          {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
        </button>
      </div>
      {isOpen && (
        <div className="md:hidden border-b border-white/10 bg-background px-4 py-4 space-y-4">
          <nav className="flex flex-col gap-4 text-sm font-medium">
            {links.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                onClick={() => setIsOpen(false)}
                className={`transition-colors hover:text-primary ${
                  pathname === link.href ? "text-primary" : "text-foreground/80"
                }`}
              >
                {link.label}
              </Link>
            ))}
            <div className="flex flex-col gap-2 pt-4 border-t border-white/10">
              <Link
                href="/login"
                onClick={() => setIsOpen(false)}
                className="w-full text-center rounded-md bg-white/5 px-4 py-2 text-sm font-medium border border-white/10 hover:bg-white/10 transition-colors"
              >
                Log In
              </Link>
              <Link
                href="/chat"
                onClick={() => setIsOpen(false)}
                className="w-full text-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-white shadow hover:bg-primary/90 transition-colors"
              >
                Start Chat
              </Link>
            </div>
          </nav>
        </div>
      )}
    </header>
  );
}
