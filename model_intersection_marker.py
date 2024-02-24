plate_node = slicer.util.getNode('Preformed Orbital, small, right  04_503_811')
orbit_node = slicer.util.getNode('bone_no_fx')


intersector = vtk.vtkIntersectionPolyDataFilter()
intersector.SetInputConnection(0,plate_node.GetPolyDataConnection())
intersector.SetInputConnection(1, orbit_node.GetPolyDataConnection())
intersector.Update()

intersectionModel_0 = slicer.modules.models.logic().AddModel(intersector.GetOutputDataObject(0))
intersectionModel_0.SetName("intersectionModel_0")
intersectionModel_0.GetDisplayNode().SetColor(0.0, 0.0, 1.0)
