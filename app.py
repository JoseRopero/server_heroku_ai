import os
from flask import Flask, request, jsonify
import openai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permitir solicitudes desde cualquier origen

@app.route('/chatbot-response', methods=['POST'])
def chatbot_response():
    user_message = request.json.get("message")
    auth_header = request.headers.get("Authorization")

    if not user_message:
        return jsonify({"response": "Por favor, proporciona un mensaje válido."}), 400

    if not auth_header:
        return jsonify({'response': 'API Key de OpenAI no proporcionada'})

    try:
        # Extraer la API Key del header Authorization
        if not auth_header.startswith("Bearer "):
            return jsonify({'response': 'Formato de autenticación inválido'}), 401

        api_key = auth_header.split(' ')[1]

        # Configurar la API Key para OpenAI
        openai.api_key = api_key

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=user_message,
            max_tokens=150,
            temperature=0.7
        )
        bot_response = response.choices[0].text.strip()
        return jsonify({"response": bot_response})
    except Exception as e:
        return jsonify({"response": "Error al procesar tu solicitud"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
