import mgear.shifter.custom_step as cstp
import mgear.rigbits as rigbits
import pymel.core as pm
import maya.cmds as cmds

class CustomShifterStep(cstp.customShifterMainStep):
    """Custom Step description

    """

    def setup(self):
        
        self.name = "ImplementSupportGimmickJoints"

        self.blendJointsMirrorList = ["arm_L0_0_jnt","arm_L0_4_jnt", "arm_L0_end_jnt", "leg_L0_0_jnt", "leg_L0_4_jnt", "leg_L0_end_jnt", 
                                      "thumb_L0_0_jnt", "thumb_L0_1_jnt", "thumb_L0_2_jnt", 
                                      "indexFinger_L1_0_jnt", "indexFinger_L1_1_jnt", "indexFinger_L1_2_jnt",
                                      "middleFinger_L1_0_jnt", "middleFinger_L1_1_jnt", "middleFinger_L1_2_jnt",
                                      "pinkyFinger_L1_0_jnt", "pinkyFinger_L1_1_jnt", "pinkyFinger_L1_2_jnt",
                                      "foot_L0_0_jnt"]
        
        self.blendJointsCenterList = ["spine_C0_3_jnt", "spine_C0_2_jnt", "spine_C0_1_jnt", "spine_C0_0_jnt"]

    def createGimmicJoints(self):
        
        for jnt in self.blendJointsCenterList:
            print(f"+++++ Create New Gimmick Joint at: {jnt}")
            jntName = pm.PyNode(jnt)
            newBlendedJnt = rigbits.addBlendedJoint(jntName)

            print(f"+++++ New Blended Joint: {newBlendedJnt}")
        
        for side in "LR":
            for jnt in self.blendJointsMirrorList:
                print(f"+++++ Create New Gimmick Joint at: {jnt}")
                jntName = pm.PyNode(jnt.replace("_L", f"_{side}"))
                newBlendedJnt = rigbits.addBlendedJoint(jntName)

                print(f"+++++ New Blended Joint: {newBlendedJnt}")

    def support_gimmick(self, gimmickJoint, supportJointPositions):
        print(f"+++++ Adding Support joints to: {gimmickJoint} +++++")
        print(f"+++++ Support Joint Positions: {supportJointPositions} +++++")

        for position in supportJointPositions:
            cmds.select(clear=True)
            cmds.select(gimmickJoint)
            supportJoint = rigbits.addSupportJoint()
            supportJoint[0].setTranslation(position)

    def createSupportJoints(self):
        #Order (front, back, left, right, up, down)
        leftShoulderPositions = [[0.0, -5.0, 0.0],
                                 [0.0, 6.0, 0.0],
                                 [0.0, 0.0, 7.0],
                                 [0.0, 0.0, -8.0]]
        rightShoulderPositions = [[0.0, -5.0, 0.0],
                                 [0.0, 6.0, 0.0],
                                 [0.0, 0.0, -7.0],
                                 [0.0, 0.0, 8.0]]
        self.support_gimmick("blend_arm_L0_0_jnt", leftShoulderPositions)
        self.support_gimmick("blend_arm_R0_0_jnt", rightShoulderPositions)

        leftElbowPositions = [[0.0, -3.0, 0.0],
                              [0.0, 2.5, 0.0],
                              [0.0, 0.0, 2.5],
                              [0.0, 0.0, -2.3]]
        rightElbowPositions = [[0.0, -3.0, 0.0],
                              [0.0, 2.5, 0.0],
                              [0.0, 0.0, -2.5],
                              [0.0, 0.0, 2.3]]
        self.support_gimmick("blend_arm_L0_4_jnt", leftElbowPositions)
        self.support_gimmick("blend_arm_R0_4_jnt", rightElbowPositions)

        leftWristPositions = [[0.0, -2.7, 0.0],
                              [0.0, 2.2, 0.0],
                              [0.0, 0.0, 1.7],
                              [0.0, 0.0, -2.2]]
        rightWristPositions = [[0.0, -2.7, 0.0],
                              [0.0, 2.2, 0.0],
                              [0.0, 0.0, -1.7],
                              [0.0, 0.0, 2.2]]
        self.support_gimmick("blend_arm_L0_end_jnt", leftWristPositions )
        self.support_gimmick("blend_arm_R0_end_jnt", rightWristPositions )

        leftThumbPositon = [[0.0, 0.0, -2.7],
                            [0.0, 0.0, 2.7],
                            [0.0, -2.4, 0.0],
                            [0.0, 1.5, 0.0]]
        rightThumbPositon = [[0.0, 0.0, 2.7],
                            [0.0, 0.0, -2.7],
                            [0.0, 2.4, 0.0],
                            [0.0, -1.5, 0.0]]
        self.support_gimmick("blend_thumb_L0_0_jnt", leftThumbPositon)
        self.support_gimmick("blend_thumb_R0_0_jnt", rightThumbPositon)

        leftThumb01Position = [[0.0, -1.8, 0.0],
                               [0.0, 2.0, 0.0]]
        rightThumb01Position = [[0.0, 1.8, 0.0],
                               [0.0, -2.0, 0.0]]
        self.support_gimmick("blend_thumb_L0_1_jnt", leftThumb01Position)
        self.support_gimmick("blend_thumb_R0_1_jnt", rightThumb01Position)
        
        leftThumb02Position = [[0.0, -1.2, 0.0],
                               [0.0, 1.0, 0.0]]
        rightThumb02Position = [[0.0, 1.2, 0.0],
                               [0.0, -1.0, 0.0]]
        self.support_gimmick("blend_thumb_L0_2_jnt", leftThumb02Position)
        self.support_gimmick("blend_thumb_R0_2_jnt", rightThumb02Position)
        
        leftFingerPositions = [[0.0, -1.0, 0.0],
                               [0.0, 1.0, 0.0]]
        rightFingerPositions = [[0.0, 1.0, 0.0],
                               [0.0, -1.0, 0.0]]
        
        leftFingerBlendJoints = ["blend_indexFinger_L1_0_jnt", "blend_indexFinger_L1_1_jnt", "blend_indexFinger_L1_2_jnt", 
                                 "blend_middleFinger_L1_0_jnt", "blend_middleFinger_L1_1_jnt","blend_middleFinger_L1_2_jnt",
                                 "blend_pinkyFinger_L1_0_jnt", "blend_pinkyFinger_L1_1_jnt", "blend_pinkyFinger_L1_2_jnt"]
        
        for side in "LR":
            for blend in leftFingerBlendJoints:
                if side == "L":
                    self.support_gimmick(blend, leftFingerPositions)
                else:
                    self.support_gimmick(blend.replace("_L", "_R"), rightFingerPositions)

        leftLegPositions = [[0.0, 10.0, 0.0],
                            [0.0, -10.0, 0.0],
                            [0.0, 0.0, -7.0]]
        rightLegPositions = [[0.0, 10.0, 0.0],
                            [0.0, -10.0, 0.0],
                            [0.0, 0.0, 7.0]]
        self.support_gimmick("blend_leg_L0_0_jnt", leftLegPositions)
        self.support_gimmick("blend_leg_R0_0_jnt", rightLegPositions)
        
        leftKneePositions = [[0.0, 4.3, 0.0],
                             [0.0, -5.5, 0.0],
                             [0.0, 0.0, -4.3],
                             [0.0, 0.0, 4.5]]
        rightKneePositions = [[0.0, 4.3, 0.0],
                             [0.0, -5.5, 0.0],
                             [0.0, 0.0, 4.3],
                             [0.0, 0.0, -4.5]]
        self.support_gimmick("blend_leg_L0_4_jnt", leftKneePositions)
        self.support_gimmick("blend_leg_R0_4_jnt", rightKneePositions)

        leftAnklePositions = [[0.0, 5.0, 0.0],
                              [0.0, -4.5, 0.0],
                              [0.0, 0.0, -4.0],
                              [0.0, 0.0, 4.3]]
        rightAnklePositions = [[0.0, 5.0, 0.0],
                              [0.0, -4.5, 0.0],
                              [0.0, 0.0, 4.0],
                              [0.0, 0.0, -4.3]]
        self.support_gimmick("blend_leg_L0_end_jnt", leftAnklePositions)
        self.support_gimmick("blend_leg_R0_end_jnt", rightAnklePositions)

        leftToePositions = [[0.0, 3.0, 0.0],
                            [0.0, -2.5, 0.0],
                            [0.0, 0.0, -4.8],
                            [0.0, 0.0, 3.7]]
        rightToePositions = [[0.0, -3.0, 0.0],
                            [0.0, 2.5, 0.0],
                            [0.0, 0.0, 4.8],
                            [0.0, 0.0, -3.7]]
        self.support_gimmick("blend_foot_L0_0_jnt", leftToePositions)
        self.support_gimmick("blend_foot_R0_0_jnt", rightToePositions)

        chestPositons = [[0.0, 0.0, 12.0],
                         [0.0, 0.0, -12.0]]
        self.support_gimmick("blend_spine_C0_3_jnt", chestPositons)

        spinePositions = [[0.0, 0.0, 12.0],
                          [0.0, 0.0, -12.0],
                          [12.0, 0.0, 0.0],
                          [-12.0, 0.0, 0.0]]
        
        spineBlendJoints = ["blend_spine_C0_2_jnt", "blend_spine_C0_1_jnt"]

        for blend in spineBlendJoints:
            self.support_gimmick(blend, spinePositions)

        cmds.rename("blendSupport_2_spine_C0_2_jnt", "blendSupport_L2_spine_C0_2_jnt")
        cmds.rename("blendSupport_3_spine_C0_2_jnt", "blendSupport_R2_spine_C0_2_jnt")

        cmds.rename("blendSupport_2_spine_C0_1_jnt", "blendSupport_L2_spine_C0_1_jnt")
        cmds.rename("blendSupport_3_spine_C0_1_jnt", "blendSupport_R2_spine_C0_1_jnt")

        return
    
    def run(self):

        self.createGimmicJoints()
        self.createSupportJoints()

        return
