import os
from datetime import datetime

from flask import Flask, abort, request

# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from pymongo.mongo_client import MongoClient

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))
mongo_client = MongoClient(os.environ.get("MONGODB_URI"))


@app.route("/", methods=["GET", "POST"])
def callback():

    if request.method == "GET":
        return "Hello Heroku"
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return "OK"


usage = '''使用說明
<項目><空格><金額>
例如：早餐 100
也支援透過半形逗號分隔多筆
例如：早餐 100, 午餐 200
'''

def proc_msg(uid, msg):
    if msg.startswith("/"):
        return usage
    elif msg.count(' ') > 0:
        tokens = [x.strip() for x in msg.split(',')]
        data = []
        for token in tokens:
            try:
                item, cost = [t(s) for t,s in zip((str,int), token.split())]
            except Exception as e:
                return e

            data.append({'item': item, 'cost': cost})

        try:
            client['accounting'].uid.insert_many(data)
            return f'成功寫入{len(data)}筆'
        except Exception as e:
            return e

    return usage
        

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get_message = event.message.text
    user_id = event.source.user_id

    ret = proc_msg(user_id, get_message)

    # Send To Line
    reply = TextSendMessage(text=f"{ret}")
    line_bot_api.reply_message(event.reply_token, reply)
