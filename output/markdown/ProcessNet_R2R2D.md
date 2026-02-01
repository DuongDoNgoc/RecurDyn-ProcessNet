# ProcessNet.R2R2D

> ProcessNet.R2R2D API

## Overview

**Full Name:** FunctionBay.RecurDyn.ProcessNet.R2R2D

**Methods:** 121

**Examples:** 0

## Methods

### classAirResistanceForceDirection

```
classAirResistanceForceDirection(value)
```

Bases:IntEnumAirResistanceForceDirection enumeration.MembersDirectionType_ElementNormalConstant value is 0.DirectionType_VelocityConstant value is 1.

### classIR2R2DBody

```
classIR2R2DBody(oobj=None)
```

Bases:DispatchBaseClassR2R2D bodyPropertiesCommentCommentFullNameFullName such asBody1.Marker1@Model1GeneralBodyGeneralBodyNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceUserDataUser supplied data

### AddPassingBody

```
IR2R2DBodyBeam.AddPassingBody(pVal)
```

Add a passing body

### DeletePassingBody

```
IR2R2DBodyBeam.DeletePassingBody(pVal)
```

Delete a passing body

### UpdateAllProperties

```
IR2R2DBodyBeam.UpdateAllProperties()
```

Update all properties

### classIR2R2DBodyBeam

```
classIR2R2DBodyBeam(oobj=None)
```

Bases:DispatchBaseClassR2R2D Beam AssemblyPropertiesActiveActiveAirResistanceConstantAir Resistance Coefficient ConstantAirResistanceExpressionAir Resistance Coefficient ExpressionAirResistanceForceDirectionAir resistance force directionAirResistanceTypeAir Resistance Coefficient TypeBCCollectionNode boundary condition collectionCommentCommentConnectingParametersConnecting parametersFlexBodyFlex body editFullNameFullName such asBody1.Marker1@Model1GeometryGeometryInitialLongitudinalVelocityIniti

### AddPassingBody

```
AddPassingBody()
```

Add a passing body

### DeletePassingBody

```
DeletePassingBody()
```

Delete a passing body

### UpdateAllProperties

```
UpdateAllProperties()
```

Update all properties

### Item

```
IR2R2DBodyBeamCollection.Item(var)
```

Returns a specific item.

### classIR2R2DBodyBeamCollection

```
classIR2R2DBodyBeamCollection(oobj=None)
```

Bases:DispatchBaseClassPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### Item

```
Item()
```

Returns a specific item.

### Item

```
IR2R2DBodyCollection.Item(var)
```

Returns a specific item.

### classIR2R2DBodyCollection

```
classIR2R2DBodyCollection(oobj=None)
```

Bases:DispatchBaseClassPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### Item

```
Item()
```

Returns a specific item.

### classIR2R2DBodyRoller

```
classIR2R2DBodyRoller(oobj=None)
```

Bases:DispatchBaseClassR2R2D body rollerPropertiesCommentCommentContactParameterContact ParameterFullNameFullName such asBody1.Marker1@Model1GeneralBodyGeneralBodyInnerContactPointsThe number of inner contat pointsNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceUserDataUser supplied data

### classIR2R2DBodyRollerCircle

```
classIR2R2DBodyRollerCircle(oobj=None)
```

Bases:DispatchBaseClassR2R2D circle roller bodyPropertiesAssembledRadiusThe assembled radius of circle roller.CommentCommentContactParameterContact ParameterFullNameFullName such asBody1.Marker1@Model1GeneralBodyGeneralBodyGeometryGeometryInnerContactPointsThe number of inner contat pointsNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceUser

### classIR2R2DBodyRollerGeneral

```
classIR2R2DBodyRollerGeneral(oobj=None)
```

Bases:DispatchBaseClassR2R2D general roller bodyPropertiesCommentCommentContactParameterContact ParameterFullNameFullName such asBody1.Marker1@Model1GeneralBodyGeneralBodyGeometryGeometryInnerContactPointsThe number of inner contat pointsNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceUserDataUser supplied data

### Item

```
IR2R2DConcentratedLoadUSUBCollection.Item(var)
```

Returns a specific item.

### classIR2R2DConcentratedLoadUSUBCollection

```
classIR2R2DConcentratedLoadUSUBCollection(oobj=None)
```

Bases:DispatchBaseClassPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### Item

```
Item()
```

Returns a specific item.

### classIR2R2DConnectingParameters

```
classIR2R2DConnectingParameters(oobj=None)
```

Bases:DispatchBaseClassR2R2D connecting parametersPropertiesMassMassMomentOfInertiaMoment of inertiaRotationnalDampingRatioRotationnal damping ratioRotationnalStiffnessRotationnal stiffnessTranslationalDampingRatioTranslational damping ratioTranslationalStiffnessTranslational stiffnessUseForceConnectorUse force connectorUseSyncFDRUse Sync.

### classIR2R2DContact

```
classIR2R2DContact(oobj=None)
```

Bases:DispatchBaseClassR2R2D ContactPropertiesActiveActiveCommentCommentFullNameFullName such asBody1.Marker1@Model1LayerNumberLayer numberNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceUserDataUser supplied data

### classIR2R2DContactFriction

```
classIR2R2DContactFriction(oobj=None)
```

Bases:DispatchBaseClassR2R2D contact frictionPropertiesDynamicThresholdVelocityDynamic threshold velocityMaximumFrictionForceMaximum friction forceSpecialDynamicThresholdVelocitySpecial dynamic threshold velocitySpecialMaximumFrictionForceSpecial maximum friction forceSpecialStaticFrictionCoefficientSpecial static friction coefficientSpecialStaticThresholdVelocitySpecial static threshold velocityStaticFrictionCoefficientStatic friction coefficientStaticThresholdVelocityStatic threshold velocityU

### classIR2R2DContactParameter

```
classIR2R2DContactParameter(oobj=None)
```

Bases:DispatchBaseClassR2R2D contact propertyPropertiesContactFrictionTypeContact friction typeDampingCoefficientThe viscous damping coefficient for the contact normal forceDampingExponentThe damping exponent for a non-linear contact normal forceDampingSplineDamping splineFrictionFrictionFrictionCoefficientThe friction coefficient for the contact normal force.FrictionSplineThe spline which shows relative velocity to the friction coefficient or the friction force.IndentationExponentThe indentatio

### classIR2R2DContactWorkpieceToWorkpiece

```
classIR2R2DContactWorkpieceToWorkpiece(oobj=None)
```

Bases:DispatchBaseClassR2R2D Workpiece to Workpiece ContactPropertiesActionBeamAssemblyAction Beam AssemblyActiveActiveBaseBeamAssemblyBase Beam AssemblyCommentCommentContactParameterContact ParameterFullNameFullName such asBody1.Marker1@Model1InnerContactPointsThe number of inner contat pointsLayerNumberLayer numberNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning

### Item

```
IR2R2DContactWorkpieceToWorkpieceCollection.Item(var)
```

Returns a specific item.

### classIR2R2DContactWorkpieceToWorkpieceCollection

```
classIR2R2DContactWorkpieceToWorkpieceCollection(oobj=None)
```

Bases:DispatchBaseClassPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### Item

```
Item()
```

Returns a specific item.

### classIR2R2DGeometryBeam

```
classIR2R2DGeometryBeam(oobj=None)
```

Bases:DispatchBaseClassR2R2D Beam geometryPropertiesColorBelt colorDepthDepthDisplayGeometryDisplay geometryDisplayNodeIDThis is an obsolete property.DisplayNodeIDTypeDisplay Node ID typeElementLengthElement lengthNumberOfElementsNumber of elementsSpecialDepthSpecial depthSpecialThicknessSpecial thicknessStretchedLengthStretched lengthThicknessThicknessUseSpecialDepthUse special depthUseSpecialThicknessUse special thickness

### GetBoundingBox

```
IR2R2DGeometryRollerCircle.GetBoundingBox()
```

Get bounding box, internal use only

### GetBoundingBoxWithRefFrame

```
IR2R2DGeometryRollerCircle.GetBoundingBoxWithRefFrame(RefFrame)
```

Get bounding box with reference frame

### classIR2R2DGeometryRollerCircle

```
classIR2R2DGeometryRollerCircle(oobj=None)
```

Bases:DispatchBaseClassR2R2D circle roller body geometryPropertiesCommentCommentDepthThe depth of circle roller.FullNameFullName such asBody1.Marker1@Model1GraphicGraphicNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceRadiusThe radius of circle roller.RefFrameReference frameUserDataUser supplied dataVertexCollectionMethodsGetBoundingBoxGet 

### GetBoundingBox

```
GetBoundingBox()
```

Get bounding box, internal use only

### GetBoundingBoxWithRefFrame

```
GetBoundingBoxWithRefFrame()
```

Get bounding box with reference frame

### Export

```
IR2R2DGeometryRollerGeneral.Export(strName,val)
```

Export method

### GetBoundingBox

```
IR2R2DGeometryRollerGeneral.GetBoundingBox()
```

Get bounding box, internal use only

### GetBoundingBoxWithRefFrame

```
IR2R2DGeometryRollerGeneral.GetBoundingBoxWithRefFrame(RefFrame)
```

Get bounding box with reference frame

### Import

```
IR2R2DGeometryRollerGeneral.Import(strName)
```

Import method

### classIR2R2DGeometryRollerGeneral

```
classIR2R2DGeometryRollerGeneral(oobj=None)
```

Bases:DispatchBaseClassR2R2D general roller body geometryPropertiesCommentCommentDepthThe depth of general roller.FullNameFullName such asBody1.Marker1@Model1GraphicGraphicNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfacePointCollectionPoint with radius collectionRefFrameReference frameUserDataUser supplied dataVertexCollectionMethodsExportE

### Export

```
Export()
```

Export method

### GetBoundingBox

```
GetBoundingBox()
```

Get bounding box, internal use only

### GetBoundingBoxWithRefFrame

```
GetBoundingBoxWithRefFrame()
```

Get bounding box with reference frame

### Import

```
Import()
```

Import method

### UpdateAllProperties

```
IR2R2DGuide.UpdateAllProperties()
```

Update All Properties

### classIR2R2DGuide

```
classIR2R2DGuide(oobj=None)
```

Bases:DispatchBaseClassR2R2D guidePropertiesActiveActiveCommentCommentContactParameterContact ParameterFullNameFullName such asBody1.Marker1@Model1InnerContactPointsThe number of inner contat pointsLayerNumberLayer numberMotherBodyThe mother body of guideNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceUserDataUser supplied dataMethodsUpdate

### UpdateAllProperties

```
UpdateAllProperties()
```

Update All Properties

### UpdateAllProperties

```
IR2R2DGuideArc.UpdateAllProperties()
```

Update All Properties

### classIR2R2DGuideArc

```
classIR2R2DGuideArc(oobj=None)
```

Bases:DispatchBaseClassR2R2D arc guidePropertiesActiveActiveAngleThe angle of arcCenterPointThe center point of arcCircleEdgeRadiusThe radius of imaginary circle edgeCommentCommentContactParameterContact ParameterDirectionPointThe direction of arcFullNameFullName such asBody1.Marker1@Model1ImaginaryCircleEdgeEndEnd point of imaginary circle edgeImaginaryCircleEdgeStartStart point of imaginary circle edgeInnerContactPointsThe number of inner contat pointsLayerNumberLayer numberMotherBodyThe mothe

### UpdateAllProperties

```
UpdateAllProperties()
```

Update All Properties

