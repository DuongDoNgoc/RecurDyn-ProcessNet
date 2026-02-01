# ProcessNet.TrackLM

> ProcessNet.TrackLM API

## Overview

**Full Name:** FunctionBay.RecurDyn.ProcessNet.TrackLM

**Methods:** 99

**Examples:** 0

## Methods

### classContactParameterSoftGroundType

```
classContactParameterSoftGroundType(value)¶
```

Bases:IntEnumContactParameterSoftGroundType enumeration.MembersContactParameterSoftGroundType_Clayey_SoilConstant value is 4.ContactParameterSoftGroundType_Dry_SandConstant value is 0.ContactParameterSoftGroundType_Grenville_LoamConstant value is 11.ContactParameterSoftGroundType_Heavy_ClayConstant value is 5.ContactParameterSoftGroundType_LETE_SandConstant value is 7.ContactParameterSoftGroundType_Lean_ClayConstant value is 6.ContactParameterSoftGroundType_North_Gower_Clayey_LoamConstant value 

### classContactSearchType

```
classContactSearchType(value)¶
```

Bases:IntEnumContactSearchType enumeration.MembersContactSearchType_FullSearchConstant value is 0.ContactSearchType_PartialSearchConstant value is 1.

### classContactSprocketType

```
classContactSprocketType(value)¶
```

Bases:IntEnumContactSprocketType enumeration.MembersContactSprocketType_LeftPinConstant value is 0.ContactSprocketType_RightPinConstant value is 1.

### classIPassingBodyCollection

```
classIPassingBodyCollection(oobj=None)¶
```

Bases:DispatchBaseClassTrackLM passing body collection of assembly

### AddAllOutputLink

```
ITrackLMAssembly.AddAllOutputLink()¶
```

Add all the link body to output list

### AddOutputLink

```
ITrackLMAssembly.AddOutputLink(strFileName)¶
```

Add a link body to output list

### AddPassingBody

```
ITrackLMAssembly.AddPassingBody(pVal)¶
```

Add a passing body

### AddPassingBody2

```
ITrackLMAssembly.AddPassingBody2(pVal)¶
```

Add a passing body with ITrackLMBody

### CreateGrouserContact

```
ITrackLMAssembly.CreateGrouserContact()¶
```

Create a grouser contact

### DeleteGrouserContact

```
ITrackLMAssembly.DeleteGrouserContact(pVal)¶
```

Delete a grouser contact

### DeletePassingBody

```
ITrackLMAssembly.DeletePassingBody(pVal)¶
```

Delete a passing body

### DeletePassingBody2

```
ITrackLMAssembly.DeletePassingBody2(pVal)¶
```

Delete a passing body with ITrackLMBody

### GetOutputLinkList

```
ITrackLMAssembly.GetOutputLinkList()¶
```

TrackLM assembly output list

### RemoveAllOutputLink

```
ITrackLMAssembly.RemoveAllOutputLink()¶
```

Remove all the link body from output list

### RemoveOutputLink

```
ITrackLMAssembly.RemoveOutputLink(strFileName)¶
```

Remove a link body from output list

### UpdateLinkInitialVelocity

```
ITrackLMAssembly.UpdateLinkInitialVelocity()¶
```

Update initial velocity of links

### classITrackLMAssembly

```
classITrackLMAssembly(oobj=None)¶
```

Bases:DispatchBaseClassTrackLM AssemblyPropertiesBushingForceCollectionBushing force collectionBushingForceParameterBushing force parameterCommentCommentContactParameterContact ground track link shoeFullNameFullName such asBody1.Marker1@Model1GrouserContactCollectionGrouser contact collectionGrouserContactPropertyGrouser contact propertyGrouserToSphereContactGrouser to sphere contact PropertyLinkInitialVelocityXAxisLink initial velocity x-axisLinkNumbersLink numbersNameNameOwnerOwner returns own

### Export

```
ITrackLMAssemblyBushingForceParameter.Export(strName,val)¶
```

Export bushing force parameter

### Import

```
ITrackLMAssemblyBushingForceParameter.Import(strName)¶
```

Import bushing force parameter

### classITrackLMAssemblyBushingForceParameter

```
classITrackLMAssemblyBushingForceParameter(oobj=None)¶
```

Bases:DispatchBaseClassTrackLM Assembly Bushing Force ParameterPropertiesRotationDampingCoefficientXRotation damping coefficient XRotationDampingCoefficientYRotation damping coefficient YRotationDampingCoefficientZRotation damping coefficient ZRotationDampingExponentXRotation damping exponent XRotationDampingExponentYRotation damping exponent YRotationDampingExponentZRotation damping exponent ZRotationDampingSplineXRotation damping spline XRotationDampingSplineYRotation damping spline YRotationD

### Item

```
ITrackLMAssemblyCollection.Item(var)¶
```

Returns a specific item.

### classITrackLMAssemblyCollection

```
classITrackLMAssemblyCollection(oobj=None)¶
```

Bases:DispatchBaseClassTrackLM Assembly CollectionPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### Export

```
ITrackLMAssemblyContactGroundTrackLinkShoe.Export(strName,val)¶
```

Export ground parameter

### Import

```
ITrackLMAssemblyContactGroundTrackLinkShoe.Import(strName)¶
```

Import ground parameter

### SoftGroundType

```
ITrackLMAssemblyContactGroundTrackLinkShoe.SoftGroundType(val)¶
```

Soft ground type

### classITrackLMAssemblyContactGroundTrackLinkShoe

```
classITrackLMAssemblyContactGroundTrackLinkShoe(oobj=None)¶
```

Bases:DispatchBaseClassTrackLM Assembly Contact Ground TrackLink ShoePropertiesCohesionCohesion (c)DampingCoefficientThe viscous damping coefficient for the contact normal force.DampingExponentThe damping exponent for a non-linear contact normal forceDampingSplineDamping splineExponentialNumberExponential number (n)FrictionFrictionFrictionCoefficientThe friction coefficient for the contact normal force.FrictionSplineThe spline which shows relative velocity to the friction coefficient or the fric

### classITrackLMAssemblyGrouserContact

```
classITrackLMAssemblyGrouserContact(oobj=None)¶
```

Bases:DispatchBaseClassTrackLM Assembly Grouser ContactPropertiesActionPositionAction positionActionRadiusAction radiusBasePositionBase positionBaseRadiusBase radiusDistanceBetweenLinksDistance between Links

### Item

```
ITrackLMAssemblyGrouserContactCollection.Item(var)¶
```

Returns a specific item.

### classITrackLMAssemblyGrouserContactCollection

```
classITrackLMAssemblyGrouserContactCollection(oobj=None)¶
```

Bases:DispatchBaseClassTrackLM Assembly Grouser Contact CollectionPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### AddGrouserToSphereContact

```
ITrackLMAssemblyGrouserToSphereContact.AddGrouserToSphereContact(pGeometrySphere)¶
```

Add a grouser to sphere contact

### classITrackLMAssemblyGrouserToSphereContact

```
classITrackLMAssemblyGrouserToSphereContact(oobj=None)¶
```

Bases:DispatchBaseClassTrackLM grouser to sphere contact propertyPropertiesContactPropertyGrouser to sphere contact propertyGeometrySphereCollectionSphere geometry collection of grouser to sphere contactMaximumPenetrationMaximum penetration.MethodsAddGrouserToSphereContactAdd a grouser to sphere contact

### classITrackLMBody

```
classITrackLMBody(oobj=None)¶
```

Bases:DispatchBaseClassTrackLM bodyPropertiesCommentCommentFullNameFullName such asBody1.Marker1@Model1GeneralBodyGeneralBodyNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceUserDataUser supplied data

### Item

```
ITrackLMBodyCollection.Item(var)¶
```

Returns a specific item.

### classITrackLMBodyCollection

```
classITrackLMBodyCollection(oobj=None)¶
```

Bases:DispatchBaseClassTrackLM roller guard body collectionPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### classITrackLMBodyFlangeCenter

```
classITrackLMBodyFlangeCenter(oobj=None)¶
```

Bases:DispatchBaseClassTrackLM flange centerPropertiesCommentCommentContactPropertyContact PropertyContactSearchContactSearchTypeFullNameFullName such asBody1.Marker1@Model1GeneralBodyGeneralBodyGeometryGeometryNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceUserDataUser supplied data

### classITrackLMBodyFlangeDouble

```
classITrackLMBodyFlangeDouble(oobj=None)¶
```

Bases:DispatchBaseClassTrackLM flange doublePropertiesCommentCommentContactPropertyContact PropertyContactSearchContactSearchTypeFullNameFullName such asBody1.Marker1@Model1GeneralBodyGeneralBodyGeometryGeometryNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceUserDataUser supplied data

### classITrackLMBodyFlangeFlat

```
classITrackLMBodyFlangeFlat(oobj=None)¶
```

Bases:DispatchBaseClassTrackLM flange flatPropertiesCommentCommentContactPropertyContact PropertyContactSearchContactSearchTypeFullNameFullName such asBody1.Marker1@Model1GeneralBodyGeneralBodyGeometryGeometryNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceUserDataUser supplied data

### classITrackLMBodyFlangeSingle

```
classITrackLMBodyFlangeSingle(oobj=None)¶
```

Bases:DispatchBaseClassTrackLM flange singlePropertiesCommentCommentContactPropertyContact PropertyContactSearchContactSearchTypeFullNameFullName such asBody1.Marker1@Model1GeneralBodyGeneralBodyGeometryGeometryNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceUserDataUser supplied data

### CreateMarker

```
ITrackLMBodyLink.CreateMarker(strName,pRefFrame)¶
```

Creates a marker

### UpdateGeometry

```
ITrackLMBodyLink.UpdateGeometry()¶
```

Update geometry

### classITrackLMBodyLink

```
classITrackLMBodyLink(oobj=None)¶
```

Bases:DispatchBaseClassTrackLM Body LinkPropertiesCommentCommentFullNameFullName such asBody1.Marker1@Model1GeneralBodyGeneralBodyGeometryGeometryGraphicGraphicLinkGrouserProfileLink grouser profileLinkShapeProfileLink shape profileNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceUseBodyGraphicUse graphic of clone boyUseLinkShapeUse link sha

### Item

```
ITrackLMBodyLinkCollection.Item(var)¶
```

Returns a specific item.

### classITrackLMBodyLinkCollection

```
classITrackLMBodyLinkCollection(oobj=None)¶
```

Bases:DispatchBaseClassTrackLM Body Link CollectionPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### classITrackLMBodyRollerGuard

```
classITrackLMBodyRollerGuard(oobj=None)¶
```

Bases:DispatchBaseClassTrackLM Body Roller GuardPropertiesCommentCommentContactPropertyContact PropertyContactSearchContactSearchTypeFullNameFullName such asBody1.Marker1@Model1GeneralBodyGeneralBodyGeometryGeometryNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceUserDataUser supplied data

### UpdateProperties

```
ITrackLMBodySprocket.UpdateProperties()¶
```

Update Properties

### classITrackLMBodySprocket

```
classITrackLMBodySprocket(oobj=None)¶
```

Bases:DispatchBaseClassTrackLMBodySprocketPropertiesCommentCommentContactPropertyContact PropertyContactSearchContactSearchTypeCreateContactOutputFileCreate contact output fileFullNameFullName such asBody1.Marker1@Model1GeneralBodyGeneralBodyGeometryGeometryNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceToothProfileToothProfileUserDataUser

### classITrackLMContactFriction

```
classITrackLMContactFriction(oobj=None)¶
```

Bases:DispatchBaseClassTrackLM contact frictionPropertiesDynamicThresholdVelocityDynamic threshold velocityStaticFrictionCoefficientStatic friction coefficientStaticThresholdVelocityStatic threshold velocity

### classITrackLMContactProperty

```
classITrackLMContactProperty(oobj=None)¶
```

Bases:DispatchBaseClassTrackLM contact propertyPropertiesDampingCoefficientThe viscous damping coefficient for the contact normal force.DampingExponentThe damping exponent for a non-linear contact normal forceDampingSplineDamping splineFrictionFrictionFrictionCoefficientThe friction coefficient for the contact normal force.FrictionSplineThe spline which shows relative velocity to the friction coefficient or the friction force.FrictionTypeFriction typeIndentationExponentThe indentation exponent y

### classITrackLMContactSearch

```
classITrackLMContactSearch(oobj=None)¶
```

Bases:DispatchBaseClassTrackLM flange contact searchPropertiesTypeSearch type of the flange.UseUserBoundaryForPartialSearchUse the user boundary of the partial search.UserBoundaryForPartialSearchUser boundary of the partial search.

### classITrackLMGeometryFlangeCenter

```
classITrackLMGeometryFlangeCenter(oobj=None)¶
```

Bases:DispatchBaseClassTrackLM flange center geometryPropertiesInnerFlangeRadiusInner flange radius.InnerFlangeWidthInner flange width.TotalWidthTotal width.WheelRadiusWheel radius.

