# ProcessNet.ExternalSPI

> ProcessNet.ExternalSPI API

## Overview

**Full Name:** FunctionBay.RecurDyn.ProcessNet.ExternalSPI

**Methods:** 45

**Examples:** 0

## Methods

### CreateMassCenter

```
IExternalSPIToolkit.CreateMassCenter(Name)¶
```

Creates a MassCenter

### CreateParticleSensorBox

```
IExternalSPIToolkit.CreateParticleSensorBox(Name,referenceBody)¶
```

Creates a box ParticleSensor

### CreateParticleSensorSphere

```
IExternalSPIToolkit.CreateParticleSensorSphere(Name,referenceBody)¶
```

Creates a sphere ParticleSensor

### CreateProfile2D

```
IExternalSPIToolkit.CreateProfile2D(Name,referenceBody)¶
```

Creates a 2D profile

### CreateTrace

```
IExternalSPIToolkit.CreateTrace(Name)¶
```

Creates a Trace

### CreateWall

```
IExternalSPIToolkit.CreateWall(Name,entity)¶
```

Creates a wall

### ExportParticlePostData

```
IExternalSPIToolkit.ExportParticlePostData(path,titles,groupSequences)¶
```

Export Particle Post Data

### ExportWallFile

```
IExternalSPIToolkit.ExportWallFile(folderName)¶
```

Export wall file with target folder

### ExportWallPostData

```
IExternalSPIToolkit.ExportWallPostData(path,titles,wallSequences)¶
```

Export Wall Post Data

### FluidDisplay

```
IExternalSPIToolkit.FluidDisplay(GroupSequence)¶
```

Fluid Display

### GetClipMinMaxValue

```
IExternalSPIToolkit.GetClipMinMaxValue(GroupSequence,particleDataTitle)¶
```

Get Clip Min Max Value of target Data name

### SetClipMinMaxValue

```
IExternalSPIToolkit.SetClipMinMaxValue(GroupSequence,particleDataTitle,minValue,maxValue,fUse)¶
```

Set Clip Min Max Value of target Data name

### UpdatePostData

```
IExternalSPIToolkit.UpdatePostData()¶
```

Update post data

### classIExternalSPIToolkit

```
classIExternalSPIToolkit(oobj=None)¶
```

Bases:DispatchBaseClassExternalSPI ToolkitPropertiesCommentCommentConnectCurrent program's Switch of Co-SimulationContourParticleContourWallFullNameFullName such asBody1.Marker1@Model1HideParticleSetsIf true, RecurDyn hide all particle sets.MassCenterCollectionMassCenter CollectionNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceParticlePost

### Item

```
IMassCenterCollection.Item(var)¶
```

Returns a specific item.

### classIMassCenterCollection

```
classIMassCenterCollection(oobj=None)¶
```

Bases:DispatchBaseClassMass Center CollectionPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### AddParticleSet

```
IMassCenterExternal.AddParticleSet(GroupSequence,density)¶
```

Add a particle set and define its density

### classIMassCenterExternal

```
classIMassCenterExternal(oobj=None)¶
```

Bases:DispatchBaseClassMass CenterPropertiesColorColor of the Mass CenterCommentCommentFullNameFullName such asBody1.Marker1@Model1NameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceUserDataUser supplied dataVisibleVisible Flag of the Mass CenterWidthWidth of the Mass CenterMethodsAddParticleSetAdd a particle set and define its density

### Create

```
IParticleFluidDisplay.Create()¶
```

Create Fluid Data

### Import

```
IParticleFluidDisplay.Import()¶
```

Import Fluid Data

### classIParticleFluidDisplay

```
classIParticleFluidDisplay(oobj=None)¶
```

Bases:DispatchBaseClassFluid DisplayPropertiesAlphaAlpah ParameterCellSizeCell sizeDirectoryDirectoryDrawLineDraw LineEndFrameEnd FrameShowShow Fulid DisplySmoothRenderingVertex NormalStartFrameStart FrameThresholdThreshold ValueUseDirectoryUse DirectoryMethodsCreateCreate Fluid DataImportImport Fluid Data

### Item

```
IParticleSensorCollection.Item(var)¶
```

Returns a specific item.

### classIParticleSensorCollection

```
classIParticleSensorCollection(oobj=None)¶
```

Bases:DispatchBaseClassParticle Sensor CollectionPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### HidePlotDialog

```
IParticleSensorExternal.HidePlotDialog()¶
```

Hide the plot dialog

### ShowPlotDialog

```
IParticleSensorExternal.ShowPlotDialog()¶
```

Show the plot dialog

### classIParticleSensorExternal

```
classIParticleSensorExternal(oobj=None)¶
```

Bases:DispatchBaseClassParticle SensorPropertiesColorColorCommentCommentFullNameFullName such asBody1.Marker1@Model1GroupSequenceSequence of the Particle GroupNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfacePositionSensor PositionReferenceBodyReference BodyUserDataUser supplied dataVisibleVisible FlagMethodsHidePlotDialogHide the plot dialo

### HidePlotDialog

```
IParticleSensorExternalBox.HidePlotDialog()¶
```

Hide the plot dialog

### ShowPlotDialog

```
IParticleSensorExternalBox.ShowPlotDialog()¶
```

Show the plot dialog

### classIParticleSensorExternalBox

```
classIParticleSensorExternalBox(oobj=None)¶
```

Bases:DispatchBaseClassParticle SensorPropertiesColorColorCommentCommentDepthDepth of box sensorFullNameFullName such asBody1.Marker1@Model1GroupSequenceSequence of the Particle GroupHeightHeight of box sensorNameNameNormalDirectionSensor Normal DirectionOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfacePositionSensor PositionReferenceBodyReference B

### HidePlotDialog

```
IParticleSensorExternalSphere.HidePlotDialog()¶
```

Hide the plot dialog

### ShowPlotDialog

```
IParticleSensorExternalSphere.ShowPlotDialog()¶
```

Show the plot dialog

### classIParticleSensorExternalSphere

```
classIParticleSensorExternalSphere(oobj=None)¶
```

Bases:DispatchBaseClassParticle SensorPropertiesColorColorCommentCommentFullNameFullName such asBody1.Marker1@Model1GroupSequenceSequence of the Particle GroupNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfacePositionSensor PositionRadiusRadius of sphere sensorReferenceBodyReference BodyUserDataUser supplied dataVisibleVisible FlagMethodsHide

### classIParticleSetExternal

```
classIParticleSetExternal(oobj=None)¶
```

Bases:DispatchBaseClassParticleSetExternalPropertiesGraphicMaterialGraphic MaterialNameName

### Item

```
IParticleSetExternalCollection.Item(var)¶
```

Returns a specific item.

### classIParticleSetExternalCollection

```
classIParticleSetExternalCollection(oobj=None)¶
```

Bases:DispatchBaseClassParticleSetExternal CollectionPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### Item

```
IProfile2DCollection.Item(var)¶
```

Returns a specific item.

### classIProfile2DCollection

```
classIProfile2DCollection(oobj=None)¶
```

Bases:DispatchBaseClass2D Profile CollectionPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### HidePlotDialog

```
IProfile2DExternal.HidePlotDialog()¶
```

Hide the plot dialog

### ShowPlotDialog

```
IProfile2DExternal.ShowPlotDialog()¶
```

Show the plot dialog

### classIProfile2DExternal

```
classIProfile2DExternal(oobj=None)¶
```

Bases:DispatchBaseClass2D ProfilePropertiesColorColorCommentCommentDivisionDivision of the 2D ProfileFullNameFullName such asBody1.Marker1@Model1GroupSequenceSequence of the Particle GroupHalfdepthHalfdepth of the 2D ProfileLengthReference length of the 2D ProfileNameNameNormalDirectionNormal direction of the 2D profileOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISub

### Item

```
ITraceCollection.Item(var)¶
```

Returns a specific item.

### classITraceCollection

```
classITraceCollection(oobj=None)¶
```

Bases:DispatchBaseClassTrace CollectionPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### classITraceExternal

```
classITraceExternal(oobj=None)¶
```

Bases:DispatchBaseClassTracePropertiesColorColor of the Trace LineCommentCommentFullNameFullName such asBody1.Marker1@Model1GroupSequenceSequence of the Particle SetNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceParticleIDID of the ParticleUserDataUser supplied dataVisibleVisible Flag of the Trace LineWidthWidth of the Trace Line

### Item

```
IWallCollection.Item(var)¶
```

Returns a specific item.

### classIWallCollection

```
classIWallCollection(oobj=None)¶
```

Bases:DispatchBaseClassWall CollectionPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

