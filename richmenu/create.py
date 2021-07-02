
from linebot.models import RichMenu, RichMenuSize, RichMenuArea, RichMenuBounds, URIAction
import sys
from linebot import LineBotApi

import os

from linebot.models.actions import MessageAction, PostbackAction

try:
    channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN') or 'YOUR_SECRET'
except:
    raise Exception("Can't get access token")

if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)

# Example: https://github.com/line/line-bot-sdk-python#create_rich_menuself-rich_menu-timeoutnone
# Document: https://developers.line.biz/en/reference/messaging-api/#create-rich-menu

rich_menu_to_create = RichMenu(
    size=RichMenuSize(width=2495, height=1474),
    selected=False,
    name="Main Richmenu",
    chat_bar_text="Tap here", 
    areas=[RichMenuArea(
        bounds=RichMenuBounds(x=831, y=0, width=831, height=1474),
        action=MessageAction(label='emergency', text='I have an emergency')),
        RichMenuArea(
        bounds=RichMenuBounds(x=0, y=0, width=831, height=737),
        action=MessageAction(label='consult_doctor', text='I want to consult a doctor')),
        RichMenuArea(
        bounds=RichMenuBounds(x=0, y=737, width=831, height=737),
        action=MessageAction(label='medical_data', text='Open medical data')),
        RichMenuArea(
        bounds=RichMenuBounds(x=1662, y=0, width=831, height=737),
        action=MessageAction(label='video_data', text='I want to video call with an emergency professional')),
        RichMenuArea(
        bounds=RichMenuBounds(x=1662, y=737, width=831, height=737),
        action=PostbackAction(label ='learning_centre', data='learning_centre'))
        ]
)
rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
print(rich_menu_id)


