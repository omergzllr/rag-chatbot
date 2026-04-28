import sys
import io
import contextlib
import traceback
from flask import Flask, jsonify, request
from flask_cors import CORS
from functools import lru_cache
from citizen import CitizenFlowService

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
citizen_service = CitizenFlowService()


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


@app.post("/api/rag/initialize")
def initialize_rag() -> tuple:
    payload = request.get_json(silent=True) or {}
    force_reload = bool(payload.get("force_reload", False))
    if RAGChatbot is None:
        return jsonify({"error": "RAGChatbot import edilemedi", "details": RAG_IMPORT_ERROR}), 500
    try:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            ok = get_chatbot().initialize(force_reload=force_reload)
        return jsonify({"initialized": bool(ok), "force_reload": force_reload}), 200
    except Exception as exc:  # noqa: BLE001
        return jsonify({"error": "RAG initialize hatasi", "details": str(exc)}), 500


@app.get("/api/citizen/doc-types")
def citizen_doc_types() -> tuple:
    return jsonify({"items": citizen_service.list_document_types()}), 200


@app.post("/api/citizen/session/start")
def citizen_start_session() -> tuple:
    payload = request.get_json(silent=True) or {}
    doc_type = str(payload.get("doc_type", "")).strip()
    initial_prompt = str(payload.get("prompt", "")).strip()
    if not doc_type:
        return jsonify({"error": "doc_type gerekli"}), 400
    try:
        result = citizen_service.start_session(doc_type=doc_type, initial_prompt=initial_prompt)
        return jsonify(result), 200
    except Exception as exc:  # noqa: BLE001
        return jsonify({"error": str(exc)}), 400


@app.post("/api/citizen/session/<session_id>/message")
def citizen_send_message(session_id: str) -> tuple:
    payload = request.get_json(silent=True) or {}
    message = str(payload.get("message", "")).strip()
    if not message:
        return jsonify({"error": "message gerekli"}), 400
    try:
        result = citizen_service.submit_user_message(session_id=session_id, message=message)
        return jsonify(result), 200
    except Exception as exc:  # noqa: BLE001
        return jsonify({"error": str(exc)}), 400


@app.get("/api/citizen/session/<session_id>")
def citizen_get_session(session_id: str) -> tuple:
    try:
        result = citizen_service.get_session(session_id=session_id)
        return jsonify(result), 200
    except Exception as exc:  # noqa: BLE001
        return jsonify({"error": str(exc)}), 404


@app.post("/api/citizen/assist")
def citizen_assist() -> tuple:
    payload = request.get_json(silent=True) or {}
    narrative = str(payload.get("narrative", "")).strip()
    city = str(payload.get("city", "istanbul")).strip() or "istanbul"
    if not narrative:
        return jsonify({"error": "narrative gerekli"}), 400
    result = citizen_service.run_citizen_assist(narrative=narrative, city=city)
    return jsonify(result), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
