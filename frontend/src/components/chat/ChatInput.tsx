import { useState } from "react";
import { useChat } from "../../hooks/userChat";

export default function ChatInput() {
  const [input, setInput] = useState("");

  const { chat, loading,streamChat } = useChat();

  const handleSend = async () => {
    const text = input.trim();

    if (!text) return;

    await streamChat(text);

    setInput("");
  };

  return (
    <div className="flex gap-2 p-4 border-t border-gray-700">
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();

            handleSend();
          }
        }}
        className="flex-1 rounded-md bg-zinc-800 px-4 py-2"
        placeholder="Message DORK..."
      />

      <button
        onClick={handleSend}
        disabled={loading}
        className={`rounded bg-blue-600 px-4 ${input.length > 0 && !loading ? "text-white" : "text-[#9CA3AF]"}`}
      >
        Send
      </button>
    </div>
  );
}
