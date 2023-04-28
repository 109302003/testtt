import openai
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import json
from json import load
import sqlite3
import json
from flask import Flask
app = Flask(__name__)

# 初始化OpenAI客戶端
openai.api_key = "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"
#model_engine = "text-davinci-002"
#openai_model = openai.CompletionV1()

# 初始化Line Bot
channel_secret = "aef7718e792000641f69a5b5cbef4351"
channel_access_token = "cwWpk4v1Y+XUHUwLqUvRK9d6hX2GHwl76dafyTpDnzgATA1Et0XZ4XYf1weItN2UTBTdoAKI1Edo1OvCwco9qlz0znoa+eE5cBVsPAKpwYrSCvR2q2ngSshMbhM5gCZN5xtXLsBzFNLhc+ZD+CE4JQdB04t89/1O/w1cDnyilFU="
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

# 初始化Flask應用程式
#app = Flask(__name__)

# 讀取 config.json，取得 secret 和 token
#CONFIG = json.load(open("/home/config.json", "r"))
#line_bot_api = LineBotApi(os.getenv("ACCESS_TOKEN"))
#handler = WebhookHandler(os.getenv("CHANNEL_SECRET"))
"""
# 處理用戶輸入的訊息
def handle_message(text):
    prompt = f"{text.strip()}\nAI："
    response = openai_model.create(
        engine=model_engine,
        prompt=prompt,
        temperature=0.7,
        max_tokens=50,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\n"]
    )
    message = response.choices[0].text.strip()
    return message
# 實現API端點
@app.route("/callback", methods=["POST"])
def callback():
   # 獲取Line發送的請求中的資訊
   signature = request.headers["X-Line-Signature"]
   body = request.get_data(as_text=True)
   app.logger.info("Request body: "+body)
   # 驗證請求的簽名
   try:
       handler.handle(body, signature)
   except InvalidSignatureError:
       abort(400)
   return "OK"
# 處理用戶發送的訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_user_message(event):
   # 從Line獲取使用者發送的訊息
   user_message = event.message.text
    
   # 將使用者發送的訊息送到ChatGPT API伺服器中進行處理並獲取回覆的訊息
   # 將回覆的訊息發送回Line
   ai_message = handle_message(user_message)
   line_bot_api.reply_message(
       event.reply_token,
       TextSendMessage(text=user_message)
   )
"""
@app.route("/callback", methods=['POST'])
def callback():
    body = request.get_data(as_text=True)
    json_data = json.loads(body)
    print(json_data)
    try:
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        tk = json_data['events'][0]['replyToken']
        msg = json_data['events'][0]['message']['text']
        # 取出文字的前五個字元，轉換成小寫
        ai_msg = msg[:7].lower()
        reply_msg = ''

        response = openai.Completion.create(
                model='text-davinci-003',
                prompt=msg[:],
                max_tokens=256,
                temperature=0.5,
                )
        # 接收到回覆訊息後，移除換行符號
        reply_msg = response["choices"][0]["text"].replace('\n','')

        text_message = TextSendMessage(text = reply_msg)
        line_bot_api.reply_message(tk , text_message)
    except:
        print('error')
    return 'OK'

    

@app.route("/")
def hello():
    return "Hello, World!"

if __name__ == "__main__":
    app.run()