import { useChat } from "../../hooks/userChat";
import ChatMessage from "./ChatMessage";

export default function ChatWindow() {
  const { messages, loading } = useChat();

  return (
    <div className="m-4 h-[85%] overflow-auto">
      {messages.map((message) => (
        <ChatMessage key={message.id} message={message}/>
      ))}
      {
        loading &&
        <div>Loading...</div>
      }
    </div>
  );
}
