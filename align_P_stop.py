import numpy as np

source_node = slicer.util.getNode('plate_lm')
target_node = slicer.util.getNode('orbit_lm')

p_stop_source = [0, 0, 0]
source_node.GetNthControlPointPosition(1, p_stop_source)

p_stop_target = [0, 0, 0 ]
target_node.GetNthControlPointPosition(1, p_stop_target)

translation = np.subtract(p_stop_target, p_stop_source)

# homogeneous transformation
T = np.identity(4)
T[:3, 3] = translation
rotationTransformNode =  slicer.mrmlScene.AddNewNodeByClass('vtkMRMLTransformNode', "align_p_stop_transform")
rotationTransformNode.SetMatrixTransformToParent(slicer.util.vtkMatrixFromArray(T))
