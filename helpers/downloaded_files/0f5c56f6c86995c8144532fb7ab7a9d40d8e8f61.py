import Rhino
#removing a lineType by name
lineTypeIndex = Rhino.RhinoDoc.ActiveDoc.Linetypes.Find("Dashed", True)
lineType = Rhino.RhinoDoc.ActiveDoc.Linetypes[lineTypeIndex]
Rhino.RhinoDoc.ActiveDoc.Linetypes.Delete(lineType)