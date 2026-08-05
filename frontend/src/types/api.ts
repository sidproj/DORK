import type { ChatMessage } from "./chat";

export interface ChatRequest {
    messages: ChatMessage[];
}

export interface ChatResponse {
    success: boolean;
    data: {
        message: ChatMessage;
    } | null;
    error: string | null;
}