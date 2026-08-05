from flask import Flask
from flask_cors import CORS
from database.init_db import initialize_database

from routes.chat import chat_bp
from routes.conversations import conversation_bp

app = Flask(__name__)

CORS(app)

app.register_blueprint(chat_bp)
app.register_blueprint(
    conversation_bp,
    url_prefix="/api/conversations"
)

if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)