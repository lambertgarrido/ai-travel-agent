"use client";

import { useState } from "react";

export default function Home() {
  const [response, setResponse] = useState("");
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

  if (response.type === "places") {
    return (
      <div>
        {response.data.map((p, i) => (
          <div key={i}>
          📍 {p.name}
        </div>
      ))}
      </div>
    );
  }

  return (
    <div style={{ padding: 20 }}>
      <h1>AI Travel Agent</h1>

      <input
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Plan my trip..."
      />

      <button onClick={sendMessage}>Send</button>

      <pre>{response}</pre>
    </div>
  );
}