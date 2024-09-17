import mgear.shifter.custom_step as cstp
import maya.cmds as cmds

class CustomShifterStep(cstp.customShifterMainStep):
    """Custom Step description
    """

    def setup(self):
        
        self.name = "ImplementingEyeRig"
        self.rigName = "CuckooRig"

        self.topNode = "Eyes_rig"
        self.parentTarget = "upperJaw_C0_fk0_ctl"

        self.LeftRingTopNode = "eye_L_ring_rig"
        self.RightRingTopNode = "eye_R_ring_rig"
        
    def run(self):
        print("+++++ Start Implementing Eye Rig ++++++")

        cmds.parent(self.topNode, self.parentTarget)
        cmds.parent(self.LeftRingTopNode, self.rigName)
        cmds.parent(self.RightRingTopNode, self.rigName)

        print("+++++ End Implementing Eye Rig ++++++")

        blendShape = "LocalDeformationShape"
        leftFootCtrl = "leg_R0_ik_ctl"
        rightFootCtrl = "leg_L0_ik_ctl"

        cmds.addAttr(leftFootCtrl, ln="FootSquashToe", at = "float", minValue=0, maxValue=1, defaultValue = 0, keyable=True)
        cmds.addAttr(leftFootCtrl, ln="FootSquashHeel", at = "float", minValue=0, maxValue=1, defaultValue = 0, keyable=True)

        cmds.connectAttr(f"{leftFootCtrl}.FootSquashToe", f"{blendShape}.Cuckoo_L_frontFootSquash")
        cmds.connectAttr(f"{leftFootCtrl}.FootSquashHeel", f"{blendShape}.Cuckoo_L_heelFootSquash")

        cmds.addAttr(rightFootCtrl, ln="FootSquashToe", at = "float", minValue=0, maxValue=1, defaultValue = 0, keyable=True)
        cmds.addAttr(rightFootCtrl, ln="FootSquashHeel", at = "float", minValue=0, maxValue=1, defaultValue = 0, keyable=True)

        cmds.connectAttr(f"{rightFootCtrl}.FootSquashToe", f"{blendShape}.Cuckoo_R_frontFootSquash")
        cmds.connectAttr(f"{rightFootCtrl}.FootSquashHeel", f"{blendShape}.Cuckoo_R_heelFootSquash")

        return
