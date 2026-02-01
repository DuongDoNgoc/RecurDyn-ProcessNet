# ProcessNet.FFlex

> ProcessNet.FFlex API

## Overview

**Full Name:** FunctionBay.RecurDyn.ProcessNet.FFlex

**Methods:** 648

**Examples:** 0

## Methods

### classBeamCrossSection

```
classBeamCrossSection(value)
```

Bases:IntEnumBeamCrossSection enumeration.MembersBCS_CircularConstant value is 1.BCS_EllipticalConstant value is 2.BCS_HollowRectangularConstant value is 6.BCS_IBeamConstant value is 7.BCS_RectangularConstant value is 3.BCS_TBeamConstant value is 8.BCS_ThickWallTubeConstant value is 5.BCS_ThinWallTubeConstant value is 4.BCS_UserDefinedConstant value is 0.

### classBeamRecoveryType

```
classBeamRecoveryType(value)
```

Bases:IntEnumBeamRecoveryType enumeration.MembersBeamRecoveryType_CConstant value is 1.BeamRecoveryType_DConstant value is 2.BeamRecoveryType_EConstant value is 3.BeamRecoveryType_FConstant value is 4.BeamRecoveryType_MAX_DISTANCEConstant value is 0.BeamRecoveryType_MAX_VONMISES_STRESSConstant value is 5.

### classChordalErrorType

```
classChordalErrorType(value)
```

Bases:IntEnumChordalErrorType enumeration.MembersChordalError_AbsoluteConstant value is 1.ChordalError_RelativeConstant value is 0.

### classConcentratedLoadType

```
classConcentratedLoadType(value)
```

Bases:IntEnumConcentratedLoadType enumeration.MembersRelativeConstant value is 1.UniformConstant value is 0.

### classConvectionDataType

```
classConvectionDataType(value)
```

Bases:IntEnumConvectionDataType enumeration.MembersConstantValueConstant value is 0.VariableValueConstant value is 1.

### classDisplacementDataPrecision

```
classDisplacementDataPrecision(value)
```

Bases:IntEnumDisplacementDataPrecision enumeration.MembersDisplacementDataPrecision_DoubleConstant value is 1.DisplacementDataPrecision_FloatConstant value is 0.

### classElementType

```
classElementType(value)
```

Bases:IntEnumElementType enumeration.MembersElementType_Beam2Constant value is 0.ElementType_Shell3Constant value is 1.ElementType_Shell4Constant value is 2.ElementType_Solid4Constant value is 3.ElementType_Solid8Constant value is 4.

### classFDRElementType

```
classFDRElementType(value)
```

Bases:IntEnumFDRElementType enumeration.MembersInterpEConstant value is 1.RigidEConstant value is 0.

### classFFlexImportFileType

```
classFFlexImportFileType(value)
```

Bases:IntEnumFFlexImportFileType enumeration.MembersI_ANSYSConstant value is 1.I_DesignSpaceConstant value is 2.I_NASTRANConstant value is 0.

### classFFlexPropertyType

```
classFFlexPropertyType(value)
```

Bases:IntEnumFFlexPropertyType enumeration.MembersFFlexPropertyType_BeamConstant value is 0.FFlexPropertyType_FDRConstant value is 3.FFlexPropertyType_MASSConstant value is 4.FFlexPropertyType_ShellConstant value is 1.FFlexPropertyType_SolidConstant value is 2.

### classFatigueSoftwareType

```
classFatigueSoftwareType(value)
```

Bases:IntEnumFatigueSoftwareType enumeration.MembersFemFatConstant value is 0.

### classGeoPatchThickness

```
classGeoPatchThickness(value)
```

Bases:IntEnumGeoPatchThickness enumeration.MembersThickness_OriginalConstant value is 0.Thickness_SpecificConstant value is 1.

### SetGeometries

```
IAssistConstraint.SetGeometries(pFaceArray)
```

Set face geometries

### classIAssistConstraint

```
classIAssistConstraint(oobj=None)
```

Bases:DispatchBaseClassConstraint to assist modelingPropertiesGeometryNameFace geometries' nameNameContraint's nameUseFDRUse FDRUseSelectionUse selectionMethodsSetGeometriesSet face geometries

### SetGeometries

```
SetGeometries()
```

Set face geometries

### Item

```
IAssistConstraintCollection.Item(var)
```

Returns a specific item.

### classIAssistConstraintCollection

```
classIAssistConstraintCollection(oobj=None)
```

Bases:DispatchBaseClassPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### Item

```
Item()
```

Returns a specific item.

### classIAssistPrePatchSet

```
classIAssistPrePatchSet(oobj=None)
```

Bases:DispatchBaseClassConstraint to assist modelingPropertiesGeometryNameFace geometries' nameKeepGeoContactKeep GeoContactNameContct's namePatchSetCreate patch setUseSelectionUse selection

### Item

```
IAssistPrePatchSetCollection.Item(var)
```

Returns a specific item.

### classIAssistPrePatchSetCollection

```
classIAssistPrePatchSetCollection(oobj=None)
```

Bases:DispatchBaseClassPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### Item

```
Item()
```

Returns a specific item.

### classIAssistPreSet

```
classIAssistPreSet(oobj=None)
```

Bases:DispatchBaseClassConstraint to assist modelingPropertiesGeometryNameEdge geometries' nameKeepGeoContactKeep GeoContactLineSetCreate line setNameContraint's nameUseSelectionUse selection

### Item

```
IAssistPreSetCollection.Item(var)
```

Returns a specific item.

### classIAssistPreSetCollection

```
classIAssistPreSetCollection(oobj=None)
```

Bases:DispatchBaseClassPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### Item

```
Item()
```

Returns a specific item.

### classIAssistSurfaceConstraint

```
classIAssistSurfaceConstraint(oobj=None)
```

Bases:DispatchBaseClassSurface constraint to assist modelingPropertiesGeometryNameFace geometries' nameNameContraint's namePatchSetCreate patch setUseSelectionUse selection

### Item

```
IAssistSurfaceConstraintCollection.Item(var)
```

Returns a specific item.

### classIAssistSurfaceConstraintCollection

```
classIAssistSurfaceConstraintCollection(oobj=None)
```

Bases:DispatchBaseClassPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### Item

```
Item()
```

Returns a specific item.

### GetAnimationScalingRotationalFactor

```
IFFlexAnimationDataScaling.GetAnimationScalingRotationalFactor()
```

GetAnimationScalingRotationalFactor is obsolete function.

### GetAnimationScalingTranslationalFactor

```
IFFlexAnimationDataScaling.GetAnimationScalingTranslationalFactor()
```

GetAnimationScalingTranslationalFactor is obsolete function.

### SetAnimationScalingRotationalFactor

```
IFFlexAnimationDataScaling.SetAnimationScalingRotationalFactor(x,y,z)
```

SetAnimationScalingRotationalFactor is obsolete function.

### SetAnimationScalingTranslationalFactor

```
IFFlexAnimationDataScaling.SetAnimationScalingTranslationalFactor(x,y,z)
```

SetAnimationScalingTranslationalFactor is obsolete function.

### classIFFlexAnimationDataScaling

```
classIFFlexAnimationDataScaling(oobj=None)
```

Bases:DispatchBaseClassFFlex Animation ScalingPropertiesReferenceNodeReferenceNode is obsolete property.UseAnimationScalingUseAnimationScaling is obsolete property.MethodsGetAnimationScalingRotationalFactorGetAnimationScalingRotationalFactor is obsolete function.GetAnimationScalingTranslationalFactorGetAnimationScalingTranslationalFactor is obsolete function.SetAnimationScalingRotationalFactorSetAnimationScalingRotationalFactor is obsolete function.SetAnimationScalingTranslationalFactorSetAnimat

### GetAnimationScalingRotationalFactor

```
GetAnimationScalingRotationalFactor()
```

GetAnimationScalingRotationalFactor is obsolete function.

### GetAnimationScalingTranslationalFactor

```
GetAnimationScalingTranslationalFactor()
```

GetAnimationScalingTranslationalFactor is obsolete function.

### SetAnimationScalingRotationalFactor

```
SetAnimationScalingRotationalFactor()
```

SetAnimationScalingRotationalFactor is obsolete function.

### SetAnimationScalingTranslationalFactor

```
SetAnimationScalingTranslationalFactor()
```

SetAnimationScalingTranslationalFactor is obsolete function.

### ChangeElementID

```
IFFlexBody.ChangeElementID(pElement,uiID)
```

Change element ID

### ChangeNodeID

```
IFFlexBody.ChangeNodeID(pNode,uiID)
```

Change node ID

### CreateBoundaryCondition

```
IFFlexBody.CreateBoundaryCondition(strName,arrNodeID)
```

Create a boundary condition

### CreateElement

```
IFFlexBody.CreateElement(uiID,ElementType,pMultiPoint,pProperty)
```

Create a element

### CreateElementFDR

```
IFFlexBody.CreateElementFDR(uiID,pMasterNode,pNodeSet)
```

CreateElementFDR is obsolete function, use CreateElementFDRWithProperty

### CreateElementFDRWithProperty

```
IFFlexBody.CreateElementFDRWithProperty(uiID,varPrimaryNode,pNodeSet,pPropertyFDR)
```

Create a FDR element

### CreateElementMass

```
IFFlexBody.CreateElementMass(uiID,varPrimaryNode,pPropertyMass)
```

Create a mass element

### CreateElementSet

```
IFFlexBody.CreateElementSet(strName,arrElementID)
```

Create a element set

### CreateFFlexMaterialAnisotropic2D

```
IFFlexBody.CreateFFlexMaterialAnisotropic2D(strName)
```

Create a fflex Anisotropic2D material

### CreateFFlexMaterialArrudaBoyce

```
IFFlexBody.CreateFFlexMaterialArrudaBoyce(strName)
```

Create a fflex arruda boyce material

### CreateFFlexMaterialArrudaBoyceRubber

```
IFFlexBody.CreateFFlexMaterialArrudaBoyceRubber(strName)
```

Create a fflex arruda boyce rubber material

