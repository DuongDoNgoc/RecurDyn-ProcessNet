# ProcessNet.AutoDesign

> ProcessNet.AutoDesign API

## Overview

**Full Name:** FunctionBay.RecurDyn.ProcessNet.AutoDesign

**Methods:** 207

**Examples:** 0

## Methods

### classADSimulationType

```
classADSimulationType(value)
```

Bases:IntEnumADSimulationType enumeration.MembersADSimulation_DynKinematicConstant value is 0.ADSimulation_StaticConstant value is 1.

### classAnalysisResponseType

```
classAnalysisResponseType(value)
```

Bases:IntEnumAnalysisResponseType enumeration.MembersAnalysisResponse_BasicConstant value is 0.AnalysisResponse_FEResultConstant value is 1.AnalysisResponse_ProcessNetConstant value is 3.AnalysisResponse_ScopeConstant value is 2.

### classCheckFlagType

```
classCheckFlagType(value)
```

Bases:IntEnumCheckFlagType enumeration.MembersCheckFlag_ExportConstant value is 1.CheckFlag_GetConstant value is 0.

### classCombinationType

```
classCombinationType(value)
```

Bases:IntEnumCombinationType enumeration.MembersCombination_MAXConstant value is 1.Combination_MINConstant value is 0.

### classConfigurationDesignType

```
classConfigurationDesignType(value)
```

Bases:IntEnumConfigurationDesignType enumeration.MembersConfigurationDesign_OFFConstant value is 1.ConfigurationDesign_ONConstant value is 0.

### classConstraintGoalType

```
classConstraintGoalType(value)
```

Bases:IntEnumConstraintGoalType enumeration.MembersConstraintGoal_EQConstant value is 0.ConstraintGoal_GEConstant value is 2.ConstraintGoal_LEConstant value is 1.

### classConvergenceRelaxationControlType

```
classConvergenceRelaxationControlType(value)
```

Bases:IntEnumConvergenceRelaxationControlType enumeration.MembersConvergenceRelaxationControl_OFFConstant value is 0.ConvergenceRelaxationControl_ONConstant value is 1.

### classDOEMethodType

```
classDOEMethodType(value)
```

Bases:IntEnumDOEMethodType enumeration.MembersDOEMethod_BoseOrthogonalArrayConstant value is 5.DOEMethod_ExtendedPlackettBurmanConstant value is 0.DOEMethod_FullFactorialDesignConstant value is 1.DOEMethod_LevelBalancedDescriptiveDesignConstant value is 3.DOEMethod_ThreelevelOrthogonalArrayConstant value is 2.DOEMethod_TwoLevelOrthogonalArrayConstant value is 4.

### classDPFormType

```
classDPFormType(value)
```

Bases:IntEnumDPFormType enumeration.MembersDPForm_ScaleConstant value is 1.DPForm_ValueConstant value is 0.

### classDefinitionType

```
classDefinitionType(value)
```

Bases:IntEnumDefinitionType enumeration.MembersDefinition_ConstraintConstant value is 1.Definition_ObjectiveConstant value is 0.

### classDesignParameterType

```
classDesignParameterType(value)
```

Bases:IntEnumDesignParameterType enumeration.MembersDesignParameter_AngularConstant value is 4.DesignParameter_CylindricalConstant value is 2.DesignParameter_DirectConstant value is 0.DesignParameter_SphericalConstant value is 3.DesignParameter_TranslationalConstant value is 1.

### classDesignVariableType

```
classDesignVariableType(value)
```

Bases:IntEnumDesignVariableType enumeration.MembersDesignVariable_ConstantConstant value is 1.DesignVariable_VariableConstant value is 0.

### classDeviationType

```
classDeviationType(value)
```

Bases:IntEnumDeviationType enumeration.MembersDeviation_COVConstant value is 1.Deviation_SDConstant value is 0.

### classExportDataType

```
classExportDataType(value)
```

Bases:IntEnumExportDataType enumeration.MembersExportData_ARConstant value is 4.ExportData_AllConstant value is 6.ExportData_DVConstant value is 5.ExportData_DesignCostConstant value is 0.ExportData_SimulationDescriptionConstant value is 1.ExportData_SimulationStatusConstant value is 2.ExportData_ViolationConstant value is 3.

### classExtendedPlackettBurmanLevelType

```
classExtendedPlackettBurmanLevelType(value)
```

Bases:IntEnumExtendedPlackettBurmanLevelType enumeration.MembersExtendedPlackettBurmanLevel_Level2Constant value is 0.ExtendedPlackettBurmanLevel_Level3Constant value is 1.ExtendedPlackettBurmanLevel_Level4Constant value is 2.

### classFEResultType

```
classFEResultType(value)
```

Bases:IntEnumFEResultType enumeration.MembersFEResult_Mass_ElementSetConstant value is 2.FEResult_Stress_ElementSetConstant value is 1.FEResult_Stress_NodeSetConstant value is 0.

### classFETreatmentType

```
classFETreatmentType(value)
```

Bases:IntEnumFETreatmentType enumeration.MembersFETreatment_AverageValueConstant value is 3.FETreatment_EndValueConstant value is 2.FETreatment_InitialValueConstant value is 1.FETreatment_MaxValueConstant value is 5.FETreatment_MinValueConstant value is 4.

### classFullFactorialDesignLevelType

```
classFullFactorialDesignLevelType(value)
```

Bases:IntEnumFullFactorialDesignLevelType enumeration.MembersFullFactorialDesignLevel_Level2Constant value is 0.FullFactorialDesignLevel_Level3Constant value is 1.FullFactorialDesignLevel_Level4Constant value is 2.FullFactorialDesignLevel_Level5Constant value is 3.

### classHybridSamplingOptionType

```
classHybridSamplingOptionType(value)
```

Bases:IntEnumHybridSamplingOptionType enumeration.MembersHybridSamplingOption_GetFromSimulationHistoryConstant value is 2.HybridSamplingOption_KoshalMethodConstant value is 0.HybridSamplingOption_LatinHypercubeSampleConstant value is 1.

### classIADAnalysisControlMonteCarloReliability

```
classIADAnalysisControlMonteCarloReliability(oobj=None)
```

Bases:DispatchBaseClassAnalysis Control - MonteCarlo ReliabilityPropertiesSamplingMethodTypeSampling Method TypeSamplingPointsNumber of Sampling PointsSaveResultSave resultsSimulationTypeSimulation TypeUseNewSamplingUse New SamplingUseSaveResultUse save results

### classIADAnalysisControlSAOReliability

```
classIADAnalysisControlSAOReliability(oobj=None)
```

Bases:DispatchBaseClassAnalysis Control - SAOReliabilityPropertiesConvergenceToleranceConvergence ToleranceHybridSamplingOptionTypeSampling Option Type for Hybrid MethodLatinHybercubeSampleLatinHybercube SampleReliablitySolverTypeReliablity Solver TypeSaveResultSave resultsSimulationTypeSimulation TypeUseSaveResultUse save results

### classIADAnalysisResponse

```
classIADAnalysisResponse(oobj=None)
```

Bases:DispatchBaseClassAnalysisResponsePropertiesAnalysisResponseTypeAnalysis Response TypeCommentCommentDescriptionDescriptionFullNameFullName such asBody1.Marker1@Model1NameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceUseUse PIUserDataUser supplied data

### classIADAnalysisResponseBasic

```
classIADAnalysisResponseBasic(oobj=None)
```

Bases:DispatchBaseClassAnalysisResponse - BasicPropertiesAnalysisResponseTypeAnalysis Response TypeCommentCommentDescriptionDescriptionFullNameFullName such asBody1.Marker1@Model1NameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceResultOutputResult OutputTreatmentTypeTreatment TypeUseUse PIUserDataUser supplied data

### Item

```
IADAnalysisResponseCollection.Item(var)
```

Returns a specific item.

### classIADAnalysisResponseCollection

```
classIADAnalysisResponseCollection(oobj=None)
```

Bases:DispatchBaseClassAnalysisResponse CollectionPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### classIADAnalysisResponseFEResult

```
classIADAnalysisResponseFEResult(oobj=None)
```

Bases:DispatchBaseClassAnalysisResponse - FEResultPropertiesAnalysisResponseTypeAnalysis Response TypeCommentCommentDescriptionDescriptionFullNameFullName such asBody1.Marker1@Model1NameNameNodeElementSetNodeSet or ElementSetOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceResultTypeFEResult TypeTreatmentTypeTreatment TypeUseUse PIUserDataUser suppl

### classIADAnalysisResponseScope

```
classIADAnalysisResponseScope(oobj=None)
```

Bases:DispatchBaseClassAnalysisResponse - ScopePropertiesAnalysisResponseTypeAnalysis Response TypeCommentCommentDescriptionDescriptionFullNameFullName such asBody1.Marker1@Model1NameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceScopeScopeTreatmentTypeTreatment TypeUseUse PIUserDataUser supplied data

### classIADConvergenceTolerance

```
classIADConvergenceTolerance(oobj=None)
```

Bases:DispatchBaseClassConvergence TolerancePropertiesLimitStateValueLimit State ValueMaximumIterationMaximum IterationObjectiveChangeRateObjective Change Rate in Consecutive Interations

### classIADConvergenceToleranceOptimization

```
classIADConvergenceToleranceOptimization(oobj=None)
```

Bases:DispatchBaseClassConvergence Tolerance - OptimizationPropertiesConvergenceRelaxationControlTypeConvergence Relaxation Control TypeEqualityConstraintsEquality ConstraintsInequalityConstraintsInequality ConstraintsMaximumIterationMaximum Iteration of SAOObjectiveChangeRateObjective Change Rate in Consecutive Interations

### AnalysisResponseResult

```
IADCorrelationAnalysis.AnalysisResponseResult(AR)
```

Result of Analysis Response

### classIADCorrelationAnalysis

```
classIADCorrelationAnalysis(oobj=None)
```

Bases:DispatchBaseClassCorrelation AnalysisMethodsAnalysisResponseResultResult of Analysis Response

### Execute

```
IADDesignMonteCarloReliability.Execute()
```

Execution

### classIADDesignMonteCarloReliability

```
classIADDesignMonteCarloReliability(oobj=None)
```

Bases:DispatchBaseClassMonteCarlo ReliabilityPropertiesAnalysisControlAnalysis ControlCommentCommentDesignVariableDesign VariableFullNameFullName such asBody1.Marker1@Model1NameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfacePerformanceIndexPerformance IndexResultSheetResult SheetSummarySheetSummary SheetUserDataUser supplied dataMethodsExecute

### Execute

```
IADDesignOptimization.Execute()
```

Execution

### classIADDesignOptimization

```
classIADDesignOptimization(oobj=None)
```

Bases:DispatchBaseClassOptimizationPropertiesCommentCommentDesignVariableDesign VariableFullNameFullName such asBody1.Marker1@Model1NameNameOptimizationControlOptimization ControlOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfacePerformanceIndexPerformance IndexResultSheetResult SheetSummarySheetSummary SheetUserDataUser supplied dataMethodsExecuteEx

### classIADDesignParameter

```
classIADDesignParameter(oobj=None)
```

Bases:DispatchBaseClassDesignParameterPropertiesCommentCommentCurrentCurrentDescriptionDescriptionDesignParameterTypeDesign Parameter TypeFullNameFullName such asBody1.Marker1@Model1LBLower boundNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceUBUpper boundUseUse DVUserDataUser supplied data

### classIADDesignParameterAngular

```
classIADDesignParameterAngular(oobj=None)
```

Bases:DispatchBaseClassFEShape4 : Angular RelationPropertiesCommentCommentConfigurationDesignTypeCartesian motion typeCurrentCurrentDescriptionDescriptionDesignParameterTypeDesign Parameter TypeFullNameFullName such asBody1.Marker1@Model1LBLower boundNameNameNodeSetNodeSetOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceRefMarkerReference markerRefe

### Item

```
IADDesignParameterCollection.Item(var)
```

Returns a specific item.

### classIADDesignParameterCollection

```
classIADDesignParameterCollection(oobj=None)
```

Bases:DispatchBaseClassDesignParameter CollectionPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### classIADDesignParameterCylindrical

```
classIADDesignParameterCylindrical(oobj=None)
```

Bases:DispatchBaseClassFEShape2 : Cylindrical DistancePropertiesCenterAxisUnitVectorCenter Axis Unit VectorCenterRefMarkerCenter Reference markerCommentCommentConfigurationDesignTypeCartesian motion typeCurrentCurrentDescriptionDescriptionDesignParameterTypeDesign Parameter TypeFullNameFullName such asBody1.Marker1@Model1LBLower boundNameNameNodeSetNodeSetOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSys

### classIADDesignParameterDirect

```
classIADDesignParameterDirect(oobj=None)
```

Bases:DispatchBaseClassDirect RelationPropertiesCommentCommentCurrentCurrentDescriptionDescriptionDesignParameterTypeDesign Parameter TypeFullNameFullName such asBody1.Marker1@Model1LBLower boundNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceParametricValueParametric valueUBUpper boundUseUse DVUserDataUser supplied data

### classIADDesignParameterSpherical

```
classIADDesignParameterSpherical(oobj=None)
```

Bases:DispatchBaseClassFEShape3 : Spherical DistancePropertiesCenterRefMarkerCenter Reference markerCommentCommentConfigurationDesignTypeCartesian motion typeCurrentCurrentDescriptionDescriptionDesignParameterTypeDesign Parameter TypeFullNameFullName such asBody1.Marker1@Model1LBLower boundNameNameNodeSetNodeSetOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSyste

### classIADDesignParameterTranslational

```
classIADDesignParameterTranslational(oobj=None)
```

Bases:DispatchBaseClassFEShape1 : Translational RelationPropertiesCommentCommentConfigurationDesignTypeCartesian motion typeCurrentCurrentDescriptionDescriptionDesignParameterTypeDesign Parameter TypeDirectionalUnitVectorDirectional Unit VectorFullNameFullName such asBody1.Marker1@Model1LBLower boundNameNameNodeSetNodeSetOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning IS

### Execute

```
IADDesignRobustOptimization.Execute()
```

Execution

### classIADDesignRobustOptimization

```
classIADDesignRobustOptimization(oobj=None)
```

Bases:DispatchBaseClassRobust OptimizationPropertiesCommentCommentDesignVariableDesign VariableFullNameFullName such asBody1.Marker1@Model1NameNameOptimizationControlOptimization ControlOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfacePerformanceIndexPerformance IndexResultSheetResult SheetSummarySheetSummary SheetUserDataUser supplied dataMethodsEx

### Execute

```
IADDesignSAOReliability.Execute()
```

Execution

### classIADDesignSAOReliability

```
classIADDesignSAOReliability(oobj=None)
```

Bases:DispatchBaseClassSAO ReliabilityPropertiesAnalysisControlAnalysis ControlCommentCommentDesignVariableDesign VariableFullNameFullName such asBody1.Marker1@Model1NameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfacePerformanceIndexPerformance IndexResultSheetResult SheetSummarySheetSummary SheetUserDataUser supplied dataMethodsExecuteExecuti

### Check

```
IADDesignSimulationHistory.Check(type,flag,startIndex,endIndex)
```

Check Get or Export flag

### CheckAll

```
IADDesignSimulationHistory.CheckAll(type,flag)
```

Check all Get or Export flag

### Delete

```
IADDesignSimulationHistory.Delete(startIndex,endIndex)
```

Delete simualtion history values

