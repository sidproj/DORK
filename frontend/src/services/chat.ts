import axios from "axios";
import type { ChatMessage } from "../types/chat";
import type { Conversation } from "../types/conversation";
import type { StreamEvent } from "../types/streamEvents";

const API_URL = "http://localhost:5000/api";

export interface ChatRequest {
  conversation_id: number | null;
  message: string;
}

export interface ChatResponse {
  conversation: Conversation;
  messages: ChatMessage[];
}

export class ChatService {
  static async getMessages(conversationId: number): Promise<ChatMessage[]> {
    const response = await axios.get(
      `${API_URL}/conversations/${conversationId}/messages`,
    );

    return response.data.data;
  }

  static async chat(body: ChatRequest): Promise<ChatResponse> {
    const response = await axios.post(`${API_URL}/chat`, body);

    return response.data.data;
  }

  static async *streamChat(
    body: ChatRequest,
  ): AsyncGenerator<StreamEvent, void, unknown> {
    const response = await fetch(`${API_URL}/chat/stream`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        conversation_id: body.conversation_id,
        message: body.message,
      }),
    });

    if (!response.ok) {
      throw new Error(`Request failed with status ${response.status}`);
    }

    if (!response.body) {
      throw new Error("Response body is null.");
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();

    let buffer = "";
    try {
      while (true) {
        const { done, value } = await reader.read();

        if (done) {
          break;
        }

        buffer += decoder.decode(value, { stream: true });

        const events = buffer.split("\n\n");

        // Keep incomplete event in the buffer
        buffer = events.pop() ?? "";

        for (const rawEvent of events) {
          const lines = rawEvent
            .split("\n")
            .filter((line) => line.startsWith("data:"));

          if (!lines.length) {
            continue;
          }

          const json = lines
            .map((line) => line.replace(/^data:\s*/, ""))
            .join("");

          try {
            const event = JSON.parse(json);
            yield event;
          } catch (err) {
            console.error("Failed to parse SSE event:", json, err);
          }
        }
      }

      // Flush any remaining buffered event
      if (buffer.trim()) {
        const lines = buffer
          .split("\n")
          .filter((line) => line.startsWith("data:"));

        if (lines.length) {
          try {
            const event = JSON.parse(
              lines.map((line) => line.replace(/^data:\s*/, "")).join(""),
            );
            yield event;
          } catch (err) {
            console.error("Failed to parse final SSE event:", err);
          }
        }
      }
    } finally {
      reader.releaseLock();
    }
  }
}
