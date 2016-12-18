#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.headers

    print("Request:")
    print(req)

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    baseurl = "http://uinames.com/api/"
    yql_url = baseurl + "?gender=" + req['gender'] + "&region=" + req['region']
    result = urllib.urlopen(yql_url).read()
    data = json.loads(result)
    print("Data:")
    print(data)
    res = makeWebhookResult(data)
    return res


def makeWebhookResult(data):
    name = data.get('name')
    if name is None:
        return {}

    speech = "El nombre sugerido es " + name

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "name-webhook"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=False, port=port, host='0.0.0.0')
