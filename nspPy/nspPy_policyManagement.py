################################################################################
# NAME 
#   nspPy_policyManagement.py
#
# DESCRIPTION
#   This file maintains NSP IP Optim app handling mechanism
# 
# HISTORY
#   dd-mm-yyyy - author - comment
#   05-03-2021 - Asad Arafat - Creation
################################################################################
import json
import requests
import pprint
import base64
import yaml
import CM_Log
import nspPy_session
from jsonpath_ng import jsonpath, parse

#requests.packages.urllib3.disable_warnings()


## Constant
GLBL_NSP_POLICY_MANAGEMENT_BASE_URL                          = ":8543/sdn/api/v4/policy/"
GLBL_NSP_POLICY_MANAGEMENT_TUNNEL_PROFILE_FILENAME           = "/Users/aarafat/PycharmProjects/NSP-Project/nspPy/template/PM/PM_tunnelProfile.yaml"

class policyMgmnt(object):
    def __init__(self):
        self.pathProfileData            = None

    def createTunnelProfile(self, urlHost,token):
        with open(GLBL_NSP_POLICY_MANAGEMENT_TUNNEL_PROFILE_FILENAME) as file:
            self.pathProfileData = yaml.load(file, Loader=yaml.FullLoader)  

        url = 'https://' + urlHost + GLBL_NSP_POLICY_MANAGEMENT_BASE_URL + 'tunnel-selections'
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer " + token
            }
        payload = json.dumps(self.pathProfileData, indent=4)
        CM_Log.info("payload:\n" + payload)

        response = requests.request("POST", url, headers=headers, verify=False, data=payload)
        response = json.loads(response.text)
        CM_Log.info("createAddressResponse:\n" + json.dumps(response, indent=4))


    def listTunnelProfile(self, urlHost,token):
        with open(GLBL_NSP_POLICY_MANAGEMENT_TUNNEL_PROFILE_FILENAME) as file:
            self.pathProfileData = yaml.load(file, Loader=yaml.FullLoader)  

        url = 'https://' + urlHost + GLBL_NSP_POLICY_MANAGEMENT_BASE_URL + 'tunnel-selections'
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer " + token
            }
        payload = json.dumps(self.pathProfileData, indent=4)
        CM_Log.info("payload:\n" + payload)

        response = requests.request("GET", url, headers=headers, verify=False, data=payload)
        response = json.loads(response.text)
        CM_Log.info("createAddressResponse:\n" + json.dumps(response, indent=4))
        return response


    def getTunnelProfileUuid(self, tunnelProfileName, urlHost,token):
        listTunnelProfile = self.listTunnelProfile(urlHost,token)
        jsonpath_expression = parse('$.response.data[*]')   ## find the json path from here https://jsonpath.com/
        for match in jsonpath_expression.find(listTunnelProfile):
            #CM_Log.info(json.dumps(match.value, indent=4))
            if match.value["name"] == tunnelProfileName:   
                CM_Log.info("ProfileUuid: "+match.value["id"])
                return match.value["id"]


    def deleteTunnelProfile(self, tunnelProfileUUuid, urlHost, token):
        url = 'https://' + urlHost + GLBL_NSP_POLICY_MANAGEMENT_BASE_URL + 'tunnel-selections/' + tunnelProfileUUuid
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer " + token
            }

        response = requests.request("DELETE", url, headers=headers, verify=False)
        response = json.loads(response.text)
        CM_Log.info("DeletePathProfileResponse:\n" + json.dumps(response, indent=4))
        return response 

  ###
  ## Request URL: https://10.58.22.244:8543/sdn/api/v4/policy/tunnel-selections/eea946c1-8cc0-4dc8-ac11-623d90a0cc58
  ## Request Method: DELETE
  ## Status Code: 200 
  ## Remote Address: 10.58.22.244:8543
## Referrer Policy: strict-origin-when-cross-origin


def UT_policyManagement():
    x = nspPy_session.nspPy_session()
    x.encodeUserName()
    x.getRestToken()
    token = x.token
    urlHost = x.IP

    pm = policyMgmnt()

    ## create tunnel profile
    ## pm.createTunnelProfile(urlHost,token)

    ## list tunnel profile
    pm.listTunnelProfile(urlHost,token)

    
    ## delete path profile
    tunnelProfileUuid = pm.getTunnelProfileUuid("asad", urlHost,token)
    pm.deleteTunnelProfile(tunnelProfileUuid, urlHost, token)

    x.revokeRestToken()

#
# Execute main program
if (__name__ == '__main__'):
    UT_policyManagement()


