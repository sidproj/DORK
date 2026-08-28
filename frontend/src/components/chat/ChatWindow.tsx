import { useEffect, useRef } from "react";
import { useChat } from "../../hooks/userChat";
import ChatMessage from "./ChatMessage";

export default function ChatWindow() {
  const { messages, loading } = useChat();
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView();
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  return (
    <div className="m-4 h-[84%] overflow-auto">
      {messages.map((message) => (
        <ChatMessage key={message.id} message={message}/>
      ))}
      {
        loading &&
        <div>Loading...</div>
      }
      {/* Invisible element used as a scroll target */}
      <div ref={messagesEndRef} />  
    </div>
  );
}
