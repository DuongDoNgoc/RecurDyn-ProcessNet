# ProcessNet.ToolkitCommon

> ProcessNet.ToolkitCommon API

## Overview

**Full Name:** FunctionBay.RecurDyn.ProcessNet.ToolkitCommon

**Methods:** 20

**Examples:** 0

## Methods

### classIContactTrackToSurface

```
classIContactTrackToSurface(oobj=None)¶
```

Bases:DispatchBaseClassTrack to surface contactPropertiesActionEntityAction entityActionPatchOptionSolid contact action patch optionActionUpDirectionAction up directionActiveActiveBaseEntityBase entityCommentCommentContactParameterContact parameterFullNameFullName such asBody1.Marker1@Model1LayerNumberLayer numberNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning IS

### Export

```
IContactTrackToSurfaceProperty.Export(strName,Val)¶
```

Export is obsolete function

### Import

```
IContactTrackToSurfaceProperty.Import(strName)¶
```

Import is obsolete function

### SoftGroundType

```
IContactTrackToSurfaceProperty.SoftGroundType(Val)¶
```

Soft ground type

### classIContactTrackToSurfaceProperty

```
classIContactTrackToSurfaceProperty(oobj=None)¶
```

Bases:DispatchBaseClassTrack assembly to surface contact propertyPropertiesCohesionCohesion (c)DampingCoefficientThe viscous damping coefficient for the contact normal force.DampingExponentThe damping exponent for a non-linear contact normal forceDampingSplineDamping splineExponentialNumberExponential number (n)FrictionFrictionFrictionCoefficientThe friction coefficient for the contact normal force.FrictionSplineThe spline which shows relative velocity to the friction coefficient or the friction

### CopyActionToBase

```
IForceConnectorBushing.CopyActionToBase(Type)¶
```

Copy action to base

### CopyBaseToAction

```
IForceConnectorBushing.CopyBaseToAction(Type)¶
```

Copy base to action

### classIForceConnectorBushing

```
classIForceConnectorBushing(oobj=None)¶
```

Bases:DispatchBaseClassBushing forcePropertiesActionMarkerAction markerActiveActiveBaseMarkerBase markerCommentCommentForceDisplayForce displayForceDisplayColorForce display colorForceDisplayUseForce display useFullNameFullName such asBody1.Marker1@Model1LayerNameLayer nameLayerNumberLayer numberNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interf

### CopyActionToBase

```
IForceConnectorFixed.CopyActionToBase(Type)¶
```

Copy action to base

### CopyBaseToAction

```
IForceConnectorFixed.CopyBaseToAction(Type)¶
```

Copy base to action

### classIForceConnectorFixed

```
classIForceConnectorFixed(oobj=None)¶
```

Bases:DispatchBaseClassConnector fixed forcePropertiesActionMarkerAction markerActiveActiveBaseMarkerBase markerCommentCommentForceDisplayForce displayForceDisplayColorForce display colorForceDisplayUseForce display useFullNameFullName such asBody1.Marker1@Model1LayerNameLayer nameLayerNumberLayer numberNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSyste

### CopyActionToBase

```
IForceConnectorRevolute.CopyActionToBase(Type)¶
```

Copy action to base

### CopyBaseToAction

```
IForceConnectorRevolute.CopyBaseToAction(Type)¶
```

Copy base to action

### classIForceConnectorRevolute

```
classIForceConnectorRevolute(oobj=None)¶
```

Bases:DispatchBaseClassConnector revolute forcePropertiesActionMarkerAction markerActiveActiveBaseMarkerBase markerCommentCommentForceDisplayForce displayForceDisplayColorForce display colorForceDisplayUseForce display useFullNameFullName such asBody1.Marker1@Model1LayerNameLayer nameLayerNumberLayer numberNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSy

### CopyActionToBase

```
IForceConnectorSpring.CopyActionToBase(Type)¶
```

Copy action to base

### CopyBaseToAction

```
IForceConnectorSpring.CopyBaseToAction(Type)¶
```

Copy base to action

### classIForceConnectorSpring

```
classIForceConnectorSpring(oobj=None)¶
```

Bases:DispatchBaseClassConnector Spring forcePropertiesActionMarkerAction markerActiveActiveBaseMarkerBase markerCommentCommentDampingDampingForceDisplayForce displayForceDisplayColorForce display colorForceDisplayUseForce display useFreeLengthThe free length of the springFullNameFullName such asBody1.Marker1@Model1LayerNameLayer nameLayerNumberLayer numberNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOw

### classIToolkitContactFriction

```
classIToolkitContactFriction(oobj=None)¶
```

Bases:DispatchBaseClassToolkit contact frictionPropertiesDynamicThresholdVelocityDynamic threshold velocityMaxStictionDeformatonMax friction forceStaticFrictionCoefficientStatic friction coefficientStaticThresholdVelocityStatic threshold velocityUseMaxStictionDeformatonUse max friction force

### classToolkitSoftGroundType

```
classToolkitSoftGroundType(value)¶
```

Bases:IntEnumToolkitSoftGroundType enumeration.MembersToolkitSoftGroundType_Clayey_SoilConstant value is 4.ToolkitSoftGroundType_Dry_SandConstant value is 0.ToolkitSoftGroundType_Grenville_LoamConstant value is 11.ToolkitSoftGroundType_Heavy_ClayConstant value is 5.ToolkitSoftGroundType_LETE_SandConstant value is 7.ToolkitSoftGroundType_Lean_ClayConstant value is 6.ToolkitSoftGroundType_North_Gower_Clayey_LoamConstant value is 10.ToolkitSoftGroundType_Rubicon_Sandy_LoamConstant value is 9.Toolki

### classTrackFrictionType

```
classTrackFrictionType(value)¶
```

Bases:IntEnumTrackFrictionType enumeration.MembersTrackFrictionType_DynamicFrictionCoefficientConstant value is 0.TrackFrictionType_FrictionCoefficientSplineConstant value is 2.TrackFrictionType_FrictionForceSplineConstant value is 1.

