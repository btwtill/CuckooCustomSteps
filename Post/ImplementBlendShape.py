import mgear.shifter.custom_step as cstp
import maya.cmds as cmds

class CustomShifterStep(cstp.customShifterMainStep):
    """Custom Step description
    """

    def setup(self):
        
        self.name = "ImplementBlendShape"
        self.rigName = "CuckooRig"
        self.mainGeometry = "Cuckoo_Body_Geo"

        self.localBlendShape = "Cuckoo_Body_LocalGeo"


    def run(self):
        print("+++++ Start Implementing BlendShapes ++++++")
        
        localGeometryNode = cmds.createNode("transform", name = "Cuckoo_LocalGeometries")
        cmds.parent(localGeometryNode, self.rigName)
        cmds.addAttr(f"{self.rigName}", ln = "LocalGeometry", at = "enum", enumName = "OFF:ON", keyable=True)
        cmds.connectAttr(f"{self.rigName}.LocalGeometry", f"{localGeometryNode}.visibility")
        cmds.parent(self.localBlendShape, localGeometryNode)

        localBlendShape = cmds.blendShape(self.localBlendShape, self.mainGeometry, name = "MainBodyLocalRigsBlendShape")[0]
        cmds.setAttr(f"{localBlendShape}.{self.localBlendShape}", 1)

        print("+++++ End Implementing BlendShapes ++++++")
        return
