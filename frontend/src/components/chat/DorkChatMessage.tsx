import type { ChatMessage as ChatMessageType } from "../../types/chat";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeHighlight from "rehype-highlight";

import "highlight.js/styles/github-dark.css";

interface Props {
  message: ChatMessageType;
}

const DorkChatMessage = ({ message }: Props) => {
  const content = message.content;

  if (content.trim().length === 0) {
    return (
      <div className="flex justify-start mb-4">
        {" "}
        <i className="text-gray-400">--error--</i>{" "}
      </div>
    );
  }

  return (
    <div className="flex justify-start mb-4">
      <div className="max-w-[75%] rounded-xl bg-(--surface) text-(--text) border border-(--border) px-4 py-3 text-left ">
        <div className="prose prose-invert max-w-none">
          <ReactMarkdown
            children={content}
            remarkPlugins={[remarkGfm]}
            rehypePlugins={[rehypeHighlight]}
          />
        </div>
      </div>
    </div>
  );
};

export default DorkChatMessage;
