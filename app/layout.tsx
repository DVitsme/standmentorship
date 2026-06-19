import type { Metadata } from "next";
import { Archivo, Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

const archivo = Archivo({
  subsets: ["latin"],
  variable: "--font-archivo",
  display: "swap",
  weight: ["600", "700", "800", "900"],
});

export const metadata: Metadata = {
  title: {
    default: "S.T.A.N.D Mentorship",
    template: "%s — S.T.A.N.D Mentorship",
  },
  description:
    "Stepping Towards A New Destiny — free youth leadership, life-skills, and skilled-trades mentorship in Baltimore and Howard County, Maryland.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${inter.variable} ${archivo.variable}`}>
      {/* suppressHydrationWarning: benign browser-extension attribute injection on <body>. */}
      <body
        suppressHydrationWarning
        className="min-h-dvh bg-background text-foreground antialiased"
      >
        <a
          href="#main"
          className="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-50 focus:rounded-md focus:bg-brand focus:px-4 focus:py-2 focus:text-sm focus:text-brand-foreground"
        >
          Skip to content
        </a>
        <main id="main">{children}</main>
      </body>
    </html>
  );
}
