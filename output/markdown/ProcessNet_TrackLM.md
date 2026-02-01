# ProcessNet.TrackLM

> ProcessNet.TrackLM API

## Overview

**Full Name:** FunctionBay.RecurDyn.ProcessNet.TrackLM

**Methods:** 156

**Examples:** 0

## Methods

### classContactParameterSoftGroundType

```
classContactParameterSoftGroundType(value)
```

Bases:IntEnumContactParameterSoftGroundType enumeration.MembersContactParameterSoftGroundType_Clayey_SoilConstant value is 4.ContactParameterSoftGroundType_Dry_SandConstant value is 0.ContactParameterSoftGroundType_Grenville_LoamConstant value is 11.ContactParameterSoftGroundType_Heavy_ClayConstant value is 5.ContactParameterSoftGroundType_LETE_SandConstant value is 7.ContactParameterSoftGroundType_Lean_ClayConstant value is 6.ContactParameterSoftGroundType_North_Gower_Clayey_LoamConstant value 

### classContactSearchType

```
classContactSearchType(value)
```

Bases:IntEnumContactSearchType enumeration.MembersContactSearchType_FullSearchConstant value is 0.ContactSearchType_PartialSearchConstant value is 1.

### classContactSprocketType

```
classContactSprocketType(value)
```

Bases:IntEnumContactSprocketType enumeration.MembersContactSprocketType_LeftPinConstant value is 0.ContactSprocketType_RightPinConstant value is 1.

### classIPassingBodyCollection

```
classIPassingBodyCollection(oobj=None)
```

Bases:DispatchBaseClassTrackLM passing body collection of assembly

### AddAllOutputLink

```
ITrackLMAssembly.AddAllOutputLink()
```

Add all the link body to output list

### AddOutputLink

```
ITrackLMAssembly.AddOutputLink(strFileName)
```

Add a link body to output list

### AddPassingBody

```
ITrackLMAssembly.AddPassingBody(pVal)
```

Add a passing body

### AddPassingBody2

```
ITrackLMAssembly.AddPassingBody2(pVal)
```

Add a passing body with ITrackLMBody

### CreateGrouserContact

```
ITrackLMAssembly.CreateGrouserContact()
```

Create a grouser contact

### DeleteGrouserContact

```
ITrackLMAssembly.DeleteGrouserContact(pVal)
```

Delete a grouser contact

### DeletePassingBody

```
ITrackLMAssembly.DeletePassingBody(pVal)
```

Delete a passing body

### DeletePassingBody2

```
ITrackLMAssembly.DeletePassingBody2(pVal)
```

Delete a passing body with ITrackLMBody

### GetOutputLinkList

```
ITrackLMAssembly.GetOutputLinkList()
```

TrackLM assembly output list

### RemoveAllOutputLink

```
ITrackLMAssembly.RemoveAllOutputLink()
```

Remove all the link body from output list

### RemoveOutputLink

```
ITrackLMAssembly.RemoveOutputLink(strFileName)
```

Remove a link body from output list

### UpdateLinkInitialVelocity

```
ITrackLMAssembly.UpdateLinkInitialVelocity()
```

Update initial velocity of links

### classITrackLMAssembly

```
classITrackLMAssembly(oobj=None)
```

Bases:DispatchBaseClassTrackLM AssemblyPropertiesBushingForceCollectionBushing force collectionBushingForceParameterBushing force parameterCommentCommentContactParameterContact ground track link shoeFullNameFullName such asBody1.Marker1@Model1GrouserContactCollectionGrouser contact collectionGrouserContactPropertyGrouser contact propertyGrouserToSphereContactGrouser to sphere contact PropertyLinkInitialVelocityXAxisLink initial velocity x-axisLinkNumbersLink numbersNameNameOwnerOwner returns own

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

Add a passing body with ITrackLMBody

### CreateGrouserContact

```
CreateGrouserContact()
```

Create a grouser contact

### DeleteGrouserContact

```
DeleteGrouserContact()
```

Delete a grouser contact

### DeletePassingBody

```
DeletePassingBody()
```

Delete a passing body

### DeletePassingBody2

```
DeletePassingBody2()
```

Delete a passing body with ITrackLMBody

### GetOutputLinkList

```
GetOutputLinkList()
```

TrackLM assembly output list

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
ITrackLMAssemblyBushingForceParameter.Export(strName,val)
```

Export bushing force parameter

### Import

```
ITrackLMAssemblyBushingForceParameter.Import(strName)
```

Import bushing force parameter

### classITrackLMAssemblyBushingForceParameter

```
classITrackLMAssemblyBushingForceParameter(oobj=None)
```

Bases:DispatchBaseClassTrackLM Assembly Bushing Force ParameterPropertiesRotationDampingCoefficientXRotation damping coefficient XRotationDampingCoefficientYRotation damping coefficient YRotationDampingCoefficientZRotation damping coefficient ZRotationDampingExponentXRotation damping exponent XRotationDampingExponentYRotation damping exponent YRotationDampingExponentZRotation damping exponent ZRotationDampingSplineXRotation damping spline XRotationDampingSplineYRotation damping spline YRotationD

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
ITrackLMAssemblyCollection.Item(var)
```

Returns a specific item.

### classITrackLMAssemblyCollection

```
classITrackLMAssemblyCollection(oobj=None)
```

Bases:DispatchBaseClassTrackLM Assembly CollectionPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### Item

```
Item()
```

Returns a specific item.

### Export

```
ITrackLMAssemblyContactGroundTrackLinkShoe.Export(strName,val)
```

Export ground parameter

### Import

```
ITrackLMAssemblyContactGroundTrackLinkShoe.Import(strName)
```

Import ground parameter

### SoftGroundType

```
ITrackLMAssemblyContactGroundTrackLinkShoe.SoftGroundType(val)
```

Soft ground type

### classITrackLMAssemblyContactGroundTrackLinkShoe

```
classITrackLMAssemblyContactGroundTrackLinkShoe(oobj=None)
```

Bases:DispatchBaseClassTrackLM Assembly Contact Ground TrackLink ShoePropertiesCohesionCohesion (c)DampingCoefficientThe viscous damping coefficient for the contact normal force.DampingExponentThe damping exponent for a non-linear contact normal forceDampingSplineDamping splineExponentialNumberExponential number (n)FrictionFrictionFrictionCoefficientThe friction coefficient for the contact normal force.FrictionSplineThe spline which shows relative velocity to the friction coefficient or the fric

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

### classITrackLMAssemblyGrouserContact

```
classITrackLMAssemblyGrouserContact(oobj=None)
```

Bases:DispatchBaseClassTrackLM Assembly Grouser ContactPropertiesActionPositionAction positionActionRadiusAction radiusBasePositionBase positionBaseRadiusBase radiusDistanceBetweenLinksDistance between Links

### Item

```
ITrackLMAssemblyGrouserContactCollection.Item(var)
```

Returns a specific item.

### classITrackLMAssemblyGrouserContactCollection

```
classITrackLMAssemblyGrouserContactCollection(oobj=None)
```

Bases:DispatchBaseClassTrackLM Assembly Grouser Contact CollectionPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### Item

```
Item()
```

Returns a specific item.

### AddGrouserToSphereContact

```
ITrackLMAssemblyGrouserToSphereContact.AddGrouserToSphereContact(pGeometrySphere)
```

Add a grouser to sphere contact

### classITrackLMAssemblyGrouserToSphereContact

```
classITrackLMAssemblyGrouserToSphereContact(oobj=None)
```

Bases:DispatchBaseClassTrackLM grouser to sphere contact propertyPropertiesContactPropertyGrouser to sphere contact propertyGeometrySphereCollectionSphere geometry collection of grouser to sphere contactMaximumPenetrationMaximum penetration.MethodsAddGrouserToSphereContactAdd a grouser to sphere contact

