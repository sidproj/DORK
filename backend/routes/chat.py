from flask import Blueprint, jsonify, request, Response, stream_with_context

from services.conversation_service import ConversationService
from services.sse_event import sse_event

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
                "conversation": {
                    "id":result["conversation"].id,
                    "title":result["conversation"].title,
                    "created_at":result["conversation"].created_at,
                    "updated_at":result["conversation"].updated_at
                },
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
        
@chat_bp.route("/api/chat/stream", methods=["POST"])
def chat_stream():
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

        def event_stream():
            for event in ConversationService.stream_chat(
                conversation_id=conversation_id,
                user_message=message
            ):
                yield sse_event(event['type'],event)
            
        return Response(
            stream_with_context(event_stream()),
            mimetype="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",  # Helpful when behind nginx
            },
        )
    except Exception as e:

        print(e)

        return jsonify({
            "success": False,
            "data": None,
            "error": str(e)
        }), 500