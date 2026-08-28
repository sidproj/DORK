import type { ChatMessage as ChatMessageType } from "../../types/chat";

interface Props {
  message: ChatMessageType;
}

const UserChatMessage = ({ message }: Props) => {
  return (
    <div className="flex justify-end mb-4">
      <div className="max-w-[75%] rounded-xl bg-(--text) text-(--bg) border border-transparent px-4 py-3 whitespace-pre-wrap text-left">
        {message.content}
      </div>
    </div>
  );
};

export default UserChatMessage;
