from flask import Flask, request

from chat_model import ChatModel
from config import HF_ACCESS_TOKEN, PORT

app = Flask(__name__)

llama_model = ChatModel(access_token=HF_ACCESS_TOKEN)


@app.route('/api', methods=['POST'])
def generate():
    data = request.get_json()

    system_prompt = data.get('system', '').strip()
    user_prompt = data.get('user', '').strip()

    if not system_prompt or not user_prompt:
        return "Bad request", 400

    try:
        response = llama_model.generate_response(system_prompt, user_prompt)
        return response, 200
    except Exception as e:
        return str(e), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
