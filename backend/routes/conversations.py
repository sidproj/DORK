from flask import Blueprint, jsonify

from repositories.conversation_repository import ConversationRepository
from services.conversation_service import ConversationService

conversation_bp = Blueprint("conversation", __name__)


@conversation_bp.route("/", methods=["GET"])
def get_conversations():

    conversations = ConversationRepository.get_all()

    return jsonify({
        "success": True,
        "data": [
            {
                "id": c.id,
                "title": c.title,
                "created_at": c.created_at,
                "updated_at": c.updated_at
            }
            for c in conversations
        ],
        "error": None
    })


@conversation_bp.route(
    "/<int:conversation_id>/messages",
    methods=["GET"]
)
def get_messages(conversation_id):

    try:

        messages = ConversationService.get_messages(
            conversation_id
        )

        return jsonify({

            "success": True,

            "data": [

                {
                    "id": message.id,
                    "conversation_id": message.conversation_id,
                    "role": message.role,
                    "content": message.content,
                    "created_at": message.created_at,
                }

                for message in messages

            ],

            "error": None,

        })

    except Exception as e:

        return jsonify({

            "success": False,
            "data": None,
            "error": str(e)

        }), 500
        

@conversation_bp.route(
    "",
    methods=["POST"]
)
def create_conversation():

    try:

        conversation = ConversationService.create()

        return jsonify({

            "success": True,

            "data": {

                "id": conversation.id,
                "title": conversation.title,
                "created_at": conversation.created_at,

            },

            "error": None

        }), 201

    except Exception as e:

        return jsonify({

            "success": False,
            "data": None,
            "error": str(e)

        }), 500