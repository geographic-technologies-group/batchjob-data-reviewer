## J. Van Horn
## 03/2019

# ------------------------------------------------------------------------------------------------------------------------

import arcpy
from arcpy import env
from arcpy.sa import *
import os

arcpy.CheckOutExtension("datareviewer")

# ------------------------------------------------------------------------------------------------------------------------

##  Run data reviewer for database

# ------------------------------------------------------------------------------------------------------------------------

def runDataReview(workspace, spatRef, sessionName, polyRBJ, lineRBJ, pointRBJ, featureList, prodWorkspace):

    # enable Data Reviewer in workspace
    arcpy.EnableDataReviewer_Reviewer(workspace, spatRef)

    # start reviewer session
    session = arcpy.CreateReviewerSession_Reviewer(workspace, sessionName)

    # grab geodatabase name from prodWorkspace
    wDesc = arcpy.Describe(prodWorkspace)
    gdbName, gdbExt = os.path.splitext(str(wDesc.name))

    # Loop through provided feature classes and run appropriate
    for feature in featureList.split(';'):

        feature = feature.strip("'")

        # describe feature to get shape type
        featDesc = arcpy.Describe(feature)

        # assign correct batch job check to var RBJfile based on geometry
        if featDesc.shapeType == 'Polygon':
            RBJfile = polyRBJ
        elif featDesc.shapeType == 'Polyline':
            RBJfile = lineRBJ
        elif featDesc.shapeType == 'Point':
            RBJfile = pointRBJ
        else:
            arcpy.AddMessage("Check %s shape type" % feature)

        # get directory to RBJ file
        dirRBJ = os.path.dirname(RBJfile)

        # open read version of RBJfile as string 
        s = open(RBJfile).read()

        # replace text with parameters
        s1 = s.replace('FEATURE', featDesc.name)
        s2 = s1.replace('GDBpath', prodWorkspace)
        s3 = s2.replace('GDBname', gdbName)

        # open new file to copy into
        newBatchFile = open(dirRBJ + r"\%sBatchJob.RBJ" % featDesc.name, 'w')
        # copy code over
        newBatchFile.write(s3)
        newBatchFile.close()

        # get new batch job file path name
        batchFilePath = dirRBJ + r"\%sBatchJob.RBJ" % featDesc.name

        # run data reviewer
        arcpy.AddMessage("Running %s check on %s" % (featDesc.shapeType, featDesc.name))
        rev = arcpy.ExecuteReviewerBatchJob_Reviewer(workspace, session, batchFilePath, prodWorkspace)

        # delete new batch file
        os.remove(batchFilePath)


if __name__ == "__main__":

    # inputs
    workspace = arcpy.GetParameterAsText(0)
    spatRef = arcpy.GetParameterAsText(1)
    sessionName = arcpy.GetParameterAsText(2)
    polyRBJ = arcpy.GetParameterAsText(3)
    lineRBJ = arcpy.GetParameterAsText(4)
    pointRBJ = arcpy.GetParameterAsText(5)
    prodWorkspace = arcpy.GetParameterAsText(6)
    featureList = arcpy.GetParameterAsText(7)

    # module
    runDataReview(workspace, spatRef, sessionName, polyRBJ, lineRBJ, pointRBJ, featureList, prodWorkspace)
