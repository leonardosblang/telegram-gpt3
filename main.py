from flask import Flask
from flask import request
from flask import Response
import requests
import openai
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--model', required=True, help='Name of the model to use')
args = parser.parse_args()

# Add your models here then run python --model your_model_name
models = {
    'text-davinci-003': Davinci(),
    'text-embedding-ada-002': Ada()   
}


model_picked = models[args.model_name]



TOKEN = "your_bot_token"

app = Flask(__name__)


def parse_message(message):
    print("message-->", message)
    chat_id = message['message']['chat']['id']
    txt = message['message']['text']
    print("chat_id-->", chat_id)
    print("txt-->", txt)
    return chat_id, txt


def tel_send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }

    r = requests.post(url, json=payload)
    return r


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        openai.api_key = "your_openai_api_key"

        msg = request.get_json()

        chat_id, txt = parse_message(msg)

        r = openai.Completion.create(
            model=model_picked,
            prompt=txt,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        r = r['choices'][0]['text'].replace('\\n', ' ')
        tel_send_message(chat_id, r)

        return Response('ok', status=200)
    else:
        return "<h1>Welcome!</h1>"


if __name__ == '__main__':
    app.run(debug=True)
