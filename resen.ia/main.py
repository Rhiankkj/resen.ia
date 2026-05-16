import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from core.prompt_mestre import PromptMestre
from services.ai_service import IAService

# inicialização do app e dos serviços

app = Flask(
    __name__,
    static_folder="frontend",
    static_url_path=""
)
CORS(app)

prompt_service = PromptMestre()
ia_service = IAService()


# rota principal - serve o HTML

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


# rota do chat

@app.route("/chat", methods=["POST"])
def chat():
    dados = request.get_json()

    if not dados:
        return jsonify({"error": "Nenhum dado recebido."}), 400

    mensagem_usuario = dados.get("mensagem", "").strip()
    historico = dados.get("historico", [])

    if not mensagem_usuario:
        return jsonify({"error": "A mensagem não pode ficar vazia."}), 400

    historico.append({
        "role": "user",
        "content": mensagem_usuario
    })

    try:
        system_prompt = prompt_service.get_prompt()
        resposta_ia = ia_service.enviar_mensagem(historico, system_prompt)  # corrigido: enviar_mensagem
        return jsonify({"resposta": resposta_ia})

    except Exception as e:
        print(f"[ERRO] {e}")
        return jsonify({"erro": str(e)}), 500


@app.route("/status")
def status():
    return jsonify({"status": "online", "bot": "resen.IA"})


if __name__ == "__main__":
    print("=" * 55)
    print("    Resen.IA Preparado para resenhar 😎😎😎")
    print("    Acesse: http://localhost:5000")
    print("    Acesse: http://localhost:5000/chat")
    print("    Acesse: http://localhost:5000/status")
    print("=" * 55)

    app.run(debug=True, port=5000)
