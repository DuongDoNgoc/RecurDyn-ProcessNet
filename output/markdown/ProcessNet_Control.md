# ProcessNet.Control

> ProcessNet.Control API

## Overview

**Full Name:** FunctionBay.RecurDyn.ProcessNet.Control

**Methods:** 67

**Examples:** 0

## Methods

### classControlCoSimFMIInterfaceTimeStepUnit

```
classControlCoSimFMIInterfaceTimeStepUnit(value)
```

Bases:IntEnumControlCoSimFMIInterfaceTimeStepUnit enumeration.MembersControlCoSimFMIInterfaceTimeStepUnit_MillisecondConstant value is 1.ControlCoSimFMIInterfaceTimeStepUnit_SecondConstant value is 0.

### classControlCoSimFMIType

```
classControlCoSimFMIType(value)
```

Bases:IntEnumControlCoSimFMIType enumeration.MembersControlCoSimFMIType_ExportConstant value is 1.ControlCoSimFMIType_ImportConstant value is 0.

### classControlCoSimFMIVersion

```
classControlCoSimFMIVersion(value)
```

Bases:IntEnumControlCoSimFMIVersion enumeration.MembersControlCoSimFMIVersion_V10Constant value is 0.ControlCoSimFMIVersion_V20Constant value is 1.

### classControlCoSimHostProgram

```
classControlCoSimHostProgram(value)
```

Bases:IntEnumControlCoSimHostProgram enumeration.MembersControlCoSimHostProgram_GeneralConstant value is 1.ControlCoSimHostProgram_RecurDynConstant value is 2.ControlCoSimHostProgram_SimulinkConstant value is 0.

### classControlCoSimInterfaceVersion

```
classControlCoSimInterfaceVersion(value)
```

Bases:IntEnumControlCoSimInterfaceVersion enumeration.MembersControlCoSimInterfaceVersion_1_0Constant value is 0.ControlCoSimInterfaceVersion_2_0Constant value is 1.ControlCoSimInterfaceVersion_3_0Constant value is 2.

### classControlCoSimType

```
classControlCoSimType(value)
```

Bases:IntEnumControlCoSimType enumeration.MembersControlCoSimType_AMESimConstant value is 3.ControlCoSimType_FMIConstant value is 4.ControlCoSimType_GeneralConstant value is 1.ControlCoSimType_RDExternalConstant value is 5.ControlCoSimType_SimplorerConstant value is 2.ControlCoSimType_SimulinkConstant value is 0.

### classIControlCoSim

```
classIControlCoSim(oobj=None)
```

Bases:DispatchBaseClassControl CoSimPropertiesHostProgramHost ProgramInterfaceVersionInterfaceVersion is obsoleted.PlantFileNamePlant File NameSamplingPeriodSampling Period

### classIControlCoSimAMESim

```
classIControlCoSimAMESim(oobj=None)
```

Bases:DispatchBaseClassControl CoSim AMESimPropertiesInterfaceTimeStepIControlCoSimAMESim is obsoleted.ModelFileNameIControlCoSimAMESim is obsoleted.

### ExportFMUFile

```
IControlCoSimFMI.ExportFMUFile()
```

Export a FMU File

### classIControlCoSimFMI

```
classIControlCoSimFMI(oobj=None)
```

Bases:DispatchBaseClassControl CoSim FMIPropertiesActiveConnectionActive ConnectionFMUFileNameFMU File NameInterfaceTimeStepInterface Time StepInterfaceTimeStepUnitInterface Time Step UnitInterfaceVersionInterface VersionModelFileNameModel File NamePlantFileNamePlant File NameTypeFMI TypeUseFollowingInterfaceTimeOfHostUse Following the Interface Time of HostUseFollowingInterfaceTimeOfMasterUseFollowingInterfaceTimeOfMaster is obsolete propertyWaitingTimeWaiting TimeMethodsExportFMUFileExport a F

### ExportFMUFile

```
ExportFMUFile()
```

Export a FMU File

### classIControlCoSimGeneral

```
classIControlCoSimGeneral(oobj=None)
```

Bases:DispatchBaseClassControl CoSim GeneralPropertiesClientProgramPathNameIControlCoSimGeneral is obsoleted.HostProgramHost ProgramInterfaceVersionInterfaceVersion is obsoleted.PlantFileNamePlant File NameSamplingPeriodSampling PeriodWaitingTimeIControlCoSimGeneral is obsoleted.

### classIControlCoSimRDExternal

```
classIControlCoSimRDExternal(oobj=None)
```

Bases:DispatchBaseClassControl CoSim RDExternalPropertiesClientProgramPathNameClient Program Path and NameHostProgramHost ProgramInterfaceVersionInterfaceVersion is obsoleted.PlantFileNamePlant File NameSamplingPeriodSampling PeriodUseFollowingInterfaceTimeOfHostUse Following the Interface Time of HostWaitingTimeWaiting Time

### classIControlCoSimSimplorer

```
classIControlCoSimSimplorer(oobj=None)
```

Bases:DispatchBaseClassControl CoSim SimplorerPropertiesHostProgramHost ProgramInterfaceVersionInterfaceVersion is obsoleted.PlantFileNamePlant File NameSamplingPeriodSampling Period

### ExportMFileToCreatePlantBlock

```
IControlCoSimSimulink.ExportMFileToCreatePlantBlock(strName)
```

Obsolete Function

### ExportMFileToCreatePlantBlock2

```
IControlCoSimSimulink.ExportMFileToCreatePlantBlock2()
```

Export M-File to create Plant Block

### ExportMFileToRunSimulinkModel

```
IControlCoSimSimulink.ExportMFileToRunSimulinkModel(strName)
```

Obsolete Function

### ExportMFileToRunSimulinkModel2

```
IControlCoSimSimulink.ExportMFileToRunSimulinkModel2()
```

Export M-File to run Simulink Model

### classIControlCoSimSimulink

```
classIControlCoSimSimulink(oobj=None)
```

Bases:DispatchBaseClassControl CoSim SimulinkPropertiesHostProgramHost ProgramInterfaceVersionInterfaceVersion is obsoleted.MFilePlantBlockM-File to Create Plant BlockMFileSimulinkModelM-File to Run Simulink ModelMatlabProgramPathNameMatlab Program Path and NameOutputFileNameOutput File NamePlantFileNamePlant File NameSamplingPeriodSampling PeriodSimulinkModelPathNameSimulink Model Path and NameUseFollowingInterfaceTimeOfHostUse Following the Interface Time of HostUseFollowingInterfaceTimeOfMast

### ExportMFileToCreatePlantBlock

```
ExportMFileToCreatePlantBlock()
```

Obsolete Function

### ExportMFileToCreatePlantBlock2

```
ExportMFileToCreatePlantBlock2()
```

Export M-File to create Plant Block

### ExportMFileToRunSimulinkModel

```
ExportMFileToRunSimulinkModel()
```

Obsolete Function

### ExportMFileToRunSimulinkModel2

```
ExportMFileToRunSimulinkModel2()
```

Export M-File to run Simulink Model

### AddGeneralPlantInput

```
IControlGeneralCoSim.AddGeneralPlantInput(pVal)
```

Add a General Plant Input

### AddGeneralPlantOutput

```
IControlGeneralCoSim.AddGeneralPlantOutput(pVal)
```

Add a General Plant Output

### DeleteGeneralPlantInput

```
IControlGeneralCoSim.DeleteGeneralPlantInput(pVal)
```

Delete a General Plant Input

### DeleteGeneralPlantOutput

```
IControlGeneralCoSim.DeleteGeneralPlantOutput(pVal)
```

Delete a General Plant Output

### classIControlGeneralCoSim

```
classIControlGeneralCoSim(oobj=None)
```

Bases:DispatchBaseClassGeneral CoSimPropertiesActiveUse FlagCoSimGeneralPlantInputCollectionCoSimGeneralPlantOutputCollectionCoSimTypeData TypeCommentCommentFMIFMIFullNameFullName such asBody1.Marker1@Model1NameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceRDExternalRDExternalSimulinkSimulinkUserDataUser supplied dataMethodsAddGeneralPlantInp

### AddGeneralPlantInput

```
AddGeneralPlantInput()
```

Add a General Plant Input

### AddGeneralPlantOutput

```
AddGeneralPlantOutput()
```

Add a General Plant Output

### DeleteGeneralPlantInput

```
DeleteGeneralPlantInput()
```

Delete a General Plant Input

### DeleteGeneralPlantOutput

```
DeleteGeneralPlantOutput()
```

Delete a General Plant Output

### Item

```
IControlGeneralCoSimCollection.Item(var)
```

Returns a specific item.

### classIControlGeneralCoSimCollection

```
classIControlGeneralCoSimCollection(oobj=None)
```

Bases:DispatchBaseClassControl General CoSim CollectionPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### Item

```
Item()
```

Returns a specific item.

### CreateGeneralCoSim

```
IControlGeneralToolkit.CreateGeneralCoSim(strName)
```

Create a General CoSim

### CreateGeneralPlantInput

```
IControlGeneralToolkit.CreateGeneralPlantInput(strName)
```

CreateGeneralPlantInput is obsoleted. Use CreateGeneralPlantInput2

### CreateGeneralPlantOutput

```
IControlGeneralToolkit.CreateGeneralPlantOutput(strName,pExpression)
```

CreateGeneralPlantOutput is obsoleted. Use CreateGeneralPlantOutput2

### DeleteGeneralPlantInput

```
IControlGeneralToolkit.DeleteGeneralPlantInput(pVal)
```

DeleteGeneralPlantInput is obsoleted. Use DeleteGeneralPlantInput2

### DeleteGeneralPlantOutput

```
IControlGeneralToolkit.DeleteGeneralPlantOutput(pVal)
```

DeleteGeneralPlantOutput is obsoleted. Use DeleteGeneralPlantOutput2

### classIControlGeneralToolkit

```
classIControlGeneralToolkit(oobj=None)
```

Bases:DispatchBaseClassControl Gerneral ToolkitPropertiesCommentCommentControlGeneralCoSimCollectionControlGeneralPlantInputCollectionControlGeneralPlantOutputCollectionFullNameFullName such asBody1.Marker1@Model1NameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceUseCoSimInfoCheck whether the GCoSim information exists or not.UserDataUser suppl

### CreateGeneralCoSim

```
CreateGeneralCoSim()
```

Create a General CoSim

### CreateGeneralPlantInput

```
CreateGeneralPlantInput()
```

CreateGeneralPlantInput is obsoleted.

### CreateGeneralPlantOutput

```
CreateGeneralPlantOutput()
```

CreateGeneralPlantOutput is obsoleted.

### DeleteGeneralPlantInput

```
DeleteGeneralPlantInput()
```

DeleteGeneralPlantInput is obsoleted.

### DeleteGeneralPlantOutput

```
DeleteGeneralPlantOutput()
```

DeleteGeneralPlantOutput is obsoleted.

### classIControlPlantInput

```
classIControlPlantInput(oobj=None)
```

Bases:DispatchBaseClassPlant InputPropertiesActiveUse FlagCommentCommentFullNameFullName such asBody1.Marker1@Model1NameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceUserDataUser supplied data

### Item

```
IControlPlantInputCollection.Item(var)
```

Returns a specific item.

### classIControlPlantInputCollection

```
classIControlPlantInputCollection(oobj=None)
```

Bases:DispatchBaseClassControlPlantInputCollectionPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### Item

```
Item()
```

Returns a specific item.

