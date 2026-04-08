"use client";

import { useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8080";

export default function Home() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSearch() {
    if (!query.trim()) return;
    setLoading(true);
    setResponse("");

    try {
      const res = await fetch(`${API_URL}/api/v1/chat/stream`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: query }),
      });

      const reader = res.body?.getReader();
      const decoder = new TextDecoder();

      if (reader) {
        let done = false;
        while (!done) {
          const result = await reader.read();
          done = result.done;
          if (result.value) {
            const chunk = decoder.decode(result.value);
            const lines = chunk
              .split("\n")
              .filter((line) => line.startsWith("data: "));

            for (const line of lines) {
              try {
                const data = JSON.parse(line.replace("data: ", ""));
                if (data.type === "token") {
                  setResponse((prev) => prev + data.content);
                }
              } catch {
                /* skip malformed SSE lines */
              }
            }
          }
        }
      }
    } catch {
      setResponse(
        "Could not connect to the API. Make sure the backend is running."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ maxWidth: "800px", margin: "0 auto", padding: "48px 24px" }}>
      <div style={{ textAlign: "center", marginBottom: "48px" }}>
        <h1
          style={{ fontSize: "36px", fontWeight: "bold", margin: "0 0 12px" }}
        >
          Find Your Perfect Bike
        </h1>
        <p style={{ color: "#6b7280", fontSize: "18px", margin: 0 }}>
          Tell me about yourself — height, budget, commute, riding style — and
          I&apos;ll recommend the perfect motorcycle.
        </p>
      </div>

      <div style={{ display: "flex", gap: "8px", marginBottom: "32px" }}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") handleSearch();
          }}
          placeholder="Try: 5'7, Bangalore commute 25km, budget 2.5L, weekend trips"
          style={{
            flex: 1,
            padding: "14px 16px",
            fontSize: "16px",
            border: "2px solid #e5e7eb",
            borderRadius: "12px",
            outline: "none",
          }}
        />
        <button
          onClick={handleSearch}
          disabled={loading}
          style={{
            padding: "14px 28px",
            fontSize: "16px",
            fontWeight: "600",
            background: loading ? "#9ca3af" : "#2563eb",
            color: "white",
            border: "none",
            borderRadius: "12px",
            cursor: loading ? "wait" : "pointer",
          }}
        >
          {loading ? "Thinking..." : "Ask RideShala"}
        </button>
      </div>

      {response && (
        <div
          style={{
            background: "#f9fafb",
            border: "1px solid #e5e7eb",
            borderRadius: "12px",
            padding: "24px",
            whiteSpace: "pre-wrap",
            lineHeight: "1.7",
            fontSize: "15px",
          }}
        >
          {response}
        </div>
      )}

      <footer
        style={{
          marginTop: "64px",
          paddingTop: "24px",
          borderTop: "1px solid #e5e7eb",
          textAlign: "center",
          color: "#9ca3af",
          fontSize: "13px",
        }}
      >
        <p>
          RideShala is open source (MIT). Every recommendation cites its source.
          No scraping. No tracking. No ads.
        </p>
      </footer>
    </div>
  );
}
