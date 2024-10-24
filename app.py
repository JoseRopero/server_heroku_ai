import os
from flask import Flask, request, jsonify
import openai
from flask_cors import CORS
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)  # Permitir solicitudes desde cualquier origen

load_dotenv()

# Tenemos que configurar la API Key de forma segura
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/chatbot-response', methods=['POST'])
def chatbot_response():
    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"response": "Por favor, proporciona un mensaje válido."}), 400

    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=user_message,
            max_tokens=150,
            temperature=0.7
        )
        bot_response = response.choices[0].text.strip()
        return jsonify({"response": bot_response}), 500
    except Exception as e:
        return jsonify({"response": "Error al procesar tu solicitud"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
