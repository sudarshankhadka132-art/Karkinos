import './globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import Link from 'next/link';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Karkinos Intelligence',
  description: 'Minimalist oncology intelligence portal'
};

export default function RootLayout({
  children
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="bg-white text-slate-900">
      <body className={`${inter.className} antialiased`}>
        <div className="min-h-screen px-6 py-12 sm:px-12 lg:px-24">
          <header className="flex items-center justify-between border-b border-slate-200 pb-6">
            <Link href="/" className="text-xl font-semibold tracking-tight">
              Karkinos Intelligence
            </Link>
            <nav className="flex gap-6 text-sm font-medium text-slate-500">
              <Link href="/intelligence" className="transition hover:text-primary-600">
                Intelligence
              </Link>
              <a
                href="https://github.com"
                className="transition hover:text-primary-600"
                target="_blank"
                rel="noreferrer"
              >
                GitHub
              </a>
            </nav>
          </header>
          <main className="mx-auto max-w-5xl py-12">{children}</main>
          <footer className="border-t border-slate-200 pt-6 text-sm text-slate-400">
            © {new Date().getFullYear()} Karkinos. Built for oncology insights.
          </footer>
        </div>
      </body>
    </html>
  );
}
