# flask_server.py
from flask import Flask  # Flask web framework

app = Flask(__name__)  # Create Flask app instance

@app.route("/ask")  # 🧠 Flask registers this function for GET /ask route
def ask():
    return "Hello from Flask!"  # Auto-wrapped in HTTP response by Flask

if __name__ == "__main__":
    app.run(port=8000)  # Start Flask dev server
