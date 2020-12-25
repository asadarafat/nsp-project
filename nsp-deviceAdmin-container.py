import json
import requests
import base64
import ssl
import pprint
import datetime
from json import JSONDecoder
from collections import OrderedDict

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
s = "10.58.82.201"  # data['gatewayUrl']
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


def revokeRestToken(token):
    url = 'https://' + urlHost + '/session-manager/api/v1/sessions/' + token
    # print url
    headers = {'content-type': "application/x-www-form-urlencoded"}
    # 'authorization': "Bearer " + token}
    response = requests.request("DELETE", url, headers=headers, verify=False)

    print(datetime.datetime.now())
    print(json.dumps(json.loads(response.text), indent=5))

    # print response
    return response


addressRuleTemplate = """
{
  "type": "IpAddrRule",
     "dto": {
           "ipaddress": "10.10.10.11",
           "maskBits": "32",
           "filterType": "include"
     }
}
  """


def createAddressRule(payload, token):
    jPayload = json.loads(payload, object_pairs_hook=OrderedDict)
    jPayload['dto']['ipaddress'] = '10.10.10.208'
    jPayload['dto']['maskBits'] = '32'

    url = 'https://' + urlHost + ':8548/mdm-necontrol-rest-api-app/api/v1/neControl/discoveryrule'
    headers = {'content-type': "application/json",
               'authorization': "Bearer " + token}
    response = requests.request("POST", url, headers=headers, verify=False, data=payload)
    response = json.loads(response.text)
    AddressRuleFdn = response['response']['data']['fdn']['fdn']
    # print AddressRuleFdn
    print(datetime.datetime.now())

    return AddressRuleFdn


NeSnmpReachabilityPolicyTemplate = """
{
  "type": "NeReachabilityPolicy",
     "dto": {
           "name": "SnmpReachability",
           "interval": "2",
           "timeout": "1",
           "adminState" : "up",
           "reachabilityType" :"snmp"
     }
}
"""
NePingReachabilityPolicyTemplate = """
{
  "type": "NeReachabilityPolicy",
     "dto": {
           "name": "PingReachability",
           "interval": "2",
           "timeout": "1",
           "adminState" : "up",
           "reachabilityType" : "ping"
     }
}
"""


def createNeReachabilityPolicy(policyPrefix, payload, token):
    url = 'https://' + urlHost + ':8548/mdm-necontrol-rest-api-app/api/v1/neControl/discoveryrule'
    headers = {'content-type': "application/json",
               'authorization': "Bearer " + token}

    jPayload = json.loads(payload, object_pairs_hook=OrderedDict)
    jPayload['dto']['name'] = policyPrefix + jPayload['dto']['name']
    jPayload = json.dumps(jPayload)

    response = requests.request("POST", url, headers=headers, verify=False, data=jPayload)

    print(datetime.datetime.now())
    print(json.dumps(json.loads(response.text), indent=5))
    response = json.loads(response.text)
    NeReachabilityPolicyFdn = response['response']['data']['fdn']['fdn']
    return NeReachabilityPolicyFdn


SnmpUserTemplate = """
{
  "type":"SnmpUser",
      "dto" : {
    "userName": "admin",
    "description": "PushedFromRestAPI",
    "community": "private"
      }
}
"""
SnmpProtocolTemplate = """
{
      "type":"SnmpProtocol",
      "dto" : {
        "protocolName":"SnmpProtocolViaREST",
        "port": "161",
        "timeout":"10",
        "securityModel":"snmpv2c",
        "retries":"3",
        "description":"SrosSnmpUserPushedFromRestAPI"
      }
}
"""


NetconfUserTemplate = """
{
  "type":"NetconfUser",
      "dto" : {
    "userName": "admin",
    "description": "NetconfUserPushedFromRestAPI",
    "password": "admin"
      }
}
"""

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

CliUserTemplate = """
{
  "type":"CliUser",
      "dto" : {
    "userName": "admin",
    "description": "CliUserPushedFromRestAPI",
    "password": "admin",
    "preLoginUserName":"blart",
    "preLoginPassword":"blart"
      }
}
"""

CliProtocolTemplate = """
{
      "type":"CliProtocol",
      "dto" : {
        "protocolName":"GrpcProtocolViaREST",
        "commProtocol": "SSH2",
        "port": "22",
        "connectTimeout":"3000"
      }
}
"""

GrpcUserTemplate = """
{
  "type":"GrpcUser",
      "dto" : {
    "userName": "admin",
    "description": "GRPC user object for SROS",
    "password": "admin"
      }
}
"""

GrpcProtocolTemplate = """
{
      "type":"GrpcProtocol",
      "dto" : {
        "protocolName":"SROSGrpcProtocolViaREST",
    	"port": "57400",
    	"secure":"false",
    	"connectTimeout":"20",
		"keepaliveInterval":"10",
    	"keepaliveTimeout":"22022"
      }
}
"""

NeMediationPolicyTemplate = """
{
  "type": "NeMediationPolicy",
  "dto": {
    "policyName": "<NAME>",
    "policyType": "SNMP",
    "description": "blah blah blah blah",
    "user":

    {
      "dto": {
        "fdn": {
          "scheme": "model",
          "namespace": "mediationpolicy",
          "fdn": "<USER>"
        }
      }
    },
    "neCommProtocol": {
      "dto": {
        "fdn": {
          "scheme": "model",
          "namespace": "mediationpolicy",
          "fdn": "<PROTOCOL>"
        }
      }
    },
    "readOnlyNes": []
  }
}
"""


def createUser(payload, token):
    url = 'https://' + urlHost + ':8548/mdm-necontrol-rest-api-app/api/v1/neuser'
    headers = {'content-type': "application/json",
               'authorization': "Bearer " + token}
    response = requests.request("POST", url, headers=headers, verify=False, data=payload)

    # print(datetime.datetime.now())
    # print (json.dumps(json.loads(response.text), indent=5))
    response = json.loads(response.text)
    SnmpUserFdn = response['response']['data']['fdn']['fdn']
    # print SnmpUserFdn
    return SnmpUserFdn


def createProtocol(payload, token):
    url = 'https://' + urlHost + ':8548/mdm-necontrol-rest-api-app/api/v1/neprotocol'
    headers = {'content-type': "application/json",
               'authorization': "Bearer " + token}
    response = requests.request("POST", url, headers=headers, verify=False, data=payload)

    print(datetime.datetime.now())
    print (json.dumps(json.loads(response.text), indent=5))
    response = json.loads(response.text)
    SnmpProtocolFdn = response['response']['data']['fdn']['fdn']
    # print SnmpProtocolFdn
    return SnmpProtocolFdn


def createSnmpMediationPolicy(policyPrefix, payload, token):
    # print payload

    jPayload = json.loads(payload, object_pairs_hook=OrderedDict)
    jPayload['dto']['policyName'] = policyPrefix + 'SnmpMediationPolicy'
    jPayload['dto']['policyType'] = 'SNMP'
    jPayload['dto']['user']['dto']['fdn']['fdn'] = createUser(SnmpUserTemplate, token)
    jPayload['dto']['neCommProtocol']['dto']['fdn']['fdn'] = createProtocol(SnmpProtocolTemplate, token)
    jPayload = json.dumps(jPayload)
    # print json.dumps( jPayload, indent=5)
    # print type (payload, token)
    # print type (jPayload)

    url = 'https://' + urlHost + ':8548/mdm-necontrol-rest-api-app/api/v1/nemediationpolicy'
    headers = {'content-type': "application/json",
               'authorization': "Bearer " + token}
    response = requests.request("POST", url, headers=headers, verify=False, data=jPayload)

    print(datetime.datetime.now())
    print(json.dumps(json.loads(response.text), indent=5))
    response = json.loads(response.text)
    SnmpMediationPolicyeFdn = response['response']['data']['fdn']['fdn']
    return SnmpMediationPolicyeFdn


def createNetconfMediationPolicy(policyPrefix, payload, token):
    # print payload

    jPayload = json.loads(payload, object_pairs_hook=OrderedDict)
    jPayload['dto']['policyName'] = policyPrefix + 'NetconfMediationPolicy'
    jPayload['dto']['policyType'] = 'NETCONF'
    jPayload['dto']['user']['dto']['fdn']['fdn'] = createUser(NetconfUserTemplate, token)
    jPayload['dto']['neCommProtocol']['dto']['fdn']['fdn'] = createProtocol(NetconfProtocolTemplate, token)
    jPayload = json.dumps(jPayload)
    # print json.dumps( jPayload, indent=5)
    # print type (payload, token)
    # print type (jPayload)

    url = 'https://' + urlHost + ':8548/mdm-necontrol-rest-api-app/api/v1/nemediationpolicy'
    headers = {'content-type': "application/json",
               'authorization': "Bearer " + token}
    response = requests.request("POST", url, headers=headers, verify=False, data=jPayload)

    print(datetime.datetime.now())
    print(json.dumps(json.loads(response.text), indent=5))
    response = json.loads(response.text)
    NetconfMediationPolicyFdn = response['response']['data']['fdn']['fdn']
    return NetconfMediationPolicyFdn


def createCliMediationPolicy(policyPrefix, payload, token):
    # print payload

    jPayload = json.loads(payload, object_pairs_hook=OrderedDict)
    jPayload['dto']['policyName'] = policyPrefix + 'CliMediationPolicy'
    jPayload['dto']['policyType'] = 'CLI'
    jPayload['dto']['user']['dto']['fdn']['fdn'] = createUser(CliUserTemplate, token)
    jPayload['dto']['neCommProtocol']['dto']['fdn']['fdn'] = createProtocol(CliProtocolTemplate, token)
    jPayload = json.dumps(jPayload)

    # print json.dumps( jPayload, indent=5)
    # print type (payload, token)
    # print type (jPayload)

    url = 'https://' + urlHost + ':8548/mdm-necontrol-rest-api-app/api/v1/nemediationpolicy'
    headers = {'content-type': "application/json",
               'authorization': "Bearer " + token}
    response = requests.request("POST", url, headers=headers, verify=False, data=jPayload)

    print(datetime.datetime.now())
    print(json.dumps(json.loads(response.text), indent=5))

    response = json.loads(response.text)
    NetconfMediationPolicyFdn = response['response']['data']['fdn']['fdn']
    return NetconfMediationPolicyFdn

def createGrpcMediationPolicy(policyPrefix, payload, token):
    # print payload

    jPayload = json.loads(payload, object_pairs_hook=OrderedDict)
    jPayload['dto']['policyName'] = policyPrefix + 'GrpcMediationPolicy'
    jPayload['dto']['policyType'] = 'GRPC'
    jPayload['dto']['user']['dto']['fdn']['fdn'] = createUser(CliUserTemplate, token)
    jPayload['dto']['neCommProtocol']['dto']['fdn']['fdn'] = createProtocol(CliProtocolTemplate, token)
    jPayload = json.dumps(jPayload)

    # print json.dumps( jPayload, indent=5)
    # print type (payload, token)
    # print type (jPayload)

    url = 'https://' + urlHost + ':8548/mdm-necontrol-rest-api-app/api/v1/nemediationpolicy'
    headers = {'content-type': "application/json",
               'authorization': "Bearer " + token}
    response = requests.request("POST", url, headers=headers, verify=False, data=jPayload)

    print(datetime.datetime.now())
    print(json.dumps(json.loads(response.text), indent=5))

    response = json.loads(response.text)
    GrpcMediationPolicyFdn = response['response']['data']['fdn']['fdn']
    return GrpcMediationPolicyFdn


DiscoveryRule = """
{
  "type" : "NeDiscRule",
  "dto": {
       "name" : "SrSnmpDiscoveryRuleWithNetconf",
       "description" : "SrosDiscoveryRuleViaSnmpAndNetconfCLIandGrpc",
       "scanInterval" : "60",
       "adminState" : "up",
       "operState" : "active",
       "orderDiscovery" : {"1":"SNMP","2":"NETCONF","3":"CLI","4":"GRPC"},
       "ipAddrRules": [{

                              "scheme" : "model",
                              "namespace":"necontrol",
                              "fdn" : "{{IpAddrRuleSr}}"

            }],
       "neROMedPolicies" : [ 
                              {"scheme" : "model",
                               "namespace":"mediationpolicy",
                               "fdn" : "{{NeMediationPolicySnmpSr}}"},
                              {"scheme" : "model",
                              "namespace":"mediationpolicy",
                              "fdn" : "{{NeMediationPolicyNetconfSr}}"},
                              {"scheme" : "model",
                              "namespace":"mediationpolicy",
                              "fdn" : "{{NeMediationPolicyCliSr}}"},
                              {"scheme" : "model",
                              "namespace":"mediationpolicy",
                              "fdn" : "{{NeMediationPolicyGrpciSr}}"}
                      ],
       "neRWMedPolicies" : [ 
                              {"scheme" : "model","namespace":"mediationpolicy","fdn" : "{{NeMediationPolicySnmpSr}}"},
                              {"scheme" : "model","namespace":"mediationpolicy","fdn" : "{{NeMediationPolicyNetconfSr}}"},
                              {"scheme" : "model","namespace":"mediationpolicy","fdn" : "{{NeMediationPolicyCliSr}}"},
                              {"scheme" : "model","namespace":"mediationpolicy","fdn" : "{{NeMediationPolicyGrpcSr}}"}
    
                      ],
       "neTrapMedPolicies" : [ 
                              {"scheme" : "model","namespace":"mediationpolicy","fdn" : "{{NeMediationPolicySnmpSr}}"},
                              {"scheme" : "model","namespace":"mediationpolicy","fdn" : "{{NeMediationPolicyNetconfSr}}"},
                              {"scheme" : "model","namespace":"mediationpolicy","fdn" : "{{NeMediationPolicyCliSr}}"},
                              {"scheme" : "model","namespace":"mediationpolicy","fdn" : "{{NeMediationPolicyGrpcSr}}"}
                      ],
       "neReachabilityPolicies" : [ 
                     { "scheme" : "model","namespace":"necontrol","fdn" : "{{NePingReachabilityPolicySr}}" },
                     { "scheme" : "model","namespace":"necontrol","fdn" : "{{NeSnmpReachabilityPolicySr}}" }
                 ]
   }
}
"""


def createDiscoveryRule(policyPrefix, payload, token):
    jPayload = json.loads(payload, object_pairs_hook=OrderedDict)
    SnmpMediationPolicyFdn = createSnmpMediationPolicy(policyPrefix, NeMediationPolicyTemplate, token)
    NetconfMediationPolicFdn = createNetconfMediationPolicy(policyPrefix, NeMediationPolicyTemplate, token)
    CliMediationPolicyFdn  = createCliMediationPolicy(policyPrefix , NeMediationPolicyTemplate, token)
    GrpcMediationPolicyFdn = createGrpcMediationPolicy(policyPrefix, NeMediationPolicyTemplate, token)
    AddressRuleFdn = createAddressRule(addressRuleTemplate, token)
    # print jPayload
    # print jPayload['dto']['ipAddrRules']
    jPayload['dto']['name'] = policyPrefix + "DiscoveryRule"
    jPayload['dto']['ipAddrRules'][0]['fdn'] = AddressRuleFdn
    jPayload['dto']['neROMedPolicies'][0]['fdn'] = SnmpMediationPolicyFdn
    jPayload['dto']['neROMedPolicies'][1]['fdn'] = NetconfMediationPolicFdn
    jPayload['dto']['neROMedPolicies'][2]['fdn'] = CliMediationPolicyFdn
    jPayload['dto']['neROMedPolicies'][3]['fdn'] = GrpcMediationPolicyFdn
    jPayload['dto']['neRWMedPolicies'][0]['fdn'] = SnmpMediationPolicyFdn
    jPayload['dto']['neRWMedPolicies'][1]['fdn'] = NetconfMediationPolicFdn
    jPayload['dto']['neRWMedPolicies'][2]['fdn'] = CliMediationPolicyFdn
    jPayload['dto']['neRWMedPolicies'][3]['fdn'] = GrpcMediationPolicyFdn
    jPayload['dto']['neTrapMedPolicies'][0]['fdn'] = SnmpMediationPolicyFdn
    jPayload['dto']['neTrapMedPolicies'][1]['fdn'] = NetconfMediationPolicFdn
    jPayload['dto']['neTrapMedPolicies'][2]['fdn'] = CliMediationPolicyFdn
    jPayload['dto']['neTrapMedPolicies'][3]['fdn'] = GrpcMediationPolicyFdn
    jPayload['dto']['neReachabilityPolicies'][0]['fdn'] = createNeReachabilityPolicy(policyPrefix, NePingReachabilityPolicyTemplate,
                                                                                     token)
    jPayload['dto']['neReachabilityPolicies'][1]['fdn'] = createNeReachabilityPolicy(policyPrefix, NeSnmpReachabilityPolicyTemplate,
                                                                                     token)
    # print jPayload
    jPayload = json.dumps(jPayload, indent=5)
    # print jPayload

    url = 'https://' + urlHost + ':8548/mdm-necontrol-rest-api-app/api/v1/neControl/discoveryrule'
    headers = {'content-type': "application/json",
               'authorization': "Bearer " + token}
    response = requests.request("POST", url, headers=headers, verify=False, data=jPayload)

    print(datetime.datetime.now())
    print(json.dumps(json.loads(response.text), indent=5))

    return response


def main():
    encodeUserName()
    token = getRestToken()
    # print 'token:' + token
    policyPrefix = "a5ad"
    createDiscoveryRule(policyPrefix, DiscoveryRule, token)
    #createGrpcMediationPolicy(policyPrefix, NeMediationPolicyTemplate, token)


    #revokeRestToken(token)


main()
