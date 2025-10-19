// App-wide layout and navigation chrome
import type { Metadata } from "next";
import Link from "next/link";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

// Basic SEO metadata; adjust per page if needed
export const metadata: Metadata = {
  title: "Ikarus 3D - AI Product Recommendations",
  description: "AI-powered furniture product recommendations with creative descriptions",
  icons: { icon: "/favicon.ico" },
};

/**
 * Root layout wraps all pages with nav and global styles.
 */
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className={inter.className}>
        <nav className="bg-card border-b border-border shadow-sm">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex items-center">
                <Link href="/" className="text-xl font-bold text-foreground font-gantari">
                  Ikarus 3D Assignment
                </Link>
              </div>
              <div className="flex items-center space-x-8">
                <Link 
                  href="/" 
                  className="text-muted-foreground hover:text-foreground px-3 py-2 rounded-md text-sm font-medium transition-colors"
                >
                  Recommendations
                </Link>
                <Link 
                  href="/analytics" 
                  className="text-muted-foreground hover:text-foreground px-3 py-2 rounded-md text-sm font-medium transition-colors"
                >
                  Analytics
                </Link>
              </div>
            </div>
          </div>
        </nav>
        <main className="min-h-screen bg-background">
          {children}
        </main>
      </body>
    </html>
  );
}

