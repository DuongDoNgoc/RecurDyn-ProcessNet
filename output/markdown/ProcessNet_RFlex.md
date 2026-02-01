# ProcessNet.RFlex

> ProcessNet.RFlex API

## Overview

**Full Name:** FunctionBay.RecurDyn.ProcessNet.RFlex

**Methods:** 158

**Examples:** 0

## Methods

### classAScalingType

```
classAScalingType(value)¶
```

Bases:IntEnumAScalingType enumeration.MembersAnimation_Scaling_ModeConstant value is 1.Animation_Scaling_TraRotConstant value is 0.

### classBeamGroupInertiaPropertyInput

```
classBeamGroupInertiaPropertyInput(value)¶
```

Bases:IntEnumBeamGroupInertiaPropertyInput enumeration.MembersBeamGroup_DensityConstant value is 1.BeamGroup_TotalMassConstant value is 0.

### classBeamRecoveryType

```
classBeamRecoveryType(value)¶
```

Bases:IntEnumBeamRecoveryType enumeration.MembersBeam_Recovery_CConstant value is 1.Beam_Recovery_DConstant value is 2.Beam_Recovery_EConstant value is 3.Beam_Recovery_FConstant value is 4.Beam_Recovery_MAX_DISTANCEConstant value is 0.Beam_Recovery_MAX_VONMISES_STRESSConstant value is 5.

### classDataPrecisionofStressStrainShapeType

```
classDataPrecisionofStressStrainShapeType(value)¶
```

Bases:IntEnumDataPrecisionofStressStrainShapeType enumeration.MembersDataPrecisionDoubleConstant value is 1.DataPrecisionSingleConstant value is 0.

### classDisplacementDataPrecision

```
classDisplacementDataPrecision(value)¶
```

Bases:IntEnumDisplacementDataPrecision enumeration.MembersDisplacementDataPrecision_DoubleConstant value is 1.DisplacementDataPrecision_FloatConstant value is 0.

### classFEMFATVersionType

```
classFEMFATVersionType(value)¶
```

Bases:IntEnumFEMFATVersionType enumeration.MembersFEMFAT_48Constant value is 0.FEMFAT_50Constant value is 1.FEMFAT_53Constant value is 2.FEMFAT_532Constant value is 3.

### classFESoftwareType

```
classFESoftwareType(value)¶
```

Bases:IntEnumFESoftwareType enumeration.MembersAnsysConstant value is 0.MSC_NastranConstant value is 2.NX_NastranConstant value is 1.

### GetAnimationScalingModeShapeFactor

```
IRFlexAnimationDataScaling.GetAnimationScalingModeShapeFactor()¶
```

GSetAnimationScalingModeShapeFactor is obsolete function.

### GetAnimationScalingRotationalFactor

```
IRFlexAnimationDataScaling.GetAnimationScalingRotationalFactor()¶
```

GetAnimationScalingRotationalFactor is obsolete function.

### GetAnimationScalingTranslationalFactor

```
IRFlexAnimationDataScaling.GetAnimationScalingTranslationalFactor()¶
```

GetAnimationScalingTranslationalFactor is obsolete function.

### SetAnimationScalingModeShapeFactor

```
IRFlexAnimationDataScaling.SetAnimationScalingModeShapeFactor(dFactor)¶
```

SetAnimationScalingModeShapeFactor is obsolete function.

### SetAnimationScalingRotationalFactor

```
IRFlexAnimationDataScaling.SetAnimationScalingRotationalFactor(x,y,z)¶
```

SetAnimationScalingRotationalFactor is obsolete function.

### SetAnimationScalingTranslationalFactor

```
IRFlexAnimationDataScaling.SetAnimationScalingTranslationalFactor(x,y,z)¶
```

SetAnimationScalingTranslationalFactor is obsolete function.

### classIRFlexAnimationDataScaling

```
classIRFlexAnimationDataScaling(oobj=None)¶
```

Bases:DispatchBaseClassRFlex Animation ScalingPropertiesAnimationScalingRefMarkerAnimationScalingRefMarker is obsolete property.AnimationScalingTypeAnimationScalingType is obsolete property.ReferenceNodeReferenceNode is obsolete property.UseAnimationScalingUseAnimationScaling is obsolete property.MethodsGetAnimationScalingModeShapeFactorGSetAnimationScalingModeShapeFactor is obsolete function.GetAnimationScalingRotationalFactorGetAnimationScalingRotationalFactor is obsolete function.GetAnimation

### CreateElementSet

```
IRFlexBody.CreateElementSet(strName,arrElementID)¶
```

Create a element set

### CreateLineSet

```
IRFlexBody.CreateLineSet(strName,arrNodeID)¶
```

Create a line set

### CreateMarker

```
IRFlexBody.CreateMarker(strName,pRefFrame)¶
```

Create a marker

### CreateMarkerOnNode

```
IRFlexBody.CreateMarkerOnNode(strName,uiNodeID)¶
```

Create a marker on target node

### CreateNodeSet

```
IRFlexBody.CreateNodeSet(strName,arrNodeID)¶
```

Create a node set

### CreateOutput

```
IRFlexBody.CreateOutput(strName,arrNodeID)¶
```

Create an output

### CreateParametricPoint

```
IRFlexBody.CreateParametricPoint(strName,pPoint,pRefMarker)¶
```

Creates a parametric point

### CreateParametricPointWithText

```
IRFlexBody.CreateParametricPointWithText(strName,strText,pRefMarker)¶
```

Creates a parametric point with text

### CreateParametricValue

```
IRFlexBody.CreateParametricValue(strName,dValue)¶
```

Creates a parametric value

### CreateParametricValueWithText

```
IRFlexBody.CreateParametricValueWithText(strName,strText)¶
```

Creates a parametric value with text

### CreatePatchSet

```
IRFlexBody.CreatePatchSet(strName,arrNodeID)¶
```

Create a patch set

### CreatePatchSetWithBox

```
IRFlexBody.CreatePatchSetWithBox(strName,pRefFrame,dWidth,dHeight,dDepth)¶
```

Create a patch set with a box

### CreatePatchSetWithCone

```
IRFlexBody.CreatePatchSetWithCone(strName,pFirstPoint,pSecondPoint,dTopRadius,dBottomRadius,dTolerance)¶
```

Create a patch set with a cone

### CreatePatchSetWithElementIDs

```
IRFlexBody.CreatePatchSetWithElementIDs(strName,arrElementID)¶
```

Create a patch set with ElementIDs

### CreatePatchSetWithElementIDsContinuous

```
IRFlexBody.CreatePatchSetWithElementIDsContinuous(strName,arrElementID,dAngle,bCheckReverse)¶
```

Create a patch set with ElementIDs, patches connected with the external patch of the element continuoulsy

### CreatePatchSetWithNodeSet

```
IRFlexBody.CreatePatchSetWithNodeSet(strName,pNodeSet)¶
```

Create a patch set with a nodeset

### CreatePatchSetWithPatchIndices

```
IRFlexBody.CreatePatchSetWithPatchIndices(strName,arrPatchesIndices)¶
```

Create a patch set with patches’ indices

### CreatePatchSetWithPatchIndicesContinuous

```
IRFlexBody.CreatePatchSetWithPatchIndicesContinuous(strName,arrPatchesIndices,dAngle,bCheckReverse)¶
```

Create a patch set with patches’ indices, patches connected continuously will be used for the patchset

### DeleteAnimationScaling

```
IRFlexBody.DeleteAnimationScaling()¶
```

Delete Animation Scaling

### ExportParametricPoint

```
IRFlexBody.ExportParametricPoint(strFileName)¶
```

Export parametric point

### ExportParametricValue

```
IRFlexBody.ExportParametricValue(strFileName)¶
```

Export parametric value

### GetElementByID

```
IRFlexBody.GetElementByID(nID)¶
```

Get element by ID

### GetEntity

```
IRFlexBody.GetEntity(strName)¶
```

Get an entity

### GetNodeByID

```
IRFlexBody.GetNodeByID(nID)¶
```

Get node by ID

### ImportParametricPoint

```
IRFlexBody.ImportParametricPoint(strFileName)¶
```

Import parametric point

### ImportParametricValue

```
IRFlexBody.ImportParametricValue(strFileName)¶
```

Import parametric value

### ModeInformation

```
IRFlexBody.ModeInformation(pModeSequence)¶
```

Get the Mode Information

### Redraw

```
IRFlexBody.Redraw()¶
```

Redraw method

### classIRFlexBody

```
classIRFlexBody(oobj=None)¶
```

Bases:DispatchBaseClassFunctionBay Internal Use OnlyPropertiesActiveActiveAnimationDataScalingAnimationDataScaling is obsolete property.AnimationScalingAnimationScalingCommentCommentDisplaySettingGet Display SettingExportSetDataGet Export Set DataExportShellFormatDataGet Export Shell Format DataFullNameFullName such asBody1.Marker1@Model1GraphicGraphicInitialRotationalVelocityXInitial rotational velocity XInitialRotationalVelocityYInitial rotational velocity YInitialRotationalVelocityZInitial ro

### Item

```
IRFlexBodyCollection.Item(var)¶
```

Returns a specific item.

### classIRFlexBodyCollection

```
classIRFlexBodyCollection(oobj=None)¶
```

Bases:DispatchBaseClassPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### classIRFlexBodyImportOption

```
classIRFlexBodyImportOption(oobj=None)¶
```

Bases:DispatchBaseClassRFlexBody import optionPropertiesUseInternalNodesUseInternalNodes is obsolete functionUseNodalResidualUseNodalResidual is obsolete functionUseUserDefinedRigidBodyFrequencyUse user defined rigid body frequencyUserDefinedRigidBodyFrequencyUser defined rigid body frequency

### classIRFlexElement

```
classIRFlexElement(oobj=None)¶
```

Bases:DispatchBaseClassRFlex ElementPropertiesCommentCommentElementTypeElement typeFullNameFullName such asBody1.Marker1@Model1IDIDNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceUserDataUser supplied data

### Item

```
IRFlexElementCollection.Item(var)¶
```

Returns a specific item.

### classIRFlexElementCollection

```
classIRFlexElementCollection(oobj=None)¶
```

Bases:DispatchBaseClassPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### classIRFlexElementSet

```
classIRFlexElementSet(oobj=None)¶
```

Bases:DispatchBaseClassPropertiesColorElement set colorCommentCommentElementCollectionElement CollectionFullNameFullName such asBody1.Marker1@Model1NameNameNodeCollectionNode Collection of Element setOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceUserDataUser supplied data

