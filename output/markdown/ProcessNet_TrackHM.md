# ProcessNet.TrackHM

> ProcessNet.TrackHM API

## Overview

**Full Name:** FunctionBay.RecurDyn.ProcessNet.TrackHM

**Methods:** 126

**Examples:** 0

## Methods

### AddAllOutputLink

```
ITrackHMAssembly.AddAllOutputLink()
```

Add all the link body to output list

### AddOutputLink

```
ITrackHMAssembly.AddOutputLink(strFileName)
```

Add a link body to output list

### AddPassingBody

```
ITrackHMAssembly.AddPassingBody(pVal)
```

Add a passing body

### AddPassingBody2

```
ITrackHMAssembly.AddPassingBody2(pVal)
```

Add a passing body with ITrackHMBody

### DeletePassingBody

```
ITrackHMAssembly.DeletePassingBody(pVal)
```

Delete a passing body

### DeletePassingBody2

```
ITrackHMAssembly.DeletePassingBody2(pVal)
```

Delete a passing body with ITrackHMBody

### GetOutputLinkList

```
ITrackHMAssembly.GetOutputLinkList()
```

TrackHM assembly output list

### RemoveAllOutputLink

```
ITrackHMAssembly.RemoveAllOutputLink()
```

Remove all the link body from output list

### RemoveOutputLink

```
ITrackHMAssembly.RemoveOutputLink(strFileName)
```

Remove a link body from output list

### UpdateLinkInitialVelocity

```
ITrackHMAssembly.UpdateLinkInitialVelocity()
```

Update initial velocity of links

### classITrackHMAssembly

```
classITrackHMAssembly(oobj=None)
```

Bases:DispatchBaseClassTrackHM AssemblyPropertiesBushingForceCollectionBushing force collectionBushingForceParameterBushing force parameterCommentCommentContactParameterContact ground track link shoeFullNameFullName such asBody1.Marker1@Model1LinkInitialVelocityReferenceFramelink initialvelocity Reference FrameLinkInitialVelocityXAxisLink initial velocity x-axisLinkNumbersLink numbersNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody retu

### AddAllOutputLink

```
AddAllOutputLink()
```

Add all the link body to output list

### AddOutputLink

```
AddOutputLink()
```

Add a link body to output list

### AddPassingBody

```
AddPassingBody()
```

Add a passing body

### AddPassingBody2

```
AddPassingBody2()
```

Add a passing body with ITrackHMBody

### DeletePassingBody

```
DeletePassingBody()
```

Delete a passing body

### DeletePassingBody2

```
DeletePassingBody2()
```

Delete a passing body with ITrackHMBody

### GetOutputLinkList

```
GetOutputLinkList()
```

TrackHM assembly output list

### RemoveAllOutputLink

```
RemoveAllOutputLink()
```

Remove all the link body from output list

### RemoveOutputLink

```
RemoveOutputLink()
```

Remove a link body from output list

### UpdateLinkInitialVelocity

```
UpdateLinkInitialVelocity()
```

Update initial velocity of links

### Export

```
ITrackHMAssemblyBushingForceParameter.Export(strName,val)
```

Export bushing force parameter

### Import

```
ITrackHMAssemblyBushingForceParameter.Import(strName)
```

Import bushing force parameter

### classITrackHMAssemblyBushingForceParameter

```
classITrackHMAssemblyBushingForceParameter(oobj=None)
```

Bases:DispatchBaseClassTrackHM Assembly Bushing Force ParameterPropertiesRotationDampingCoefficientXRotation damping coefficient XRotationDampingCoefficientYRotation damping coefficient YRotationDampingCoefficientZRotation damping coefficient ZRotationDampingExponentXRotation damping exponent XRotationDampingExponentYRotation damping exponent YRotationDampingExponentZRotation damping exponent ZRotationDampingSplineXRotation damping spline XRotationDampingSplineYRotation damping spline YRotationD

### Export

```
Export()
```

Export bushing force parameter

### Import

```
Import()
```

Import bushing force parameter

### Item

```
ITrackHMAssemblyCollection.Item(var)
```

Returns a specific item.

### classITrackHMAssemblyCollection

```
classITrackHMAssemblyCollection(oobj=None)
```

Bases:DispatchBaseClassTrackHM Assembly CollectionPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### Item

```
Item()
```

Returns a specific item.

### Export

```
ITrackHMAssemblyContactGroundTrackLinkShoePad.Export(strName,val)
```

Export ground parameter

### Import

```
ITrackHMAssemblyContactGroundTrackLinkShoePad.Import(strName)
```

Import ground parameter

### SoftGroundType

```
ITrackHMAssemblyContactGroundTrackLinkShoePad.SoftGroundType(val)
```

Soft ground type

### classITrackHMAssemblyContactGroundTrackLinkShoePad

```
classITrackHMAssemblyContactGroundTrackLinkShoePad(oobj=None)
```

Bases:DispatchBaseClassTrackHM Assembly Contact Ground TrackLink Shoe PadPropertiesCohesionCohesion (c)DampingCoefficientThe viscous damping coefficient for the contact normal force.DampingExponentThe damping exponent for a non-linear contact normal forceDampingSplineDamping splineExponentialNumberExponential number (n)FrictionFrictionFrictionCoefficientThe friction coefficient for the contact normal force.FrictionSplineThe spline which shows relative velocity to the friction coefficient or the 

### Export

```
Export()
```

Export ground parameter

### Import

```
Import()
```

Import ground parameter

### SoftGroundType

```
SoftGroundType()
```

Soft ground type

### classITrackHMAssemblySphereContact

```
classITrackHMAssemblySphereContact(oobj=None)
```

Bases:DispatchBaseClassTrackHM sphere contact propertyPropertiesContactPropertySphere contact propertyGeometrySphereCollectionSphere geometry collection of the sphere contactMaximumPenetrationMaximum penetration.MethodsAddSphereContactAdd a sphere contact

### AddSphereContact

```
AddSphereContact()
```

Add a sphere contact

### classITrackHMBody

```
classITrackHMBody(oobj=None)
```

Bases:DispatchBaseClassTrackHM bodyPropertiesCommentCommentFullNameFullName such asBody1.Marker1@Model1GeneralBodyGeneralBodyNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceUserDataUser supplied data

### classITrackHMBodyCollection

```
classITrackHMBodyCollection(oobj=None)
```

Bases:DispatchBaseClassTrackHM wheel body collectionPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### Item

```
Item()
```

Returns a specific item.

### classITrackHMBodyLink

```
classITrackHMBodyLink(oobj=None)
```

Bases:DispatchBaseClassTrackHM body linkPropertiesActiveDoubleShoePadDouble shoe padActiveShoePadActive shoe padCommentCommentDoubleShoePadFirstDouble shoe pad first profileDoubleShoePadSecondDouble shoe pad second profileFullNameFullName such asBody1.Marker1@Model1GeneralBodyGeneralBodyGraphicGraphicMeshSegmentMesh segmentNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns

### CreateMarker

```
CreateMarker()
```

Creates a marker

### UpdateAssembly

```
UpdateAssembly()
```

Update assembly

### UpdateGeometry

```
UpdateGeometry()
```

Update geometry

### classITrackHMBodyLinkCollection

```
classITrackHMBodyLinkCollection(oobj=None)
```

Bases:DispatchBaseClassTrackHM Body Link CollectionPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### Item

```
Item()
```

Returns a specific item.

### classITrackHMBodyLinkDouble

```
classITrackHMBodyLinkDouble(oobj=None)
```

Bases:DispatchBaseClassTrackHM double link bodyPropertiesActiveDoubleShoePadDouble shoe padActiveShoePadActive shoe padCommentCommentDoubleShoePadFirstDouble shoe pad first profileDoubleShoePadSecondDouble shoe pad second profileFullNameFullName such asBody1.Marker1@Model1GeneralBodyGeneralBodyGeometryGeometryGraphicGraphicMeshSegmentMesh segmentNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSyste

### CreateMarker

```
CreateMarker()
```

Creates a marker

### UpdateAssembly

```
UpdateAssembly()
```

Update assembly

