#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response
from odata import ODataService
#from pyrfc import Connection

# Flask app should start in global layout
app = Flask(__name__)
url = 'http://services.odata.org/V4/Northwind/Northwind.svc/'
Service = ODataService(url, reflect_entities=True)
Order = Service.entities['Order']
query = Service.query(Order)
query = query.limit(2)
query = query.order_by(Order.ShippedDate.desc())
for order in query:
    speech = "Date:: " + order.ShippedDate + " OKKKKKKA."



@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "shipping.cost":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    zone = parameters.get("shipping-zone")
	#conn = Connection(ashost='10.0.0.1', sysnr='00', client='100', user='me', passwd='secret')
	#conn = Connection(ashost='',sysnr='',client='',user='',passwd='')
	#result = conn.call('STFC_CONNECTION', REQUTEXT=u'Hello SAP!')
    cost = {'Europe':100, 'North America':200, 'South America':300, 'Asia':400, 'Africa':500}
    #speech = "The cost of shipping to " + zone + " is " + str(cost[zone]) + " euros."
	#rprint("Response:")
	
    
    print("Response:")
    #speech = order.ShippedDate
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "connect-sap-shipping-list"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print ("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')
