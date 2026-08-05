import { useState } from "react";

import type { ChatMessage } from "../types/chat";
import { sendMessage } from "../services/chat";

export const useChat = () => {
    const [messages, setMessages] = useState<ChatMessage[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const send = async (content: string) => {
        if (!content.trim()) return;

        const userMessage: ChatMessage = {
            role: "user",
            content,
        };

        const updatedMessages = [...messages, userMessage];

        setMessages(updatedMessages);
        setLoading(true);
        setError(null);

        try {
            const response = await sendMessage({
                messages: updatedMessages,
            });

            if (!response.success || !response.data) {
                throw new Error(response.error ?? "Unknown error");
            }

            setMessages([
                ...updatedMessages,
                response.data.message,
            ]);
        } catch (err) {
            setError(
                err instanceof Error
                    ? err.message
                    : "Something went wrong."
            );
        } finally {
            setLoading(false);
        }
    };

    return {
        messages,
        loading,
        error,
        send,
    };
};