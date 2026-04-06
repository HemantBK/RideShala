import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "RideShala - AI Motorcycle Advisor for Indian Riders",
  description:
    "Find the perfect bike based on your height, budget, commute, and riding style. AI-powered recommendations with source citations. Free, open-source, legally compliant.",
  keywords: [
    "motorcycle comparison",
    "bike advisor",
    "India bikes",
    "AI recommendation",
    "Royal Enfield",
    "Honda",
    "Hero",
    "Bajaj",
  ],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body style={{ margin: 0, fontFamily: "system-ui, -apple-system, sans-serif" }}>
        <header
          style={{
            padding: "16px 24px",
            borderBottom: "1px solid #e5e7eb",
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
            <strong style={{ fontSize: "20px" }}>RideShala</strong>
            <span
              style={{
                fontSize: "11px",
                background: "#dcfce7",
                color: "#166534",
                padding: "2px 8px",
                borderRadius: "9999px",
              }}
            >
              Open Source
            </span>
          </div>
          <nav style={{ display: "flex", gap: "24px", fontSize: "14px" }}>
            <a href="/" style={{ color: "#374151", textDecoration: "none" }}>
              Home
            </a>
            <a href="/chat" style={{ color: "#374151", textDecoration: "none" }}>
              AI Chat
            </a>
            <a href="/compare" style={{ color: "#374151", textDecoration: "none" }}>
              Compare
            </a>
          </nav>
        </header>
        <main>{children}</main>
      </body>
    </html>
  );
}
