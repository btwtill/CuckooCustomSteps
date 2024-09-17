import mgear.shifter.custom_step as cstp
import mgear.rigbits as rigbits
import maya.cmds as cmds
import os
import re

class CustomShifterStep(cstp.customShifterMainStep):
    """Custom Step description
    """

    def setup(self):
        
        self.name = "ImplementRBFs"
        self.currentWorkspacePath = cmds.workspace(q=True, rootDirectory=True)
        self.rbfPath = "scenes/Rig/Data/RBFs"

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
    

    def run(self):
        print("+++++ Importing and Implementing RBFs +++++")
        latestRBFFilePath, latestRBFVersion = self.getLatestAssetFilePath(os.path.join(self.currentWorkspacePath, self.rbfPath))
        print(f"+++++ Latest RBF File Path: {latestRBFFilePath}")
        print(f"+++++ Latest RBF Version: {latestRBFVersion}")

        rigbits.rbf_io.importRBFs(latestRBFFilePath[0])

        return
