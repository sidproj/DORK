from flask import Flask
from app.config import Config
from app.routes.chat import chat_bp
from app.routes.home import home_bp

def create_app():
    app = Flask(__name__,template_folder="templates")
    app.config.from_object(Config)
    
    app.register_blueprint(chat_bp)
    app.register_blueprint(home_bp)
    
    return app