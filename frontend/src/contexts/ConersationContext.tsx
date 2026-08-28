import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";

import type { Conversation } from "../types/conversation";
import { ConversationService } from "../services/conversation";

interface ConversationContextType {
  conversations: Conversation[];

  selectedConversation: Conversation | null;

  loading: boolean;

  refresh: () => Promise<void>;

  selectConversation: (conversation: Conversation | null) => void;

  createConversation: () => Promise<void>;

  updateConversation: (conversation: Conversation) => void;
}

const ConversationContext = createContext<ConversationContextType | null>(null);

interface Props {
  children: ReactNode;
}

export function ConversationProvider({ children }: Props) {
  const [conversations, setConversations] = useState<Conversation[]>([]);

  const [selectedConversation, setSelectedConversation] =
    useState<Conversation | null>(null);

  // Only represents the initial conversation fetch.
  const [loading, setLoading] = useState(true);

  const refresh = useCallback(async () => {
    try {
      const data = await ConversationService.getAll();

      setConversations(data);

      setSelectedConversation((current) => {
        // Keep the currently selected conversation.
        if (current) {
          const updatedConversation = data.find(
            (conversation) => conversation.id === current.id,
          );

          return updatedConversation ?? current;
        }

        // Select the first conversation only if
        // nothing is currently selected.
        if (data.length > 0) {
          return data[0];
        }

        return null;
      });
    } finally {
      // Loading only matters during the initial fetch.
      setLoading(false);
    }
  }, []);

  const createConversation = async () => {
    try {
      const conversation = await ConversationService.create();

      /*
       * Add the new conversation directly instead
       * of refetching the entire conversation list.
       */
      setConversations((previous) => [conversation, ...previous]);

      setSelectedConversation(conversation);
    } catch (error) {
      console.error(error);
    }
  };

  const updateConversation = (conversation: Conversation) => {
    setConversations((previous) =>
      previous.map((current) =>
        current.id === conversation.id ? conversation : current,
      ),
    );

    setSelectedConversation((current) =>
      current?.id === conversation.id ? conversation : current,
    );
  };

  const selectConversation = (conversation: Conversation | null) => {
    setSelectedConversation(conversation);
  };

  useEffect(() => {
    refresh();
  }, [refresh]);

  return (
    <ConversationContext.Provider
      value={{
        conversations,
        selectedConversation,
        loading,
        refresh,
        selectConversation,
        createConversation,
        updateConversation,
      }}
    >
      {children}
    </ConversationContext.Provider>
  );
}

export function useConversationContext() {
  const context = useContext(ConversationContext);

  if (!context) {
    throw new Error(
      "useConversationContext must be used inside ConversationProvider",
    );
  }

  return context;
}
