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

  const [messagesByConversation, setMessagesByConversation] = useState<
    Record<number, ChatMessage[]>
  >({});

  const [loadingByConversation, setLoadingByConversation] = useState<
    Record<number, boolean>
  >({});

  const [error, setError] = useState<string | null>(null);

  /*
   * Messages visible in the UI.
   *
   * This is derived from selectedConversation.
   * It is NOT a separate state variable.
   */
  const messages = selectedConversation
    ? (messagesByConversation[selectedConversation.id] ?? [])
    : [];

  const loading = selectedConversation
    ? (loadingByConversation[selectedConversation.id] ?? false)
    : false;

  /**
   * Loads all messages for the selected conversation.
   */
  const refresh = useCallback(async () => {
    if (!selectedConversation) {
      return;
    }

    const conversationId = selectedConversation.id;

    setError(null);

    try {
      const data = await ChatService.getMessages(conversationId);

      setMessagesByConversation((prev) => ({
        ...prev,
        [conversationId]: data,
      }));
    } catch (err) {
      console.error(err);
      setError("Unable to load conversation.");
    }
  }, [selectedConversation]);

  /**
   * Sends a new message.
   */
  const chat = async (content: string) => {
    if (!selectedConversation) return;

    const conversationId = selectedConversation.id;

    setLoadingByConversation((prev) => ({
      ...prev,
      [conversationId]: true,
    }));

    setError(null);

    try {
      const response = await ChatService.chat({
        conversation_id: conversationId,
        message: content,
      });

      updateConversation(response.conversation);

      setMessagesByConversation((prev) => ({
        ...prev,
        [conversationId]: [
          ...(prev[conversationId] ?? []),
          ...response.messages,
        ],
      }));
    } catch (err) {
      console.error(err);
      setError("Failed to send message.");
    } finally {
      setLoadingByConversation((prev) => ({
        ...prev,
        [conversationId]: false,
      }));
    }
  };

  const streamChat = async (message: string) => {
    if (!selectedConversation) {
      throw new Error("No conversation selected.");
    }

    /*
     * Capture this immediately.
     *
     * DO NOT use selectedConversation.id inside the
     * streaming loop later.
     */
    const conversationId = selectedConversation.id;

    setLoadingByConversation((prev) => ({
      ...prev,
      [conversationId]: true,
    }));

    setError(null);

    try {
      /*
       * Temporary user message.
       */
      const userMessage: ChatMessage = {
        id: `temp-user-${Date.now()}`,
        role: "user",
        content: message,
      };

      /*
       * Temporary assistant message.
       */
      const assistantMessage: ChatMessage = {
        id: `temp-assistant-${Date.now()}`,
        role: "assistant",
        content: "",
      };

      /*
       * Add both messages ONLY to this conversation.
       */
      setMessagesByConversation((prev) => ({
        ...prev,
        [conversationId]: [
          ...(prev[conversationId] ?? []),
          userMessage,
          assistantMessage,
        ],
      }));

      /*
       * Start streaming.
       *
       * The request is now associated with conversationId,
       * not with the currently selected conversation.
       */
      for await (const event of ChatService.streamChat({
        conversation_id: conversationId,
        message,
      })) {
        switch (event.type) {
          case "token":
            setMessagesByConversation((prev) => {
              const conversationMessages = prev[conversationId] ?? [];

              if (conversationMessages.length === 0) {
                return prev;
              }

              const updatedMessages = [...conversationMessages];

              const lastIndex = updatedMessages.length - 1;

              const lastMessage = updatedMessages[lastIndex];

              updatedMessages[lastIndex] = {
                ...lastMessage,
                content: lastMessage.content + event.content,
              };

              return {
                ...prev,
                [conversationId]: updatedMessages,
              };
            });

            break;

          case "title":
            /*
             * Handle this when your backend starts emitting
             * title events.
             */

            if (event.conversation) {
              updateConversation(event.conversation);
            }

            break;

          case "done":
            /*
             * Eventually use the persisted assistant message
             * returned by the backend to replace the temporary
             * assistant message.
             */
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

      /*
       * Don't allow an error in conversation A to affect
       * another conversation.
       */
      setError("Failed to send message.");
    } finally {
      /*
       * IMPORTANT:
       *
       * Stop loading ONLY for the conversation that
       * started this request.
       */
      setLoadingByConversation((prev) => ({
        ...prev,
        [conversationId]: false,
      }));
    }
  };

  /**
   * Clears the local message list.
   */
  const clear = () => {
    if (!selectedConversation) {
      return;
    }

    const conversationId = selectedConversation.id;

    setMessagesByConversation((prev) => ({
      ...prev,
      [conversationId]: [],
    }));
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
