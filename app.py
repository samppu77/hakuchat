
import os
import uuid
from threading import Lock

from flask import Flask, jsonify, render_template, request, session

from chat_core import chat

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or os.urandom(32)

# Istuntokohtainen keskusteluhistoria palvelimen muistissa.
sessions = {}
session_lock = Lock()


def get_session_id():
    """Luo selainistunnolle oman tunnisteen."""
    if "sid" not in session:
        session["sid"] = str(uuid.uuid4())
    return session["sid"]


@app.get("/")
def index():
    """Näyttää chatin verkkosivun."""
    return render_template("index.html")


@app.post("/api/chat")
def api_chat():
    """Vastaanottaa käyttäjän viestin ja palauttaa vastauksen."""
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Virheellinen JSON-pyyntö"}), 400

    message = data.get("message")

    if not isinstance(message, str) or not message.strip():
        return jsonify({"error": "Kirjoita viesti"}), 400

    message = message.strip()

    if len(message) > 2000:
        return jsonify({"error": "Viesti on liian pitkä"}), 400

    sid = get_session_id()

    with session_lock:
        history = [item.copy() for item in sessions.get(sid, [])]

    history.append({"role": "user", "content": message})

    # Testitilassa ei tehdä OpenRouter-kutsuja.
    if os.environ.get("MOCK_MODE") == "1":
        answer = f"Testivastaus viestiisi: {message}"
        history.append({"role": "assistant", "content": answer})
        searches = []
    else:
        try:
            answer, history, searches = chat(history)
        except Exception:
            return jsonify({
                "error": "Kielimallin käsittely epäonnistui"
            }), 502

    with session_lock:
        sessions[sid] = history

    return jsonify({
        "response": answer,
        "searches": searches
    })


@app.get("/api/history")
def api_history():
    """Palauttaa nykyisen selainistunnon viestit."""
    sid = get_session_id()

    with session_lock:
        history = sessions.get(sid, [])

        messages = [
            {"role": item["role"], "content": item["content"]}
            for item in history
            if item.get("role") in ("user", "assistant")
            and isinstance(item.get("content"), str)
        ]

    return jsonify({"messages": messages})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
