import "./globals.css";
import { Inter, JetBrains_Mono } from "next/font/google";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-jetbrains-mono",
  display: "swap",
});

export const metadata = {
  title: "LLM Control Plane",
  description: "Controlled, auditable AI inference system",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${inter.variable} ${jetbrainsMono.variable}`}>
      <body className="min-h-screen flex flex-col bg-neutral-950 text-neutral-100 font-sans antialiased">
        <header className="border-b border-neutral-800 px-6 py-4 bg-neutral-950">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-lg font-semibold tracking-tight text-neutral-100">
                LLM Control Plane
              </h1>
              <p className="text-xs text-neutral-500 mt-0.5">
                Controlled · Auditable · Safe
              </p>
            </div>
            <span className="text-xs text-neutral-400 font-mono">
              v0.3.0
            </span>
          </div>
        </header>

        <main className="flex-1 px-6 py-8">{children}</main>

        <footer className="border-t border-neutral-800 px-6 py-3 text-xs text-neutral-500">
          Internal AI Governance Console
        </footer>
      </body>
    </html>
  );
}
