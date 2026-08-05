import type { ChatMessage as ChatMessageType } from "../../types/chat";

interface Props {
    message: ChatMessageType;
}

const ChatMessage = ({ message }: Props) => {
    const isUser = message.role === "user";

    return (
        <div
            className={`flex mb-4 ${
                isUser ? "justify-end" : "justify-start"
            }`}
        >
            <div
                className={`max-w-[75%] rounded-xl px-4 py-3 whitespace-pre-wrap text-left ${
                    isUser
                        ? "bg-blue-600 text-white"
                        : "bg-gray-700 text-white"
                }`}
            >
                {message.content}
            </div>
        </div>
    );
};

export default ChatMessage;