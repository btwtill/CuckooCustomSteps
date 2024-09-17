import mgear.shifter.custom_step as cstp
import maya.cmds as cmds
import os
import re
import math
import maya.mel as mel
import pymel.core as pm
from tlpf_toolkit.utils import ZeroOffsetFunction
from tlpf_toolkit.locator import LocatorFunctions
import maya.cmds as cmds
from tlpf_toolkit.mtrx import MatrixFunctions as mtrxFunc

class CustomShifterStep(cstp.customShifterMainStep):
    """Custom Step description
    """

    def setup(self):
        
        self.name = "ImplementLipRig"
        self.rigName = "CuckooRig"
        self.lipLocalRigTopNode = "lipLocalRig"

        self.localLipControlsHirarchy = "lipLocal_controls"
        self.mainGeometry = "Cuckoo_Body_Geo"
        self.mainGemoetryShape = "Cuckoo_Body_GeoShape"

        self.localLipList = []
        self.sitckyObjects = []

        self.upperReferenceSet = ["upperJaw_C0_1_jnt", "upperJaw_C0_2_jnt", "upperJaw_C0_3_jnt", "upperJaw_C0_4_jnt", "upperJaw_C0_5_jnt"]
        self.lowerReferenceSet = ["lowerJaw_C0_1_jnt", "lowerJaw_C0_2_jnt", "lowerJaw_C0_3_jnt", "lowerJaw_C0_4_jnt"]


    def get_edges_from_vertex(self, mesh, vertex_index):
        vertex = mesh.vtx[vertex_index]
        connected_edges = vertex.connectedEdges()
        edge_indices = [edge.index() for edge in connected_edges]
        return edge_indices

    def calcDistanceFromVectors(self, vec1, vec2) -> float:

        dist = math.sqrt(math.pow(vec1[0] - vec2[0], 2) + math.pow(vec1[1] - vec2[1], 2) + math.pow(vec1[2] - vec2[2], 2))
        return dist

    def calulateClosestDeformJointFromSelectionSet(self, referenceItem, selectionSet):
        
        self.closestSetMember = ""
        currentSmalestDistance = None
        referencePos = cmds.xform(referenceItem, query = True, t = True, ws = True)

        for member in selectionSet:
            memberPos = cmds.xform(member, query = True, t = True, ws = True)
            distance = self.calcDistanceFromVectors(referencePos, memberPos)

            if currentSmalestDistance == None:
                currentSmalestDistance = distance
                self.closestSetMember = member
            elif distance < currentSmalestDistance:
                currentSmalestDistance = distance
                self.closestSetMember = member

        return self.closestSetMember

    def getLocalLipControls(self):
        for grp in cmds.listRelatives(self.localLipControlsHirarchy, children =True):
            control = cmds.listRelatives(grp, children = True, ad =True)[1]
            self.localLipList.append(control)
    
    def buildRivet(baseName, orientationObject, slide = True):

        edgeSelection = cmds.ls(sl=True)[0]

        meshShape = edgeSelection.split(".")[0] + "Shape"

        index = re.search(r"\[([A-Za-z0-9_]+)\]", edgeSelection)

        index = int(index.group(1))

        edgeToCurveNode = cmds.createNode("curveFromMeshEdge", name = baseName + "Rivet_meshEdgeToCurve")
        cmds.setAttr(f"{edgeToCurveNode}.edgeIndex[0]", index)
        pciNode = cmds.createNode("pointOnCurveInfo", name = baseName + "Rivet_pci")
        rivetLocator = cmds.spaceLocator(name = baseName + "Rivet_pos")[0]

        cmds.connectAttr(f"{meshShape}.worldMesh[0]", f"{edgeToCurveNode}.inputMesh")
        cmds.connectAttr(f"{edgeToCurveNode}.outputCurve", f"{pciNode}.inputCurve")
        cmds.setAttr(f"{pciNode}.turnOnPercentage", 1)
        cmds.connectAttr(f"{pciNode}.position", f"{rivetLocator}.translate")
        cmds.orientConstraint(orientationObject, rivetLocator)

    def createStickyControl(self, localControl, mesh, scaleDecompose,  orientObject):


        offsetGroup = cmds.listRelatives(localControl, parent=True)[0]
        #duplicate shape
        stickyControl = cmds.duplicate(localControl, name = f"{localControl.replace('ctrl', 'stickyCtrl')}")[0]

        print(f"+++++ new Sticky Control: {stickyControl}")

        closestPointOnMeshNode = cmds.createNode("closestPointOnMesh", name = f"{localControl}_closestPoint_tmpNode")
        
        tmpdecomposeNode = cmds.createNode("decomposeMatrix", name = f"{localControl}_wrldMtxDecompose_tmp")
        
        cmds.connectAttr(f"{localControl}.worldMatrix[0]", f"{tmpdecomposeNode}.inputMatrix")
        cmds.connectAttr(f"{tmpdecomposeNode}.outputTranslate", f"{closestPointOnMeshNode}.inPosition")
        cmds.connectAttr(f"{mesh + 'Shape'}.worldMesh[0]", f"{closestPointOnMeshNode}.inMesh")
        vertex_index = cmds.getAttr(f"{closestPointOnMeshNode}.closestVertexIndex")

        mesh = pm.PyNode(mesh)
        edges_from_vertex = self.get_edges_from_vertex(mesh, vertex_index)
        print(f"Edges connected to vertex {vertex_index}: {edges_from_vertex}")

        cmds.select(clear=True)
        cmds.select(f"{mesh}.e[{edges_from_vertex[0]}]")

        LocatorFunctions.buildRivet(f"{stickyControl}_rivet_pin", orientObject)

        cmds.delete([closestPointOnMeshNode, tmpdecomposeNode])

        stickyPin = f"{stickyControl}_rivet_pinRivet_pos"

        cmds.parent(stickyControl, stickyPin)

        ZeroOffsetFunction.TimZero([stickyControl],["_grp", "_off"])

        backtrackNode = cmds.createNode("multiplyDivide", name = f"{stickyControl}_backtrackMultiply")
            
        controlsOffsetNode = cmds.listRelatives(stickyControl, parent=True)[0]

        for channel in "XYZ":
            cmds.connectAttr(f"{stickyControl}.translate{channel}", f"{backtrackNode}.input1{channel}")
            cmds.setAttr(f"{backtrackNode}.input2{channel}", -1)
            cmds.connectAttr(f"{backtrackNode}.output{channel}", f"{controlsOffsetNode}.translate{channel}")

        cmds.parent(stickyControl, world=True)

        cmds.connectAttr(f"{controlsOffsetNode}.worldMatrix[0]", f"{stickyControl}.offsetParentMatrix")

        scaleMultiplyNode = cmds.createNode("multiplyDivide", name = f"{stickyControl}_scaleDivide_fNode")
        cmds.setAttr(f"{scaleMultiplyNode}.operation", 2)

        for channel in "XYZ":
            cmds.setAttr(f"{stickyControl}.translate{channel}", 0)
            cmds.setAttr(f"{stickyControl}.rotate{channel}", 0)
            cmds.setAttr(f"{stickyControl}.scale{channel}", 1)
                        
            cmds.connectAttr(f"{stickyControl}.translate{channel}", f"{scaleMultiplyNode}.input1{channel}")
            cmds.connectAttr(f"{scaleMultiplyNode}.output{channel}", f"{localControl}.translate{channel}")
            cmds.connectAttr(f"{scaleDecompose}.outputScale{channel}", f"{scaleMultiplyNode}.input2{channel}")

        for channel in "XYZ":
            cmds.connectAttr(f"{scaleDecompose}.outputScale{channel}", f"{stickyControl}.scale{channel}")

            cmds.setAttr(f"{stickyControl}.scale{channel}", lock = True, keyable=False, channelBox = False)
            cmds.setAttr(f"{stickyControl}.rotate{channel}", lock = True, keyable=False, channelBox = False)


        return stickyControl,stickyPin



    def run(self):
        print("+++++ Implement Lip Rig +++++")
        print("+++++ Get Local Lip Controls")

        self.getLocalLipControls()
        print(f"++++ Local Lip Controls: {self.localLipList}")
        
        stickyControlHirarchy = cmds.createNode("transform", name = "lipControls_hrc")
        stickyPinHirarchy = cmds.createNode("transform", name = "lipPin_hrc")

        headScaleDecompose = cmds.createNode("decomposeMatrix", name = "SquishLocalRigScaleDecomposition_fNode")
        cmds.connectAttr(f"neck_C0_head_ctl.worldMatrix[0]", f"{headScaleDecompose}.inputMatrix")

        for control in self.localLipList:
            if "lower" in control:
                self.sitckyObjects.append(self.createStickyControl(control, self.mainGeometry, headScaleDecompose, self.calulateClosestDeformJointFromSelectionSet(control, self.lowerReferenceSet)))
            else:
                self.sitckyObjects.append(self.createStickyControl(control, self.mainGeometry, headScaleDecompose, self.calulateClosestDeformJointFromSelectionSet(control, self.upperReferenceSet)))

        #sort dag
        for stickyPair in self.sitckyObjects:
            cmds.parent(stickyPair[0], stickyControlHirarchy)
            cmds.parent(stickyPair[1], stickyPinHirarchy)

        cmds.parent(stickyPinHirarchy, self.lipLocalRigTopNode)
        cmds.parent(stickyControlHirarchy, self.rigName)

        cmds.parent(self.lipLocalRigTopNode, self.rigName)

        cmds.addAttr(self.rigName, ln = "lipLocalRig", at="enum", enumName="OFF:ON", keyable=True)

        cmds.connectAttr(f"{self.rigName}.lipLocalRig", f"{self.lipLocalRigTopNode}.visibility")

        print("+++++ End Implementing Lip Rig ++++++")
        
        return
