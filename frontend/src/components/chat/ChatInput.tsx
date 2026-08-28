import { useState } from "react";
import { useChat } from "../../hooks/userChat";

export default function ChatInput() {
  const [input, setInput] = useState("");

  const { loading, streamChat } = useChat();

  const handleSend = async () => {
    const text = input.trim();

    if (!text || loading) return;

    setInput("");
    await streamChat(text);
  };

  const canSend = input.trim().length > 0 && !loading;

  return (
    <div className="border-t border-(--border) bg-(--bg) px-4 py-4">
      <div
        className="
          flex
          items-center
          gap-3
          rounded-md
          border
          border-(--border)
          bg-(--surface)
          px-3
          py-2
          shadow-(--shadow-sm)
          transition-colors
          focus-within:border-(--blue)
        "
      >
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              handleSend();
            }
          }}
          disabled={loading}
          className="
            min-w-0
            flex-1
            bg-transparent
            px-2
            py-2
            text-sm
            text-(--text)
            outline-none
            placeholder:text-(--text-faint)
            disabled:cursor-not-allowed
            disabled:opacity-60
            "
          placeholder={loading ? "DORK is thinking..." : "Message DORK..."}
        />
        <button
          onClick={handleSend}
          disabled={!canSend}
          className="
        flex
        h-9
        shrink-0
        items-center
        justify-center
        rounded-md
        border
        px-4
        text-sm
        font-medium
        transition-all
        duration-150
        focus:outline-none
        focus-visible:ring-2
        focus-visible:ring-(--blue)
        disabled:cursor-not-allowed
        disabled:border-(--border)
        disabled:text-(--text-faint)
      "
        >
          {loading ? "..." : "Send"}
        </button>
      </div>
    </div>
  );
}
