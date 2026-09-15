import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Bound By Books",
  description: "A digital home for your physical book collection.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
