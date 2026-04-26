import sys
import io
import contextlib
import traceback
from flask import Flask, jsonify, request
from flask_cors import CORS
from functools import lru_cache

RAGChatbot = None
RAG_IMPORT_ERROR = None

# Windows terminal encoding kaynakli UnicodeEncodeError hatalarini engeller.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
try:
    from rag_chatbot import RAGChatbot as _RAGChatbot

    RAGChatbot = _RAGChatbot
except Exception as import_exc:  # noqa: BLE001
    RAG_IMPORT_ERROR = str(import_exc)

app = Flask(__name__)
CORS(app)


@lru_cache(maxsize=1)
def get_chatbot() -> RAGChatbot:
    if RAGChatbot is None:
        raise RuntimeError(RAG_IMPORT_ERROR or "RAGChatbot import edilemedi")
    chatbot = RAGChatbot()
    # Alttaki moduller terminale Unicode karakterler basabildigi icin
    # stdout/stderr'i yutarak API'nin 500'e dusmesini engelleriz.
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        chatbot.initialize()
    return chatbot


@app.get("/health")
def health() -> tuple:
    return (
        jsonify(
            {
                "status": "ok",
                "rag_available": RAGChatbot is not None,
                "rag_import_error": RAG_IMPORT_ERROR,
            }
        ),
        200,
    )


@app.post("/api/chat")
def api_chat() -> tuple:
    payload = request.get_json(silent=True) or {}
    question = str(payload.get("question", "")).strip()
    if not question:
        return jsonify({"error": "Soru bos olamaz"}), 400

    if RAGChatbot is None:
        return (
            jsonify(
                {
                    "answer": "Demo modu aktif. RAG bagimliliklari eksik oldugu icin ornek yanit donuluyor.",
                    "sources": [],
                    "relevant_chunks": 0,
                    "found_in_docs": False,
                    "demo_mode": True,
                    "rag_import_error": RAG_IMPORT_ERROR,
                }
            ),
            200,
        )

    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            result = get_chatbot().ask(question)
        return jsonify(
            {
                "answer": result["answer"],
                "sources": result.get("sources", []),
                "relevant_chunks": result.get("relevant_chunks", 0),
                "found_in_docs": result.get("found_in_docs", False),
            }
        ), 200
    except Exception as exc:  # noqa: BLE001
        return (
            jsonify(
                {
                    "error": "Sistem hatasi",
                    "details": str(exc),
                    "traceback": traceback.format_exc(),
                }
            ),
            500,
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
