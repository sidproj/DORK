from flask import Blueprint, jsonify, request

from services.llm import LLMService
from services.prompt_manager import  PromptManager

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/chat", methods=["POST"])
def chat():

    try:
        body = request.get_json()

        if body is None:
            return jsonify({
                "success": False,
                "data": None,
                "error": "Request body is missing."
            }), 400

        messages = body.get("messages")

        if not messages:
            return jsonify({
                "success": False,
                "data": None,
                "error": "Messages are required."
            }), 400

        messages = PromptManager.build(messages)
        
        assistant_message = LLMService.chat(messages)

        return jsonify({
            "success": True,
            "data": {
                "message": assistant_message
            },
            "error": None
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "data": None,
            "error": str(e)
        }), 500