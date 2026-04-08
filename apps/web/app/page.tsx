"use client";

import { useEffect, useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8080";

interface Bike {
  slug: string;
  name: string;
  brand: string;
  category: string;
  engine_cc: number;
  power_bhp: number;
  price_ex_showroom_inr: number;
  seat_height_mm: number;
  abs_type: string;
  image_url?: string;
}

export default function Home() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const [bikes, setBikes] = useState<Bike[]>([]);

  useEffect(() => {
    fetch(`${API_URL}/api/v1/specs?limit=9`)
      .then((res) => res.json())
      .then((data) => setBikes(data.bikes || []))
      .catch(() => setBikes([]));
  }, []);

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

  function formatPrice(price: number) {
    if (price >= 100000) return `₹${(price / 100000).toFixed(2)}L`;
    return `₹${price.toLocaleString("en-IN")}`;
  }

  return (
    <div style={{ maxWidth: "900px", margin: "0 auto", padding: "48px 24px" }}>
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

      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: "8px",
          justifyContent: "center",
          marginBottom: "16px",
        }}
      >
        {[
          { label: "Budget", icon: "💰", query: "Best bike under 2 lakh" },
          { label: "Height", icon: "📏", query: "Best bike for 5'5 short rider" },
          { label: "Mileage", icon: "⛽", query: "Most fuel efficient bike for daily commute" },
          { label: "Safety", icon: "🛡️", query: "Safest bike with dual ABS under 2.5L" },
          { label: "Comfort", icon: "🪑", query: "Most comfortable bike for long rides and back pain" },
          { label: "Power", icon: "⚡", query: "Most powerful bike under 3 lakh" },
          { label: "Compare", icon: "⚖️", query: "Compare Meteor 350 vs CB350 vs Hunter 350" },
          { label: "Cost", icon: "🧮", query: "Total 5 year ownership cost of Pulsar NS200 in Bangalore" },
          { label: "Beginner", icon: "🏁", query: "Best first bike for 18 year old beginner" },
          { label: "Ride Plan", icon: "🗺️", query: "Plan a ride from Bangalore to Coorg on Himalayan 450" },
          { label: "Insurance", icon: "📋", query: "Insurance cost for Royal Enfield Meteor 350 first year and renewal" },
          { label: "Maintenance", icon: "🔧", query: "Annual maintenance and service cost of Honda CB350" },
        ].map((chip) => (
          <button
            key={chip.label}
            onClick={() => {
              setQuery(chip.query);
              setResponse("");
            }}
            style={{
              padding: "6px 14px",
              fontSize: "13px",
              border: "1px solid #e5e7eb",
              borderRadius: "20px",
              background: "white",
              cursor: "pointer",
              display: "flex",
              alignItems: "center",
              gap: "4px",
              color: "#374151",
            }}
          >
            <span>{chip.icon}</span>
            <span>{chip.label}</span>
          </button>
        ))}
      </div>

      <div
        style={{
          background: "#f9fafb",
          borderRadius: "12px",
          padding: "16px 20px",
          marginBottom: "24px",
          fontSize: "13px",
          color: "#6b7280",
        }}
      >
        <strong style={{ color: "#374151" }}>Key parameters to consider before buying:</strong>{" "}
        Seat Height (matches your height) · Engine CC &amp; Power (performance) ·
        ABS Type (single vs dual channel for safety) · Mileage (claimed vs real-world) ·
        Weight (handling in city traffic) · Insurance Cost (1st year + renewal) ·
        Annual Service &amp; Maintenance Cost · Tyre &amp; Spare Parts Cost ·
        Riding Posture (commuter vs sport vs cruiser) ·
        Ground Clearance (speed bumps &amp; rough roads) · Fuel Tank (range per fill) ·
        Resale Value · RTO &amp; Registration Charges · EMI Options ·
        Total Cost of Ownership (5 year)
      </div>

      <div style={{ display: "flex", gap: "8px", marginBottom: "32px" }}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") handleSearch();
          }}
          placeholder="Ask anything — budget, height, city, riding style, compare bikes..."
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
            marginBottom: "48px",
          }}
        >
          {response}
        </div>
      )}

      {bikes.length > 0 && (
        <div>
          <h2
            style={{
              fontSize: "24px",
              fontWeight: "bold",
              marginBottom: "24px",
              textAlign: "center",
            }}
          >
            Popular Bikes
          </h2>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fill, minmax(260px, 1fr))",
              gap: "20px",
            }}
          >
            {bikes.map((bike) => (
              <div
                key={bike.slug}
                style={{
                  border: "1px solid #e5e7eb",
                  borderRadius: "12px",
                  overflow: "hidden",
                  background: "white",
                }}
              >
                <img
                  src={
                    bike.image_url ||
                    `https://placehold.co/600x400/333/white?text=${bike.brand}+${bike.name}`
                  }
                  alt={`${bike.brand} ${bike.name}`}
                  style={{
                    width: "100%",
                    height: "180px",
                    objectFit: "cover",
                  }}
                />
                <div style={{ padding: "16px" }}>
                  <div
                    style={{
                      fontSize: "11px",
                      color: "#6b7280",
                      textTransform: "uppercase",
                      letterSpacing: "0.5px",
                    }}
                  >
                    {bike.brand}
                  </div>
                  <div
                    style={{
                      fontSize: "18px",
                      fontWeight: "bold",
                      margin: "4px 0 8px",
                    }}
                  >
                    {bike.name}
                  </div>
                  <div
                    style={{
                      fontSize: "20px",
                      fontWeight: "bold",
                      color: "#2563eb",
                      marginBottom: "8px",
                    }}
                  >
                    {formatPrice(bike.price_ex_showroom_inr)}
                  </div>
                  <div
                    style={{
                      display: "flex",
                      flexWrap: "wrap",
                      gap: "6px",
                      fontSize: "12px",
                      color: "#6b7280",
                    }}
                  >
                    <span
                      style={{
                        background: "#f3f4f6",
                        padding: "2px 8px",
                        borderRadius: "4px",
                      }}
                    >
                      {bike.engine_cc}cc
                    </span>
                    <span
                      style={{
                        background: "#f3f4f6",
                        padding: "2px 8px",
                        borderRadius: "4px",
                      }}
                    >
                      {bike.power_bhp} bhp
                    </span>
                    <span
                      style={{
                        background: "#f3f4f6",
                        padding: "2px 8px",
                        borderRadius: "4px",
                      }}
                    >
                      {bike.seat_height_mm}mm seat
                    </span>
                    <span
                      style={{
                        background:
                          bike.abs_type === "dual_channel"
                            ? "#dcfce7"
                            : "#fef9c3",
                        color:
                          bike.abs_type === "dual_channel"
                            ? "#166534"
                            : "#854d0e",
                        padding: "2px 8px",
                        borderRadius: "4px",
                      }}
                    >
                      {bike.abs_type === "dual_channel"
                        ? "Dual ABS"
                        : bike.abs_type === "single_channel"
                          ? "Single ABS"
                          : "No ABS"}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
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
        <p style={{ fontSize: "11px", marginTop: "8px" }}>
          Insurance estimates use IRDAI published tariff rates. Service costs are
          community-reported averages. All financial figures are estimates for
          educational purposes only — not financial or insurance advice.
          Verify with your dealer and insurer before making decisions.
        </p>
      </footer>
    </div>
  );
}
