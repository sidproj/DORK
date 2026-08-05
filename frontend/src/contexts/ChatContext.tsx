import {
    createContext,
    useCallback,
    useContext,
    useEffect,
    useState,
    type ReactNode,
} from "react";
import type { ChatMessage } from "../types/chat";
import { useConversation } from "../hooks/useConversations";
import { ChatService } from "../services/chat";


interface ChatContextType {
    messages: ChatMessage[];
    loading: boolean;
    error: string | null;

    refresh: () => Promise<void>;
    chat: (content: string) => Promise<void>;
    clear: () => void;
}

const ChatContext = createContext<ChatContextType | null>(null);

interface Props {
    children: ReactNode;
}

export function ChatProvider({ children }: Props) {

    const { selectedConversation } = useConversation();

    const [messages, setMessages] = useState<ChatMessage[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    /**
     * Loads all messages for the selected conversation.
     */
    const refresh = useCallback(async () => {

        if (!selectedConversation) {
            setMessages([]);
            return;
        }

        setLoading(true);
        setError(null);

        try {

            const data = await ChatService.getMessages(
                selectedConversation.id
            );

            setMessages(data);

        } catch (err) {

            console.error(err);
            setError("Unable to load conversation.");

        } finally {

            setLoading(false);

        }

    }, [selectedConversation]);

    /**
     * Sends a new message.
     */
    const chat = async (content: string) => {

        if (!selectedConversation)
            return;

        setLoading(true);
        setError(null);

        try {

            await ChatService.chat({
                conversation_id: selectedConversation.id,
                message: content,
            });

            await refresh();

        } catch (err) {

            console.error(err);
            setError("Unable to send message.");

        } finally {

            setLoading(false);

        }

    };

    /**
     * Clears the local message list.
     */
    const clear = () => {

        setMessages([]);

    };

    /**
     * Automatically load messages whenever
     * the selected conversation changes.
     */
    useEffect(() => {

        refresh();

    }, [refresh]);

    return (

        <ChatContext.Provider
            value={{
                messages,
                loading,
                error,
                refresh,
                chat,
                clear,
            }}
        >
            {children}
        </ChatContext.Provider>

    );

}

export function useChatContext() {

    const context = useContext(ChatContext);

    if (!context) {

        throw new Error(
            "useChatContext must be used inside ChatProvider"
        );

    }

    return context;

}