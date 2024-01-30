# surgical_plate_registration

-The rotation center is the 2nd landmark posterior stop, rather than the centroid.
-The rotation center is tranlated to the origin.
-SVP is then used to calculate rotation angles as in rigid-body registration.
-The configurations are then translated back to their original positions.
-Transformation matrix calculated accordingly.
