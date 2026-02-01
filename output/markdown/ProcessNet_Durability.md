# ProcessNet.Durability

> ProcessNet.Durability API

## Overview

**Full Name:** FunctionBay.RecurDyn.ProcessNet.Durability

**Methods:** 65

**Examples:** 0

## Methods

### classAngleType

```
classAngleType(value)
```

Bases:IntEnumAngleType enumeration.MembersAngleType_MaxDamageConstant value is 0.AngleType_UserDefinedConstant value is 1.

### classAxialMode

```
classAxialMode(value)
```

Bases:IntEnumAxialMode enumeration.MembersBiAxialConstant value is 1.UniAxialConstant value is 0.

### classBWIWeldType

```
classBWIWeldType(value)
```

Bases:IntEnumBWIWeldType enumeration.MembersBWI_CLASS_BConstant value is 0.BWI_CLASS_CConstant value is 1.BWI_CLASS_DConstant value is 2.BWI_CLASS_EConstant value is 3.BWI_CLASS_FConstant value is 4.BWI_CLASS_F2Constant value is 5.BWI_CLASS_GConstant value is 6.BWI_CLASS_SConstant value is 8.BWI_CLASS_TConstant value is 9.BWI_CLASS_WConstant value is 7.

### classBandLegendLocationType

```
classBandLegendLocationType(value)
```

Bases:IntEnumBandLegendLocationType enumeration.MembersBand_Legned_Location_BottomConstant value is 1.Band_Legned_Location_LeftConstant value is 2.Band_Legned_Location_RightConstant value is 3.Band_Legned_Location_TopConstant value is 0.

### classBandLegendType

```
classBandLegendType(value)
```

Bases:IntEnumBandLegendType enumeration.MembersBand_Legned_DialogConstant value is 1.Band_Legned_DisableConstant value is 0.Band_Legned_DisplayConstant value is 2.

### classColorStyle

```
classColorStyle(value)
```

Bases:IntEnumColorStyle enumeration.MembersColor_Style_SmoothConstant value is 0.Color_Style_SteppedConstant value is 2.Color_Style_WireConstant value is 1.

### classColorType

```
classColorType(value)
```

Bases:IntEnumColorType enumeration.MembersColor_Gray_ScaleConstant value is 1.Color_SpectrumConstant value is 0.

### classContourOptionType

```
classContourOptionType(value)
```

Bases:IntEnumContourOptionType enumeration.MembersDamageConstant value is 0.LifeConstant value is 1.

### classContourViewType

```
classContourViewType(value)
```

Bases:IntEnumContourViewType enumeration.MembersView_BothConstant value is 2.View_Contour_OnlyConstant value is 0.View_Mean_StressConstant value is 3.View_Stress_AmplitudeConstant value is 4.View_Vector_OnlyConstant value is 1.

### classFatigueMaterialUnitType

```
classFatigueMaterialUnitType(value)
```

Bases:IntEnumFatigueMaterialUnitType enumeration.Membersinch_lbConstant value is 2.m_NConstant value is 0.mm_NConstant value is 1.

### classFatigueSurfaceFactorType

```
classFatigueSurfaceFactorType(value)
```

Bases:IntEnumFatigueSurfaceFactorType enumeration.MembersForgedTypeConstant value is 4.GroundTypeConstant value is 1.MachinedTypeConstant value is 2.PolishedTypeConstant value is 0.RolledTypeConstant value is 3.UserInputTypeConstant value is 5.

### ContourView

```
IDurabilityContour.ContourView()
```

Contour View

### ExportContourData

```
IDurabilityContour.ExportContourData(Val)
```

Export Contour Data

### ExportContourDataWithNodeSet

```
IDurabilityContour.ExportContourDataWithNodeSet(Val,pVal)
```

Export Contour Data with Nodeset

### classIDurabilityContour

```
classIDurabilityContour(oobj=None)
```

Bases:DispatchBaseClassDurability ContourPropertiesBandOptionGet Contour Band OptionMinMaxOptionGet Contour MinMax OptionOptionTypeContour Option TypeProbeOptionGet Contour Probe OptionRecoveryTypeContour Recovery TypeStyleOptionGet Contour Style OptionTimeHistoryIndexTimeHistory IndexViewTypeContour View TypeMethodsContourViewContour ViewExportContourDataExport Contour DataExportContourDataWithNodeSetExport Contour Data with Nodeset

### classIDurabilityContourBandOption

```
classIDurabilityContourBandOption(oobj=None)
```

Bases:DispatchBaseClassDurability Contour Band OptionPropertiesBandLevelBand LevelLegendLocationContour Band Legend Location TypeLegendTypeContour Band Legend TypeShowTextLegendShow Text Legend

### Calculation

```
IDurabilityContourMinMaxOption.Calculation()
```

Min Max Calculation

### classIDurabilityContourMinMaxOption

```
classIDurabilityContourMinMaxOption(oobj=None)
```

Bases:DispatchBaseClassDurability Contour MinMax OptionPropertiesEnableLogScaleEnable Log ScaleMaxMax ValueMinMin ValueMinMaxTypeContour Min Max TypeShowMinMaxShow Min MaxUserDefinedMaxUser Defined Max ValueUserDefinedMinUser Defined Min ValueMethodsCalculationMin Max Calculation

### Clear

```
IDurabilityContourProbeOption.Clear()
```

Clear Probe Data

### Select

```
IDurabilityContourProbeOption.Select(Val)
```

Select Probe Data

### classIDurabilityContourProbeOption

```
classIDurabilityContourProbeOption(oobj=None)
```

Bases:DispatchBaseClassDurability Contour Probe OptionPropertiesShowProbeResultShow Probe ResultMethodsClearClear Probe DataSelectSelect Probe Data

### classIDurabilityContourStyleOption

```
classIDurabilityContourStyleOption(oobj=None)
```

Bases:DispatchBaseClassDurability Contour Style OptionPropertiesColorTypeColor TypeGrayScaleColorGray Scale ColorMeshLinesColorMesh Lines ColorShowMeshLinesShow Mesh LinesSpectrumMaxColorSpectrum Max ColorSpectrumMinColorSpectrum Min ColorStyleColor StyleTextColorText ColorVectorColorVector ColorVectorSizeVector Size

### Calculation

```
IDurabilityFatigueEvaluation.Calculation()
```

Calculation Fatigue

### ClearTimeHistory

```
IDurabilityFatigueEvaluation.ClearTimeHistory()
```

Clear Time History List

### CreateTimeHistory

```
IDurabilityFatigueEvaluation.CreateTimeHistory(use,Name,timeRange)
```

Create Time History

### Import

```
IDurabilityFatigueEvaluation.Import(strFileName)
```

Import Previous Fatigue Results

### PlotHistory

```
IDurabilityFatigueEvaluation.PlotHistory()
```

Plot Original History in Fatigue Tool

### RainFlowCounting

```
IDurabilityFatigueEvaluation.RainFlowCounting()
```

RainFlow Counting in Fatigue Tool

### classIDurabilityFatigueEvaluation

```
classIDurabilityFatigueEvaluation(oobj=None)
```

Bases:DispatchBaseClassDurability Fatigue EvaluationPropertiesAxialModeAxial ModeElementPatchSetElement/ Patch SetLifeCriteriaLife CriteriaMaterialGet fatigue MaterialOccurrenceOccurrencePlotOriginalHistoryGet Plot Original HistoryPreStressFilePre-Stress fileRainFlowGet Rainflow CountingResultGet fatigue Evaluation ResultSafetyFactorGet fatigue Evaluation Safety FactorSpecificAngleCalculationOptionGet Specific Angle Calculation OptionSpecificAngleCalculationResultGet Specific Angle Calculation R

### classIDurabilityFatigueEvaluationSafetyFactor

```
classIDurabilityFatigueEvaluationSafetyFactor(oobj=None)
```

Bases:DispatchBaseClassDurability Fatigue Evaluation - Safety FactorPropertiesLifeCriterionLife CriterionSearchingIncrementSearching Increment

### classIDurabilityFatigueEvaluationStrain

```
classIDurabilityFatigueEvaluationStrain(oobj=None)
```

Bases:DispatchBaseClassDurability Fatigue Evaluation - StrainPropertiesLifeCriterionLife CriterionSearchingIncrementSearching Increment

### classIDurabilityFatigueEvaluationStress

```
classIDurabilityFatigueEvaluationStress(oobj=None)
```

Bases:DispatchBaseClassDurability Fatigue Evaluation - StressPropertiesBWI_WeldBWI Weld TypeLifeCriterionLife CriterionMeanStressEffectMean Stress EffectNumofStdDeviationsNumber of Std.SearchingIncrementSearching Increment

### classIDurabilityFatigueMaterial

```
classIDurabilityFatigueMaterial(oobj=None)
```

Bases:DispatchBaseClassDurability Fatigue Evaluation - MaterialPropertiesActiveMaterialActive Material NameFileNameMaterial XML File NameUnitMaterial Unit TypeUserDefinedGet User Defined Material

### Export

```
IDurabilityFatigueMaterialUserDefined.Export(path,OverWrite)
```

Export method

### Import

```
IDurabilityFatigueMaterialUserDefined.Import(path)
```

Import method

### classIDurabilityFatigueMaterialUserDefined

```
classIDurabilityFatigueMaterialUserDefined(oobj=None)
```

Bases:DispatchBaseClassDurability Fatigue Evaluation - User Defined MaterialPropertiesAmplitudeAmplitudeCycleToFailureCycle to FailureInterpolationTypeUser Defined Interpolation TypeStrengthCoefficientStrength CoefficientUltimateStrengthUltimate StrengthYieldStressYield StressMethodsExportExport methodImportImport method

### MeanStressList

```
IDurabilityFatigueResult.MeanStressList(timeHist)
```

Mean stress list

### StressAmplitudeList

```
IDurabilityFatigueResult.StressAmplitudeList(timeHist)
```

Stress amplitude list

### classIDurabilityFatigueResult

```
classIDurabilityFatigueResult(oobj=None)
```

Bases:DispatchBaseClassDurability Fatigue Evaluation - ResultPropertiesDamageDamageDamageListDamage listFaceNodeIDsFace Node IDsFaceNodeIDsListFace Node IDs listLifeLifeLifeListLife listSafetyFactorSafety FactorSafetyFactorListSafety Factor listTimeHistoryNameListTimeHistory Name listMethodsMeanStressListMean stress listStressAmplitudeListStress amplitude list

### classIDurabilityPlotOriginalHistory

```
classIDurabilityPlotOriginalHistory(oobj=None)
```

Bases:DispatchBaseClassDurability Fatigue Evaluation - Plot Original HistoryPropertiesAngleTypeAngle TypeLocationTypeLocationTypeTimeHistoryNameTimeHistory NameUserDefinedAngleUser Defined Angle (Degree)UserDefinedPatchIndexUser Defined Patch Index

### Execute

```
IDurabilityPreStress.Execute()
```

Execute method

### classIDurabilityPreStress

```
classIDurabilityPreStress(oobj=None)
```

Bases:DispatchBaseClassDurability Pre-StressPropertiesElementPatchSetElement/ Patch SetInputFileInput CSV fileReferenceMarkerReference markerResultFileResult DNSRD fileMethodsExecuteExecute method

### classIDurabilityPreference

```
classIDurabilityPreference(oobj=None)
```

Bases:DispatchBaseClassDurability PreferencePropertiesConvergenceControlGet Preference Convergence ControlFatigueInfluencingFactorsGet Preference Fatigue Influencing FactorsMaterialGet Preference MaterialRainFlowCountingGet Preference Rainflow Counting

### classIDurabilityPreferenceConvergenceControl

```
classIDurabilityPreferenceConvergenceControl(oobj=None)
```

Bases:DispatchBaseClassDurability Preference - Convergence ControlPropertiesAbsoluteErrorAbsolute ErrorInitialValueInital ValueMaxNumberIterationMax Number Iteration

### classIDurabilityPreferenceFatigueInfluencingFactors

```
classIDurabilityPreferenceFatigueInfluencingFactors(oobj=None)
```

Bases:DispatchBaseClassDurability Preference - Fatigue Influencing FactorsPropertiesLoadFactorLoad FactorNotchFactorAmpNotch Factor AmpOtherFactorOther FactorScaleFactorScale FactorSizeFactorSize FactorSurfaceFactorSurface FactorSurfaceFactorTypeSurface Factor type

### classIDurabilityPreferenceMaterial

```
classIDurabilityPreferenceMaterial(oobj=None)
```

Bases:DispatchBaseClassDurability Preference - MaterialPropertiesLibraryPathMaterial Library Path

### classIDurabilityPreferenceRainflowCounting

```
classIDurabilityPreferenceRainflowCounting(oobj=None)
```

Bases:DispatchBaseClassDurability Preference - RainFlow CountingPropertiesNumberRangesNumber RangesPeakValleyPeak Valley

### classIDurabilityRainflowCounting

```
classIDurabilityRainflowCounting(oobj=None)
```

Bases:DispatchBaseClassDurability Fatigue Evaluation - Rainflow CountingPropertiesAngleTypeAngle TypeLocationTypeLocationTypeTimeHistoryNameTimeHistory NameUserDefinedAngleUser Defined Angle (Degree)UserDefinedPatchIndexUser Defined Patch Index

### classIDurabilitySpecificAngleCalculationOption

```
classIDurabilitySpecificAngleCalculationOption(oobj=None)
```

Bases:DispatchBaseClassDurability Fatigue Evaluation - Specific Angle Calculation OptionPropertiesAngleTypeAngle TypeLocationTypePatch Location TypeTimeHistoryNameTimeHistory NameUserDefinedAngleUser Defined Angle (Degree)UserDefinedPatchIndexUser Defined Patch Index

### classIDurabilitySpecificAngleCalculationResult

```
classIDurabilitySpecificAngleCalculationResult(oobj=None)
```

Bases:DispatchBaseClassDurability Fatigue Evaluation - Specific Angle Calculation ResultPropertiesDamageDamageLifeLifeSafetyFactorSafety Factor

