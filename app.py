from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
from gemini_chat import chat

app = Flask(__name__)
app.secret_key = "super-secret-key" 
app.config["SESSION_TYPE"] = "filesystem"  
Session(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/command", methods=["POST"])
def command():
    data = request.json
    user_input = data.get("command", "")

    if "jarvis_session" not in session:
        session["jarvis_session"] = {}

    response_text = chat(user_input, session["jarvis_session"])

    session.modified = True

    return jsonify({"response": response_text})

if __name__ == "__main__":
    app.run(debug=True)