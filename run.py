from app import create_app

app = create_app()

if __name__  == "__main__":
    print(f"Starting Flask server with model: {app.config['MODEL_NAME']}")
    app.run(host="0.0.0.0", port=5000, debug=True)