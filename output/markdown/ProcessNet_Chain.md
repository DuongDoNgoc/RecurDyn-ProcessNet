# ProcessNet.Chain

> ProcessNet.Chain API

## Overview

**Full Name:** FunctionBay.RecurDyn.ProcessNet.Chain

**Methods:** 198

**Examples:** 0

## Methods

### classChainAssemblyBushingType

```
classChainAssemblyBushingType(value)¶
```

Bases:IntEnumChainAssemblyBushingType enumeration.MembersChainAssemblyBushingType_DoubleConstant value is 1.ChainAssemblyBushingType_SingleConstant value is 0.

### classChainContactSearchType

```
classChainContactSearchType(value)¶
```

Bases:IntEnumChainContactSearchType enumeration.MembersChainContactSearchType_FullSearchConstant value is 0.ChainContactSearchType_PartialSearchConstant value is 1.

### classChainFrictionType

```
classChainFrictionType(value)¶
```

Bases:IntEnumChainFrictionType enumeration.MembersChainFrictionType_DynamicFrictionCoefficientConstant value is 0.ChainFrictionType_FrictionCoefficientSplineConstant value is 2.ChainFrictionType_FrictionForceSplineConstant value is 1.

### classChainGuardInactiveType

```
classChainGuardInactiveType(value)¶
```

Bases:IntEnumChainGuardInactiveType enumeration.MembersChainGuardInactiveType_Left_InactiveConstant value is 1.ChainGuardInactiveType_NoneConstant value is 0.ChainGuardInactiveType_Right_InactiveConstant value is 2.

### classChainGuidePointsType

```
classChainGuidePointsType(value)¶
```

Bases:IntEnumChainGuidePointsType enumeration.MembersChainGuidePointsType_CenterPointsAndArcAngleConstant value is 2.ChainGuidePointsType_CenterPointsAndRadiusConstant value is 1.ChainGuidePointsType_PassingPointsConstant value is 0.

### classChainInOutType

```
classChainInOutType(value)¶
```

Bases:IntEnumChainInOutType enumeration.MembersChainInOutType_InConstant value is 0.ChainInOutType_NoneConstant value is 2.ChainInOutType_OutConstant value is 1.

### classChainLinkPlateShapeType

```
classChainLinkPlateShapeType(value)¶
```

Bases:IntEnumChainLinkPlateShapeType enumeration.MembersChainLinkPlateShapeType_BoxConstant value is 1.ChainLinkPlateShapeType_CircleConstant value is 0.

### classChainLinkType

```
classChainLinkType(value)¶
```

Bases:IntEnumChainLinkType enumeration.MembersChainLinkType_GeneralRollerLinkConstant value is 0.ChainLinkType_ISO606_05BConstant value is 1.ChainLinkType_ISO606_06BConstant value is 2.ChainLinkType_ISO606_081Constant value is 5.ChainLinkType_ISO606_083Constant value is 6.ChainLinkType_ISO606_084Constant value is 7.ChainLinkType_ISO606_085Constant value is 8.ChainLinkType_ISO606_08AConstant value is 3.ChainLinkType_ISO606_08BConstant value is 4.ChainLinkType_ISO606_10AConstant value is 9.ChainLi

### classChainNormalDirectionType

```
classChainNormalDirectionType(value)¶
```

Bases:IntEnumChainNormalDirectionType enumeration.MembersChainNormalDirectionType_DownConstant value is 1.ChainNormalDirectionType_UpConstant value is 0.

### classChainSprocketType

```
classChainSprocketType(value)¶
```

Bases:IntEnumChainSprocketType enumeration.MembersChainSprocketType_GeneralConstant value is 0.ChainSprocketType_ISO606LibraryConstant value is 1.ChainSprocketType_ParametersConstant value is 2.

### AddAllOutputLink

```
IChainAssembly.AddAllOutputLink()¶
```

Add all the link body to output list

### AddOutputLink

```
IChainAssembly.AddOutputLink(strFileName)¶
```

Add a link body to output list

### AddPassingBody

```
IChainAssembly.AddPassingBody(pVal)¶
```

Add a Passing Body

### DeletePassingBody

```
IChainAssembly.DeletePassingBody(pVal)¶
```

Delete a Passing Body

### GetOutputLinkList

```
IChainAssembly.GetOutputLinkList()¶
```

Chain assembly output list

### RemoveAllOutputLink

```
IChainAssembly.RemoveAllOutputLink()¶
```

Remove all the link body from output list

### RemoveOutputLink

```
IChainAssembly.RemoveOutputLink(strFileName)¶
```

Remove a link body from output list

### UpdateLinkInitialVelocityXAxis

```
IChainAssembly.UpdateLinkInitialVelocityXAxis()¶
```

Update Link Initial Velocity X-Axis Value

### classIChainAssembly

```
classIChainAssembly(oobj=None)¶
```

Bases:DispatchBaseClassChain AssemblyPropertiesBushingForceParameterBushing Force ParameterChainBodyLinkCollectionGet the Chain Body Link CollectionCommentCommentForceDisplayForce displayFullNameFullName such asBody1.Marker1@Model1LinkInitialVelocityXAxisLink Initial Velocity X-AxisLinkNumbersLink NumbersLinkPlateShapeTypeLink Plate Shape TypeNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOw

### Export

```
IChainAssemblyBushingForceParameter.Export(strName,val)¶
```

Export bushing force parameter

### Import

```
IChainAssemblyBushingForceParameter.Import(strName)¶
```

Import bushing force parameter

### classIChainAssemblyBushingForceParameter

```
classIChainAssemblyBushingForceParameter(oobj=None)¶
```

Bases:DispatchBaseClassChain AssemblyPropertiesFrictionFriction ParameterRotationDampingCoefficientXRotation damping coefficient XRotationDampingCoefficientYRotation damping coefficient YRotationDampingCoefficientZRotation damping coefficient ZRotationDampingExponentXRotation damping exponent XRotationDampingExponentYRotation damping exponent YRotationDampingExponentZRotation damping exponent ZRotationDampingSplineXRotation damping spline XRotationDampingSplineYRotation damping spline YRotationD

### Item

```
IChainAssemblyCollection.Item(var)¶
```

Returns a specific item.

### classIChainAssemblyCollection

```
classIChainAssemblyCollection(oobj=None)¶
```

Bases:DispatchBaseClassPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### classIChainAssemblyContactFriction

```
classIChainAssemblyContactFriction(oobj=None)¶
```

Bases:DispatchBaseClassChain Contact FrictionPropertiesDynamicFrictionCoefficientDynamic Friction CoefficientDynamicThresholdVelocityDynamic Threshold VelocityPinDiameterPin DiameterStaticFrictionCoefficientStatic Friction CoefficientStaticThresholdVelocityStatic Threshold Velocity

### classIChainBody

```
classIChainBody(oobj=None)¶
```

Bases:DispatchBaseClassChain bodyPropertiesCommentCommentFullNameFullName such asBody1.Marker1@Model1GeneralBodyGeneralBodyNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceUserDataUser supplied data

### Item

```
IChainBodyCollection.Item(var)¶
```

Returns a specific item.

### classIChainBodyCollection

```
classIChainBodyCollection(oobj=None)¶
```

Bases:DispatchBaseClassPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### classIChainBodyGuardLateral

```
classIChainBodyGuardLateral(oobj=None)¶
```

Bases:DispatchBaseClassChain guidePropertiesCommentCommentContactPropertyContact PropertyContactSearchContactSearchTypeFullNameFullName such asBody1.Marker1@Model1GeneralBodyGeneralBodyGeometryGeometryNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceUserDataUser supplied data

### UpdateGeometry

```
IChainBodyGuide.UpdateGeometry()¶
```

Update geometry

### classIChainBodyGuide

```
classIChainBodyGuide(oobj=None)¶
```

Bases:DispatchBaseClassChain guidePropertiesCommentCommentContactPropertyContact PropertyContactSearchContactSearchTypeForceDisplayForce displayFullNameFullName such asBody1.Marker1@Model1GeneralBodyGeneralBodyGeometryGeometryNameNameNormalDirectionNormal DirectionOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceUserDataUser supplied dataMethodsUpda

### classIChainBodyLink

```
classIChainBodyLink(oobj=None)¶
```

Bases:DispatchBaseClassChain Body LinkPropertiesCommentCommentFullNameFullName such asBody1.Marker1@Model1GeneralBodyGeneralBodyGraphicGraphicNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceUseBodyGraphicUse graphic of clone boyUserDataUser supplied data

### Item

```
IChainBodyLinkCollection.Item(var)¶
```

Returns a specific item.

### classIChainBodyLinkCollection

```
classIChainBodyLinkCollection(oobj=None)¶
```

Bases:DispatchBaseClassPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### classIChainBodyLinkMultiplexOffset

```
classIChainBodyLinkMultiplexOffset(oobj=None)¶
```

Bases:DispatchBaseClassChain Body Link Offset MultiplexPropertiesCommentCommentFullNameFullName such asBody1.Marker1@Model1GeneralBodyGeneralBodyGraphicGraphicNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceUseBodyGraphicUse graphic of clone boyUserDataUser supplied data

### UpdateGeometry

```
IChainBodyLinkMultiplexPin.UpdateGeometry()¶
```

Update geometry

### classIChainBodyLinkMultiplexPin

```
classIChainBodyLinkMultiplexPin(oobj=None)¶
```

Bases:DispatchBaseClassChain Body Link Pin MultiplexPropertiesCommentCommentFullNameFullName such asBody1.Marker1@Model1GeneralBodyGeneralBodyGeometryGeometryGraphicGraphicNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceUseBodyGraphicUse graphic of clone boyUserDataUser supplied dataMethodsUpdateGeometryUpdate geometry

### UpdateGeometry

```
IChainBodyLinkMultiplexRoller.UpdateGeometry()¶
```

Update geometry

### classIChainBodyLinkMultiplexRoller

```
classIChainBodyLinkMultiplexRoller(oobj=None)¶
```

Bases:DispatchBaseClassChain Body Link Roller MultiplexPropertiesCommentCommentFullNameFullName such asBody1.Marker1@Model1GeneralBodyGeneralBodyGeometryGeometryGraphicGraphicNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceUseBodyGraphicUse graphic of clone boyUserDataUser supplied dataMethodsUpdateGeometryUpdate geometry

### classIChainBodyLinkOffset

```
classIChainBodyLinkOffset(oobj=None)¶
```

Bases:DispatchBaseClassChain Body Link OffsetPropertiesCommentCommentFullNameFullName such asBody1.Marker1@Model1GeneralBodyGeneralBodyGraphicGraphicNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceUseBodyGraphicUse graphic of clone boyUserDataUser supplied data

### UpdateGeometry

```
IChainBodyLinkPin.UpdateGeometry()¶
```

Update geometry

### classIChainBodyLinkPin

```
classIChainBodyLinkPin(oobj=None)¶
```

Bases:DispatchBaseClassChain Body Link PinPropertiesCommentCommentFullNameFullName such asBody1.Marker1@Model1GeneralBodyGeneralBodyGeometryGeometryGraphicGraphicNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceUseBodyGraphicUse graphic of clone boyUserDataUser supplied dataMethodsUpdateGeometryUpdate geometry

### UpdateGeometry

```
IChainBodyLinkRoller.UpdateGeometry()¶
```

Update geometry

### classIChainBodyLinkRoller

```
classIChainBodyLinkRoller(oobj=None)¶
```

Bases:DispatchBaseClassChain Body Link RollerPropertiesCommentCommentFullNameFullName such asBody1.Marker1@Model1GeneralBodyGeneralBodyGeometryGeometryGraphicGraphicNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceUseBodyGraphicUse graphic of clone boyUserDataUser supplied dataMethodsUpdateGeometryUpdate geometry

### UpdateGeometry

```
IChainBodyLinkSilentInner.UpdateGeometry()¶
```

Update geometry

### classIChainBodyLinkSilentInner

```
classIChainBodyLinkSilentInner(oobj=None)¶
```

Bases:DispatchBaseClassChain Body Link Silent OuterPropertiesCommentCommentFullNameFullName such asBody1.Marker1@Model1GeneralBodyGeneralBodyGeometryGeometryGraphicGraphicNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceProfileProfile of Link SilentUseBodyGraphicUse graphic of clone boyUserDataUser supplied dataMethodsUpdateGeometryUpdate ge

### UpdateGeometry

```
IChainBodyLinkSilentOuter.UpdateGeometry()¶
```

Update geometry

### classIChainBodyLinkSilentOuter

```
classIChainBodyLinkSilentOuter(oobj=None)¶
```

Bases:DispatchBaseClassChain Body Link Silent OuterPropertiesCommentCommentFullNameFullName such asBody1.Marker1@Model1GeneralBodyGeneralBodyGeometryGeometryGraphicGraphicNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceProfileProfile of Link SilentUseBodyGraphicUse graphic of clone boyUserDataUser supplied dataMethodsUpdateGeometryUpdate ge

### classIChainBodyRoller

```
classIChainBodyRoller(oobj=None)¶
```

Bases:DispatchBaseClassChain Roller RollerPropertiesCommentCommentContactPropertyContact PropertyContactSearchContactSearchTypeFullNameFullName such asBody1.Marker1@Model1GeneralBodyGeneralBodyGeometryGeometryNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceUserDataUser supplied data

### classIChainBodySprocketMultiplex

```
classIChainBodySprocketMultiplex(oobj=None)¶
```

Bases:DispatchBaseClassChain Sprocket MultiplexPropertiesCommentCommentContactPropertyContact PropertyContactSearchContactSearchTypeFullNameFullName such asBody1.Marker1@Model1GeneralBodyGeneralBodyGeometryGeometryNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceSideContactPropertySide Contact PropertyUserDataUser supplied data

