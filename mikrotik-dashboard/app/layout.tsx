import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "MikroTik Dashboard - SKS Router",
  description: "Modern web dashboard for MikroTik router management",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}
