import numpy as np

source_node = slicer.util.getNode('plate_lm')
target_node = slicer.util.getNode('orbit_lm')

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
rotation_center = target_points[1, :] # Specify the center point as the posterior stop

# Calculate the translation to bring the rotation center to the origin
translation = -rotation_center

# Translate both the source and target point sets
translated_source_points = source_points + translation
translated_target_points = target_points + translation

# Perform singular value decomposition (SVD)
U, _, Vt = np.linalg.svd(translated_source_points.T @ translated_target_points, full_matrices=False)


# Calculate the optimal rotation matrix
rotation_matrix = Vt.T @ U.T

# special reflection case
m = translated_source_points.shape[1]
if np.linalg.det(rotation_matrix) < 0:
    Vt[m - 1, :] *= -1
rotation_matrix = np.dot(Vt.T, U.T)

#translation
t = rotation_center.T - np.dot(rotation_matrix, rotation_center.T)

# homogeneous transformation
T = np.identity(4)
T[:3, :3] = rotation_matrix
T[:3, 3] = t

# 
rotationTransformNode =  slicer.mrmlScene.AddNewNodeByClass('vtkMRMLTransformNode', "svd_rotation_transform")
rotationTransformNode.SetMatrixTransformToParent(slicer.util.vtkMatrixFromArray(T))




