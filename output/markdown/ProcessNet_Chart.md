# ProcessNet.Chart

> ProcessNet.Chart API

## Overview

**Full Name:** FunctionBay.RecurDyn.ProcessNet.Chart

**Methods:** 88

**Examples:** 0

## Methods

### classAxisAngleType

```
classAxisAngleType(value)
```

Bases:IntEnumAxisAngleType enumeration.MembersAxisAngleType_45DegreesConstant value is 2.AxisAngleType_HorizontalConstant value is 0.AxisAngleType_VerticalConstant value is 1.

### classAxisPositionType

```
classAxisPositionType(value)
```

Bases:IntEnumAxisPositionType enumeration.MembersAxisPositionType_FarConstant value is 2.AxisPositionType_NearConstant value is 0.

### classDockedPositionType

```
classDockedPositionType(value)
```

Bases:IntEnumDockedPositionType enumeration.MembersDockedPositionType_BottomConstant value is 2.DockedPositionType_LeftConstant value is 1.DockedPositionType_RightConstant value is 3.DockedPositionType_TopConstant value is 0.

### classGalleryType

```
classGalleryType(value)
```

Bases:IntEnumGalleryType enumeration.MembersGalleryType_AreaConstant value is 3.GalleryType_BarConstant value is 2.GalleryType_ContourConstant value is 18.GalleryType_CurveConstant value is 6.GalleryType_CurveAreaConstant value is 19.GalleryType_LineConstant value is 1.GalleryType_ReservedConstant value is 0.GalleryType_ScatterConstant value is 4.GalleryType_StepConstant value is 8.GalleryType_SurfaceConstant value is 10.

### classIAxis

```
classIAxis(oobj=None)
```

Bases:DispatchBaseClassPropertiesAngleChange the angle of the axis labels.AutoScalealways recalculate the specified Axis scale values (Min, Max) when new values are set to the chart.GridAllows customization of grid lines by providing access to the supported members of the Grids.LabelsFormatUsed to format the labels displayed on the selected axis.LineAllows you to apply supported Line class members to a selected axis line.LogBaseUsed to set a logarithmic scale for a numerical axis and recalculate

### classIAxisX

```
classIAxisX(oobj=None)
```

Bases:DispatchBaseClassPropertiesAngleChange the angle of the axis labels.AutoScalealways recalculate the specified Axis scale values (Min, Max) when new values are set to the chart.GridAllows customization of grid lines by providing access to the supported members of the Grids.LabelsFormatUsed to format the labels displayed on the selected axis.LineAllows you to apply supported Line class members to a selected axis line.LogBaseUsed to set a logarithmic scale for a numerical axis and recalculate

### classIAxisY

```
classIAxisY(oobj=None)
```

Bases:DispatchBaseClassPropertiesAngleChange the angle of the axis labels.AutoScalealways recalculate the specified Axis scale values (Min, Max) when new values are set to the chart.GridAllows customization of grid lines by providing access to the supported members of the Grids.LabelsFormatUsed to format the labels displayed on the selected axis.LineAllows you to apply supported Line class members to a selected axis line.LogBaseUsed to set a logarithmic scale for a numerical axis and recalculate

### DeleteSeries

```
IChart.DeleteSeries(uiSeriesIndex)
```

Delete series with the index

### Get3D

```
IChart.Get3D()
```

Return the 3D setting of the chart.

### GetAddtionalYAxis

```
IChart.GetAddtionalYAxis()
```

Returns a additional y axis.

### GetAngleX

```
IChart.GetAngleX()
```

Return the degree of the view angle X

### GetAngleY

```
IChart.GetAngleY()
```

Return the degree of the view angle Y

### GetAxisY

```
IChart.GetAxisY(index)
```

Returns a indexed y axis.

### GetCluster

```
IChart.GetCluster()
```

Return cluster setting of the chart.

### GetLineStyle

```
IChart.GetLineStyle()
```

Get the Line Style of the Chart

### GetLineWidth

```
IChart.GetLineWidth()
```

Get the line width of chart

### GetPane

```
IChart.GetPane(index)
```

Returns a indexed pane.

### GetPlotDataWithSeriesIndex

```
IChart.GetPlotDataWithSeriesIndex(uiSeriesIndex)
```

Get plot data with sereis index

### GetPlotDataXWithSeriesIndex

```
IChart.GetPlotDataXWithSeriesIndex(uiSeriesIndex)
```

Get plot data X with sereis index

### GetSeries

```
IChart.GetSeries(index)
```

Returns a indexed series attribute.

### GetView3D

```
IChart.GetView3D()
```

Return the 3D View setting of the chart.

### GetView3DDepth

```
IChart.GetView3DDepth()
```

Get the depth of the series in 3D Chart

### GetVolume

```
IChart.GetVolume()
```

Get the gap between two series in 3D Chart

### Invalidate

```
IChart.Invalidate()
```

Invalidate method

### RecalculateScale

```
IChart.RecalculateScale()
```

calculate the Min, Max and Step for the axes. this method reads the entire data array, so abusing this method could affect the performance of your application

### Set3D

```
IChart.Set3D(Val)
```

Set 3D setting of the chart.

### SetAngleX

```
IChart.SetAngleX(Val)
```

Set the view angle X in degree

### SetAngleY

```
IChart.SetAngleY(Val)
```

Set the view angle Y in degree

### SetCluster

```
IChart.SetCluster(Val)
```

Set cluster of the chart.

### SetLineStyle

```
IChart.SetLineStyle(dashStyle)
```

Set the Line Style of the Chart

### SetLineWidth

```
IChart.SetLineWidth(lLineWidth)
```

Set the line width of chart

### SetVeiw3DDepth

```
IChart.SetVeiw3DDepth(uiDepth)
```

Set the depth of the series in 3D Chart

### SetView3D

```
IChart.SetView3D(Val)
```

Set 3D View setting of the chart.

### SetVolume

```
IChart.SetVolume(uiVolume)
```

Set the gap between two series in 3D Chart

### classIChart

```
classIChart(oobj=None)
```

Bases:DispatchBaseClassPropertiesAxisXAssigns properties specifically to the primary X axis.AxisYAssigns properties specifically to the primary Y axis of the chart.AxisY2Assigns properties specifically to the secondary Y axis of the chart.BackColorthe background color of the chart.BackgroundImagethe fulll path of background image.GalleryTypethe gallery type of the chart.InsideColorthe inside color of the chart.LegendBoxAllows you to acces the legend box of the chart.SeriesCountthe number of seri

### DeleteSeries

```
DeleteSeries()
```

Delete series with the index

### Get3D

```
Get3D()
```

Return the 3D setting of the chart.

### GetAddtionalYAxis

```
GetAddtionalYAxis()
```

Returns a additional y axis.

### GetAngleX

```
GetAngleX()
```

Return the degree of the view angle X

### GetAngleY

```
GetAngleY()
```

Return the degree of the view angle Y

### GetAxisY

```
GetAxisY()
```

Returns a indexed y axis.

### GetCluster

```
GetCluster()
```

Return cluster setting of the chart.

### GetLineStyle

```
GetLineStyle()
```

Get the Line Style of the Chart

### GetLineWidth

```
GetLineWidth()
```

Get the line width of chart

### GetPane

```
GetPane()
```

Returns a indexed pane.

### GetPlotDataWithSeriesIndex

```
GetPlotDataWithSeriesIndex()
```

Get plot data with sereis index

### GetPlotDataXWithSeriesIndex

```
GetPlotDataXWithSeriesIndex()
```

Get plot data X with sereis index

### GetSeries

```
GetSeries()
```

Returns a indexed series attribute.

### GetView3D

```
GetView3D()
```

Return the 3D View setting of the chart.

### GetView3DDepth

```
GetView3DDepth()
```

Get the depth of the series in 3D Chart

