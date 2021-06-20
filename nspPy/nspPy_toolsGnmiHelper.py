################################################################################
# NAME 
#   nspPy_topoBuilder.py
#
# DESCRIPTION
#   This file maintains the gnmi connection to the routers
# 
# HISTORY
#   dd-mm-yyyy - author - comment
#   09-06-2021 - Asad Arafat - Creation
################################################################################
import json
from pygnmi.client import gNMIclient


class gnmiHelper(object):
    def __init__(self):
        self.pathProfileData            = None

    def getBgpLuRoutes(self):
        host = ('172.23.160.35', '57400')
        # Body
        with gNMIclient(target=host, username='admin', password='admin', insecure=True) as gc:
             ## result = gc.get(path=['openconfig-interfaces:interfaces', 'openconfig-acl:acl'])
             ## result = gc.capabilities()
            result = gc.get(path=['/state/router/bgp/rib/label-ipv4/label-ipv4-statistics/prefix'])
            
        
        print (json.dumps(result, indent=4, sort_keys=True))


def UT_gnmiHelper():

    gh = gnmiHelper()

    print (gh.getBgpLuRoutes())
    

# Execute main program
if (__name__ == '__main__'):
    UT_gnmiHelper()