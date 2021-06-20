################################################################################
# NAME 
#   nspPy_topoBuilder.py
#
# DESCRIPTION
#   This file maintains the use case of vimplecom
#   [NRCP] -------------------------- compare -------------- [NFMP]
#     pcep lsp reserved                                        SNMP
#     interface bw calculated                                  Measured Interface and LSP BW
#     from lsp reservation
#                            
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
import pandas


class vimplecom(object):
    def __init__(self):
        self.pathProfileData            = None
    
    def jsonToExcel(self, jsonContainer, excelFile):
        pandas.DataFrame(jsonContainer).to_excel(excelFile)

    

def UT_vimplecom():
    x = nspPy_session.nspPy_session()
    x.encodeUserName()
    x.getRestToken()
    token = x.token
    urlHost = x.IPsdn 
    
    ip = nspPy_ipOptim.ipOptim()
    lspList = ip.getLspPath(urlHost,token)

    vmplcm = vimplecom()
    vmplcm.jsonToExcel(lspList, 'lspList.xlsx')


    x.revokeRestToken()


# Execute main program
if (__name__ == '__main__'):
    UT_vimplecom()