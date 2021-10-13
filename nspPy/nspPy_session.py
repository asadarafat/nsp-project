################################################################################
# NAME 
#   nspPy_session.py
#
# DESCRIPTION
#   This file maintains NSP token handling mechanism
# 
# HISTORY
#   dd-mm-yyyy - author - comment
#   23-01-2021 - Asad Arafat - Creation
################################################################################
import json
import requests
import base64
import yaml
import CM_Log

## Constant
GLBL_NSP_PROPERTIES_FILENAME = "./nspPy/nspProperties.yaml"

class nspPy_session(object):
    def __init__(self):
        with open(GLBL_NSP_PROPERTIES_FILENAME) as file:
            self.data = yaml.load(file, Loader=yaml.FullLoader)
        self.IP             =  self.data[0]['IP']
        self.IPsdn          =  self.data[0]['IPsdn']
        self.username       =  self.data[0]['username']
        self.password       =  self.data[0]['password']
        self.base64Str      =  None
        self.token          =  None

    def encodeUserName(self):
        combined = self.username + ":" + self.password
        a = base64.b64encode(bytes(combined, encoding='utf8'))
        self.base64Str = a.decode('utf-8')
        #print (self.base64Str)
        #print (combined)
        #print (a.decode('utf-8'))
        #print (self.data[0]['IP'])
        #print (self.IP)

    def getRestToken(self):
        try:
            url = "https://" + self.IP + "/rest-gateway/rest/api/v1/auth/token"
            headers = {
                'content-type': "application/json",
                'authorization': "Basic " + self.base64Str
            }
            payload = '{ "grant_type": "client_credentials" }'
            response = requests.request("POST", url, headers=headers, data=payload,verify=False)
            self.token = json.loads(response.text)['access_token']
            CM_Log.info("Get token succesful.. Token=" + self.token)
            
            # print("Getting REST Token....")
            # print (json.loads(my_json))
            return self.token

        except Exception:
            CM_Log.warning("Cannot sent REST request to get token.")
            CM_Log.warning("Ensure the NSP IP address in nspProperties.yaml config is reacble from the terminal.")
            return False

    def revokeRestToken(self):
            try:
                url = "https://" + self.IP + "/rest-gateway/rest/api/v1/auth/revocation"
                headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': "Basic " + self.base64Str
                }
                payload='token='+ self.token +'&token_type_hint=token'            
                response = requests.request("POST", url, headers=headers, data=payload, verify=False)
                CM_Log.info("Revoke token succesful.")
                #print(response.text)

            except Exception:
                CM_Log.warning("Cannot revoke token.")
                return False

            

def UT_session():
    x = nspPy_session()
    print  (x.encodeUserName())
    print  (x.base64Str)

    x.getRestToken()
    x.revokeRestToken()

    print ('done')
#
# Execute main program
if (__name__ == '__main__'):
    UT_session()


