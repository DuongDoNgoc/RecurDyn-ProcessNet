# ProcessNet.Flexible

> ProcessNet.Flexible API

## Overview

**Full Name:** FunctionBay.RecurDyn.ProcessNet.Flexible

**Methods:** 106

**Examples:** 0

## Methods

### classBodyType

```
classBodyType(value)¶
```

Bases:IntEnumBodyType enumeration.MembersBodyType_FFLEXConstant value is 1.BodyType_RFLEXConstant value is 2.BodyType_RIGIDConstant value is 0.

### classContourBandLegendType

```
classContourBandLegendType(value)¶
```

Bases:IntEnumContourBandLegendType enumeration.MembersCB_Legned_DialogConstant value is 1.CB_Legned_DisableConstant value is 0.CB_Legned_DisplayConstant value is 2.

### classContourColorSetType

```
classContourColorSetType(value)¶
```

Bases:IntEnumContourColorSetType enumeration.MembersColorSetType_GradationConstant value is 1.ColorSetType_SpectrumConstant value is 0.

### classContourColorStyle

```
classContourColorStyle(value)¶
```

Bases:IntEnumContourColorStyle enumeration.MembersC_Style_SmoothConstant value is 0.C_Style_SteppedConstant value is 2.C_Style_WireConstant value is 1.

### classContourComponent

```
classContourComponent(value)¶
```

Bases:IntEnumContourComponent enumeration.MembersCC_CONTACT_MAGNITUDEConstant value is 33.CC_CONTACT_NORMALConstant value is 31.CC_CONTACT_TANGENTConstant value is 32.CC_CP_CPConstant value is 42.CC_CP_ELConstant value is 41.CC_E1Constant value is 15.CC_E2Constant value is 16.CC_E3Constant value is 17.CC_EINTConstant value is 18.CC_EMISESConstant value is 19.CC_ERPConstant value is 51.CC_ERP_DENSITYConstant value is 52.CC_EXConstant value is 9.CC_EXYConstant value is 12.CC_EYConstant value is 10

### classContourContactSurfaceOnlyType

```
classContourContactSurfaceOnlyType(value)¶
```

Bases:IntEnumContourContactSurfaceOnlyType enumeration.MembersContact_Patches_OnlyConstant value is 1.UserDefine_Contact_SurfaceConstant value is 0.

### classContourDataExportSelectType

```
classContourDataExportSelectType(value)¶
```

Bases:IntEnumContourDataExportSelectType enumeration.MembersSelect_AllConstant value is 5.Select_ElementSetConstant value is 4.Select_LineSetConstant value is 3.Select_NodeConstant value is 0.Select_NodeSetConstant value is 1.Select_PatchSetConstant value is 2.

### classContourDataExportType

```
classContourDataExportType(value)¶
```

Bases:IntEnumContourDataExportType enumeration.MembersExport_MinMaxConstant value is 2.Export_NodeConstant value is 0.Export_TimeConstant value is 1.

### classContourMinMaxType

```
classContourMinMaxType(value)¶
```

Bases:IntEnumContourMinMaxType enumeration.MembersMM_DisplayConstant value is 0.MM_UserDefinedConstant value is 1.

### classContourReferenceType

```
classContourReferenceType(value)¶
```

Bases:IntEnumContourReferenceType enumeration.MembersReferenceType_MarkerConstant value is 1.ReferenceType_NodeConstant value is 0.

### classContourType

```
classContourType(value)¶
```

Bases:IntEnumContourType enumeration.MembersCT_CONTACT_FORCEConstant value is 3.CT_CONTACT_PRESSUREConstant value is 4.CT_DISPLACEMENTConstant value is 0.CT_ELASTIC_STRAINConstant value is 5.CT_PLASTIC_STRAINConstant value is 6.CT_SOUNDConstant value is 8.CT_STRAINConstant value is 1.CT_STRESSConstant value is 2.CT_TEMPERATUREConstant value is 9.CT_THERMAL_STRAINConstant value is 7.

### classConvertFFlexToRFlexType

```
classConvertFFlexToRFlexType(value)¶
```

Bases:IntEnumConvertFFlexToRFlexType enumeration.MembersFFlexToRFlex_Swap_RFIConstant value is 1.FFlexToRFlex_Swap_RFlexGenConstant value is 0.

### classConvertFFlexToRigidType

```
classConvertFFlexToRigidType(value)¶
```

Bases:IntEnumConvertFFlexToRigidType enumeration.MembersFFlexToRigid_ConvertConstant value is 1.FFlexToRigid_Convert_RigidShellConstant value is 0.FFlexToRigid_Swap_CADDataConstant value is 2.

### classConvertRFlexToFFlexType

```
classConvertRFlexToFFlexType(value)¶
```

Bases:IntEnumConvertRFlexToFFlexType enumeration.MembersRFlexToFFlex_ConvertConstant value is 0.RFlexToFFlex_SwapConstant value is 1.

### classConvertRFlexToRFlexType

```
classConvertRFlexToRFlexType(value)¶
```

Bases:IntEnumConvertRFlexToRFlexType enumeration.MembersRFlexToRFlex_Swap_RFIConstant value is 1.RFlexToRFlex_Swap_RFlexGenConstant value is 0.

### classConvertRFlexToRigidType

```
classConvertRFlexToRigidType(value)¶
```

Bases:IntEnumConvertRFlexToRigidType enumeration.MembersRFlexToRigid_Convert_RigidShellConstant value is 0.RFlexToRigid_Swap_CADDataConstant value is 1.

### classConvertRigidToFFlexType

```
classConvertRigidToFFlexType(value)¶
```

Bases:IntEnumConvertRigidToFFlexType enumeration.MembersRigidToFFlex_MeshConstant value is 0.RigidToFFlex_SwapConstant value is 1.

### classCuttingPlaneFlexType

```
classCuttingPlaneFlexType(value)¶
```

Bases:IntEnumCuttingPlaneFlexType enumeration.MembersCuttingPlaneFlexType_CrossSectionConstant value is 0.CuttingPlaneFlexType_ElementShapeConstant value is 1.

### AddDataTrace

```
IContour.AddDataTrace(pVal,Val)¶
```

Add DataTrace

### AddPartSelction

```
IContour.AddPartSelction(pBody,pSet)¶
```

Add Part Selection

### CloseContourDialog

```
IContour.CloseContourDialog()¶
```

Close Contour Dialog

### DeleteDataTrace

```
IContour.DeleteDataTrace(pVal)¶
```

Delete DataTrace

### DeleteDataTracebyIndex

```
IContour.DeleteDataTracebyIndex(Val)¶
```

Delete DataTrace

### DeletePartSelction

```
IContour.DeletePartSelction(pVal)¶
```

Delete Part Selection

### DeletePartSelctionbyIndex

```
IContour.DeletePartSelctionbyIndex(Val)¶
```

Delete Part Selection

### OpenContourDialog

```
IContour.OpenContourDialog()¶
```

Open Contour Dialog

### UpdateLegend

```
IContour.UpdateLegend()¶
```

Contour Setting Done

### classIContour

```
classIContour(oobj=None)¶
```

Bases:DispatchBaseClassContourPropertiesBandOptionBandOption is obsolete function.BandOption2Get Contour Band OptionDataExportGet Contour Data ExportDataTraceCollectionContains Contour Data TraceEnableViewEnable View FlagMinMaxOptionMinMaxOption is obsolete function.MinMaxOption2Get Contour MinMax OptionPartSelectionCollectionContains Contour Part SelectionReferenceNodeCollectionContains Contour Reference NodeStyleOptionStyleOption is obsolete function.StyleOption2Get Contour Style OptionTypeOpt

### classIContourBandOption

```
classIContourBandOption(oobj=None)¶
```

Bases:DispatchBaseClassIContourBandOptionn is obsolete interface. Use IContourBandOption2.PropertiesBandLevelBandLevel is obsolete functionLegendLocationLegendLocationType is obsolete functionLegendTypeLegendType is obsolete functionShowTextLegendShowTextLegend is obsolete function

### SetCustomizeBandValuesColors

```
IContourBandOption2.SetCustomizeBandValuesColors(arrValues,arrColors)¶
```

Set Customize Band Option Values and Colors

### UpdateCustomizeBandValuesWithLogScale

```
IContourBandOption2.UpdateCustomizeBandValuesWithLogScale(arrValues,bLogScale)¶
```

Update Customize Band Values with Log Scale

### classIContourBandOption2

```
classIContourBandOption2(oobj=None)¶
```

Bases:DispatchBaseClassContour Band Option2PropertiesBandLevelBand LevelColorSetTypeContour Color Set TypeCustomizeBandColorsCustomize Band ColorsCustomizeBandEnableLogScaleCustomize Band Log ScaleCustomizeBandValuesCustomize Band ValuesEnableLogScaleLog ScaleMaxColorMax ColorMinColorMin ColorUseCustomizeBandOptionCustomize Band OptionMethodsSetCustomizeBandValuesColorsSet Customize Band Option Values and ColorsUpdateCustomizeBandValuesWithLogScaleUpdate Customize Band Values with Log Scale

### Export

```
IContourDataExport.Export(Val)¶
```

Export Contour Data

### SelectFramesWithRange

```
IContourDataExport.SelectFramesWithRange(start,end)¶
```

Select Frames

### SelectNodesWithRange

```
IContourDataExport.SelectNodesWithRange(start,end)¶
```

Select Nodes

### classIContourDataExport

```
classIContourDataExport(oobj=None)¶
```

Bases:DispatchBaseClassContour Data ExportPropertiesBodyExport BodySelectFramesSelect FramesSelectNodesSelect NodesSelectTypeSelect TypeSignificantDigitsSignificant digitsTypeTypeUseScientificNotationExport data with scientific notation flagMethodsExportExport Contour DataSelectFramesWithRangeSelect FramesSelectNodesWithRangeSelect Nodes

### classIContourDataTrace

```
classIContourDataTrace(oobj=None)¶
```

Bases:DispatchBaseClassContour Data TracePropertiesBodyBodyNodeIDReference Node IDSelectSelection

### Item

```
IContourDataTraceCollection.Item(var)¶
```

Returns a specific item.

### classIContourDataTraceCollection

```
classIContourDataTraceCollection(oobj=None)¶
```

Bases:DispatchBaseClassPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### Calculation

```
IContourMinMaxOption.Calculation()¶
```

MinMaxCalculation is obsolete function

### classIContourMinMaxOption

```
classIContourMinMaxOption(oobj=None)¶
```

Bases:DispatchBaseClassIContourMinMaxOption is obsolete function. Use IContourMinMaxOption2.PropertiesEnableLogScaleLogScale is obsolete functionMaxMaxValue is obsolete functionMinMinValue is obsolete functionShowMaxShowMax is obsolete functionShowMinShowMin is obsolete functionShowMinMaxShowMinMax is obsolete functionTypeMinMaxType is obsolete functionUserDefinedMaxUserDefinedMaxValue is obsolete functionUserDefinedMaxColorUserDefinedMaxColor is obsolete functionUserDefinedMinUserDefinedMinValu

### Calculation

```
IContourMinMaxOption2.Calculation()¶
```

Min Max Calculation

### classIContourMinMaxOption2

```
classIContourMinMaxOption2(oobj=None)¶
```

Bases:DispatchBaseClassContour MinMax Option2PropertiesMaxMax ValueMinMin ValueShowMaxShow MaxShowMinShow MinTypeMin Max TypeUserDefinedMaxUser Defined Max ValueUserDefinedMinUser Defined Min ValueMethodsCalculationMin Max Calculation

### classIContourPartSelection

```
classIContourPartSelection(oobj=None)¶
```

Bases:DispatchBaseClassContour Part SelectionPropertiesBodyBodyElementSetElement SetSelectSelection

### Item

```
IContourPartSelectionCollection.Item(var)¶
```

Returns a specific item.

### classIContourPartSelectionCollection

```
classIContourPartSelectionCollection(oobj=None)¶
```

Bases:DispatchBaseClassPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### classIContourReferenceNode

```
classIContourReferenceNode(oobj=None)¶
```

Bases:DispatchBaseClassContour Reference NodePropertiesBodyBodyMarkerreference markerNodeIDReference Node IDOrientationReferenceMarkerOrientationReferenceMarker is obsolete functionReferenceTypeReference TypeSelectSelectionUseOrientationReferenceMarkerUseOrientationReferenceMarker is obsolete function

### Item

```
IContourReferenceNodeCollection.Item(var)¶
```

Returns a specific item.

### classIContourReferenceNodeCollection

```
classIContourReferenceNodeCollection(oobj=None)¶
```

Bases:DispatchBaseClassIConourReferenceNodeCollectionPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### classIContourStyleOption

```
classIContourStyleOption(oobj=None)¶
```

Bases:DispatchBaseClassIContourStyleOption is obsolete interface. Use IContourStyleOption2.PropertiesColorTypeColorType is obsolete functionExceedMaxColorExceedMaxColor is obsolete functionGrayScaleColorGrayScaleColor is obsolete functionLessThanMinColorLessthanMinColor is obsolete functionMeshLinesColorMeshLinesColor is obsolete functionShowMeshLinesShowMeshLines is obsolete functionSpectrumMaxColorSpectrumMaxColor is obsolete functionSpectrumMinColorSpectrumMinColor is obsolete functionStyleCo

