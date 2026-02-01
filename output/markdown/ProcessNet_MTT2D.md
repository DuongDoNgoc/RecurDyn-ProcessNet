# ProcessNet.MTT2D

> ProcessNet.MTT2D API

## Overview

**Full Name:** FunctionBay.RecurDyn.ProcessNet.MTT2D

**Methods:** 131

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

### classGuideVelocityType

```
classGuideVelocityType(value)
```

Bases:IntEnumGuideVelocityType enumeration.MembersGuideVelocityType_ConstantConstant value is 0.GuideVelocityType_ExpressionConstant value is 1.

### GetContactedGeometry

```
IMTT2DAssembly.GetContactedGeometry(pVal)
```

Get a contacted geometry

### GetContactedSheet

```
IMTT2DAssembly.GetContactedSheet(pVal)
```

Get a contacted sheet

### SetContactedGeometry

```
IMTT2DAssembly.SetContactedGeometry(pVal,vBool)
```

Set a contacted geometry

### SetContactedSheet

```
IMTT2DAssembly.SetContactedSheet(pVal,vBool)
```

Set a contacted sheet

### classIMTT2DAssembly

```
classIMTT2DAssembly(oobj=None)
```

Bases:DispatchBaseClassMTT2D assemblyPropertiesBufferRadiusFactorBuffer radius factorCommentCommentFullNameFullName such asBody1.Marker1@Model1MaximumNoOfSheetSegmentsMaximum number of sheet's segmentsMaximumStepsizeFactorMaximum stepsize factorNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfacePenetrationParameterPenetration parameterReferenc

### classIMTT2DContactProperty

```
classIMTT2DContactProperty(oobj=None)
```

Bases:DispatchBaseClassMTT2D contact propertyPropertiesBoundaryPenetrationBoundary penetrationContactParameterTypeContact parameter typeFrictionCoefficientFriction coefficientFrictionTypeFriction typeIndentationExponentIndentation exponentMaximumDampingMaximum dampingRDFRDFSpecialBoundaryPenetrationSpecial boundary penetrationSpecialFrictionCoefficientSpecial friction coefficientSpecialIndentationExponentSpecial indentation exponentSpecialMaximumDampingSpecial maximum dampingSpecialRDFSpecial RD

### classIMTT2DContactPropertyGuide

```
classIMTT2DContactPropertyGuide(oobj=None)
```

Bases:DispatchBaseClassMTT2D guide contact propertyPropertiesBoundaryPenetrationBoundary penetrationContactParameterTypeContact parameter typeFrictionCoefficientFriction coefficientFrictionTypeFriction typeGuideToleranceGuide toleranceGuideVelocityGuide velocity constant valueGuideVelocityExpressionGuide velocity expressionGuideVelocityTypeGuide velocity typeIndentationExponentIndentation exponentMaximumDampingMaximum dampingRDFRDFSpecialBoundaryPenetrationSpecial boundary penetrationSpecialFric

### classIMTT2DContactPropertyPGuide

```
classIMTT2DContactPropertyPGuide(oobj=None)
```

Bases:DispatchBaseClassMTT2D circular guide contact propertyPropertiesBoundaryPenetrationBoundary penetrationContactParameterTypeContact parameter typeFrictionCoefficientFriction coefficientFrictionTypeFriction typeGuideVelocityGuide velocity constant valueGuideVelocityExpressionGuide velocity expressionGuideVelocityTypeGuide velocity typeIndentationExponentIndentation exponentMaximumDampingMaximum dampingRDFRDFSpecialBoundaryPenetrationSpecial boundary penetrationSpecialFrictionCoefficientSpeci

### classIMTT2DContactPropertyRoller

```
classIMTT2DContactPropertyRoller(oobj=None)
```

Bases:DispatchBaseClassMTT2D contact propertyPropertiesBoundaryPenetrationBoundary penetrationContactParameterTypeContact parameter typeFrictionCoefficientFriction coefficientFrictionTypeFriction typeIndentationExponentIndentation exponentMaxStictionDeformationMaximum stiction deformationMaximumDampingMaximum dampingRDFRDFSpecialBoundaryPenetrationSpecial boundary penetrationSpecialFrictionCoefficientSpecial friction coefficientSpecialIndentationExponentSpecial indentation exponentSpecialMaximum

### classIMTT2DContactPropertyRollerMovableToFixed

```
classIMTT2DContactPropertyRollerMovableToFixed(oobj=None)
```

Bases:DispatchBaseClassMTT2D movable roller contact propertyPropertiesBoundaryPenetrationBoundary penetrationContactParameterTypeContact parameter typeFrictionCoefficientFriction coefficientFrictionTypeFriction typeIndentationExponentIndentation exponentMaxStictionDeformationMaximum stiction deformationMaximumDampingMaximum dampingOffsetPenetrationOffset penetrationRDFRDFSpecialBoundaryPenetrationSpecial boundary penetrationSpecialFrictionCoefficientSpecial friction coefficientSpecialIndentation

### classIMTT2DContactPropertyRollerToSheet

```
classIMTT2DContactPropertyRollerToSheet(oobj=None)
```

Bases:DispatchBaseClassMTT2D fixed roller contact propertyPropertiesBoundaryPenetrationBoundary penetrationContactParameterTypeContact parameter typeFrictionCoefficientFriction coefficientFrictionTypeFriction typeIndentationExponentIndentation exponentMaxStictionDeformationMaximum stiction deformationMaximumDampingMaximum dampingRDFRDFSpecialBoundaryPenetrationSpecial boundary penetrationSpecialFrictionCoefficientSpecial friction coefficientSpecialIndentationExponentSpecial indentation exponentS

### classIMTT2DContactSheetToSheet

```
classIMTT2DContactSheetToSheet(oobj=None)
```

Bases:DispatchBaseClassMTT2D sheet to sheet contactPropertiesActionSheetGroupAction sheet groupActiveActiveBaseSheetGroupBase sheet groupCommentCommentContactPointsThe number of max contact pointsContactPropertySheetToSheetThe contact parameters of contact forces applied between the sheetsForceDisplayForce displayFullNameFullName such asBody1.Marker1@Model1LayerNumberLayer numberNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns o

### Item

```
IMTT2DContactSheetToSheetCollection.Item(var)
```

Returns a specific item.

### classIMTT2DContactSheetToSheetCollection

```
classIMTT2DContactSheetToSheetCollection(oobj=None)
```

Bases:DispatchBaseClassPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### Item

```
IMTT2DFixedRollerGroupCollection.Item(var)
```

Returns a specific item.

### classIMTT2DFixedRollerGroupCollection

```
classIMTT2DFixedRollerGroupCollection(oobj=None)
```

Bases:DispatchBaseClassPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### classIMTT2DFlexibleRollerProperty

```
classIMTT2DFlexibleRollerProperty(oobj=None)
```

Bases:DispatchBaseClassMTT2D flexible roller propertyPropertiesAllDampingRatioAll damping ratioAllDensityAll densityAllPoissonsRatioAll Poisson's ratioAllTotalMassAll total massAllYoungsModulusAll Young's modulusColorColorDampingRatioDamping ratioDensityDensityDepthThe depth of the fixed roller bodyDrillingStiffnessFactorDrilling stiffness factorFDRRadiusThe FDR radiusMassTypeThe type of method to apply massNoOfNodesCircumferenceNumber of nodes at circumferenceNoOfNodesRadialNumber of nodes at r

### GetAppliedBody

```
IMTT2DForceNodal.GetAppliedBody(pVal)
```

Specifies whether nodal force is applied to a body.

### SetAppliedBody

```
IMTT2DForceNodal.SetAppliedBody(pVal,vBool)
```

Applies nodal force to a body

### classIMTT2DForceNodal

```
classIMTT2DForceNodal(oobj=None)
```

Bases:DispatchBaseClassMTT2D nodal forcePropertiesActiveActiveBaseBodyBase BodyCommentCommentFullNameFullName such asBody1.Marker1@Model1LayerNumberLayer numberNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceUserDataUser supplied dataUserSubroutineUser subroutineMethodsGetAppliedBodySpecifies whether nodal force is applied to a body.SetAppl

### Item

```
IMTT2DForceNodalCollection.Item(var)
```

Returns a specific item.

### classIMTT2DForceNodalCollection

```
classIMTT2DForceNodalCollection(oobj=None)
```

Bases:DispatchBaseClassIForceNodalCollectionPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### CopyActionToBase

```
IMTT2DForceSpring.CopyActionToBase(Type)
```

Copy action to base

### CopyBaseToAction

```
IMTT2DForceSpring.CopyBaseToAction(Type)
```

Copy base to action

### classIMTT2DForceSpring

```
classIMTT2DForceSpring(oobj=None)
```

Bases:DispatchBaseClassMTT2D spring forcePropertiesActionMarkerAction markerActiveActiveBaseBodyBase bodyBaseMarkerBase markerCommentCommentDampingDampingForceDisplayForce displayForceDisplayColorForce display colorForceDisplayUseForce display useFreeLengthThe free length of the springFullNameFullName such asBody1.Marker1@Model1LayerNameLayer nameLayerNumberLayer numberNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBod

### CopyActionToBase

```
IMTT2DForceSpringNip.CopyActionToBase(Type)
```

Copy action to base

### CopyBaseToAction

```
IMTT2DForceSpringNip.CopyBaseToAction(Type)
```

Copy base to action

### classIMTT2DForceSpringNip

```
classIMTT2DForceSpringNip(oobj=None)
```

Bases:DispatchBaseClassMTT2D nip spring forcePropertiesActionMarkerAction markerActiveActiveBaseBodyBase bodyBaseMarkerBase markerBasePointBase pointCommentCommentDampingDampingForceDisplayForce displayForceDisplayColorForce display colorForceDisplayUseForce display useFreeLengthThe free length of the springFullNameFullName such asBody1.Marker1@Model1LayerNameLayer nameLayerNumberLayer numberNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerB

### CopyActionToBase

```
IMTT2DForceSpringTSD.CopyActionToBase(Type)
```

Copy action to base

### CopyBaseToAction

```
IMTT2DForceSpringTSD.CopyBaseToAction(Type)
```

Copy base to action

### classIMTT2DForceSpringTSD

```
classIMTT2DForceSpringTSD(oobj=None)
```

Bases:DispatchBaseClassMTT2D TSD spring forcePropertiesActionMarkerAction markerActionPointAction pointActiveActiveBaseBodyBase bodyBaseMarkerBase markerCommentCommentDampingDampingForceDisplayForce displayForceDisplayColorForce display colorForceDisplayUseForce display useFreeLengthThe free length of the springFullNameFullName such asBody1.Marker1@Model1LayerNameLayer nameLayerNumberLayer numberNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOw

### SetLayerNumber

```
IMTT2DGroupFixedRoller.SetLayerNumber(iVal)
```

Set layer Number

### UpdateActiveFlagOfAllEntities

```
IMTT2DGroupFixedRoller.UpdateActiveFlagOfAllEntities(Val)
```

Update active flag of all entities

### UpdateAllProperties

```
IMTT2DGroupFixedRoller.UpdateAllProperties()
```

Update all properties

### UpdateNonGeometricProperties

```
IMTT2DGroupFixedRoller.UpdateNonGeometricProperties()
```

Update non-geometric properties

### classIMTT2DGroupFixedRoller

```
classIMTT2DGroupFixedRoller(oobj=None)
```

Bases:DispatchBaseClassMTT2D fixed roller groupPropertiesActiveActiveBaseBodyThe base body of the revolute jointCenterPointThe center point of the fixed roller bodyCommentCommentContactPointsThe number of max contact pointsContactPropertyToSheetThe parameters of contact forces applied between sheet and fixed rollerEachRenderModeRendering modeForceDisplayForce displayFullNameFullName such asBody1.Marker1@Model1InertiaIzz, the mass moment of inertia in the z-axis of the rollerLayerNumberLayer numb

### SetLayerNumber

```
IMTT2DGroupFixedRollerShell.SetLayerNumber(iVal)
```

Set layer Number

### UpdateActiveFlagOfAllEntities

```
IMTT2DGroupFixedRollerShell.UpdateActiveFlagOfAllEntities(Val)
```

Update active flag of all entities

### UpdateAllProperties

```
IMTT2DGroupFixedRollerShell.UpdateAllProperties()
```

Update all properties

### UpdateNonGeometricProperties

```
IMTT2DGroupFixedRollerShell.UpdateNonGeometricProperties()
```

Update non-geometric properties

### classIMTT2DGroupFixedRollerShell

```
classIMTT2DGroupFixedRollerShell(oobj=None)
```

Bases:DispatchBaseClassMTT2D fixed shell roller groupPropertiesActiveActiveBaseBodyThe base body of the revolute jointCenterPointThe center point of the fixed roller bodyCommentCommentContactPointsThe number of max contact pointsContactPropertyToSheetThe parameters of contact forces applied between sheet and fixed rollerEachRenderModeRendering modeFlexBodyFlex body editFlexibleRollerPropertyFlexible roller propertyForceDisplayForce displayFullNameFullName such asBody1.Marker1@Model1LayerNumberLa

### SetLayerNumber

```
IMTT2DGroupGuideBody.SetLayerNumber(iVal)
```

Set layer Number

### SetSecondParametricPoint

```
IMTT2DGroupGuideBody.SetSecondParametricPoint(pVal)
```

Set second point

### SetSecondPoint

```
IMTT2DGroupGuideBody.SetSecondPoint(dX,dY,dZ)
```

Set second point

### SetStartParametricPoint

```
IMTT2DGroupGuideBody.SetStartParametricPoint(pVal)
```

Set start point

### SetStartPoint

```
IMTT2DGroupGuideBody.SetStartPoint(dX,dY,dZ)
```

Set start point

