from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('LMQlr6KcrQ4dOOREzxK5FtG17zRyIihD7/6fFHyntHmRGRK4LADdyaorvr6r5aTkHLEWGayYWVIG1f+T1uw9lI/l5TXjG0WjzsbaMxYdpmEZMKgU6mqoflLlaej/PyVKuuNcb7v5WtrOl/gKzjYKAwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('50eaa1e2387f087c44b23eacadcd0f5e')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
