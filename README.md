# ⚖️ Pakistani Legal Advisor AI

An enterprise-grade, AI-powered Pakistani Legal Advisor Chatbot built using Next.js, Tailwind CSS, Framer Motion, and Lucide React. Designed with modern SaaS dark mode aesthetics (glassmorphism, glowing gradients, high-end layouts), this application replicates a ChatGPT-like conversational workflow tailored to the Constitution and Code of Criminal/Civil Procedure of Pakistan.

---

## 🌟 Key Features

1. **🤖 Advanced Legal Chatbot (`/chat`)**:
   - Sidebar history with localized state persistence (`localStorage`).
   - Suggested prompts for common Pakistani legal situations (FIR registration, Tenant rights, Women's inheritance protection, Cyber Crime under PECA 2016).
   - Right-aligned purple-gradient user chat bubbles, left-aligned premium dark glass chatbot responses.
   - Message feedback (like/dislike) and one-click copy response utilities.
   - Streaming/typing animation placeholders to represent live AI processing.
   
2. **📂 PDF Legal Analyzer (`/pdf-analyzer`)**:
   - Drag-and-drop zone for police complaints (FIRs), contracts, or lease agreements.
   - Simulated progressive extraction with state loading indicators.
   - Clause identifier highlighting corresponding sections of the Pakistan Penal Code (PPC).
   - "Executive Summary", "Plain English/Urdu translation", and "Advised Actions" result panel.

3. **📊 Analytics Dashboard (`/dashboard`)**:
   - Interactive high-performance SVG activity line chart.
   - Gradient statistics metrics for consultations, document uploads, and case distribution.
   - Dynamic list of recent consultation histories.

4. **🗺️ Legal Categories Catalog (`/categories`)**:
   - Interactive premium cards with gradient borders, glow accents, and custom hover states.
   - Specific details on Pakistani law frameworks (e.g. Muslim Family Laws Ordinance 1961, PECA 2016, Rented Premises Acts).

5. **🎙️ Speech-to-Text Voice Recognition**:
   - Real-time microphone input integration within the chat window utilizing the browser's web speech recognition API.

6. **🔒 Secure Authentication Portal**:
   - Glassmorphic forms with input validation for Log In and Secure Registration.
   - Privacy consent agreement specifically acknowledging protection under Pakistan's privacy laws.

---

## 🎨 Design Theme & Brand Identity

* **Primary Background**: `#0B0F19` (Deep Black)
* **Secondary Cards**: `#111827` (Dark Navy)
* **Accent Colors**: `#7C3AED` (Violet Violet) & `#06B6D4` (Electric Cyan Glow)
* **Typography**: Geist Sans & Mono (premium next-generation terminal fonts)
* **Visual FX**: Glassmorphism cards with border glows (`backdrop-blur-lg`)

---

## 📂 Project Architecture

```
├── src/
│   ├── app/
│   │   ├── categories/       # Legal Categories Catalog page
│   │   ├── chat/             # ChatGPT-style Consultation window
│   │   ├── dashboard/        # Professional usage analytics
│   │   ├── login/            # Authentication portal (Sign In)
│   │   ├── signup/           # Secure registration (Sign Up)
│   │   ├── pdf-analyzer/     # Drag & drop legal document clauses parser
│   │   ├── globals.css       # Core Tailwind CSS & custom glass classes
│   │   ├── layout.tsx        # Shell wrapping Header, Footer, and next-themes
│   │   └── page.tsx          # High-converting SaaS landing hero page
│   └── components/
│       ├── navbar.tsx        # Global responsive header navigation
│       ├── footer.tsx        # Standard disclaimer & global footer
│       └── theme-provider.tsx# Light/Dark context wrapper
```

---

## 🚀 Running the Project Locally

Ensure Node.js is installed on your system.

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Launch development server**:
   ```bash
   npm run dev
   ```

3. **Open browser**:
   Go to [http://localhost:3000](http://localhost:3000) to view your premium legal dashboard!

---

### ⚠️ Disclaimer
This AI chatbot provides informational legal guidance only and is not a substitute for professional legal advice from a registered High Court advocate.
