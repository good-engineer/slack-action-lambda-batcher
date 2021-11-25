from datetime import datetime
from json.decoder import JSONDecoder
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework import viewsets
from pytz import timezone
from .models import Order
from .serializers import OrderSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
import json
from django.views.decorators.csrf import csrf_exempt
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os
from urllib.parse import unquote
from rest_framework import status

client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

# /orders get all orders 
class OrdersViewSet(viewsets.ModelViewSet):
    # order = Order(title = "test order", address = "서울시 테헤란로 503 1211층 한국공간데이터", status = 0)
    # order.save()
    queryset = Order.objects.all()
    serializer_class =OrderSerializer

# url : orders/create/
@csrf_exempt
def create_list(request):
    print("*" * 100)
    print(request.body)
    print("*" * 100)
    body = json.loads(request.body)
    list = body["orders"]
    for i in range(0,len(list)):
        order = OrderSerializer(data=list[i])
        if order.is_valid():
            order.save()
        else:
            return Response(order.errors, status=status.HTTP_400_BAD_REQUEST)
    return HttpResponse(status=status.HTTP_200_OK)

# url : slack/
@csrf_exempt
def slack(request):
    print("*" * 100)
    print(request.POST.dict()["payload"])
    print("*" * 100)
    payload = json.loads(request.POST.dict()["payload"])
    channel = payload["channel"]["id"]
    ts = payload["message"]["ts"]
    name = payload["user"]["name"]
    blocks = payload["message"]["blocks"]
    actions = payload["actions"]
    old_id = actions[0]["block_id"]
    value = actions[0]["value"]
    order = Order.objects.get(old_id=int(old_id))
    order.status = int(value)
    order.save()
    # todo : send to oldapi
    to_slack(ts, channel , value, blocks, name)
    return HttpResponse(status=status.HTTP_200_OK)


def to_slack(ts, channel, value, blocks, name):
    fmt = "%Y-%m-%d %H:%M:%S"
    now = datetime.strftime(datetime.now(), fmt)
   
    if value == "1" :
        blocks[2]["elements"][0]= {
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": "수리 완료"
            },
            "style": "primary",
            "value": "2",
            "action_id": "complete_order"
		}
        time  = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "시작 시간: " + now + " ( "+name+" )"
            }
        }
        blocks.insert(2,time)
       
        
    else:
        time = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "완료 시간: " + now + " ( "+name+" )"
            }
        }
        msg = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "✅  정상적으로 완료되었습니다."
            }
        }
        blocks.insert(3,time)
        blocks[4]= msg

    try:
        client.chat_update(channel=channel, text="작업 업데이트" ,blocks=blocks, ts=ts)
    except SlackApiError as e :
        assert e.response["ok"] is False
        assert e.response["error"]
        print(f"Got an error: {e.response['error']}")


