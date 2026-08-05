import axios from "axios";
import type { Conversation } from "../types/conversation";

const API_URL = "http://localhost:5000/api";

export class ConversationService {
  static async getAll(): Promise<Conversation[]> {
    const response = await axios.get(`${API_URL}/conversations`);

    return response.data.data;
  }

  static async create() {
    const response = await axios.post(`${API_URL}/conversations`);

    return response.data.data;
  }
}
