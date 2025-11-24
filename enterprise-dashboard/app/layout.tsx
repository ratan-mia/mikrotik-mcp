import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
    title: "MikroTik Enterprise Management",
    description: "Enterprise-level MikroTik Router Management System",
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en" suppressHydrationWarning>
            <body suppressHydrationWarning>
                {children}
            </body>
        </html>
    );
}
