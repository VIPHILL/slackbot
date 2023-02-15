import requests
import os
import urllib3
import json
from datetime import datetime
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from jinja2 import Environment, FileSystemLoader


client = WebClient(token=os.environ['API_KEY'])
mensa = requests.get('https://dev.neuland.app/api/mensa').json()
reimanns = requests.get('https://dev.neuland.app/api/reimanns').json()
barker = urllib3.PoolManager()

environment = Environment(loader=FileSystemLoader("templates/"), trim_blocks=True)
template = environment.get_template("message.txt")
template.globals['now'] = datetime.now()

msg = template.render(mensa = mensa, reimanns = reimanns)
try:
    response = client.chat_postMessage(channel='#mittagspause', text=msg)
    r=barker.request('POST','https://thide.webhook.office.com/webhookb2/1f4906f1-3c48-436b-905f-c27fa0d1d0f9@28bcace8-4ce7-4949-868f-170f67122379/IncomingWebhook/b9a816edd8bb44d69855f366614b0b49/b7f56d59-b48b-48a3-a16f-3afae5b0976b', headers={'Content-Type': 'application/json'},
body=json.dumps({"text":msg}).encode('utf-8')

except SlackApiError as e:
    print(e)
