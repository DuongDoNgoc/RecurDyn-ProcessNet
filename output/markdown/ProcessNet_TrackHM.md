# ProcessNet.TrackHM

> ProcessNet.TrackHM API

## Overview

**Full Name:** FunctionBay.RecurDyn.ProcessNet.TrackHM

**Methods:** 55

**Examples:** 0

## Methods

### AddAllOutputLink

```
ITrackHMAssembly.AddAllOutputLink()¶
```

Add all the link body to output list

### AddOutputLink

```
ITrackHMAssembly.AddOutputLink(strFileName)¶
```

Add a link body to output list

### AddPassingBody

```
ITrackHMAssembly.AddPassingBody(pVal)¶
```

Add a passing body

### AddPassingBody2

```
ITrackHMAssembly.AddPassingBody2(pVal)¶
```

Add a passing body with ITrackHMBody

### DeletePassingBody

```
ITrackHMAssembly.DeletePassingBody(pVal)¶
```

Delete a passing body

### DeletePassingBody2

```
ITrackHMAssembly.DeletePassingBody2(pVal)¶
```

Delete a passing body with ITrackHMBody

### GetOutputLinkList

```
ITrackHMAssembly.GetOutputLinkList()¶
```

TrackHM assembly output list

### RemoveAllOutputLink

```
ITrackHMAssembly.RemoveAllOutputLink()¶
```

Remove all the link body from output list

### RemoveOutputLink

```
ITrackHMAssembly.RemoveOutputLink(strFileName)¶
```

Remove a link body from output list

### UpdateLinkInitialVelocity

```
ITrackHMAssembly.UpdateLinkInitialVelocity()¶
```

Update initial velocity of links

### classITrackHMAssembly

```
classITrackHMAssembly(oobj=None)¶
```

Bases:DispatchBaseClassTrackHM AssemblyPropertiesBushingForceCollectionBushing force collectionBushingForceParameterBushing force parameterCommentCommentContactParameterContact ground track link shoeFullNameFullName such asBody1.Marker1@Model1LinkInitialVelocityReferenceFramelink initialvelocity Reference FrameLinkInitialVelocityXAxisLink initial velocity x-axisLinkNumbersLink numbersNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody retu

### Export

```
ITrackHMAssemblyBushingForceParameter.Export(strName,val)¶
```

Export bushing force parameter

### Import

```
ITrackHMAssemblyBushingForceParameter.Import(strName)¶
```

Import bushing force parameter

### classITrackHMAssemblyBushingForceParameter

```
classITrackHMAssemblyBushingForceParameter(oobj=None)¶
```

Bases:DispatchBaseClassTrackHM Assembly Bushing Force ParameterPropertiesRotationDampingCoefficientXRotation damping coefficient XRotationDampingCoefficientYRotation damping coefficient YRotationDampingCoefficientZRotation damping coefficient ZRotationDampingExponentXRotation damping exponent XRotationDampingExponentYRotation damping exponent YRotationDampingExponentZRotation damping exponent ZRotationDampingSplineXRotation damping spline XRotationDampingSplineYRotation damping spline YRotationD

### Item

```
ITrackHMAssemblyCollection.Item(var)¶
```

Returns a specific item.

### classITrackHMAssemblyCollection

```
classITrackHMAssemblyCollection(oobj=None)¶
```

Bases:DispatchBaseClassTrackHM Assembly CollectionPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### Export

```
ITrackHMAssemblyContactGroundTrackLinkShoePad.Export(strName,val)¶
```

Export ground parameter

### Import

```
ITrackHMAssemblyContactGroundTrackLinkShoePad.Import(strName)¶
```

Import ground parameter

### SoftGroundType

```
ITrackHMAssemblyContactGroundTrackLinkShoePad.SoftGroundType(val)¶
```

Soft ground type

### classITrackHMAssemblyContactGroundTrackLinkShoePad

```
classITrackHMAssemblyContactGroundTrackLinkShoePad(oobj=None)¶
```

Bases:DispatchBaseClassTrackHM Assembly Contact Ground TrackLink Shoe PadPropertiesCohesionCohesion (c)DampingCoefficientThe viscous damping coefficient for the contact normal force.DampingExponentThe damping exponent for a non-linear contact normal forceDampingSplineDamping splineExponentialNumberExponential number (n)FrictionFrictionFrictionCoefficientThe friction coefficient for the contact normal force.FrictionSplineThe spline which shows relative velocity to the friction coefficient or the 

### classITrackHMAssemblySphereContact

```
classITrackHMAssemblySphereContact(oobj=None)¶
```

Bases:DispatchBaseClassTrackHM sphere contact propertyPropertiesContactPropertySphere contact propertyGeometrySphereCollectionSphere geometry collection of the sphere contactMaximumPenetrationMaximum penetration.MethodsAddSphereContactAdd a sphere contact

### classITrackHMBody

```
classITrackHMBody(oobj=None)¶
```

Bases:DispatchBaseClassTrackHM bodyPropertiesCommentCommentFullNameFullName such asBody1.Marker1@Model1GeneralBodyGeneralBodyNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceUserDataUser supplied data

### classITrackHMBodyCollection

```
classITrackHMBodyCollection(oobj=None)¶
```

Bases:DispatchBaseClassTrackHM wheel body collectionPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### classITrackHMBodyLink

```
classITrackHMBodyLink(oobj=None)¶
```

Bases:DispatchBaseClassTrackHM body linkPropertiesActiveDoubleShoePadDouble shoe padActiveShoePadActive shoe padCommentCommentDoubleShoePadFirstDouble shoe pad first profileDoubleShoePadSecondDouble shoe pad second profileFullNameFullName such asBody1.Marker1@Model1GeneralBodyGeneralBodyGraphicGraphicMeshSegmentMesh segmentNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns

### classITrackHMBodyLinkCollection

```
classITrackHMBodyLinkCollection(oobj=None)¶
```

Bases:DispatchBaseClassTrackHM Body Link CollectionPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### classITrackHMBodyLinkDouble

```
classITrackHMBodyLinkDouble(oobj=None)¶
```

Bases:DispatchBaseClassTrackHM double link bodyPropertiesActiveDoubleShoePadDouble shoe padActiveShoePadActive shoe padCommentCommentDoubleShoePadFirstDouble shoe pad first profileDoubleShoePadSecondDouble shoe pad second profileFullNameFullName such asBody1.Marker1@Model1GeneralBodyGeneralBodyGeometryGeometryGraphicGraphicMeshSegmentMesh segmentNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSyste

### classITrackHMBodyLinkInner

```
classITrackHMBodyLinkInner(oobj=None)¶
```

Bases:DispatchBaseClassTrackHM inner link bodyPropertiesActiveDoubleShoePadDouble shoe padActiveShoePadActive shoe padCommentCommentDoubleShoePadFirstDouble shoe pad first profileDoubleShoePadSecondDouble shoe pad second profileFullNameFullName such asBody1.Marker1@Model1GeneralBodyGeneralBodyGeometryGeometryGraphicGraphicMeshSegmentMesh segmentNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystem

### classITrackHMBodyLinkSingle

```
classITrackHMBodyLinkSingle(oobj=None)¶
```

Bases:DispatchBaseClassTrackHM single link bodyPropertiesActiveDoubleShoePadDouble shoe padActiveShoePadActive shoe padCommentCommentDoubleShoePadFirstDouble shoe pad first profileDoubleShoePadSecondDouble shoe pad second profileFullNameFullName such asBody1.Marker1@Model1GeneralBodyGeneralBodyGeometryGeometryGraphicGraphicMeshSegmentMesh segmentNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSyste

### classITrackHMBodySprocket

```
classITrackHMBodySprocket(oobj=None)¶
```

Bases:DispatchBaseClassTrackHMBodySprocketPropertiesCommentCommentContactPropertyContact PropertyContactSearchContactSearchTypeCreateContactOutputFileCreate contact output fileFullNameFullName such asBody1.Marker1@Model1GeneralBodyGeneralBodyGeometryGeometryNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceToothProfileToothProfileUserDataUser

### classITrackHMBodyWheelDouble

```
classITrackHMBodyWheelDouble(oobj=None)¶
```

Bases:DispatchBaseClassTrackHM Wheel doublePropertiesCommentCommentContactCenterPropertyCenter Contact PropertyContactPropertyContact PropertyContactSearchContactSearchTypeFullNameFullName such asBody1.Marker1@Model1GeneralBodyGeneralBodyGeometryGeometryNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceUserDataUser supplied data

### classITrackHMBodyWheelSingle

```
classITrackHMBodyWheelSingle(oobj=None)¶
```

Bases:DispatchBaseClassTrackHM wheel singlePropertiesCommentCommentContactPropertyContact PropertyContactSearchContactSearchTypeFullNameFullName such asBody1.Marker1@Model1GeneralBodyGeneralBodyGeometryGeometryNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceUserDataUser supplied data

### classITrackHMContactFriction

```
classITrackHMContactFriction(oobj=None)¶
```

Bases:DispatchBaseClassTrackHM contact frictionPropertiesDynamicThresholdVelocityDynamic threshold velocityStaticFrictionCoefficientStatic friction coefficientStaticThresholdVelocityStatic threshold velocity

### classITrackHMContactProperty

```
classITrackHMContactProperty(oobj=None)¶
```

Bases:DispatchBaseClassTrackHM contact propertyPropertiesDampingCoefficientThe viscous damping coefficient for the contact normal force.DampingExponentThe damping exponent for a non-linear contact normal forceDampingSplineDamping splineFrictionFrictionFrictionCoefficientThe friction coefficient for the contact normal force.FrictionSplineThe spline which shows relative velocity to the friction coefficient or the friction force.FrictionTypeFriction typeIndentationExponentThe indentation exponent y

### classITrackHMContactSearch

```
classITrackHMContactSearch(oobj=None)¶
```

Bases:DispatchBaseClassTrackHM contact searchPropertiesTypeSearch typeUseUserBoundaryForPartialSearchUse the user boundary of the partial search.UserBoundaryForPartialSearchUser boundary of the partial search.

### classITrackHMGeometryLinkDouble

```
classITrackHMGeometryLinkDouble(oobj=None)¶
```

Bases:DispatchBaseClassTrackHM double link geometryPropertiesCenterGuideLengthCenter guide lengthCenterGuidePositionCenter guide positionCenterGuideThicknessCenter guide thicknessEndConnectorLengthEnd connector LengthLeftLengthLeft lengthLeftPinPositionLeft pin positionLowerHeightLower heightPinLengthPin lengthPinRadiusPin radiusRightLengthRight lengthRightPinPositionRight pin positionUpperHeightUpper heightWidthWidth

### classITrackHMGeometryLinkInner

```
classITrackHMGeometryLinkInner(oobj=None)¶
```

Bases:DispatchBaseClassTrackHM inner link geometryPropertiesCenterGuideLengthCenter guide lengthCenterGuidePositionCenter guide positionCenterGuideThicknessCenter guide thicknessContactRadiusContact radiusEndConnectorLengthEnd connector lengthInnerWidthInner widthLeftContactCylinderPositionLeft contact cylinder positionLeftLengthLeft lengthLeftPinPositionLeft pin positionLinkWidthLink widthLowerHeightLower heightOuterWidthOuter widthPinLengthPin lengthPinRadiusPin radiusRightContactCylinderPosit

### classITrackHMGeometryLinkSingle

```
classITrackHMGeometryLinkSingle(oobj=None)¶
```

Bases:DispatchBaseClassTrackHM single link geometryPropertiesBushingWidthBushing WidthCenterGuideLengthCenter guide lengthCenterGuidePositionCenter guide positionCenterGuideThicknessCenter guide thicknessConnectorLengthConnector LengthLeftBushingPositionLeft bushing positionLeftLengthLeft lengthLeftPinPositionLeft pin positionLowerHeightLower heightPinLengthPin lengthPinRadiusPin radiusRightBushingPositionRight bushing positionRightLengthRight lengthRightPinPositionRight pin positionUpperHeightU

### classITrackHMGeometrySprocket

```
classITrackHMGeometrySprocket(oobj=None)¶
```

Bases:DispatchBaseClassTrackHMBodySprocketGeometryPropertiesAddendumCircleRadiusAddendum circle radius of the sprocket.BaseCircleRadiusBase circle radius of the sprocket.DedendumCircleRadiusDedendum circle radius of the sprocket.LinkAssemblyAssembledRadiusAssembled radius of the link assembly.LinkAssemblyRadialDistanceAssembled distance of the link assembly.NumberOfTeethNumber of teeth of the sprocket.PitchCircleRadiusPitch circle radius of the sprocket.SprocketCarrierRadiusCarrier Radius of the

### classITrackHMGeometryWheelDouble

```
classITrackHMGeometryWheelDouble(oobj=None)¶
```

Bases:DispatchBaseClassTrackHM Wheel double geometryPropertiesHubRadiusHub radiusHubWidthHub widthTotalWidthTotal widthWheelRadiusWheel radius

### classITrackHMGeometryWheelSingle

```
classITrackHMGeometryWheelSingle(oobj=None)¶
```

Bases:DispatchBaseClassTrackHM Wheel single geometryPropertiesWheelRadiusWheel Radius.WheelWidthWheel Width.

### classITrackHMLinkClone

```
classITrackHMLinkClone(oobj=None)¶
```

Bases:DispatchBaseClassTrackHM link clonePropertiesActiveActiveActiveDoubleShoePadDouble shoe padActiveShoePadActive shoe padCenterMarkerCenter markerCommentCommentDensityDensityDoubleShoePadFirstDouble shoe pad first profileDoubleShoePadSecondDouble shoe pad second profileFullNameFullName such asBody1.Marker1@Model1GraphicGraphicIxxIxxIxyIxyIyyIyyIyzIyzIzxIzxIzzIzzMassMassMaterialMaterialMaterialInputMaterial inputMaterialUserUser MaterialMeshSegmentMesh segmentNameNameOwnerOwner returns owning

### classITrackHMLinkCloneCollection

```
classITrackHMLinkCloneCollection(oobj=None)¶
```

Bases:DispatchBaseClassTrackHM clone link collectionPropertiesCountReturns the number of items in the collection.MethodsItemReturns a specific item.

### classITrackHMLinkCloneDouble

```
classITrackHMLinkCloneDouble(oobj=None)¶
```

Bases:DispatchBaseClassTrackHM double link clonePropertiesActiveActiveActiveDoubleShoePadDouble shoe padActiveShoePadActive shoe padCenterMarkerCenter markerCommentCommentDensityDensityDoubleShoePadFirstDouble shoe pad first profileDoubleShoePadSecondDouble shoe pad second profileFullNameFullName such asBody1.Marker1@Model1GeometryGeometryGraphicGraphicIxxIxxIxyIxyIyyIyyIyzIyzIzxIzxIzzIzzMassMassMaterialMaterialMaterialInputMaterial inputMaterialUserUser MaterialMeshSegmentMesh segmentNameNameOw

### classITrackHMLinkCloneInner

```
classITrackHMLinkCloneInner(oobj=None)¶
```

Bases:DispatchBaseClassTrackHM inner link clonePropertiesActiveActiveActiveDoubleShoePadDouble shoe padActiveShoePadActive shoe padCenterMarkerCenter markerCommentCommentDensityDensityDoubleShoePadFirstDouble shoe pad first profileDoubleShoePadSecondDouble shoe pad second profileFullNameFullName such asBody1.Marker1@Model1GeometryGeometryGraphicGraphicIxxIxxIxyIxyIyyIyyIyzIyzIzxIzxIzzIzzMassMassMaterialMaterialMaterialInputMaterial inputMaterialUserUser MaterialMeshSegmentMesh segmentNameNameOwn

### classITrackHMLinkCloneSingle

```
classITrackHMLinkCloneSingle(oobj=None)¶
```

Bases:DispatchBaseClassTrackHM single link clonePropertiesActiveActiveActiveDoubleShoePadDouble shoe padActiveShoePadActive shoe padCenterMarkerCenter markerCommentCommentDensityDensityDoubleShoePadFirstDouble shoe pad first profileDoubleShoePadSecondDouble shoe pad second profileFullNameFullName such asBody1.Marker1@Model1GeometryGeometryGraphicGraphicIxxIxxIxyIxyIyyIyyIyzIyzIzxIzxIzzIzzMassMassMaterialMaterialMaterialInputMaterial inputMaterialUserUser MaterialMeshSegmentMesh segmentNameNameOw

### classITrackHMMeshSegment

```
classITrackHMMeshSegment(oobj=None)¶
```

Bases:DispatchBaseClassTrackHM mesh segmentPropertiesShoePadMeshHeightSegmentShoe pad height mesh segmentShoePadMeshLengthSegmentShoe pad length mesh segmentShoePadMeshWidthSegmentShoe pad width mesh segment

### classITrackHMProfileShoePoint

```
classITrackHMProfileShoePoint(oobj=None)¶
```

Bases:DispatchBaseClassTrackHM link clonePropertiesPoint3DCollection3D Point CollectionMethodsExportExport shoe pointImportImport shoe point

### classITrackHMShoePad

```
classITrackHMShoePad(oobj=None)¶
```

Bases:DispatchBaseClassTrackHM link clonePropertiesFirstPointFirst positionSecondPointSecond position

### classITrackHMSphereContactProperty

```
classITrackHMSphereContactProperty(oobj=None)¶
```

Bases:DispatchBaseClassTrackHM sphere contact propertyPropertiesDampingCoefficientThe viscous damping coefficient for the contact normal force.DampingExponentThe damping exponent for a non-linear contact normal forceDampingSplineDamping splineFrictionCoefficientThe friction coefficient for the contact normal force.FrictionSplineThe spline which shows relative velocity to the friction coefficient or the friction force.FrictionTypeFriction typeIndentationExponentThe indentation exponent yields an 

### classITrackHMSubSystem

```
classITrackHMSubSystem(oobj=None)¶
```

Bases:DispatchBaseClassTrackHM subsystemPropertiesAssemblyCollectionGet the collection of assemblyCommentCommentFullNameFullName such asBody1.Marker1@Model1GeneralSubSystemGeneral subsystemLinkCloneCollectionGet the collection of clonesNameNameOwnerOwner returns owning IGeneric interface, use Owner for IRFlexBody, IFFlexBodyOwnerBodyOwnerBody returns owning IBody interfaceOwnerSubSystemOwnerSubSystem returns owning ISubSubSystem interfaceTrackHMBodyCollectionGet the TrackHM body collection of as

