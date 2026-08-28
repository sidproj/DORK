import type { ChatMessage as ChatMessageType } from "../../types/chat";

import UserChatMessage from "./UserChatMessage";
import DorkChatMessage from "./DorkChatMessage";

interface Props {
  message: ChatMessageType;
}

const ChatMessage = ({ message }: Props) => {
  switch (message.role) {
    case "user":
      return <UserChatMessage message={message} />;
    default:
      return <DorkChatMessage message={message} />;
  }
};

export default ChatMessage;
