// src/components/Chat.js
import React, { useState, useEffect, useRef } from "react";

const Chat = () => {
  const [messages, setMessages] = useState([{ sender: "bot", text: "Hi! Ask me anything." }]);
  const [input, setInput] = useState("");
  const socketRef = useRef(null);

  useEffect(() => {
    socketRef.current = new WebSocket(`wss://${window.location.host}/ws/chat/`);
    socketRef.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.message) {
        setMessages((prev) => [...prev, { sender: "bot", text: data.message }]);
      } else if (data.error) {
        setMessages((prev) => [...prev, { sender: "bot", text: `[Error]: ${data.error}` }]);
      }
    };
    return () => socketRef.current.close();
  }, []);

  const sendMessage = () => {
    if (input.trim()) {
      socketRef.current.send(JSON.stringify({ message: input }));
      setMessages((prev) => [...prev, { sender: "user", text: input }]);
      setInput("");
    }
  };

  return (
    <div style={{ padding: "2rem", maxWidth: "600px", margin: "auto" }}>
      <div style={{ border: "1px solid #ccc", padding: "1rem", height: "400px", overflowY: "auto" }}>
        {messages.map((msg, i) => (
          <div key={i} style={{ textAlign: msg.sender === "user" ? "right" : "left" }}>
            <p><strong>{msg.sender}:</strong> {msg.text}</p>
          </div>
        ))}
      </div>
      <div style={{ marginTop: "1rem", display: "flex" }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          style={{ flexGrow: 1, padding: "0.5rem" }}
        />
        <button onClick={sendMessage} style={{ marginLeft: "1rem" }}>Send</button>
      </div>
    </div>
  );
};

export default Chat;
