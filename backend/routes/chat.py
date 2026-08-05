from flask import Blueprint, jsonify, request

from services.conversation_service import ConversationService

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/api/chat", methods=["POST"])
def chat():

    body = request.get_json(silent=True) or {}

    conversation_id = body.get("conversation_id")
    message = body.get("message")

    if not message or not isinstance(message, str):
        return jsonify({
            "success": False,
            "data": None,
            "error": "Message is required."
        }), 400

    try:

        result = ConversationService.chat(
            conversation_id=conversation_id,
            user_message=message
        )

        return jsonify({
            "success": True,
            "data": {
                "conversation_id": result["conversation_id"],
                "messages": [

                    {
                        "id": m.id,
                        "conversation_id": m.conversation_id,
                        "role": m.role,
                        "content": m.content,
                        "created_at": m.created_at,
                    }
                    for m in result["messages"]
                ],
            },
            "error": None
        })

    except Exception as e:

        print(e)

        return jsonify({
            "success": False,
            "data": None,
            "error": str(e)
        }), 500