################################################################################
# NAME 
#   nspPy_ipOptim.py
#
# DESCRIPTION
#   This file maintains NSP IP Optim app handling mechanism
# 
# HISTORY
#   dd-mm-yyyy - author - comment
#   23-01-2021 - Asad Arafat - Creation
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
GLBL_NSP_IP_OPTIM_BASE_URL                        = ":8543/sdn/api/v4/"
GLBL_NSP_IP_OPTIM_PATH_PROFILE_FILENAME           = "/Users/aarafat/PycharmProjects/NSP-Project/nspPy/template/IO/IO_pathProfile.yaml"

class ipOptim(object):
    def __init__(self):
        self.pathProfileData            = None

    def createPathProfile(self, urlHost,token):
        with open(GLBL_NSP_IP_OPTIM_PATH_PROFILE_FILENAME) as file:
            self.pathProfileData = yaml.load(file, Loader=yaml.FullLoader)  

        url = 'https://' + urlHost + GLBL_NSP_IP_OPTIM_BASE_URL + 'template/path-profiles'
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer " + token
            }
        payload = json.dumps(self.pathProfileData, indent=4)
        CM_Log.info("payload:\n" + payload)

        response = requests.request("POST", url, headers=headers, verify=False, data=payload)
        response = json.loads(response.text)
        CM_Log.info("createAddressResponse:\n" + json.dumps(response, indent=4))

    def listPathProfile(self, urlHost,token):
        url = 'https://' + urlHost + GLBL_NSP_IP_OPTIM_BASE_URL + 'template/path-profiles'
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer " + token
            }
        payload = json.dumps(self.pathProfileData, indent=4)
        CM_Log.info("payload:\n" + payload)

        response = requests.request("GET", url, headers=headers, verify=False, data=payload)
        response = json.loads(response.text)
        CM_Log.info("listPathProfileResponse:\n" + json.dumps(response, indent=4))
        return response

    def getPathProfileUuid(self, pathProfileName, urlHost,token):
        listPathProfile = self.listPathProfile(urlHost,token)
        jsonpath_expression = parse('$.response.data[*]')   ## find the json path from here https://jsonpath.com/
        for match in jsonpath_expression.find(listPathProfile):
            #CM_Log.info(json.dumps(match.value, indent=4))
            if match.value["name"] == pathProfileName:   
                CM_Log.info("ProfileUuid: "+match.value["id"])
                return match.value["id"]

    def deletePathProfile(self, pathProfileUuid, urlHost, token):
        url = 'https://' + urlHost + GLBL_NSP_IP_OPTIM_BASE_URL + 'template/path-profiles/' + pathProfileUuid
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer " + token
            }

        response = requests.request("DELETE", url, headers=headers, verify=False)
        response = json.loads(response.text)
        CM_Log.info("DeletePathProfileResponse:\n" + json.dumps(response, indent=4))
        return response 

    def getNetworksIetf(self, urlHost,token):
        url = 'https://' + urlHost + GLBL_NSP_IP_OPTIM_BASE_URL + 'ietf/te/networks'
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer " + token
            }
        payload = {}
        #payload = json.dumps(self.networksIetfData, indent=4)
        #CM_Log.info("payload:\n" + payload)

        response = requests.request("GET", url, headers=headers, verify=False, data=payload)
        response = json.loads(response.text)
        CM_Log.info("getNetworksIetfResponse:\n" + json.dumps(response, indent=4))
        return response

    def getLspPath(self, urlHost,token):
        url = 'https://' + urlHost + GLBL_NSP_IP_OPTIM_BASE_URL + '/mpls/lsp-paths'
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer " + token
            }
        payload = {}
        #payload = json.dumps(self.networksIetfData, indent=4)
        #CM_Log.info("payload:\n" + payload)

        response = requests.request("GET", url, headers=headers, verify=False, data=payload)
        response = json.loads(response.text)
        CM_Log.info("getLspResponse:\n" + json.dumps(response, indent=4))
        return response

    def getIpLink(self, urlHost,token):
        #https://{{server}}:8543/sdn/api/map/iplinks
        url = 'https://' + urlHost  + ':8543/sdn/api/map/iplinks'
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer " + token
            }
        payload = {}
        #payload = json.dumps(self.networksIetfData, indent=4)
        #CM_Log.info("payload:\n" + payload)

        response = requests.request("GET", url, headers=headers, verify=False, data=payload)
        response = json.loads(response.text)
        CM_Log.info("getLspResponse:\n" + json.dumps(response, indent=4))
        return response
    ## GET
    # Request URL: https://10.58.23.30:8543/sdn/api/v4/template/path-profiles
    # Request Method: GET
    # Status Code: 200 
    # Remote Address: 10.58.23.30:8543
    # Referrer Policy: strict-origin-when-cross-origi

    ## DELETE
    # Request URL: https://10.58.23.30:8543/sdn/api/v4/template/path-profiles/86607b58-2e4d-484d-925f-66e8e689089a
    # Request Method: DELETE
    # Status Code: 200 
    # Remote Address: 10.58.23.30:8543
    # Referrer Policy: strict-origin-when-cross-origin    


def UT_ipOptim():
    x = nspPy_session.nspPy_session()
    x.encodeUserName()
    x.getRestToken()
    token = x.token
    urlHost = x.IPsdn 

    ip = ipOptim()

    ## create path profile
    #ip.createPathProfile(urlHost,token)

    ## list path profile
    #ip.listPathProfile(urlHost,token)
    
    ## delete path profile
    #pathProfileUuid = ip.getPathProfileUuid("PCC_102_Loose_fromRestApi", urlHost,token)
    #ip.deletePathProfile(pathProfileUuid, urlHost, token)

    ## get network Ietf
    ip.getNetworksIetf(urlHost,token)

    ## get network LSP
    #ip.getLspPath(urlHost,token)

    ## get IP Links
    #ip.getIpLink(urlHost,token)

    x.revokeRestToken()

#
# Execute main program
if (__name__ == '__main__'):
    UT_ipOptim()


