import json
import requests
import base64
import ssl
import pprint
import datetime
from json import JSONDecoder
from collections import OrderedDict


NetconfProtocolTemplate = """
{
      "type":"NetconfProtocol",
      "dto" : {
        "protocolName":"NetconfProtocolViaREST",
        "transportProtocol": "SSH2",
        "port": "830",
        "connectTimeout":"10",
        "readTimeout":"10",
        "retries":"3"
      }
}
"""


'''
def loadProps():
        with open('/resignalLsp/resignalProperties.json') as data_file:    
            data = json.load(data_file)
            s = "192.168.20.152" #data['gatewayUrl']
            u = "admin" #data['userName']
            p = "NokiaNsp1!" #data['password']

        global combined
        combined = u+":"+p
        global urlHost
        urlHost = s
        print("Loading properties file.....")
'''

global combined
s = "10.58.23.30"  # data['gatewayUrl']
u = "admin"  # data['userName']
p = "NokiaNsp1!"  # data['password']
combined = u + ":" + p

print(combined)
global urlHost
urlHost = s
print("Loading properties file.....")


def encodeUserName():
    by = bytes(combined, encoding='utf8')
    a = base64.b64encode(by)
    b = base64.b64decode(a).decode('utf-8')
    global userStr
    userStr = a.decode('utf-8')
    print(userStr)


def getRestToken():
    url = "https://" + urlHost + "/rest-gateway/rest/api/v1/auth/token"
    payload = "{\n  \"grant_type\": \"client_credentials\"\n}"
    headers = {
        'content-type': "application/json",
        'authorization': "Basic " + userStr
    }
    response = requests.request("POST", url, data=payload, headers=headers, verify=False)
    my_json = response.text
    parsed = json.loads(my_json)
    # global tStr
    tStr = parsed['access_token']
    # print("Getting REST Token....")
    # print (json.loads(my_json))
    return tStr


def createProtocol(payload, token):
    url = 'https://' + urlHost + ':8548/mdm-necontrol-rest-api-app/api/v1/neprotocol'
    headers = {'content-type': "application/json",
               'authorization': "Bearer " + token}
    response = requests.request("POST", url, headers=headers, verify=False, data=payload)

    # print(datetime.datetime.now())
    # print (json.dumps(json.loads(response.text), indent=5))
    response = json.loads(response.text)
    SnmpProtocolFdn = response['response']['data']['fdn']['fdn']
    print ("SnmpProtocolFdn")
    print (SnmpProtocolFdn)
    return SnmpProtocolFdn

def main():
    encodeUserName()
    token = getRestToken()
    # print 'token:' + token
    policyPrefix = "Asad"
    jPayload['dto']['neCommProtocol']['dto']['fdn']['fdn'] = createProtocol(NetconfProtocolTemplate, token)
    print

main()