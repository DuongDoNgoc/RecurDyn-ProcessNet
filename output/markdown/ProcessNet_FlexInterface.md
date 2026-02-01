# ProcessNet.FlexInterface

> ProcessNet.FlexInterface API

## Overview

**Full Name:** FunctionBay.RecurDyn.ProcessNet.FlexInterface

**Methods:** 9

**Examples:** 0

## Methods

### classIFlexInterface

```
classIFlexInterface(oobj=None)
```

Bases:DispatchBaseClassFlex Interface ToolkitPropertiesCommentCommentFullNameFullName such asBody1.Marker1@Model1NameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceRFlexGeneratorGet RFlex GeneratorUserDataUser supplied data

### classIRFlexGenerationOption

```
classIRFlexGenerationOption(oobj=None)
```

Bases:DispatchBaseClassOption for Generating RFlex BodyPropertiesAutoMPCFlagAutoMPC FlagBDFFilePathBDF file pathBodyTarget BodyDeleteDynamisDataBaseFilesFlagFlag to delete dynamis dataBase filessDynamisInputFilePathDYNAMIS input file pathFixedInterfaceNormalModeLowerFrequencyFixed Interface Normal Mode Lower frequencyFixedInterfaceNormalModeUpperFrequencyFixed Interface Normal Mode Upper frequencyIncludeBCFlagInlcude BC from fixed joint and FFlex BC FlagInterfaceNodeFDRElementMultiInterface node

### execute

```
IRFlexGenerator.execute()
```

Generate RFlex Body

### classIRFlexGenerator

```
classIRFlexGenerator(oobj=None)
```

Bases:DispatchBaseClassRFlex GeneratorPropertiesOptionOption to generate RFlex BodyMethodsexecuteGenerate RFlex Body

### execute

```
execute()
```

Generate RFlex Body

### classInterfaceNodeType

```
classInterfaceNodeType(value)
```

Bases:IntEnumInterfaceNodeType enumeration.MembersInterfaceNodeType_DirectInputConstant value is 3.InterfaceNodeType_MultiFDRElementConstant value is 2.InterfaceNodeType_MultiNodeSetConstant value is 1.InterfaceNodeType_SingleNodeSetConstant value is 0.

### classRFIShellRecoveryType

```
classRFIShellRecoveryType(value)
```

Bases:IntEnumRFIShellRecoveryType enumeration.MembersRFIShellRecoveryType_BOTTOMConstant value is 1.RFIShellRecoveryType_TOPConstant value is 0.

### classRFISolverType

```
classRFISolverType(value)
```

Bases:IntEnumRFISolverType enumeration.MembersRFISolverType_DynamisConstant value is 1.RFISolverType_SunShineConstant value is 0.

### classRFITargetBodyType

```
classRFITargetBodyType(value)
```

Bases:IntEnumRFITargetBodyType enumeration.MembersRFITargetBodyType_BDFFileConstant value is 1.RFITargetBodyType_BodyConstant value is 0.RFITargetBodyType_DYNAMISInputFileConstant value is 2.

