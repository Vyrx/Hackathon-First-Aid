import os
import json

if os.getenv('DEVELOPMENT') is not None:
    from dotenv import load_dotenv

    load_dotenv(dotenv_path='../.env')

import sys

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FollowEvent, FlexSendMessage, PostbackEvent
)

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET') or 'YOUR_SECRET'
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN') or 'YOUR_ACCESS_TOKEN'

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)


line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


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

@handler.add(FollowEvent)
def handle_follow(event):
    with open('emergency_button.json',) as file:
        flex_emergency = json.loads(file.read())
    try:
        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text='emergency_button', 
                contents= flex_emergency
            )
        )
    except:
        print("!!!!!!!!!!!!! Can't send flex message")
    print("!!!!!!!!!!!!!! USER ID") 
    print(event.source.user_id) 
    line_bot_api.push_message(
        event.source.user_id,
        TextSendMessage(text="you have followed me!")
    )



@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    message = event.message.text
    if message == 'I have an emergency':
        try: 
            with open('flex_json/accident_flex.json',) as file:
                flex_file = json.loads(file.read())
        except:
            Exception("Can't open json")

        line_bot_api.reply_message(
            event.reply_token,
            FlexSendMessage(
                alt_text='accident_flex', 
                contents= flex_file
            )
        )
    
current_event = 0

def flex_display_accident_type(event):
    try: 
        with open('flex_json/accident_type_flex.json',) as file:
            flex_file = json.loads(file.read())
    except:
        Exception("Can't open json")

    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text='accident_type_flex', 
            contents= flex_file
        )
    )

@handler.add(PostbackEvent)  
def handle_postback(event):
    if event.postback.data == 'accident_yes':
        print("There is an accident")
        flex_display_accident_type(event)

    elif event.postback.data == 'accident_no':
        print("There is no accident") 

    elif event.postback.data == 'something_else':
        print("current event is one")       

    print(event.postback.data)   

@handler.add(PostbackEvent)
def handle_accident_type(event):
    if event.postback.data == 'accident_yes':
        print("There is an accident")
    elif event.postback.data == 'accident_no':
        print("There is no accident")
    elif event.postback.data == 'something_else':
        print("current event is one")       

    print(event.postback.data)  


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
