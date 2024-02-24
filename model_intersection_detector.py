#Using intersector

plate_node = slicer.util.getNode('Preformed Orbital, small, right  04_503_811')
orbit_node = slicer.util.getNode('bone_no_fx')

# Variables
#collisionDetection      = vtkSRCP.vtkCollisionDetectionFilter()
collisionDetection      = vtk.vtkCollisionDetectionFilter()
numberOfCollisions      = 0
collisionFlag           = False
#
# Collision Detection
node1ToWorldTransformMatrix = vtk.vtkMatrix4x4()
node2ToWorldTransformMatrix = vtk.vtkMatrix4x4()
node1ParentTransformNode = plate_node.GetParentTransformNode()
node2ParentTransformNode = orbit_node.GetParentTransformNode()
if node1ParentTransformNode != None:
    node1ParentTransformNode.GetMatrixTransformToWorld(node1ToWorldTransformMatrix)
if node2ParentTransformNode != None:
    node2ParentTransformNode.GetMatrixTransformToWorld(node2ToWorldTransformMatrix)
#
collisionDetection.SetInputData( 0, plate_node.GetPolyData() )
collisionDetection.SetInputData( 1, orbit_node.GetPolyData() )
collisionDetection.SetMatrix( 0, node1ToWorldTransformMatrix )
collisionDetection.SetMatrix( 1, node2ToWorldTransformMatrix )
collisionDetection.SetBoxTolerance( 0.0 )
collisionDetection.SetCellTolerance( 0.0 )
collisionDetection.SetNumberOfCellsPerNode( 2 )
collisionDetection.Update()
#
numberOfCollisions      = collisionDetection.GetNumberOfContacts()
if numberOfCollisions > 0:
    collisionFlag       = True
else:
    collisionFlag       = False
#
# Status Verbose
if(collisionFlag == True ):
    print( "{} Collisions Detected".format( numberOfCollisions ) )
else:
    print( "No Collisions Detected" )
#
# Return;
