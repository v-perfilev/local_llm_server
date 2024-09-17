import logging
import re

from flask import Flask, request

from chat_model import ChatModel
from config import HF_ACCESS_TOKEN, PORT

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

llama_model = ChatModel(access_token=HF_ACCESS_TOKEN)


def extract_json(response):
    json_match = re.search(r'\{.*\}', response, re.DOTALL)
    if json_match:
        return json_match.group()


@app.route('/api', methods=['POST'])
def generate():
    data = request.get_json()

    system_prompt = data.get('system', '').strip()
    user_prompt = data.get('user', '').strip()
    json = data.get('json', '')
    if isinstance(json, str):
        json = json.strip()
    json = bool(json)

    app.logger.info(' System prompt: %s', system_prompt)
    app.logger.info(' User prompt: %s', user_prompt)
    app.logger.info(' Should be in JSON: %s', json)

    if not system_prompt or not user_prompt or not json:
        return "Bad request", 400

    try:
        response = llama_model.generate_response(system_prompt, user_prompt)

        if json:
            app.logger.info(' Response before JSON extraction: %s', response)
            response = extract_json(response)

        app.logger.info(' Response: %s', response)
        return response, 200
    except Exception as e:
        app.logger.error(' Error: %s', str(e))
        return str(e), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
