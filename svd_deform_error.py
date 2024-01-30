###SVD
import numpy as np

source_node = slicer.util.getNode('plate_lm_harden') #get source lm node: the plate lm
target_node = slicer.util.getNode('orbit_lm') #get target lm node: the orbit lm

source_points = np.zeros(shape=(source_node.GetNumberOfControlPoints(), 3))
target_points = np.zeros(shape=(target_node.GetNumberOfControlPoints(), 3))

point = [0, 0, 0]

for i in range(source_node.GetNumberOfControlPoints()):
  source_node.GetNthControlPointPosition(i, point)
  source_points[i, :] = point
  # subjectFiducial.SetNthControlPointLocked(i, 1)
  target_node.GetNthControlPointPosition(i, point)
  target_points[i, :] = point

# Define the point around which you want to rotate
rotation_center = np.array([20.588, 38.868, -675.454]) # Specify the center point

# Calculate the translation to bring the rotation center to the origin
translation = -rotation_center

# Translate both the source and target point sets
translated_source_points = source_points + translation
translated_target_points = target_points + translation

# Perform singular value decomposition (SVD)
U, _, Vt = np.linalg.svd(translated_source_points.T @ translated_target_points, full_matrices=False)

# Calculate the optimal rotation matrix
rotation_matrix = Vt.T @ U.T

#translation
t = rotation_center.T - np.dot(rotation_matrix, rotation_center.T)

# homogeneous transformation
T = np.identity(4)
T[:3, :3] = rotation_matrix
T[:3, 3] = t

# 
rotationTransformNode =  slicer.mrmlScene.AddNewNodeByClass('vtkMRMLTransformNode', "svp_rotaion_transform")
rotationTransformNode.SetMatrixTransformToParent(slicer.util.vtkMatrixFromArray(T))

# rotated_translated_source_points = np.dot(translated_source_points, rotation_matrix.T)

# Translate the rotated points back to the original position
# rotated_source_points = rotated_translated_source_points - translation

# rotatedSourceNode =  slicer.mrmlScene.AddNewNodeByClass('vtkMRMLMarkupsFiducialNode', "svp_rotated_source_lm")
# for i in range(rotated_source_points.shape[0]):
#     rotatedSourceNode.AddControlPoint(rotated_source_points[i, :])

# print(rotated_source_points)
