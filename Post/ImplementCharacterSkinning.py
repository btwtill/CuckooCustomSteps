import mgear.shifter.custom_step as cstp
import maya.cmds as cmds
import os
import re
import maya.mel as mel

class CustomShifterStep(cstp.customShifterMainStep):
    """Custom Step description
    """

    def setup(self):
        
        self.name = "ImplementCharacterSkinning"
        self.currentWorkspacePath = cmds.workspace(q=True, rootDirectory=True)
        #leftInnerEyeball
        self.leftInnerEyeballGeoName = "Cuckoo_L_InnerEyes_Geo"
        self.leftInnerEyeballSetName = "LeftInnerEyeballDeformer"
        self.leftInnerEyeballWeightPath = "scenes/Rig/Data/Weights/EyesWeights/LeftInnerEyes"

        #rightInnerEyeball
        self.rightInnerEyeballGeoName = "Cuckoo_R_InnerEyes_Geo"
        self.rightInnerEyeballSetName = "RightInnerEyeballDeformers"
        self.rightInnerEyeballWeightPath = "scenes/Rig/Data/Weights/EyesWeights/RightInnerEyes"

        #leftOuterEyeball
        self.leftOuterEyeballGeoName = "Cuckoo_L_OuterEyes_Geo"
        self.leftOuterEyeballSetName = "eye_L_skn"
        self.leftOuterEyeballWeightPath = "scenes/Rig/Data/Weights/EyesWeights/LeftOuterEyes"

        #rightOuterEyeball
        self.rightOuterEyeballGeoName = "Cuckoo_R_OuterEyes_Geo"
        self.rightOuterEyeballSetName = "eye_R_skn"
        self.rightOuterEyeballWeightPath = "scenes/Rig/Data/Weights/EyesWeights/RightOuterEyes"

        #leftUpperEyelid
        self.leftUpperEyelidGeoName = "Cuckoo_L_UpperEyelid_Geo"
        self.leftUpperEyelidSetName = "LeftUpperEyelidDeformer"
        self.leftUpperEyelidWeightPath ="scenes/Rig/Data/Weights/EyesWeights/LeftUpperEyelid"

        #leftLowerEyelid
        self.leftLowerEyelidGeoName = "Cuckoo_L_LowerEyelid_Geo"
        self.leftLowerEyelidSetName = "LeftLowerEyelidDeformers"
        self.leftLowerEyelidWeightPath ="scenes/Rig/Data/Weights/EyesWeights/LeftLowerEyelid"

        #rightUpperEyelid
        self.rightUpperEyelidGeoName = "Cuckoo_R_UpperEyelid_Geo"
        self.rightUpperEyelidSetName = "RightUpperEyelidDeformers"
        self.rightUpperEyelidWeightPath ="scenes/Rig/Data/Weights/EyesWeights/RightUpperEyelid"

        #rightLowerEyelid
        self.rightLowerEyelidGeoName = "Cuckoo_R_LowerEyelid_Geo"
        self.rightLowerEyelidSetName = "RightLowerEyelidDeformers"
        self.rightLowerEyelidWeightPath ="scenes/Rig/Data/Weights/EyesWeights/RightLowerEyelid"

        #Brows
        self.browGeoName = "Cuckoo_Brow_Geo"
        self.browSetName = "browDeformationSet"
        self.browWeightPath = "scenes/Rig/Data/Weights/BrowWeights"

        #mainBody
        self.mainGeometryName = "Cuckoo_Body_Geo"
        self.eyeRingDeformersSet = "eyeRingDeformers"
        self.gimmickDeformerSet = "rig_deformers_grp"
        self.mainDeformerSet = "CuckooRig_deformers_grp"
        self.mainBodyWeightPath = "scenes/Rig/Data/Weights/BodyWeights"




    
    def find_file_with_greatest_number(self, files):
        if len(files) != 0:
            # Regular expression to match a number at the end of the file name
            number_pattern = re.compile(r'(\d+)(?=\D*$)')

            max_number = -1
            file_with_max_number = None

            for file in files:
                match = number_pattern.search(file)
                if match:
                    number = int(match.group(0))
                    if number > max_number:
                        max_number = number
                        file_with_max_number = file
            return file_with_max_number
        else:
            return "No File Available"

    def isDirectoryEmpty(self, directoryPath):
        if os.path.isdir(directoryPath):
            # Check if the directory is empty
            if not os.listdir(directoryPath):
                return True
            else:
                return False
        else:
            raise NotADirectoryError(f"{directoryPath} is not a valid directory")

    def get_files_in_directory(self, directory):
        all_files_fullPath = []
        all_files = []
        
        try:
            if self.isDirectoryEmpty(directory):
                print("The selected Directory is Empty")
            else:
                for filename in os.listdir(directory):
                    # Construct full file path
                    full_path = os.path.join(directory, filename)
                    
                    # Check if it's a file (not a directory)
                    if os.path.isfile(full_path):
                        all_files_fullPath.append(full_path)
                        all_files.append(filename)
        except NotADirectoryError as e:
            print(e)
    
        return all_files, all_files_fullPath

    def getLatestAssetFilePath(self, assetSubpath, type = "Publish"):
        current_workspace = cmds.workspace(q=True, rootDirectory=True)
        
        modelPublishDir = assetSubpath + "/" + type + "/"
        
        fullModelPublishDir = os.path.join(current_workspace, modelPublishDir)
        
        allModelPublishedFiles, allModelPublishedFilesFullPath = self.get_files_in_directory(fullModelPublishDir)
        
        
        print("All Files in Model Publish: ", allModelPublishedFiles)
        
        latestModelVersion = self.find_file_with_greatest_number(allModelPublishedFiles)
        
        print("Latest Model Publish: ", latestModelVersion)
        
        latestModelVersionFilePath = [file for file in allModelPublishedFilesFullPath if latestModelVersion in file]
        
        print("Latest Model Publish full File Path:", latestModelVersionFilePath )
        
        return latestModelVersionFilePath, latestModelVersion

    def import_maya_file_and_get_nodes(self, file_path):
        nodes_before_import = cmds.ls()

        cmds.file(file_path, i = True, type = "mayaBinary", ignoreVersion=True, mergeNamespacesOnClash=True, returnNewNodes=True)
        
        nodes_after_import = cmds.ls()

        imported_nodes = list(set(nodes_after_import) - set(nodes_before_import))

        return imported_nodes
    

    def skinTargetGeo(self, geo, deformers, path):
        print(f"+++++ Skinning process for: {geo} +++++")
        latestPublishWeightFile, latestPublishVersion = self.getLatestAssetFilePath(os.path.join(self.currentWorkspacePath, path))

        print(f"+++++ Newest File: {latestPublishVersion}")
        print(f"+++++ Path: {latestPublishWeightFile}")

        newSkinCluster = cmds.skinCluster(deformers, geo, toSelectedBones=True, name = f"{geo}_SkinCluster")[0]
        print(f"+++++ New Skin: {newSkinCluster}")

        publishPath = self.currentWorkspacePath + "/" + path + "/Publish/"
        cmds.deformerWeights(latestPublishVersion, im=True, method="index", deformer = newSkinCluster, path=publishPath)

        cmds.select(clear=True)
        cmds.select(geo)
        mel.eval('doPruneSkinClusterWeightsArgList(1, {"0.01"})')
        cmds.select(clear=True)

    
    def run(self):
        
        self.skinTargetGeo(self.leftInnerEyeballGeoName, cmds.sets(self.leftInnerEyeballSetName, q=True), self.leftInnerEyeballWeightPath)
        self.skinTargetGeo(self.rightInnerEyeballGeoName, cmds.sets(self.rightInnerEyeballSetName, q=True), self.rightInnerEyeballWeightPath)

        self.skinTargetGeo(self.leftOuterEyeballGeoName, self.leftOuterEyeballSetName, self.leftOuterEyeballWeightPath)
        self.skinTargetGeo(self.rightOuterEyeballGeoName, self.rightOuterEyeballSetName, self.rightOuterEyeballWeightPath)

        self.skinTargetGeo(self.leftUpperEyelidGeoName, cmds.sets(self.leftUpperEyelidSetName, q=True), self.leftUpperEyelidWeightPath)
        self.skinTargetGeo(self.leftLowerEyelidGeoName, cmds.sets(self.leftLowerEyelidSetName, q=True), self.leftLowerEyelidWeightPath)
        self.skinTargetGeo(self.rightUpperEyelidGeoName, cmds.sets(self.rightUpperEyelidSetName, q=True), self.rightUpperEyelidWeightPath)
        self.skinTargetGeo(self.rightLowerEyelidGeoName, cmds.sets(self.rightLowerEyelidSetName, q=True), self.rightLowerEyelidWeightPath)

        self.skinTargetGeo(self.browGeoName, cmds.sets(self.browSetName, q=True), self.browWeightPath)
        

        eyeRingDeformers = cmds.sets(self.eyeRingDeformersSet, q=True)
        gimmickDeformers = cmds.sets(self.gimmickDeformerSet, q=True)
        mainDeformerSet = cmds.sets(self.mainDeformerSet, q=True)

        allMainDeformers = eyeRingDeformers + gimmickDeformers + mainDeformerSet

        self.skinTargetGeo(self.mainGeometryName, allMainDeformers, self.mainBodyWeightPath)

        return
