###SVD
import numpy as np

source_points = np.array([[29.92973456, 65.05863408, -692.87207321], [20.58772087,38.86774826, -675.45440674],[18.2662661, 57.31554544, -682.06144071]])
target_points = np.array([[27.47413063, 61.97033691, -689.95812988], [20.58772087, 38.86774826, -675.45440674], [15.33987617, 60.87537766, -681.76153564]])

# source_points = np.array([[29.92973456, 65.05863408, -692.87207321], [20.58772087,38.86774826, -675.45440674],[18.2662661, 57.31554544, -682.06144071]])
# target_points = np.array([[27.47413063, 61.97033691, -689.95812988], [20.58772087, 38.86774826, -675.45440674], [15.33987617, 60.87537766, -681.76153564]])

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
