import CM_Log
import xmlplain

class CM_xml2yml(object):
    def __init__(self, xmlFile, ymlFile):
        self.xmlFile = xmlFile
        self.ymlFile = ymlFile
    
    def toYml(self):
        try:
            # Read to plain object
            with open(self.xmlFile) as inf:
                root = xmlplain.xml_to_obj(inf, strip_space=True, fold_dict=True)
            # Output plain YAML
            with open(self.ymlFile, "w") as outf:
                xmlplain.obj_to_yaml(root, outf)
            CM_Log.info("Convertion XML to YML success")
            print "OK"

        except Exception:
            CM_Log.warning("Cannot convert XML to YML")
            return False

    def hello(self):
        print self.xmlFile

def UT_CM_xml2yml():
    xmlFile = ("../../../evemanager/data/templates/02-srlHost-dcgw-6-nodes-setup/srlHost-dcgw-6-nodes-setup.unl")
    ymlFile = ("../../../evemanager/data/templates/02-srlHost-dcgw-6-nodes-setup/srlHost-dcgw-6-nodes-setup.yml")
    x = CM_xml2yml(xmlFile, ymlFile)
    hello = x.toYml()

#
# Execute main program
if (__name__ == '__main__'):
    UT_CM_xml2yml()