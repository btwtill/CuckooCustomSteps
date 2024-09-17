import mgear.shifter.custom_step as cstp
import maya.cmds as cmds

class CustomShifterStep(cstp.customShifterMainStep):
    """Custom Step description
    """

    def setup(self):
        
        self.name = "ImplementBrowRig"
        self.rigName = "CuckooRig"
        self.leftBrowTopNode = "brow_L_main_ctrl_grp"
        self.rightBrowTopNode = "brow_R_main_ctrl_grp"
        self.parentTarget = "upperJaw_C0_fk0_ctl"
        self.leftOuterEyeGeo = "Cuckoo_L_OuterEyes_GeoShape"
        self.rightOuterEyeGeo = "Cuckoo_R_OuterEyes_GeoShape"

        self.leftAutoFollowPinNode = "brow_L_autoEyeAnchor_UVpin"
        self.rightAutoFollowPinNode = "brow_R_autoEyeAnchor_UVpin"

        self.leftBrowExtrasRigHrcNode = "brow_R_Rig_hrc"
        self.rightBrowExtrasRigHrcNode = "brow_L_Rig_hrc"

    def run(self):
        print("+++++ Start Implementing Brow Rig ++++++")
        cmds.parent(self.leftBrowTopNode, self.parentTarget)
        cmds.parent(self.rightBrowTopNode, self.parentTarget)

        cmds.connectAttr(f"{self.leftOuterEyeGeo}.worldMesh[0]", f"{self.leftAutoFollowPinNode}.deformedGeometry")
        cmds.connectAttr(f"{self.rightOuterEyeGeo}.worldMesh[0]", f"{self.rightAutoFollowPinNode}.deformedGeometry")

        cmds.parent(self.leftBrowExtrasRigHrcNode, self.rigName)
        cmds.parent(self.rightBrowExtrasRigHrcNode, self.rigName)

        print("+++++ End Implementing Brow Rig ++++++")

        return
