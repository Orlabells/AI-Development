from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
from gemini_chat import chat

app = Flask(__name__)
app.secret_key = "super-secret-key"  # Keep this secret in production
app.config["SESSION_TYPE"] = "filesystem"  # Stores session on disk
Session(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/command", methods=["POST"])
def command():
    data = request.json
    user_input = data.get("command", "")

    # Initialize per-user session
    if "jarvis_session" not in session:
        session["jarvis_session"] = {}

    # Call chat with session data
    response_text = chat(user_input, session["jarvis_session"])

    # Mark session as modified to save history
    session.modified = True

    return jsonify({"response": response_text})

if __name__ == "__main__":
    app.run(debug=True)