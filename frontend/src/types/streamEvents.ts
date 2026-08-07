import type { ChatMessage } from "./chat";
import type { Conversation } from "./conversation";

export type StreamEvent =
    | { type: "token"; content: string }
    | { type: "title"; conversation: Conversation }
    | { type: "done"; message: ChatMessage }
    | { type: "error"; error: string };