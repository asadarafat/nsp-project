################################################################################
# NAME 
#   nspPy_deviceManager.py
#
# DESCRIPTION
#   This file maintains NSP Device Manager app handling mechanism
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

## Constant

## NSP 20.6
## GLBL_NSP_DEVICE_MANAGER_END_POINT_PORT                  = ":8545"

## NSP > 20.9
GLBL_NSP_DEVICE_MANAGER_END_POINT_PORT               = ":8548"

GLBL_NSP_DEVICE_MANAGER_ADDRESS_RULE_FILENAME           = "/Users/aarafat/PycharmProjects/NSP-Project/nspPy/template/DM/DM_addresRule.yaml"

GLBL_NSP_DEVICE_MANAGER_USER_SNMP_FILENAME              = "/Users/aarafat/PycharmProjects/NSP-Project/nspPy/template/DM/DM_userSnmp.yaml"
GLBL_NSP_DEVICE_MANAGER_USER_CLI_FILENAME               = "/Users/aarafat/PycharmProjects/NSP-Project/nspPy/template/DM/DM_userCLi.yaml"
GLBL_NSP_DEVICE_MANAGER_USER_GRPC_FILENAME              = "/Users/aarafat/PycharmProjects/NSP-Project/nspPy/template/DM/DM_userGrpc.yaml"
GLBL_NSP_DEVICE_MANAGER_USER_NETCONF_FILENAME           = "/Users/aarafat/PycharmProjects/NSP-Project/nspPy/template/DM/DM_userNetconf.yaml"

GLBL_NSP_DEVICE_MANAGER_PROTOCOL_SNMP_FILENAME          = "/Users/aarafat/PycharmProjects/NSP-Project/nspPy/template/DM/DM_protocolSmnp.yaml"
GLBL_NSP_DEVICE_MANAGER_PROTOCOL_CLI_FILENAME           = "/Users/aarafat/PycharmProjects/NSP-Project/nspPy/template/DM/DM_protocolCLi.yaml"
GLBL_NSP_DEVICE_MANAGER_PROTOCOL_GRPC_FILENAME          = "/Users/aarafat/PycharmProjects/NSP-Project/nspPy/template/DM/DM_protocolGrpc.yaml"
GLBL_NSP_DEVICE_MANAGER_PROTOCOL_NETCONF_FILENAME       = "/Users/aarafat/PycharmProjects/NSP-Project/nspPy/template/DM/DM_protocolNetconf.yaml"

GLBL_NSP_DEVICE_MANAGER_NE_MEDIATION_POLICY_FILENAME    = "/Users/aarafat/PycharmProjects/NSP-Project/nspPy/template/DM/DM_neMediationPolicy.yaml"

GLBL_NSP_DEVICE_MANAGER_NE_REACHABILITY_PING_POLICY_FILENAME    = "/Users/aarafat/PycharmProjects/NSP-Project/nspPy/template/DM/DM_reachabilityPing.yaml"
GLBL_NSP_DEVICE_MANAGER_NE_REACHABILITY_SNMP_POLICY_FILENAME    = "/Users/aarafat/PycharmProjects/NSP-Project/nspPy/template/DM/DM_reachabilitySnmp.yaml"

GLBL_NSP_DEVICE_MANAGER_DISCOVERY_RULE_FILENAME   = "/Users/aarafat/PycharmProjects/NSP-Project/nspPy/template/DM/DM_discoveryRule.yaml"


class deviceManager(object):
    def __init__(self):
        self.addressRuleData            = None
        self.addressUserData            = None
        self.addressProtocoData         = None
        self.NeMediationPolicyData      = None
        self.addressRuleFdn             = None
        self.userFdn                    = None
        self.protocolFdn                = None

        self.MediationPolicyFdn         = None
        self.MediationPolicySnmpFdn     = None
        self.MediationPolicyGrpcFdn     = None
        self.MediationPolicyCliFdn      = None
        self.MediationPolicyNetconfFdn  = None

        self.reachabilityPolicyPingFdn  = None
        self.reachabilityPolicySnmpFdn  = None

        self.DiscoveryRuleData          = None  
        self.discovertRuleFdn           = None  


    def createAddressRule(self, urlHost,token):
        with open(GLBL_NSP_DEVICE_MANAGER_ADDRESS_RULE_FILENAME) as file:
            self.addressRuleData = yaml.load(file, Loader=yaml.FullLoader)  

        url = 'https://' + urlHost + GLBL_NSP_DEVICE_MANAGER_END_POINT_PORT + '/mdm-necontrol-rest-api-app/api/v1/neControl/discoveryrule'
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer " + token
            }
        payload = json.dumps(self.addressRuleData, indent=4)
        response = requests.request("POST", url, headers=headers, verify=False, data=payload)
        response = json.loads(response.text)
        CM_Log.info("createAddressResponse:\n" + json.dumps(response, indent=4))
        self.addressRuleFdn = response['response']['data']['fdn']['fdn']
        CM_Log.info("AddressRuleFdn: " + self.addressRuleFdn)

        return self.addressRuleFdn

    def createUser(self, urlHost, kind, token):
        if  kind == "snmp":
            with open(GLBL_NSP_DEVICE_MANAGER_USER_SNMP_FILENAME) as file:
                self.userData = yaml.load(file, Loader=yaml.FullLoader) 
        elif  kind == "grpc":
            with open(GLBL_NSP_DEVICE_MANAGER_USER_GRPC_FILENAME) as file:
                self.userData = yaml.load(file, Loader=yaml.FullLoader) 
        elif  kind == "cli":
            with open(GLBL_NSP_DEVICE_MANAGER_USER_CLI_FILENAME) as file:
                self.userData = yaml.load(file, Loader=yaml.FullLoader) 
        elif  kind == "netconf":
            with open(GLBL_NSP_DEVICE_MANAGER_USER_NETCONF_FILENAME) as file:
                self.userData = yaml.load(file, Loader=yaml.FullLoader) 

        url = 'https://' + urlHost + GLBL_NSP_DEVICE_MANAGER_END_POINT_PORT + '/mdm-necontrol-rest-api-app/api/v1/neuser'
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer " + token
            }
        payload = json.dumps(self.userData, indent=4)
        CM_Log.info("userData: " + payload)

        response = requests.request("POST", url, headers=headers, verify=False, data=payload)
        response = json.loads(response.text)
        CM_Log.info("createUserResponse:\n" + json.dumps(response, indent=4))

        self.userFdn = response['response']['data']['fdn']['fdn']
        CM_Log.info("UserFdn: " + self.userFdn)

        return self.userFdn

    def createProtocol(self, urlHost, kind, token):
        if  kind == "snmp":
            with open(GLBL_NSP_DEVICE_MANAGER_PROTOCOL_SNMP_FILENAME) as file:
                self.protocolData = yaml.load(file, Loader=yaml.FullLoader) 
        elif  kind == "grpc":
            with open(GLBL_NSP_DEVICE_MANAGER_PROTOCOL_GRPC_FILENAME) as file:
                self.protocolData = yaml.load(file, Loader=yaml.FullLoader) 
        elif  kind == "cli":
            with open(GLBL_NSP_DEVICE_MANAGER_PROTOCOL_CLI_FILENAME) as file:
                self.protocolData = yaml.load(file, Loader=yaml.FullLoader) 
        elif  kind == "netconf":
            with open(GLBL_NSP_DEVICE_MANAGER_PROTOCOL_NETCONF_FILENAME) as file:
                self.protocolData = yaml.load(file, Loader=yaml.FullLoader) 

        url = 'https://' + urlHost + GLBL_NSP_DEVICE_MANAGER_END_POINT_PORT + '/mdm-necontrol-rest-api-app/api/v1/neprotocol'
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer " + token
            }
        payload = json.dumps(self.protocolData, indent=4)
        CM_Log.info("protocolData: " + payload)

        response = requests.request("POST", url, headers=headers, verify=False, data=payload)
        response = json.loads(response.text)
        CM_Log.info("createProtocolResponse: " + kind + "\n" + json.dumps(response, indent=4))

        self.protocolFdn = response['response']['data']['fdn']['fdn']
        CM_Log.info("ProtocolFdn: " + self.protocolFdn)

        return self.protocolFdn

    def createNeMediationPolicy(self, policyPrefix, urlHost, kind, token):
        with open(GLBL_NSP_DEVICE_MANAGER_NE_MEDIATION_POLICY_FILENAME) as file:
            self.neMediationPolicyData = yaml.load(file, Loader=yaml.FullLoader)
               
        payload = json.dumps(self.neMediationPolicyData, indent=4)
        self.neMediationPolicyData['dto']['policyName'] = policyPrefix + '-' + kind + 'MediationPolicy'
        self.neMediationPolicyData['dto']['policyType'] = kind.upper()
        self.neMediationPolicyData['dto']['user']['dto']['fdn']['fdn'] = self.createUser(urlHost, kind, token)
        self.neMediationPolicyData['dto']['neCommProtocol']['dto']['fdn']['fdn'] = self.createProtocol(urlHost, kind, token)

        url = 'https://' + urlHost + GLBL_NSP_DEVICE_MANAGER_END_POINT_PORT + '/mdm-necontrol-rest-api-app/api/v1/nemediationpolicy'
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer " + token
            }
        payload = json.dumps(self.neMediationPolicyData, indent=4)
        CM_Log.info("neMediationlDataTemplateEdit_" + kind + ":\n" + payload)

        response = requests.request("POST", url, headers=headers, verify=False, data=payload)
        response = json.loads(response.text)

        self.MediationPolicyFdn = response['response']['data']['fdn']['fdn']
        CM_Log.info("MediationPolicyFdn_" + kind + ":\n" + self.MediationPolicyFdn)
        CM_Log.info("createMediationPolicyResponse_" + kind + ":\n" + json.dumps(response, indent=4))

        if  kind == "snmp":
            self.MediationPolicySnmpFdn = response['response']['data']['fdn']['fdn']
            return self.MediationPolicySnmpFdn 
        elif  kind == "grpc":
            self.MediationPolicyGrpcFdn = response['response']['data']['fdn']['fdn']
            return self.MediationPolicyGrpcFdn 
        elif  kind == "cli":
            self.MediationPolicyCliFdn = response['response']['data']['fdn']['fdn']
            return self.MediationPolicyCliFdn 
        elif  kind == "netconf":
            self.MediationPolicyNetconfFdn = response['response']['data']['fdn']['fdn']
            return self.MediationPolicyNetconfFdn 
    
    # list mediation policy
    def listNeMediationPolicy(self, policyPrefix, urlHost, token): 
        url = 'https://' + urlHost + GLBL_NSP_DEVICE_MANAGER_END_POINT_PORT + '/mdm-necontrol-rest-api-app/api/v1/query-multi/?query=select%20policies,%20policies.user,%20policies.neCommProtocol%20from%20mediationpolicy_NeMediationPolicy%20policies%20where%20(policies.sourceType=%20:arg1)&arg1=8'
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer " + token
            }
        response = requests.request("GET", url, headers=headers, verify=False)
        response = json.loads(response.text)
        CM_Log.info("listMediationPolicyResponse__allPolicyPrefix_allKind: " + "\n" + json.dumps(response, indent=4))   

        
    def deleteNeMediationPolicy(self, urlHost, MediationPolicyFdn, token):
        url = 'https://' + urlHost + GLBL_NSP_DEVICE_MANAGER_END_POINT_PORT + '/mdm-necontrol-rest-api-app/api/v1/nemediationpolicy/fdn:model:mediationpolicy:' + MediationPolicyFdn
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer " + token
            }
        response = requests.request("DELETE", url, headers=headers, verify=False)
        response = json.loads(response.text)
        CM_Log.info("deleteNeMediationPolicyResponse: " + "\n" + json.dumps(response, indent=4)) 

    def createNeReachabilityPolicy(self, policyPrefix, urlHost, kind, token):
        if  kind == "ping":
            with open(GLBL_NSP_DEVICE_MANAGER_NE_REACHABILITY_PING_POLICY_FILENAME) as file:
                self.reachbilityData = yaml.load(file, Loader=yaml.FullLoader) 
        elif  kind == "snmp":
            with open(GLBL_NSP_DEVICE_MANAGER_NE_REACHABILITY_SNMP_POLICY_FILENAME) as file:
                self.reachbilityData = yaml.load(file, Loader=yaml.FullLoader) 
        
        self.reachbilityData['dto']['name'] = policyPrefix + '-' + kind + 'ReachabilityPolicy'
        
        url = 'https://' + urlHost + GLBL_NSP_DEVICE_MANAGER_END_POINT_PORT + '/mdm-necontrol-rest-api-app/api/v1/neControl/discoveryrule'
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer " + token
            }
        payload = json.dumps(self.reachbilityData, indent=4)

        response = requests.request("POST", url, headers=headers, verify=False, data=payload)
        response = json.loads(response.text)
        CM_Log.info("createNeReachabilityResponse: " + kind + "\n" + json.dumps(response, indent=4))

        if  kind == "ping":
            self.reachabilityPolicyPingFdn = response['response']['data']['fdn']['fdn']
            CM_Log.info(policyPrefix + "-ReachabilityPolicyPingFdn: " + self.reachabilityPolicyPingFdn)
            return self.reachabilityPolicyPingFdn 
        elif  kind == "snmp":
            self.reachabilityPolicySnmpFdn = response['response']['data']['fdn']['fdn']
            CM_Log.info(policyPrefix + "-ReachabilityPolicySnmpFdn: " + self.reachabilityPolicySnmpFdn)
            return self.reachabilityPolicySnmpFdn 
    
    def deleteNeReachabilityPolicy(self, urlHost, ReachabilityPolicyFdn, token):
        url = 'https://' + urlHost + GLBL_NSP_DEVICE_MANAGER_END_POINT_PORT + '/mdm-necontrol-rest-api-app/api/v1/neControl/discoveryrule/fdn:model:necontrol:' + ReachabilityPolicyFdn
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer " + token
            }
        response = requests.request("DELETE", url, headers=headers, verify=False)
        response = json.loads(response.text)
        CM_Log.info("deleteNeMediationPolicyResponse: " + "\n" + json.dumps(response, indent=4)) 

    def createDiscoveryRule(self, policyPrefix, urlHost, token):
        with open(GLBL_NSP_DEVICE_MANAGER_DISCOVERY_RULE_FILENAME) as file:
            self.DiscoveryRuleData = yaml.load(file, Loader=yaml.FullLoader)
        
        self.DiscoveryRuleData['dto']['name'] = policyPrefix + '-' + 'DiscoveryRule'
        self.DiscoveryRuleData['dto']['ipAddrRules'][0]['fdn'] = self.addressRuleFdn
        self.DiscoveryRuleData['dto']['neROMedPolicies'][0]['fdn'] = self.MediationPolicySnmpFdn
        self.DiscoveryRuleData['dto']['neROMedPolicies'][1]['fdn'] = self.MediationPolicyGrpcFdn
        self.DiscoveryRuleData['dto']['neROMedPolicies'][2]['fdn'] = self.MediationPolicyCliFdn
        self.DiscoveryRuleData['dto']['neROMedPolicies'][3]['fdn'] = self.MediationPolicyNetconfFdn
        self.DiscoveryRuleData['dto']['neRWMedPolicies'][0]['fdn'] = self.MediationPolicySnmpFdn
        self.DiscoveryRuleData['dto']['neRWMedPolicies'][1]['fdn'] = self.MediationPolicyGrpcFdn
        self.DiscoveryRuleData['dto']['neRWMedPolicies'][2]['fdn'] = self.MediationPolicyCliFdn
        self.DiscoveryRuleData['dto']['neRWMedPolicies'][3]['fdn'] = self.MediationPolicyNetconfFdn
        self.DiscoveryRuleData['dto']['neTrapMedPolicies'][0]['fdn'] = self.MediationPolicySnmpFdn
        self.DiscoveryRuleData['dto']['neTrapMedPolicies'][1]['fdn'] = self.MediationPolicyGrpcFdn
        self.DiscoveryRuleData['dto']['neTrapMedPolicies'][2]['fdn'] = self.MediationPolicyCliFdn
        self.DiscoveryRuleData['dto']['neTrapMedPolicies'][3]['fdn'] = self.MediationPolicyNetconfFdn

        self.DiscoveryRuleData['dto']['neReachabilityPolicies'][0]['fdn'] = self.reachabilityPolicyPingFdn
        self.DiscoveryRuleData['dto']['neReachabilityPolicies'][1]['fdn'] = self.reachabilityPolicySnmpFdn

        payload = json.dumps(self.DiscoveryRuleData, indent=4)
        CM_Log.info("createDiscoveryRuleDaya: " + "\n" +payload)

        url = 'https://' + urlHost + GLBL_NSP_DEVICE_MANAGER_END_POINT_PORT + '/mdm-necontrol-rest-api-app/api/v1/neControl/discoveryrule'
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer " + token
            }
        response = requests.request("POST", url, headers=headers, verify=False, data=payload)
        response = json.loads(response.text)
        CM_Log.info("createDiscoveryRuleResponse: " + "\n" + json.dumps(response, indent=4))
        self.discovertRuleFdn = response['response']['data']['fdn']['fdn']
        CM_Log.info(policyPrefix + "-ReachabilityPolicySnmpFdn: " + self.discovertRuleFdn)
        return self.discovertRuleFdn

    def deleteDiscoveryRule(self, urlHost, DiscovertRuleFdn, token):
        url = 'https://' + urlHost + GLBL_NSP_DEVICE_MANAGER_END_POINT_PORT + '/mdm-necontrol-rest-api-app/api/v1/neControl/discoveryrule/fdn:model:necontrol:' + DiscovertRuleFdn
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer " + token
            }
        response = requests.request("DELETE", url, headers=headers, verify=False)
        response = json.loads(response.text)
        CM_Log.info("deleteNeMediationPolicyResponse: " + "\n" + json.dumps(response, indent=4)) 

def UT_deviceManager():
    x = nspPy_session.nspPy_session()
    x.encodeUserName()
    x.getRestToken()
    token = x.token
    urlHost = x.IP
    policyPrefix = "SROS"

    dm = deviceManager()
    dm.createAddressRule(urlHost, token)
    dm.createUser(urlHost, "snmp", token)
    dm.createUser(urlHost, "cli", token)
    dm.createUser(urlHost, "grpc", token)
    dm.createUser(urlHost, "netconf", token)
    dm.createProtocol(urlHost, "snmp", token)
    dm.createProtocol(urlHost, "cli", token)
    dm.createProtocol(urlHost, "grpc", token)
    dm.createProtocol(urlHost, "netconf", token)
    dm.createNeMediationPolicy(policyPrefix, urlHost, "snmp", token)
    dm.createNeMediationPolicy(policyPrefix, urlHost, "cli", token)
    dm.createNeMediationPolicy(policyPrefix, urlHost, "grpc", token)
    dm.createNeMediationPolicy(policyPrefix, urlHost, "netconf", token)
    dm.listNeMediationPolicy(policyPrefix, urlHost, token)
    dm.createNeReachabilityPolicy(policyPrefix, urlHost, "ping", token)
    dm.createNeReachabilityPolicy(policyPrefix, urlHost, "snmp", token)

    dm.createDiscoveryRule(policyPrefix, urlHost, token)

    ## Unit Test For Device Manager Resources Deletion.
    ## Hard coding the FDN.
    ## Todo: mechanism to dyamicaly get the FDN from resource listing method.
    ## Deletion of Discovery rule shall take first precedence before deleting other resources. As the other resources cannot be deleted if it attached to the Discovery Rule.
    snmpFdn         = dm.MediationPolicySnmpFdn
    cliFdn          = dm.MediationPolicyCliFdn
    grpcFdn         = dm.MediationPolicyGrpcFdn
    netconfFdn      = dm.MediationPolicyNetconfFdn
    reachPingFdn    = dm.reachabilityPolicyPingFdn
    reachSnmpFdn    = dm.reachabilityPolicySnmpFdn
    discoveryFdn    = dm.discovertRuleFdn

    #dm.deleteDiscoveryRule(urlHost, discoveryFdn, token)
    #dm.deleteNeMediationPolicy(urlHost, snmpFdn, token)
    #dm.deleteNeMediationPolicy(urlHost, cliFdn, token)
    #dm.deleteNeMediationPolicy(urlHost, grpcFdn, token)
    #dm.deleteNeMediationPolicy(urlHost, netconfFdn, token)
    #dm.deleteNeReachabilityPolicy(urlHost, reachPingFdn, token)
    #dm.deleteNeReachabilityPolicy(urlHost, reachSnmpFdn, token)
    

    x.revokeRestToken()

#
# Execute main program
if (__name__ == '__main__'):
    UT_deviceManager()


