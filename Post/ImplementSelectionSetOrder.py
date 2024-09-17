import mgear.shifter.custom_step as cstp
import maya.cmds as cmds

class CustomShifterStep(cstp.customShifterMainStep):
    """Custom Step description
    """

    def setup(self):
        
        self.name = "ImplementSelectionSetOrder"
        self.leftInnerEyeballSet = "LeftInnerEyeballDeformer"
        self.LeftLowerEyelidSet = "LeftLowerEyelidDeformers"
        self.LeftUpperEyelidSet = "LeftUpperEyelidDeformer"

        self.RightInnerEyeballSet = "RightInnerEyeballDeformers"
        self.RightLowerEyelidSet = "RightLowerEyelidDeformers"
        self.RightUpperEyelidSet = "RightUpperEyelidDeformers"

        self.eyeRingDeformersSet = "eyeRingDeformers"

        self.gimmickDeformerSet = "rig_deformers_grp"

        self.browDeformationSet = "browDeformationSet"

    def run(self):

        cmds.sets(self.leftInnerEyeballSet, edit = True, fe="CuckooRig_sets_grp")
        cmds.sets(self.LeftLowerEyelidSet, edit = True, fe="CuckooRig_sets_grp")
        cmds.sets(self.LeftUpperEyelidSet, edit = True, fe="CuckooRig_sets_grp")

        cmds.sets(self.RightInnerEyeballSet, edit = True, fe="CuckooRig_sets_grp")
        cmds.sets(self.RightLowerEyelidSet, edit = True, fe="CuckooRig_sets_grp")
        cmds.sets(self.RightUpperEyelidSet, edit = True, fe="CuckooRig_sets_grp")

        cmds.sets(self.eyeRingDeformersSet, edit = True, fe="CuckooRig_sets_grp")
        cmds.sets(self.gimmickDeformerSet, edit = True, fe="CuckooRig_sets_grp")

        cmds.sets(self.browDeformationSet, edit = True, fe="CuckooRig_sets_grp")
        

        return
