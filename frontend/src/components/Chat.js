import React, { useState, useEffect, useRef } from "react";

const Chat = () => {
  const [messages, setMessages] = useState([
    { sender: "bot", text: "Hi! Ask me anything." },
  ]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const socketRef = useRef(null);

  useEffect(() => {
    const token = localStorage.getItem("token");
    const protocol = window.location.protocol === "https:" ? "wss" : "ws";
    const host = window.location.host;
    socketRef.current = new WebSocket(`${protocol}://${host}/ws/chat/?token=${token}`);

    let streamingBuffer = "";

    socketRef.current.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.typing) {
        setIsTyping(true);
        return;
      }

      if (data.partial) {
        // Display incoming message progressively
        streamingBuffer += data.partial;
        setMessages((prev) => {
          const updated = [...prev];
          if (updated[updated.length - 1]?.sender === "bot" && !updated[updated.length - 1]?.final) {
            updated[updated.length - 1].text = streamingBuffer;
          } else {
            updated.push({ sender: "bot", text: streamingBuffer });
          }
          return updated;
        });
        return;
      }

      if (data.message) {
        setIsTyping(false);
        setMessages((prev) => [...prev, { sender: "bot", text: data.message, final: true }]);
        streamingBuffer = "";
      }

      if (data.done) {
        setIsTyping(false);
        streamingBuffer = "";
      }

      if (data.error) {
        setIsTyping(false);
        setMessages((prev) => [
          ...prev,
          { sender: "bot", text: `[Error]: ${data.error}` },
        ]);
      }
    };

    return () => socketRef.current.close();
  }, []);

  const sendMessage = () => {
    if (input.trim()) {
      socketRef.current.send(JSON.stringify({ message: input }));
      setMessages((prev) => [...prev, { sender: "user", text: input }]);
      setInput("");
      setIsTyping(true);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-box">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.sender === "user" ? "user" : "bot"}`}>
            <p><strong>{msg.sender}:</strong> {msg.text}</p>
          </div>
        ))}
        {isTyping && (
          <div className="message bot">
            <p><em>Bot is typing...</em></p>
          </div>
        )}
      </div>

      <div className="input-area">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          placeholder="Type your message..."
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
};

export default Chat;
