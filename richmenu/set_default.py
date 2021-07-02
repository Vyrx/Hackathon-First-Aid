
import sys
from linebot import LineBotApi

import os

try:
    channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN') or 'YOUR_SECRET'
except:
    raise Exception("Can't get access token")

if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)

# Example: https://github.com/line/line-bot-sdk-python#set_default_rich_menuself-rich_menu_id-timeoutnone
# Document: https://developers.line.biz/en/reference/messaging-api/#set-default-rich-menu
rich_menu_id = 'richmenu-3514661b0c16b00d8fb380b1a9a4c901'
line_bot_api.set_default_rich_menu(rich_menu_id)
