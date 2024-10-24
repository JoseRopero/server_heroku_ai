import os
from crypt import methods

from flask import Flask, request, jsonify
import openai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permitir solicitudes desde cualquier origen

# Tenemos que configurar la API Key de forma segura
openai.api_key = "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"

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
