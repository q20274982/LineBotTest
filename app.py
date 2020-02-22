from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('gwZkquxNnooVwM7t+gh8FnGgnhnNiRVq6v1FeoY8LCPne/UvCz3WodFhELMappsoTVLOa33uD5ejCKmYO25ApZAoVnSnZSTLd6L7ziPvDhTHEgsLgONRccH1dhaCHmTOUKQ9XNucv0/s78cYLr3IIQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('c8779b1b244afb5b577e124c45455201')

user_id = 'Uf000dc867286bb42ed2e3ccb273df289'


@app.route("/push_function/<string:push_text_str>")
def push_message(push_text_str):
    line_bot_api.push_message(user_id, TextSendMessage(text=push_text_str))


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)


@app.route('/')
def index():
    return 'Hello vectoria'


import os

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
