#!/usr/bin/env python3
from flask import Flask, request, jsonify
from pprint import pprint

app = Flask(__name__)

base_url = 'https://raw.githubusercontent.com/tbedford/git-testing-repo/master/tunes/xmas/'

# Tunes courtesy http://www.freexmasmp3.com/ 
tunes = [
    ["Little Town of Bethlehem", "bethlem-jazz.mp3"],
    ["Ding Dong Merrily", "ding-dong-merrily.mp3"],
    ["First Noel", "first-noel-r-and-b.mp3"],
    ["Jingle Bells", "jingle-bells-country.mp3"],
    ["Silent Night", "silent-night-piano.mp3"],
    ["Twelve Days of Christmas", "twelve-days-funk.mp3"]
]

# Build options menu 
menu = "Welcome to dial a Christmas carol. You can choose from the following cheesy carols."
i = 1
for t in tunes:
    menu = menu + " Option " + str(i) + " is " + t[0] +"."
    i = i + 1
menu = menu + " Please make your selection now."
    
@app.route("/webhooks/answer")
def answer_call():
    params = request.args
    input_webhook_url = request.url_root + "webhooks/dtmf"
    ncco = [
        {
            "action": "talk",
            "bargeIn": "true",            
            "text": menu
        },
        {
            "action": "input",
            "maxDigits": 1,
            "timeOut": 5,
            "eventUrl": [input_webhook_url]
        } 
    ]
    return jsonify(ncco)

@app.route("/webhooks/dtmf", methods=['POST'])
def dtmf_webhook():
    data = request.get_json()
    selection = data['dtmf']
    if selection == "":
        selection = "1"
    index = int(selection)-1
    if index < 0 or index > len(tunes)-1:
        index = 0
    carol_url = base_url + tunes[index][1]
    print(tunes[index][1])
    msg = "Playing Christmas carol " + str(index+1)
    
    ncco = [
        {
            "action": "talk",
            "text": msg
        },
        {
            "action": "stream",
            "streamUrl": [carol_url]
        }
    ]
    return jsonify(ncco)

@app.route("/webhooks/event", methods=['POST'])
def events():
    data = request.get_json()
    pprint(data)
    return ("OK")

if __name__ == '__main__':
    app.run(port=3000)
