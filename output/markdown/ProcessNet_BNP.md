# ProcessNet.BNP

> ProcessNet.BNP API

## Overview

**Full Name:** FunctionBay.RecurDyn.ProcessNet.BNP

**Methods:** 316

**Examples:** 0

## Methods

### classBNPAssemblyInformationType

```
classBNPAssemblyInformationType(value)
```

Bases:IntEnumBNPAssemblyInformationType enumeration.MembersAssembed_RadiusConstant value is 0.Radial_DistanceConstant value is 1.

### classBNPBCOrienationType

```
classBNPBCOrienationType(value)
```

Bases:IntEnumBNPBCOrienationType enumeration.MembersBNPBCOrienationType_InertiaConstant value is 1.BNPBCOrienationType_NodeConstant value is 0.

### classBNPBeltElementDampingForceType

```
classBNPBeltElementDampingForceType(value)
```

Bases:IntEnumBNPBeltElementDampingForceType enumeration.MembersBNPBeltElementDampingForceType_10Constant value is 0.BNPBeltElementDampingForceType_100Constant value is 1.

### classBNPBeltGroupModelType

```
classBNPBeltGroupModelType(value)
```

Bases:IntEnumBNPBeltGroupModelType enumeration.MembersBNPBeltGroupModelType_BeamModelConstant value is 0.BNPBeltGroupModelType_UserMatrixConstant value is 1.

### classBNPBeltMassType

```
classBNPBeltMassType(value)
```

Bases:IntEnumBNPBeltMassType enumeration.MembersBNPBeltMassType_DensityConstant value is 0.BNPBeltMassType_TotalMassConstant value is 1.

### classBNPBeltSpecialMaterialPropertyType

```
classBNPBeltSpecialMaterialPropertyType(value)
```

Bases:IntEnumBNPBeltSpecialMaterialPropertyType enumeration.MembersBNPBeltSpecialMaterialPropertyType_AnisotropicConstant value is 2.BNPBeltSpecialMaterialPropertyType_IsotropicConstant value is 0.BNPBeltSpecialMaterialPropertyType_OrthotropicConstant value is 1.

### classBNPBeltType

```
classBNPBeltType(value)
```

Bases:IntEnumBNPBeltType enumeration.MembersBNPBeltType_FlatConstant value is 0.BNPBeltType_RoundConstant value is 2.BNPBeltType_TimingConstant value is 3.BNPBeltType_VConstant value is 1.

### classBNPContactDirectionType

```
classBNPContactDirectionType(value)
```

Bases:IntEnumBNPContactDirectionType enumeration.MembersBNPContactDirectionType_LowerConstant value is 1.BNPContactDirectionType_UpperConstant value is 0.

### classBNPContactSearchType

```
classBNPContactSearchType(value)
```

Bases:IntEnumBNPContactSearchType enumeration.MembersBNPContactSearchType_FullSearchConstant value is 0.BNPContactSearchType_PartialSearchConstant value is 1.

### classBNPGuideNormalDirectionType

```
classBNPGuideNormalDirectionType(value)
```

Bases:IntEnumBNPGuideNormalDirectionType enumeration.MembersBNPGuideNormalDirectionType_DOWNConstant value is 1.BNPGuideNormalDirectionType_UPConstant value is 0.

### classBNPInOutType

```
classBNPInOutType(value)
```

Bases:IntEnumBNPInOutType enumeration.MembersBNPInOutType_InConstant value is 0.BNPInOutType_NoneConstant value is 2.BNPInOutType_OutConstant value is 1.

### classBNPPulleyType

```
classBNPPulleyType(value)
```

Bases:IntEnumBNPPulleyType enumeration.MembersBNPPulleyType_GeneralConstant value is 1.BNPPulleyType_ParametersConstant value is 0.

### classBNPToothProfileType

```
classBNPToothProfileType(value)
```

Bases:IntEnumBNPToothProfileType enumeration.MembersBNPToothProfileType_GeneralConstant value is 0.BNPToothProfileType_ParametersConstant value is 1.

### AddAllOutputBelt

```
IBNPAssembly.AddAllOutputBelt()
```

Add all the belt body to output list

### AddOutputBelt

```
IBNPAssembly.AddOutputBelt(strFileName)
```

Add a belt body to output list

### AddPassingBody

```
IBNPAssembly.AddPassingBody(pVal)
```

Add a passing body

### DeletePassingBody

```
IBNPAssembly.DeletePassingBody(pVal)
```

Delete a passing body

### GetOutputBeltList

```
IBNPAssembly.GetOutputBeltList()
```

BNP assembly output list

### RemoveAllOutputBelt

```
IBNPAssembly.RemoveAllOutputBelt()
```

Remove all the belt body from output list

### RemoveOutputBelt

```
IBNPAssembly.RemoveOutputBelt(strFileName)
```

Remove a belt body from output list

### UpdateBeltInitialVelocity

```
IBNPAssembly.UpdateBeltInitialVelocity()
```

Update initial velocity of belts

### classIBNPAssembly

```
classIBNPAssembly(oobj=None)
```

Bases:DispatchBaseClassBNP AssemblyPropertiesBNPBodyBeltCollectionBelt body collectionBushingForceCollectionBushing force collectionCommentCommentConnectingForceParameterConnecting force parameterFullNameFullName such asBody1.Marker1@Model1InitialLongitudinalVelocityInitial longitudinal velocityNameNameNumberOfSegmentNUmber of segmentOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem retu

### AddAllOutputBelt

```
AddAllOutputBelt()
```

Add all the belt body to output list

### AddOutputBelt

```
AddOutputBelt()
```

Add a belt body to output list

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

### GetOutputBeltList

```
GetOutputBeltList()
```

BNP assembly output list

### RemoveAllOutputBelt

```
RemoveAllOutputBelt()
```

Remove all the belt body from output list

### RemoveOutputBelt

```
RemoveOutputBelt()
```

Remove a belt body from output list

### UpdateBeltInitialVelocity

```
UpdateBeltInitialVelocity()
```

Update initial velocity of belts

### AddAllOutputBelt

```
IBNPAssembly2D.AddAllOutputBelt()
```

Add all the belt body to output list

### AddOutputBelt

```
IBNPAssembly2D.AddOutputBelt(strFileName)
```

Add a belt body to output list

### AddPassingBody

```
IBNPAssembly2D.AddPassingBody(pVal)
```

Add a passing body

### DeletePassingBody

```
IBNPAssembly2D.DeletePassingBody(pVal)
```

Delete a passing body

### GetOutputBeltList

```
IBNPAssembly2D.GetOutputBeltList()
```

BNP assembly output list

### RemoveAllOutputBelt

```
IBNPAssembly2D.RemoveAllOutputBelt()
```

Remove all the belt body from output list

### RemoveOutputBelt

```
IBNPAssembly2D.RemoveOutputBelt(strFileName)
```

Remove a belt body from output list

### UpdateBeltInitialVelocity

```
IBNPAssembly2D.UpdateBeltInitialVelocity()
```

Update initial velocity of belts

### classIBNPAssembly2D

```
classIBNPAssembly2D(oobj=None)
```

Bases:DispatchBaseClassBNP 2D AssemblyPropertiesBNPBodyBeltCollectionBelt body collectionBushingForceCollectionBushing force collectionBusingForceParameter2D busing force parameterCommentCommentFullNameFullName such asBody1.Marker1@Model1InitialLongitudinalVelocityInitial longitudinal velocityNameNameNormalDirectionGlobal Normal DirectionNumberOfSegmentNUmber of segmentOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interf

### AddAllOutputBelt

```
AddAllOutputBelt()
```

Add all the belt body to output list

### AddOutputBelt

```
AddOutputBelt()
```

Add a belt body to output list

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

### GetOutputBeltList

```
GetOutputBeltList()
```

BNP assembly output list

### RemoveAllOutputBelt

```
RemoveAllOutputBelt()
```

Remove all the belt body from output list

### RemoveOutputBelt

```
RemoveOutputBelt()
```

Remove a belt body from output list

### UpdateBeltInitialVelocity

```
UpdateBeltInitialVelocity()
```

Update initial velocity of belts

### classIBNPAssembly2DBushingForceParameter

```
classIBNPAssembly2DBushingForceParameter(oobj=None)
```

Bases:DispatchBaseClassBNP assembly 2D bushing force parameterPropertiesRotationalDampingZRotational damping ZRotationalPreloadZRotational preload ZRotationalStiffnessZRotational stiffness ZTranslationalDampingXTranslational damping XTranslationalDampingYTranslational damping YTranslationalPreloadXTranslational preload XTranslationalPreloadYTranslational preload YTranslationalStiffnessXTranslational stiffness XTranslationalStiffnessYTranslational stiffness Y

### Item

```
IBNPAssembly2DCollection.Item(var)
```

Returns a specific item.

### classIBNPAssembly2DCollection

```
classIBNPAssembly2DCollection(oobj=None)
```

Bases:DispatchBaseClass2D Belt assembly collectionPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

