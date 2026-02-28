from flask import Blueprint, request,Response, stream_with_context
from app.services.llm_service import LLMService

chat_bp = Blueprint("chat",__name__)

@chat_bp.route("/chat",methods=['POST'])
def chat():
    data = request.json
    all_messages:list[str] = data.get('all_messages')
    
    if not all_messages:
        return {"error":"No message received"},500
    
    print(all_messages)
    
    try:
        
        def generate():
            for chunk in LLMService.generate_response(all_messages):
                yield f"data:{chunk}\n\n"
            yield "data:[DONE]\n\n"
        
        
        return Response(
            stream_with_context(generate()),
            content_type="text/event-stream"
        )
    except Exception as e:
        return {"error":str(e)},500