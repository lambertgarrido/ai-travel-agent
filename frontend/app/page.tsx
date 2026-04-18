"use client";

import { useState } from "react";

export default function Home() {

  type ApiResponse =
  | { type: "places"; data: any[] }
  | { type: "flights"; data: any[] }
  | { type: "text"; data: string };

  const [response, setResponse] = useState<ApiResponse | null>(null);
  const [message, setMessage] = useState("");

  const sendMessage = async () => {
    const res = await fetch(
      process.env.NEXT_PUBLIC_BACKEND_URL + "/chat",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: message,
          user_id: "user123",
        }),
      }
    );

    const data = await res.json();
    setResponse(data.response);
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>AI Travel Agent</h1>

      {/* INPUT ALWAYS VISIBLE */}
      <input
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Plan my trip..."
      />

      <button onClick={sendMessage}>Send</button>

      <hr />

      {/* RESPONSE AREA */}
      {!response && <p>Ask something to start...</p>}

      {response?.type === "flights" && (
        <div>
          {response.data.map((f: any, i: number) => (
            <div key={i}>
              ✈️ {f.from} → {f.to} <br />
              💰 {f.price} <br />
              ⏱ {f.duration} mins
            </div>
          ))}
        </div>
      )}

      {response?.type === "places" && (
        <div>
          {response.data.map((p: any, i: number) => (
            <div key={i}>📍 {p.name}</div>
          ))}
        </div>
      )}

      {response?.type === "text" && (
        <div>{response.data}</div>
      )}

    </div>
  );
}