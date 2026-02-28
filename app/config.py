import os

class Config:
    MODEL_NAME = os.getenv("MODEL_NAME","llama3:8b")