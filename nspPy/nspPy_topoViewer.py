################################################################################
# NAME 
#   nspPy_topoBuilder.py
#
# DESCRIPTION
#   This file maintains the rendering of JSON file from IP/Optim IETF network Topology
# 
# HISTORY
#   dd-mm-yyyy - author - comment
#   30-05-2021 - Asad Arafat - Creation
################################################################################
import json
import requests
import pprint
import nspPy_ipOptim
import nspPy_session
from jsonpath_ng import jsonpath, parse
import CM_Log
from pygnmi.client import gNMIclient


class topoViewer(object):
    def __init__(self):
        self.pathProfileData            = None
    
    def createNormaliseJson(self, networkIetf):
        jsonpath_expression_networkIetf = parse('$.response.data.network[*]')   ## find the json path from here https://jsonpath.com/
        links=[]
        nodes=[]
        topoJson = {}
        topoJson['nodes'] = []
        topoJson['links'] = []

        for match in jsonpath_expression_networkIetf.find(networkIetf):
            for link in match.value['link']:
                #print ('sourceNodeId: '+ link['source']['sourceNode'])
                #print ('destNodeId: '+ link['destination']['destNode'])
                sourceNodeId = link['source']['sourceNode']
                destNodeId   = link['destination']['destNode']

                for node in match.value['node']:
                    #print (node['nodeId'])
                    nodeId = node['nodeId']
                    if sourceNodeId == nodeId:
                        # print ('sourceNodeName: ' + node['teNodeAugment']['te']['teNodeId']['dottedQuad']['string'])
                        sourceNodeName = node['teNodeAugment']['te']['teNodeId']['dottedQuad']['string']
                        nodes.append([sourceNodeName])
                    if destNodeId == nodeId:
                        #print ('destNodeName: ' + node['teNodeAugment']['te']['teNodeId']['dottedQuad']['string'])
                        destNodeName = node['teNodeAugment']['te']['teNodeId']['dottedQuad']['string']
                        nodes.append([destNodeName])

                links.append([sourceNodeName,destNodeName])

        new_nodes = []
        for x in nodes:
            if not sorted(x) in new_nodes: 
                new_nodes.append(sorted(x))
        for x in new_nodes:
            topoJson['nodes'].append({"id": x, "group": 1})
        CM_Log.info(new_nodes)


        new_links = []
        for x in links:
            if not sorted(x) in new_links: 
                new_links.append(sorted(x))
        for x in new_links:
            topoJson['links'].append({"source": x[0], "target": x[1], "value": 10, "typeIp": "true", "typeBgpls": "false"})
        CM_Log.info(new_links)

        with open('./nspPy/template/topoIetf02.json', 'w') as outfile:
            json.dump(topoJson, outfile, indent=4)

def UT_topoViewer():
    x = nspPy_session.nspPy_session()
    x.encodeUserName()
    x.getRestToken()
    token = x.token
    urlHost = x.IPsdn 
    
    ip = nspPy_ipOptim.ipOptim()
    #network = json.load(open("./networkIetf.json"))
    network = ip.getNetworksIetf(urlHost,token)

    nsp_tv = topoViewer()
    nsp_tv.createNormaliseJson(network)

    x.revokeRestToken()
# Execute main program
if (__name__ == '__main__'):
    UT_topoViewer()