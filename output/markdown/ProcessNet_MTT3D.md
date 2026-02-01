# ProcessNet.MTT3D

> ProcessNet.MTT3D API

## Overview

**Full Name:** FunctionBay.RecurDyn.ProcessNet.MTT3D

**Methods:** 191

**Examples:** 0

## Methods

### classAirResistanceForceDirection

```
classAirResistanceForceDirection(value)
```

Bases:IntEnumAirResistanceForceDirection enumeration.MembersDirectionType_ElementNormalConstant value is 0.DirectionType_VelocityConstant value is 1.

### classAirResistanceType

```
classAirResistanceType(value)
```

Bases:IntEnumAirResistanceType enumeration.MembersAirResistanceType_ConstantConstant value is 0.AirResistanceType_ExpressionConstant value is 1.

### classContactParameterType

```
classContactParameterType(value)
```

Bases:IntEnumContactParameterType enumeration.MembersContactParameterType_BoundaryPenetrationConstant value is 0.ContactParameterType_IndentationExponentConstant value is 1.

### GetContactedGeometry

```
IMTT3DAssembly.GetContactedGeometry(pVal)
```

Get a contacted geometry

### GetContactedSheet

```
IMTT3DAssembly.GetContactedSheet(pVal)
```

Get a contacted sheet

### SetContactedGeometry

```
IMTT3DAssembly.SetContactedGeometry(pVal,vBool)
```

Set a contacted geometry

### SetContactedSheet

```
IMTT3DAssembly.SetContactedSheet(pVal,vBool)
```

Set a contacted sheet

### classIMTT3DAssembly

```
classIMTT3DAssembly(oobj=None)
```

Bases:DispatchBaseClassMTT3D assemblyPropertiesBufferRadiusFactorBuffer radius factorCommentCommentFullNameFullName such asBody1.Marker1@Model1MaximumNoOfSheetElementsMaximum number of sheet's elementsMaximumStepsizeFactorMaximum stepsize factorNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfacePenetrationParameterPenetration parameterReferenc

### GetContactedGeometry

```
GetContactedGeometry()
```

Get a contacted geometry

### GetContactedSheet

```
GetContactedSheet()
```

Get a contacted sheet

### SetContactedGeometry

```
SetContactedGeometry()
```

Set a contacted geometry

### SetContactedSheet

```
SetContactedSheet()
```

Set a contacted sheet

### classIMTT3DContact

```
classIMTT3DContact(oobj=None)
```

Bases:DispatchBaseClassMTT3D contactPropertiesActiveActiveCommentCommentContactPointsThe number of max contact pointsForceDisplayForce displayFullNameFullName such asBody1.Marker1@Model1LayerNumberLayer numberNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceSpecialContactPointsSpecial Number of max contact pointsUseSpecialContactPointsUse sp

### Item

```
IMTT3DContactCollection.Item(var)
```

Returns a specific item.

### classIMTT3DContactCollection

```
classIMTT3DContactCollection(oobj=None)
```

Bases:DispatchBaseClassPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### Item

```
Item()
```

Returns a specific item.

### classIMTT3DContactProperty

```
classIMTT3DContactProperty(oobj=None)
```

Bases:DispatchBaseClassMTT3D contact propertyPropertiesBoundaryPenetrationBoundary penetrationContactParameterTypeContact parameter typeFrictionCoefficientFriction coefficientFrictionTypeFriction typeIndentationExponentIndentation exponentMaximumDampingMaximum dampingRDFRDFSpecialBoundaryPenetrationSpecial boundary penetrationSpecialFrictionCoefficientSpecial friction coefficientSpecialIndentationExponentSpecial indentation exponentSpecialMaximumDampingSpecial maximum dampingSpecialRDFSpecial RD

### classIMTT3DContactPropertyCircularGuide

```
classIMTT3DContactPropertyCircularGuide(oobj=None)
```

Bases:DispatchBaseClassMTT3D circular guide contact propertyPropertiesBoundaryPenetrationBoundary penetrationContactParameterTypeContact parameter typeFrictionCoefficientFriction coefficientFrictionTypeFriction typeGuideVelocityGuide velocityIndentationExponentIndentation exponentMaximumDampingMaximum dampingRDFRDFSpecialBoundaryPenetrationSpecial boundary penetrationSpecialFrictionCoefficientSpecial friction coefficientSpecialIndentationExponentSpecial indentation exponentSpecialMaximumDampingS

### classIMTT3DContactPropertyGuide

```
classIMTT3DContactPropertyGuide(oobj=None)
```

Bases:DispatchBaseClassMTT3D guide contact propertyPropertiesBoundaryPenetrationBoundary penetrationContactParameterTypeContact parameter typeFrictionCoefficientFriction coefficientFrictionFactorVertexofSheetFriction factor at vertex of sheetFrictionTypeFriction typeGuideVelocityGuide velocityIndentationExponentIndentation exponentMaximumDampingMaximum dampingRDFRDFSpecialBoundaryPenetrationSpecial boundary penetrationSpecialFrictionCoefficientSpecial friction coefficientSpecialIndentationExpone

### classIMTT3DContactPropertyRollerMovableToFixed

```
classIMTT3DContactPropertyRollerMovableToFixed(oobj=None)
```

Bases:DispatchBaseClassMTT3D movable roller contact propertyPropertiesBoundaryPenetrationBoundary penetrationContactParameterTypeContact parameter typeFrictionCoefficientFriction coefficientFrictionTypeFriction typeIndentationExponentIndentation exponentMaximumDampingMaximum dampingOffsetPenetrationOffset penetrationRDFRDFSpecialBoundaryPenetrationSpecial boundary penetrationSpecialFrictionCoefficientSpecial friction coefficientSpecialIndentationExponentSpecial indentation exponentSpecialMaximum

### classIMTT3DContactPropertyRollerToSheet

```
classIMTT3DContactPropertyRollerToSheet(oobj=None)
```

Bases:DispatchBaseClassMTT3D fixed roller contact propertyPropertiesBoundaryPenetrationBoundary penetrationContactParameterTypeContact parameter typeFrictionCoefficientFriction coefficientFrictionTypeFriction typeIndentationExponentIndentation exponentMaximumDampingMaximum dampingOverdriveFactorOver drive factorRDFRDFSpecialBoundaryPenetrationSpecial boundary penetrationSpecialFrictionCoefficientSpecial friction coefficientSpecialIndentationExponentSpecial indentation exponentSpecialMaximumDampi

### classIMTT3DContactSheetShellToSphere

```
classIMTT3DContactSheetShellToSphere(oobj=None)
```

Bases:DispatchBaseClassMTT3D sheet shell to sphere contactPropertiesActionSheetAction sheetActiveActiveBaseSphereBase entityCommentCommentContactPointsThe number of max contact pointsContactPropertySheetToSphereThe contact parameters of contact forces applied between sheet and sphereForceDisplayForce displayFullNameFullName such asBody1.Marker1@Model1LayerNumberLayer numberNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning 

### classIMTT3DContactSheetShellToSurface

```
classIMTT3DContactSheetShellToSurface(oobj=None)
```

Bases:DispatchBaseClassMTT3D sheet shell to surface contactPropertiesActionSheetAction sheetActiveActiveBasePatchOptionBase Patch OptionBaseSurfaceBase entityCommentCommentContactPointsThe number of max contact pointsContactPropertySheetToSurfaceThe contact parameters of contact forces applied between sheet and surfaceForceDisplayForce displayFullNameFullName such asBody1.Marker1@Model1LayerNumberLayer numberNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBo

### classIMTT3DContactSheetShellToTorus

```
classIMTT3DContactSheetShellToTorus(oobj=None)
```

Bases:DispatchBaseClassMTT3D sheet shell to torus contactPropertiesActionSheetAction sheetActiveActiveBaseTorusBase entityCommentCommentContactPointsThe number of max contact pointsContactPropertySheetToTorusThe contact parameters of contact forces applied between sheet and torusForceDisplayForce displayFullNameFullName such asBody1.Marker1@Model1LayerNumberLayer numberNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBod

### Add

```
IMTT3DCrownRollerProfile.Add(dX,dY,dR)
```

Add data

### Clear

```
IMTT3DCrownRollerProfile.Clear()
```

Clear data

### Export

```
IMTT3DCrownRollerProfile.Export(strFullPathName)
```

Export a file

### Import

```
IMTT3DCrownRollerProfile.Import(strFullPathName)
```

Import a file

### classIMTT3DCrownRollerProfile

```
classIMTT3DCrownRollerProfile(oobj=None)
```

Bases:DispatchBaseClassMTT3D crown roller informationPropertiesProfileCollectionProfile CollectionMethodsAddAdd dataClearClear dataExportExport a fileImportImport a file

### Add

```
Add()
```

Add data

### Clear

```
Clear()
```

Clear data

### Export

```
Export()
```

Export a file

### Import

```
Import()
```

Import a file

### Item

```
IMTT3DFixedRollerGroupCollection.Item(var)
```

Returns a specific item.

### classIMTT3DFixedRollerGroupCollection

```
classIMTT3DFixedRollerGroupCollection(oobj=None)
```

Bases:DispatchBaseClassPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### Item

```
Item()
```

Returns a specific item.

### GetAppliedBody

```
IMTT3DForceNodal.GetAppliedBody(uiID)
```

Specifies whether nodal force is applied to a node

### SetAppliedBody

```
IMTT3DForceNodal.SetAppliedBody(uiID,vBool)
```

Applies nodal force to a node

### SetAppliedBodyAll

```
IMTT3DForceNodal.SetAppliedBodyAll(flag)
```

Applies nodal force to all nodes

### classIMTT3DForceNodal

```
classIMTT3DForceNodal(oobj=None)
```

Bases:DispatchBaseClassMTT3D nodal forcePropertiesActiveActiveBaseBodyBase BodyCommentCommentFullNameFullName such asBody1.Marker1@Model1LayerNumberLayer numberNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceReportNodeIDsReport node IDsUseReportNodesUse report nNodesUserDataUser supplied dataUserSubroutineUser subroutineMethodsGetAppliedBod

### GetAppliedBody

```
GetAppliedBody()
```

Specifies whether nodal force is applied to a node

### SetAppliedBody

```
SetAppliedBody()
```

Applies nodal force to a node

### SetAppliedBodyAll

```
SetAppliedBodyAll()
```

Applies nodal force to all nodes

### Item

```
IMTT3DForceNodalCollection.Item(var)
```

Returns a specific item.

### classIMTT3DForceNodalCollection

```
classIMTT3DForceNodalCollection(oobj=None)
```

Bases:DispatchBaseClassIForceNodalCollectionPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### Item

```
Item()
```

Returns a specific item.

### CopyActionToBase

```
IMTT3DForceSpring.CopyActionToBase(Type)
```

Copy action to base

### CopyBaseToAction

```
IMTT3DForceSpring.CopyBaseToAction(Type)
```

Copy base to action

### classIMTT3DForceSpring

```
classIMTT3DForceSpring(oobj=None)
```

Bases:DispatchBaseClassMTT3D spring forcePropertiesActionMarkerAction markerActiveActiveBaseBodyBase bodyBaseMarkerBase markerCommentCommentDampingDampingForceDisplayForce displayForceDisplayColorForce display colorForceDisplayUseForce display useFreeLengthThe free length of the springFullNameFullName such asBody1.Marker1@Model1LayerNameLayer nameLayerNumberLayer numberNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBod

### CopyActionToBase

```
CopyActionToBase()
```

Copy action to base

