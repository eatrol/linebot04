# 練習2: 練習多種訊息
# 一般文字訊息, 圖面訊息, 地址訊息, 快速選單

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import action

app = Flask(__name__)

# 設定line機器人的 channel_token 跟 channel_secret
line_bot_api = LineBotApi('9VEu/qAcwk++D6x4+xKzJ9p31SBcTvrxlmcUWy6PNhe9Fjbvlafb3/qL3MHgesxCwPuEb6f38OFYQ7B3CPu23Jffrvu00towJSY88fhCQ7gCIuJ8vUTPtt3fCilKCFHy0aoExNS58QOjSARosjDpTwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('981c8f6cf7ebc514957ef1bf0c1aafe5')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
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
    msg = event.message.text            # 讀取文字訊息

    if msg == "圖片":
        Eric_msg = ImageSendMessage(
            original_content_url='https://img.shop.com/Image/270000/272600/272631/products/1870052087__175x175__.jpg',
            preview_image_url='https://img.shop.com/Image/270000/272600/272631/products/1870052087__175x175__.jpg'
        )
    elif msg == "位置":
        Eric_msg = LocationSendMessage(
            title="GARMIM",
            address="樟樹二路",
            latitude="25.061684",
            longitude="121.640368"
        )
    elif msg == "選單":
        aaa1 = QuickReplyButton(action=MessageAction(label="小貓",text="小貓"))
        aaa2 = QuickReplyButton(action=MessageAction(label="小狗",text="小狗"))
        aaa3 = QuickReplyButton(action=MessageAction(label="小牛",text="小牛"))     
        aaalist = QuickReply(items=[aaa1,aaa2,aaa3])

        Eric_msg = TextSendMessage(text='我的最愛', quick_reply=aaalist)

    elif msg == "組圖":
        Eric_msg = action.imagemap_message()    # 呼叫 action.py 裏頭組圖函數

    elif msg == "好康":
        Eric_msg = action.buttons_message()     # 呼叫 action.py 裏頭選單
    else:
        Eric_msg = TextSendMessage(text=msg) # 轉換成line發送的字串格式

    line_bot_api.reply_message(event.reply_token, Eric_msg) #把訊息發送出去

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
