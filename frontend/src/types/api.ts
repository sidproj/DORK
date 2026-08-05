import type { ChatMessage } from "./chat";

export interface ChatRequest {
    message: string;
}

export interface ChatResponse {
    success: boolean;
    data: {
        message: ChatMessage;
    } | null;
    error: string | null;
}