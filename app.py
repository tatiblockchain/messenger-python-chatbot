from flask import Flask, request
import requests
import json
import config



#import the chatbot
from chatty import Chatty



app = Flask(__name__)
app.config['SECRET_KEY'] = '51dc30af-b37c-4b8a-90ea-4f32d6be3c62'




#Function to access the Sender API
def callSendAPI(senderPsid, response):
    PAGE_ACCESS_TOKEN = config.PAGE_ACCESS_TOKEN

    payload = {
    'recipient': {'id': senderPsid},
    'message': response,
    'messaging_type': 'RESPONSE'
    }
    headers = {'content-type': 'application/json'}

    url = 'https://graph.facebook.com/v10.0/me/messages?access_token={}'.format(PAGE_ACCESS_TOKEN)
    r = requests.post(url, json=payload, headers=headers)
    print(r.text)



#Function for handling a message from MESSENGER
def handleMessage(senderPsid, receivedMessage):
    #check if received message contains text
    print('We entered the HANDLE MESSAGE FUNCTION')
    if 'text' in receivedMessage:
        print('TEXT does exist in the RECEIVER MESSAGE')

        toSend = receivedMessage['text']

        #The Chatbot function ------------------------
        chatbot = Chatty()

        chatbotResponse = chatbot.chatbot_response(toSend)
        print('The Chatbot Response is: {}'.format(chatbotResponse))

        response = {"text": chatbotResponse }


        callSendAPI(senderPsid, response)
    else:
        response = {"text": 'This chatbot only accepts text messages'}
        callSendAPI(senderPsid, response)




@app.route('/', methods=["GET", "POST"])
def home():
    return 'HOME'


@app.route('/webhook', methods=["GET", "POST"])
def index():
    if request.method == 'GET':
        #do something.....
        VERIFY_TOKEN = "128fea16-bef2-4f86-8402-2fbb9b9ed70e"

        if 'hub.mode' in request.args:
            mode = request.args.get('hub.mode')
            print(mode)
        if 'hub.verify_token' in request.args:
            token = request.args.get('hub.verify_token')
            print(token)
        if 'hub.challenge' in request.args:
            challenge = request.args.get('hub.challenge')
            print(challenge)

        if 'hub.mode' in request.args and 'hub.verify_token' in request.args:
            mode = request.args.get('hub.mode')
            token = request.args.get('hub.verify_token')

            if mode == 'subscribe' and token == VERIFY_TOKEN:
                print('WEBHOOK VERIFIED')

                challenge = request.args.get('hub.challenge')

                return challenge, 200
            else:
                return 'ERROR', 403

        return 'SOMETHING', 200


    if request.method == 'POST':
        #do something.....
        VERIFY_TOKEN = "128fea16-bef2-4f86-8402-2fbb9b9ed70e"

        if 'hub.mode' in request.args:
            mode = request.args.get('hub.mode')
            print(mode)
        if 'hub.verify_token' in request.args:
            token = request.args.get('hub.verify_token')
            print(token)
        if 'hub.challenge' in request.args:
            challenge = request.args.get('hub.challenge')
            print(challenge)

        if 'hub.mode' in request.args and 'hub.verify_token' in request.args:
            mode = request.args.get('hub.mode')
            token = request.args.get('hub.verify_token')

            if mode == 'subscribe' and token == VERIFY_TOKEN:
                print('WEBHOOK VERIFIED')

                challenge = request.args.get('hub.challenge')

                return challenge, 200
            else:
                return 'ERROR', 403



        #do something else
        data = request.data
        body = json.loads(data.decode('utf-8'))


        if 'object' in body and body['object'] == 'page':
            entries = body['entry']
            for entry in entries:
                webhookEvent = entry['messaging'][0]
                print(webhookEvent)

                senderPsid = webhookEvent['sender']['id']
                print('Sender PSID: {}'.format(senderPsid))

                if 'message' in webhookEvent:
                    handleMessage(senderPsid, webhookEvent['message'])

                return 'EVENT_RECEIVED', 200
        else:
            return 'ERROR', 404



if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8888', debug=True)
