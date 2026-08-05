import { useState } from "react";

interface Props {
    onSend: (message: string) => void;
    loading: boolean;
}

const ChatInput = ({ onSend, loading }: Props) => {
    const [message, setMessage] = useState("");

    const handleSend = () => {
        if (!message.trim()) return;

        onSend(message);
        setMessage("");
    };

    const handleKeyDown = (
        e: React.KeyboardEvent<HTMLTextAreaElement>
    ) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <div className="border-t border-gray-700 p-4">
            <textarea
                rows={3}
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Message DORK..."
                className="w-full rounded-lg border border-gray-600 bg-gray-800 p-3 text-white resize-none"
            />

            <div className="flex justify-end mt-3">
                <button
                    onClick={handleSend}
                    disabled={loading}
                    className="rounded-lg bg-blue-600 px-5 py-2 text-white hover:bg-blue-700 disabled:opacity-50"
                >
                    {loading ? "Thinking..." : "Send"}
                </button>
            </div>
        </div>
    );
};

export default ChatInput;