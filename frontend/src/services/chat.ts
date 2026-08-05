import api from "./api";
import type { ChatRequest, ChatResponse } from "../types/api";

export const sendMessage = async (
    request: ChatRequest
): Promise<ChatResponse> => {
    const response = await api.post<ChatResponse>(
        "/chat",
        request
    );

    return response.data;
};