masterVolumeNode = slicer.util.getNode('5: DummySeriesDesc!')

#Get segments
segmentationNode = slicer.util.getNode('plate_heatmap-segmentation')
segmentationNode.SetReferenceImageGeometryParameterFromVolumeNode(masterVolumeNode)
segmentationNode.CreateDefaultDisplayNodes() 
boneSeg = segmentationNode.GetSegmentation().GetSegment('bone_copy')
plateSeg = segmentationNode.GetSegmentation().GetSegment('plate_copy')

#Create segment editor to get access to effects
segmentEditorWidget = slicer.qMRMLSegmentEditorWidget()
segmentEditorWidget.setMRMLScene(slicer.mrmlScene)
segmentEditorNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentEditorNode")
segmentEditorWidget.setMRMLSegmentEditorNode(segmentEditorNode)
segmentEditorWidget.setSegmentationNode(segmentationNode)
segmentEditorWidget.setMasterVolumeNode(masterVolumeNode)

#Logic operator
segmentEditorWidget.setActiveEffectByName("Logical operators")
effect = segmentEditorWidget.activeEffect()
effect.setParameter("Operation","INTERSECT")
boneSegID = segmentationNode.GetSegmentation().GetSegmentIdBySegmentName('bone_no_fx')
plateSegID = segmentationNode.GetSegmentation().GetSegmentIdBySegmentName('plate_copy')
segmentEditorNode.SetSelectedSegmentID(plateSegID)
effect.setParameter("ModifierSegmentID", boneSegID)
effect.self().onApply()
