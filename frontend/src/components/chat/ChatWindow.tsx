import type { ChatMessage } from "../../types/chat";
import ChatMessageComponent from "./ChatMessage";

interface Props {
    messages: ChatMessage[];
}

const ChatWindow = ({ messages }: Props) => {
    return (
        <div className="flex-1 h-[72%] overflow-y-auto p-6">
            {messages.map((message, index) => (
                <ChatMessageComponent
                    key={index}
                    message={message}
                />
            ))}
        </div>
    );
};

export default ChatWindow;