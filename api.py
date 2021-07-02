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
    MessageEvent, TextMessage, TextSendMessage, FollowEvent, FlexSendMessage
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

print(channel_secret)

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


# CSV Example
import csv

@handler.add(FollowEvent)
def handle_follow(event):
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text="you have followed me!")
    # )
    with open('emergency_button.json',) as file:
        flex_emergency = json.loads(file.read())
    print("!!!!!!!!!!!! CONTENTS")
    print(flex_emergency)
    print(type(json.dumps(flex_emergency)))
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text='emergency_button', 
            contents= {
                "type": "bubble",
                "hero": {
                "type": "image",
                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
                "action": {
                    "type": "uri",
                    "uri": "http://linecorp.com/"
                }
                },
                "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                    "type": "text",
                    "text": "Brown Cafe",
                    "weight": "bold",
                    "size": "xl"
                    },
                    {
                    "type": "box",
                    "layout": "baseline",
                    "margin": "md",
                    "contents": [
                        {
                        "type": "icon",
                        "size": "sm",
                        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                        },
                        {
                        "type": "icon",
                        "size": "sm",
                        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                        },
                        {
                        "type": "icon",
                        "size": "sm",
                        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                        },
                        {
                        "type": "icon",
                        "size": "sm",
                        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
                        },
                        {
                        "type": "icon",
                        "size": "sm",
                        "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png"
                        },
                        {
                        "type": "text",
                        "text": "4.0",
                        "size": "sm",
                        "color": "#999999",
                        "margin": "md",
                        "flex": 0
                        }
                    ]
                    },
                    {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": [
                        {
                        "type": "box",
                        "layout": "baseline",
                        "spacing": "sm",
                        "contents": [
                            {
                            "type": "text",
                            "text": "Place",
                            "color": "#aaaaaa",
                            "size": "sm",
                            "flex": 1
                            },
                            {
                            "type": "text",
                            "text": "Miraina Tower, 4-1-6 Shinjuku, Tokyo",
                            "wrap": True,
                            "color": "#666666",
                            "size": "sm",
                            "flex": 5
                            }
                        ]
                        },
                        {
                        "type": "box",
                        "layout": "baseline",
                        "spacing": "sm",
                        "contents": [
                            {
                            "type": "text",
                            "text": "Time",
                            "color": "#aaaaaa",
                            "size": "sm",
                            "flex": 1
                            },
                            {
                            "type": "text",
                            "text": "10:00 - 23:00",
                            "wrap": True,
                            "color": "#666666",
                            "size": "sm",
                            "flex": 5
                            }
                        ]
                        }
                    ]
                    }
                ]
                },
                "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "uri",
                        "label": "CALL",
                        "uri": "https://linecorp.com"
                    }
                    },
                    {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {
                        "type": "uri",
                        "label": "WEBSITE",
                        "uri": "https://linecorp.com"
                    }
                    },
                    {
                    "type": "spacer",
                    "size": "sm"
                    }
                ],
                "flex": 0
                }
            }
        )
    )


@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    message = event.message.text
    print(event)
    print("!!!!!!!!!!!!!!!!!!!!!")
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="bye")
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
