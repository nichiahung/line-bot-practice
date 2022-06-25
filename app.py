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

line_bot_api = LineBotApi('sE98AtZurPkXdm6q+/BgBE28s3Sx/q4BgTDoe0CBpLMVkiaJVIdXM+f0yVP5WBMW/SRDrk6aC2HWAhKm+bMa0W7OuYpwn/gpFlGklu2GzaXKPZ5BBgHrl5t5kYmnjAR8/GKpTej8jLQlRmWJ3Sp1eQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('077ff1c16f551f2343dfce4a7b512c0c')


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