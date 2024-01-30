# Define your source and target point sets as NumPy arrays
source_points = np.array([[29.930, 65.059, -692.872], [20.588, 38.868, -675.454], [18.266, 57.316, -682.061]])
  # Your source points
target_points = np.array([[27.474, 61.970, -689.958], [20.588, 38.868, -675.454], [15.340, 60.875, -681.762]])  # Your target points

# Define the point around which you want to rotate
rotation_center = target_points[1, :] # Specify the center point as the posterior stop

# Calculate the translation to bring the rotation center to the origin
translation = -rotation_center

# Translate both the source and target point sets
translated_source_points = source_points + translation
translated_target_points = target_points + translation

# Perform singular value decomposition (SVD)
# U, _, Vt = np.linalg.svd(translated_target_points.T @ translated_source_points, full_matrices=False)
U, _, Vt = np.linalg.svd(translated_source_points.T @ translated_target_points, full_matrices=False)


# Calculate the optimal rotation matrix
rotation_matrix = Vt.T @ U.T

#translation
t = rotation_center.T - np.dot(rotation_matrix, rotation_center.T)

# homogeneous transformation
T = np.identity(4)
T[:3, :3] = rotation_matrix
T[:3, 3] = t

# rotation_matrix_slicer = np.zeros(shape= (4, 4))
# 
# point = [0, 0, 0]
# for i in range(3):
#   rotation_matrix_slicer[i, 0:3] = rotation_matrix[i, :]
#   
# rotation_matrix_slicer[3, :] = [0, 0, 0, 1]
# 
rotationTransformNode =  slicer.mrmlScene.AddNewNodeByClass('vtkMRMLTransformNode', "svp_roataion_transform")
rotationTransformNode.SetMatrixTransformToParent(slicer.util.vtkMatrixFromArray(T))
