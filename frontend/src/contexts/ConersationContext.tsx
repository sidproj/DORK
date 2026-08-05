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
}

const ConversationContext = createContext<ConversationContextType | null>(null);

interface Props {
  children: ReactNode;
}

export function ConversationProvider({ children }: Props) {
  const [conversations, setConversations] = useState<Conversation[]>([]);

  const [selectedConversation, setSelectedConversation] =
    useState<Conversation | null>(null);

  const [loading, setLoading] = useState(false);

  const refresh = useCallback(async () => {
    setLoading(true);

    try {
      const data = await ConversationService.getAll();

      setConversations(data);

      if (!selectedConversation && data.length > 0) {
        setSelectedConversation(data[0]);
      }
    } finally {
      setLoading(false);
    }
  }, [selectedConversation]);

  const createConversation = async () => {
    try {
      const conversation = await ConversationService.create();

      await refresh();

      selectConversation(conversation);
    } catch (e) {
      console.error(e);
    }
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
