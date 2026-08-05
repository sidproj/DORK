import axios from "axios";
import type { ChatMessage } from "../types/chat";

const API_URL = "http://localhost:5000/api";

export interface ChatRequest {
    conversation_id: number | null;
    message: string;
}

export interface ChatResponse {
    conversation_id: number;
    message: ChatMessage;
}

export class ChatService {

    static async getMessages(
        conversationId: number
    ): Promise<ChatMessage[]> {

        const response = await axios.get(
            `${API_URL}/conversations/${conversationId}/messages`
        );

        return response.data.data;
    }

    static async chat(
        body: ChatRequest
    ): Promise<ChatResponse> {

        const response = await axios.post(
            `${API_URL}/chat`,
            body
        );

        return response.data.data;
    }

}