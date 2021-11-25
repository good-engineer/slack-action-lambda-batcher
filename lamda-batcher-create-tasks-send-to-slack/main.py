# all copyright is reserved for Korea space data 
# code that post order requests to slack 
# author: Mary
import logging
logging.basicConfig(level=logging.DEBUG) 
import os
import ssl
import json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import requests

# load the context
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


# create slack client 
client = WebClient(token=os.environ['SLACK_BOT_TOKEN'], ssl=ssl_context)


# load orders
def load_orders():
    # todo : (await) get order list from old api 
    # json_data = json.load(res)
    # mock data 
    orders = [ {
        "old_id" : 6,
        "title": "test order 0",
        "address": "테헤란로 503",
        "status": 1
 
    },
    {
        "old_id" : 7,
        "title": "test order 1",
        "address": "테헤란로 503",
        "status": 0

    },
    {
        "old_id" : 8,
        "title": "test order 2",
        "address": "테헤란로 503",
        "status": 0
 
    },
    {
 
        "title": "test order 3",
        "old_id" : 9,
        "address": "테헤란로 503",
        "status": 0
 
    },
    {
    
        "title": "test order 4",
        "old_id" : 10,
        "address": "테헤란로 503",
        "status": 0

    },
    {

        "title": "test order 5",
        "old_id" : 11,
        "address": "테헤란로 503",
        "status": 0

    }

    ]
    return orders


# post to slack 
def post_to_slack(orders):
    for order in orders:
        send_to_slack(order["old_id"],"📌 "+order["title"], "주소: "+order["address"])
    

def send_to_slack(id, text1, text2):
    blocks=[
        {
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": text1,
				"emoji": True
			}
		},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": text2
            }
        },
        {
        "type": "actions",
			"block_id": str(id),
			"elements": [
                {          
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": "수리 시작"
            },
            "value": "1",
            "style": "danger",
            "action_id": "start_order"
        },
        
        ]
        },
        {
			"type": "divider"
		}
    ]
    try:
        client.chat_postMessage(channel='#sk-test', blocks=blocks)
    except SlackApiError as e :
        assert e.response["ok"] is False
        assert e.response["error"]
        print(f"Got an error: {e.response['error']}")


# post to ksd-sk-dnd-api to store in server
def post_to_server(orders):
    data = {
        "orders": orders
    }
    headers = {'Content-type': 'application/json'}
    try:
        r = requests.post(url = os.environ['API_END_POINT'], data=json.dumps(data), headers=headers)
        print("response status code: " + str(r.status_code))
    except requests.ConnectionError as e:
        print(e)

# start the order
orders = load_orders()
post_to_server(orders)
post_to_slack(orders)
