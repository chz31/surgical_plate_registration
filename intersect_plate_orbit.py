masterVolumeNode = slicer.util.getNode('5 DummySeriesDesc!')

#Get segments
segmentationNode = slicer.util.getNode('plate_heatmap-segmentation')
# segmentationNode.SetReferenceImageGeometryParameterFromVolumeNode(masterVolumeNode)
segmentationNode.CreateDefaultDisplayNodes() 

#Create segment editor to get access to effects
segmentEditorWidget = slicer.qMRMLSegmentEditorWidget()
segmentEditorWidget.setMRMLScene(slicer.mrmlScene)
segmentEditorNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentEditorNode")
segmentEditorWidget.setMRMLSegmentEditorNode(segmentEditorNode)
segmentEditorWidget.setSegmentationNode(segmentationNode)
# segmentEditorWidget.setMasterVolumeNode(masterVolumeNode)

#Logic operator
segmentEditorWidget.setActiveEffectByName("Logical operators")
effect = segmentEditorWidget.activeEffect()
effect.setParameter("Operation","INTERSECT")

boneSegID = segmentationNode.GetSegmentation().GetSegmentIdBySegmentName('bone_no_fx')
plateSegID = segmentationNode.GetSegmentation().GetSegmentIdBySegmentName('plate_copy')
boneSeg = segmentationNode.GetSegmentation().GetSegment(boneSegID)
plateSeg = segmentationNode.GetSegmentation().GetSegment(plateSegID)


segmentEditorNode.SetSelectedSegmentID(plateSegID)
effect.setParameter("ModifierSegmentID", boneSegID)
effect.self().onApply()

#Grow margin
# print(segmentEditorWidget.availableEffectNames())
segmentEditorWidget.setActiveEffectByName("Margin")
effect = segmentEditorWidget.activeEffect()
effect.setParameter("MarginSizeMm", 0.25)
segmentEditorNode.SetSelectedSegmentID(plateSegID)
effect.self().onApply()

#Remove bone segment
segmentationNode.GetSegmentation().RemoveSegment(boneSegID)


#Create a new segment
# segNode = slicer.vtkMRMLSegmentationNode()
# slicer.mrmlScene.AddNode(segNode)
# segmentationNode.SetReferenceImageGeometryParameterFromVolumeNode(masterVolumeNode)
# segmentation = segNode.GetSegmentation()
# segment1 = segmentaion.AddSegment(plateSeg)



#Paint plate model by the plate_intersect segment
# InputModelNode = slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLModelNode")
# OutputModelNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelNode", "Skull_Thickness")
InputModelNode = slicer.util.getNode('Preformed Orbital small right  04_503_811')
OutputModelNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLModelNode", "plate_painted")


parameters = {}
parameters['InputVolume'] = segmentationNode.GetID()
parameters['InputModel'] = InputModelNode.GetID()
parameters['OutputModel'] = OutputModelNode.GetID()
probe = slicer.modules.probevolumewithmodel
slicer.cli.run(probe, None, parameters, wait_for_completion=True)

