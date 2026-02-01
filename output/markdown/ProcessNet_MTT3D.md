# ProcessNet.MTT3D

> ProcessNet.MTT3D API

## Overview

**Full Name:** FunctionBay.RecurDyn.ProcessNet.MTT3D

**Methods:** 119

**Examples:** 0

## Methods

### classAirResistanceForceDirection

```
classAirResistanceForceDirection(value)¶
```

Bases:IntEnumAirResistanceForceDirection enumeration.MembersDirectionType_ElementNormalConstant value is 0.DirectionType_VelocityConstant value is 1.

### classAirResistanceType

```
classAirResistanceType(value)¶
```

Bases:IntEnumAirResistanceType enumeration.MembersAirResistanceType_ConstantConstant value is 0.AirResistanceType_ExpressionConstant value is 1.

### classContactParameterType

```
classContactParameterType(value)¶
```

Bases:IntEnumContactParameterType enumeration.MembersContactParameterType_BoundaryPenetrationConstant value is 0.ContactParameterType_IndentationExponentConstant value is 1.

### GetContactedGeometry

```
IMTT3DAssembly.GetContactedGeometry(pVal)¶
```

Get a contacted geometry

### GetContactedSheet

```
IMTT3DAssembly.GetContactedSheet(pVal)¶
```

Get a contacted sheet

### SetContactedGeometry

```
IMTT3DAssembly.SetContactedGeometry(pVal,vBool)¶
```

Set a contacted geometry

### SetContactedSheet

```
IMTT3DAssembly.SetContactedSheet(pVal,vBool)¶
```

Set a contacted sheet

### classIMTT3DAssembly

```
classIMTT3DAssembly(oobj=None)¶
```

Bases:DispatchBaseClassMTT3D assemblyPropertiesBufferRadiusFactorBuffer radius factorCommentCommentFullNameFullName such asBody1.Marker1@Model1MaximumNoOfSheetElementsMaximum number of sheet's elementsMaximumStepsizeFactorMaximum stepsize factorNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfacePenetrationParameterPenetration parameterReferenc

### classIMTT3DContact

```
classIMTT3DContact(oobj=None)¶
```

Bases:DispatchBaseClassMTT3D contactPropertiesActiveActiveCommentCommentContactPointsThe number of max contact pointsForceDisplayForce displayFullNameFullName such asBody1.Marker1@Model1LayerNumberLayer numberNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceSpecialContactPointsSpecial Number of max contact pointsUseSpecialContactPointsUse sp

### Item

```
IMTT3DContactCollection.Item(var)¶
```

Returns a specific item.

### classIMTT3DContactCollection

```
classIMTT3DContactCollection(oobj=None)¶
```

Bases:DispatchBaseClassPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### classIMTT3DContactProperty

```
classIMTT3DContactProperty(oobj=None)¶
```

Bases:DispatchBaseClassMTT3D contact propertyPropertiesBoundaryPenetrationBoundary penetrationContactParameterTypeContact parameter typeFrictionCoefficientFriction coefficientFrictionTypeFriction typeIndentationExponentIndentation exponentMaximumDampingMaximum dampingRDFRDFSpecialBoundaryPenetrationSpecial boundary penetrationSpecialFrictionCoefficientSpecial friction coefficientSpecialIndentationExponentSpecial indentation exponentSpecialMaximumDampingSpecial maximum dampingSpecialRDFSpecial RD

### classIMTT3DContactPropertyCircularGuide

```
classIMTT3DContactPropertyCircularGuide(oobj=None)¶
```

Bases:DispatchBaseClassMTT3D circular guide contact propertyPropertiesBoundaryPenetrationBoundary penetrationContactParameterTypeContact parameter typeFrictionCoefficientFriction coefficientFrictionTypeFriction typeGuideVelocityGuide velocityIndentationExponentIndentation exponentMaximumDampingMaximum dampingRDFRDFSpecialBoundaryPenetrationSpecial boundary penetrationSpecialFrictionCoefficientSpecial friction coefficientSpecialIndentationExponentSpecial indentation exponentSpecialMaximumDampingS

### classIMTT3DContactPropertyGuide

```
classIMTT3DContactPropertyGuide(oobj=None)¶
```

Bases:DispatchBaseClassMTT3D guide contact propertyPropertiesBoundaryPenetrationBoundary penetrationContactParameterTypeContact parameter typeFrictionCoefficientFriction coefficientFrictionFactorVertexofSheetFriction factor at vertex of sheetFrictionTypeFriction typeGuideVelocityGuide velocityIndentationExponentIndentation exponentMaximumDampingMaximum dampingRDFRDFSpecialBoundaryPenetrationSpecial boundary penetrationSpecialFrictionCoefficientSpecial friction coefficientSpecialIndentationExpone

### classIMTT3DContactPropertyRollerMovableToFixed

```
classIMTT3DContactPropertyRollerMovableToFixed(oobj=None)¶
```

Bases:DispatchBaseClassMTT3D movable roller contact propertyPropertiesBoundaryPenetrationBoundary penetrationContactParameterTypeContact parameter typeFrictionCoefficientFriction coefficientFrictionTypeFriction typeIndentationExponentIndentation exponentMaximumDampingMaximum dampingOffsetPenetrationOffset penetrationRDFRDFSpecialBoundaryPenetrationSpecial boundary penetrationSpecialFrictionCoefficientSpecial friction coefficientSpecialIndentationExponentSpecial indentation exponentSpecialMaximum

### classIMTT3DContactPropertyRollerToSheet

```
classIMTT3DContactPropertyRollerToSheet(oobj=None)¶
```

Bases:DispatchBaseClassMTT3D fixed roller contact propertyPropertiesBoundaryPenetrationBoundary penetrationContactParameterTypeContact parameter typeFrictionCoefficientFriction coefficientFrictionTypeFriction typeIndentationExponentIndentation exponentMaximumDampingMaximum dampingOverdriveFactorOver drive factorRDFRDFSpecialBoundaryPenetrationSpecial boundary penetrationSpecialFrictionCoefficientSpecial friction coefficientSpecialIndentationExponentSpecial indentation exponentSpecialMaximumDampi

### classIMTT3DContactSheetShellToSphere

```
classIMTT3DContactSheetShellToSphere(oobj=None)¶
```

Bases:DispatchBaseClassMTT3D sheet shell to sphere contactPropertiesActionSheetAction sheetActiveActiveBaseSphereBase entityCommentCommentContactPointsThe number of max contact pointsContactPropertySheetToSphereThe contact parameters of contact forces applied between sheet and sphereForceDisplayForce displayFullNameFullName such asBody1.Marker1@Model1LayerNumberLayer numberNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning 

### classIMTT3DContactSheetShellToSurface

```
classIMTT3DContactSheetShellToSurface(oobj=None)¶
```

Bases:DispatchBaseClassMTT3D sheet shell to surface contactPropertiesActionSheetAction sheetActiveActiveBasePatchOptionBase Patch OptionBaseSurfaceBase entityCommentCommentContactPointsThe number of max contact pointsContactPropertySheetToSurfaceThe contact parameters of contact forces applied between sheet and surfaceForceDisplayForce displayFullNameFullName such asBody1.Marker1@Model1LayerNumberLayer numberNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBo

### classIMTT3DContactSheetShellToTorus

```
classIMTT3DContactSheetShellToTorus(oobj=None)¶
```

Bases:DispatchBaseClassMTT3D sheet shell to torus contactPropertiesActionSheetAction sheetActiveActiveBaseTorusBase entityCommentCommentContactPointsThe number of max contact pointsContactPropertySheetToTorusThe contact parameters of contact forces applied between sheet and torusForceDisplayForce displayFullNameFullName such asBody1.Marker1@Model1LayerNumberLayer numberNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBod

### Add

```
IMTT3DCrownRollerProfile.Add(dX,dY,dR)¶
```

Add data

### Clear

```
IMTT3DCrownRollerProfile.Clear()¶
```

Clear data

### Export

```
IMTT3DCrownRollerProfile.Export(strFullPathName)¶
```

Export a file

### Import

```
IMTT3DCrownRollerProfile.Import(strFullPathName)¶
```

Import a file

### classIMTT3DCrownRollerProfile

```
classIMTT3DCrownRollerProfile(oobj=None)¶
```

Bases:DispatchBaseClassMTT3D crown roller informationPropertiesProfileCollectionProfile CollectionMethodsAddAdd dataClearClear dataExportExport a fileImportImport a file

### Item

```
IMTT3DFixedRollerGroupCollection.Item(var)¶
```

Returns a specific item.

### classIMTT3DFixedRollerGroupCollection

```
classIMTT3DFixedRollerGroupCollection(oobj=None)¶
```

Bases:DispatchBaseClassPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### GetAppliedBody

```
IMTT3DForceNodal.GetAppliedBody(uiID)¶
```

Specifies whether nodal force is applied to a node

### SetAppliedBody

```
IMTT3DForceNodal.SetAppliedBody(uiID,vBool)¶
```

Applies nodal force to a node

### SetAppliedBodyAll

```
IMTT3DForceNodal.SetAppliedBodyAll(flag)¶
```

Applies nodal force to all nodes

### classIMTT3DForceNodal

```
classIMTT3DForceNodal(oobj=None)¶
```

Bases:DispatchBaseClassMTT3D nodal forcePropertiesActiveActiveBaseBodyBase BodyCommentCommentFullNameFullName such asBody1.Marker1@Model1LayerNumberLayer numberNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceReportNodeIDsReport node IDsUseReportNodesUse report nNodesUserDataUser supplied dataUserSubroutineUser subroutineMethodsGetAppliedBod

### Item

```
IMTT3DForceNodalCollection.Item(var)¶
```

Returns a specific item.

### classIMTT3DForceNodalCollection

```
classIMTT3DForceNodalCollection(oobj=None)¶
```

Bases:DispatchBaseClassIForceNodalCollectionPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### CopyActionToBase

```
IMTT3DForceSpring.CopyActionToBase(Type)¶
```

Copy action to base

### CopyBaseToAction

```
IMTT3DForceSpring.CopyBaseToAction(Type)¶
```

Copy base to action

### classIMTT3DForceSpring

```
classIMTT3DForceSpring(oobj=None)¶
```

Bases:DispatchBaseClassMTT3D spring forcePropertiesActionMarkerAction markerActiveActiveBaseBodyBase bodyBaseMarkerBase markerCommentCommentDampingDampingForceDisplayForce displayForceDisplayColorForce display colorForceDisplayUseForce display useFreeLengthThe free length of the springFullNameFullName such asBody1.Marker1@Model1LayerNameLayer nameLayerNumberLayer numberNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBod

### CopyActionToBase

```
IMTT3DForceSpringNip.CopyActionToBase(Type)¶
```

Copy action to base

### CopyBaseToAction

```
IMTT3DForceSpringNip.CopyBaseToAction(Type)¶
```

Copy base to action

### classIMTT3DForceSpringNip

```
classIMTT3DForceSpringNip(oobj=None)¶
```

Bases:DispatchBaseClassMTT3D nip spring forcePropertiesActionMarkerAction markerActiveActiveBaseBodyBase bodyBaseMarkerBase markerBasePointBase pointCommentCommentDampingDampingForceDisplayForce displayForceDisplayColorForce display colorForceDisplayUseForce display useFreeLengthThe free length of the springFullNameFullName such asBody1.Marker1@Model1LayerNameLayer nameLayerNumberLayer numberNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerB

### SetLayerNumber

```
IMTT3DGroupFixedRoller.SetLayerNumber(iVal)¶
```

Set layer Number

### UpdateActiveFlagOfAllEntities

```
IMTT3DGroupFixedRoller.UpdateActiveFlagOfAllEntities(Val)¶
```

Update active flag of all entities

### UpdateAllProperties

```
IMTT3DGroupFixedRoller.UpdateAllProperties()¶
```

Update all properties

### classIMTT3DGroupFixedRoller

```
classIMTT3DGroupFixedRoller(oobj=None)¶
```

Bases:DispatchBaseClassMTT3D fixed roller groupPropertiesActiveActiveBaseBodyThe base body of the revolute jointCenterPointThe center point of the fixed roller bodyCenterPoint2The center point of the fixed roller bodyCommentCommentContactPointsThe number of max contact pointsContactPropertyToSheetThe parameters of contact forces applied between sheet and fixed rollerCrownRollerProfileCrownRoller ProfileDepthThe depth of the fixed rollerDepthDirectionThe depth direction at the center point of fix

### SetLayerNumber

```
IMTT3DGroupMovableRoller.SetLayerNumber(iVal)¶
```

Set layer Number

### UpdateActiveFlagOfAllEntities

```
IMTT3DGroupMovableRoller.UpdateActiveFlagOfAllEntities(Val)¶
```

Update active flag of all entities

### UpdateAllProperties

```
IMTT3DGroupMovableRoller.UpdateAllProperties()¶
```

Update all properties

### UpdateNonGeometricProperties

```
IMTT3DGroupMovableRoller.UpdateNonGeometricProperties()¶
```

Update non-geometric properties

### classIMTT3DGroupMovableRoller

```
classIMTT3DGroupMovableRoller(oobj=None)¶
```

Bases:DispatchBaseClassMTT3D movable roller groupPropertiesActiveActiveBaseBodyThe base body of the revolute jointCenterPointThe center point of the movable roller bodyCenterPoint2The center point of the movable roller bodyCommentCommentContactPointsToRollerThe number of max contact points to rollerContactPointsToSheetThe number of max contact points to sheetContactPropertyToFixedRollerThe parameters of contact forces applied between fixed roller and movable rollerContactPropertyToSheetThe param

### UpdateAllProperties

```
IMTT3DGuide.UpdateAllProperties()¶
```

Update All Properties

### classIMTT3DGuide

```
classIMTT3DGuide(oobj=None)¶
```

Bases:DispatchBaseClassMTT3D guidePropertiesActiveActiveCommentCommentContactPointsThe number of max contact pointsForceDisplayForce displayFullNameFullName such asBody1.Marker1@Model1GraphicGraphicLayerNumberLayer numberMotherBodyThe mother body of guideNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceSpecialContactPointsSpecial Number of m

### UpdateAllProperties

```
IMTT3DGuideArc.UpdateAllProperties()¶
```

Update All Properties

