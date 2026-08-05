import type { ReactNode } from "react";
import { ConversationProvider } from "../contexts/ConersationContext";
import { ChatProvider } from "../contexts/ChatContext";

interface Props {
  children: ReactNode;
}

export default function AppProvider({ children }: Props) {
  return (
    <ConversationProvider>
      <ChatProvider>{children}</ChatProvider>
    </ConversationProvider>
  );
}
