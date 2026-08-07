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
  streamChat(message: string): Promise<void>;
  clear: () => void;
}

const ChatContext = createContext<ChatContextType | null>(null);

interface Props {
  children: ReactNode;
}

export function ChatProvider({ children }: Props) {
  const { selectedConversation, updateConversation } = useConversation();

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
      const data = await ChatService.getMessages(selectedConversation.id);

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
    if (!selectedConversation) return;

    setLoading(true);

    try {
      const response = await ChatService.chat({
        conversation_id: selectedConversation.id,
        message: content,
      });
      updateConversation(response.conversation);
      setMessages((prev) => [...prev, ...response.messages]);
    } finally {
      setLoading(false);
    }
  };

  const streamChat = async (message: string) => {
    if (!selectedConversation) {
      throw new Error("No conversation selected.");
    }

    setLoading(true);
    setError(null);

    try {
      // 1. Append the user's message immediately
      const userMessage: ChatMessage = {
        id: "-1", // Temporary ID
        role: "user",
        content: message,
      };

      // 2. Append an empty assistant placeholder
      const assistantMessage: ChatMessage = {
        id: "-2", // Temporary ID
        role: "assistant",
        content: "",
      };

      setMessages((prev) => [...prev, userMessage, assistantMessage]);

      // 3. Start streaming
      for await (const event of ChatService.streamChat({
        conversation_id: selectedConversation.id,
        message,
      })) {
        switch (event.type) {
          case "token":
            setMessages((prev) => {
              const copy = [...prev];

              copy[copy.length - 1] = {
                ...copy[copy.length - 1],
                content: copy[copy.length - 1].content + event.content,
              };

              return copy;
            });
            break;

          case "done":
            console.log("Streaming complete", event);
            break;

          case "error":
            throw new Error(event.error);

          default:
            console.warn("Unknown stream event:", event);
        }
      }
    } catch (err) {
      console.error(err);
      setError("Failed to send message.");
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
        streamChat,
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
    throw new Error("useChatContext must be used inside ChatProvider");
  }

  return context;
}
