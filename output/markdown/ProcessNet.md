# ProcessNet

> RecurDyn ProcessNet API for automation

## Overview

**Full Name:** FunctionBay.RecurDyn.ProcessNet

**Methods:** 0

**Examples:** 57

## Code Examples

### Example 1

```csharp
public void RegisterFunction ()
{
   IRibbonManager ribbonManager = application.RibbonManager;
   IRibbonTab ribbonTab = ribbonManager.FindRibbonTab("Customize");
   IRibbonGroup ribbonGroup = ribbonTab.AddRibbonGroup("PNet Example");

   //ID for user created processNet function must be between 8000 - 8999.
   IMenuControl menuControl = ribbonGroup.AddMenuControl(MenuControlType.MenuControlType_Button, 8001);

   // Set example control information.
   IntPtr iIcon = ProcessNet.Properties.Resources.example.GetHicon();
   menuControl.SetIcon(iIcon);
   menuControl.UseBigIcon = true;
   menuControl.Caption = "MyExample";
   menuControl.Tooltip = "MyTooltip";

   //menuControl.Description = "MyDescription";
   menuControl.UseProcessNetFunction = true; //if ID is not between 8000 - 8999, this can set ID to 8000

   // Get current ProcessNet dll fullpath. 'ProcessNetDllPath' must be absolute path.
   string assemblyname = System.Reflection.Assembly.GetExecutingAssembly().GetName().Name;
   string codeBase = System.Reflection.Assembly.GetExecutingAssembly().CodeBase;

   UriBuilder uri = new UriBuilder(codeBase);
   string ProcessNetDllPath = Uri.UnescapeDataString(uri.Path);

   menuControl.ProcessNetDllPath = ProcessNetDllPath;
   menuControl.ProcessNetFunctionName = "CreateBodyExample";
   menuControl.ProcessNetType = ProcessNetType.ProcessNetType_General;
}
```

*Source: RecurDynHelp/ProcessNet/ProcessNet_ch02_s07_00_index.html*

### Example 2

```csharp
def register_function():
   ribbonManager = application.RibbonManager
   ribbonTab = ribbonManager.FindRibbonTab("Customize")
   ribbonGroup = ribbonTab.AddRibbonGroup("PNet Example")

   menuControl = ribbonGroup.AddMenuControl(MenuControlType.MenuControlType_Button, 8011)
   menuControl.ProcessNetType = ProcessNetType.ProcessNetType_Python
   menuControl.Caption = "MyTooltip"
   menuControl.Tooltip = "PNet Example"
   menuControl.UseProcessNetFunction = True
   menuControl.UseBigIcon = True

   menuControl.SetIconFromFile("C:\\Examples\\example.ico", 16, 16) # Icon File Path
   menuControl.ProcessNetScriptPath = "C:\\Examples\\CreateBody.py" # Python Script Path

initialize()
register_function()
dispose
```

*Source: RecurDynHelp/ProcessNet/ProcessNet_ch03_s08_00_index.html*

### Example 3

```csharp
from recurdyn import *
from recurdyn.utils.rplt import RpltReader
from recurdyn import Chart

# Common Variables
app = None
application = None
model_document = None
plot_document = None
model = None

ref_frame_1 = None
ref_frame_2 = None

# Post Common Variable
post_main_document = None
post_main_window = None

# initialize() should be called before ProcessNet function call.
def initialize():
    global app
    global application
    global model_document
    global plot_document
    global model

    app = dispatch_recurdyn()
    application = IApplication(app.RecurDynApplication)
    model_document = application.ActiveModelDocument
    if model_document is not None:
        model_document = IModelDocument(model_document)
    plot_document = application.ActivePlotDocument
    if plot_document is not None:
        plot_document = IPlotDocument(plot_document)

    if model_document is None and plot_document is None:
        application.PrintMessage("No model file")
        model_document = application.NewModelDocument("Examples")
    if model_document is not None:
        model_document = IModelDocument(model_document)
        model = ISubSystem(model_document.Model)

    return application, model_document, plot_document, model


# dispose() should be called after ProcessNet function call.
def dispose():
    global application
    global model_document

    model_document = application.ActiveModelDocument
    if model_document is not None:
        model_document = IModelDocument(model_document)
    else:
        return

    if not model_document.Validate():
        return
    # Redraw() and UpdateDatabaseWindow() can take more time in a heavy model.
    model_document.Redraw()
    # model_document.PostProcess() # UpdateDatabaseWindow(), SetModified()
    model_document.UpdateDatabaseWindow()
    # If you call SetModified(), Animation will be reset.
    model_document.SetModified()
    model_document.SetUndoHistory("Python ProcessNet")


# Intialize global variable
ap
```

*Source: RecurDynHelp/ProcessNet/ProcessNet_ch03_s10_01.html*

### Example 4

```csharp
public void ProcessNetTutorialCreateSolidContact()
{
}
```

*Source: Tutorial/ProcessNet/General/4WDLoader/4WDLoader_General_English.html*

### Example 5

```csharp
public void ProcessNetTutorialCreateSolidContact()
{
    int BodyNumStart = 20;  // Start creating contacts with body 20
    int BodyNumEnd = 30;    // Continue until body 30
    int BodyInterval = 51;  // Interval between body number on hose 1
                            // and corresponding body's number on
                            // hose 2 is 51

    for (int i = BodyNumStart; i <= BodyNumEnd; i++)
    {
    }
}
```

*Source: Tutorial/ProcessNet/General/4WDLoader/4WDLoader_General_English.html*

### Example 6

```csharp
public void ProcessNetTutorialCreateSolidContact()
{
    int BodyNumStart = 20;  // Start creating contacts with body 20
    int BodyNumEnd = 30;    // Continue until body 30
    int BodyInterval = 51;  // Interval between body number on hose 1
                            // and corresponding body's number on
                            // hose 2 is 51

    for (int i = BodyNumStart; i <= BodyNumEnd; i++)
    {
        int j = i + BodyInterval;  // j is the index for the
                                   // corresponding bodies on hose #2
                                   // Do the contact for corresponding bodies

        IBody baseBody = model.GetEntity("BeamBody" + i.ToString()) as IBody;
        IGeometry baseGeom = baseBody.GetEntity("HollowCircularBeam1") as IGeometry;
        IBody actionBody = model.GetEntity("BeamBody" + j.ToString()) as IBody;
        IGeometry actionGeom= actionBody.GetEntity("HollowCircularBeam1") as IGeometry;
        IContactSolidContact solidContact= model.CreateContactSolidContact("solidContact" + i.ToString(), baseGeom, actionGeom);
    }
}
```

*Source: Tutorial/ProcessNet/General/4WDLoader/4WDLoader_General_English.html*

### Example 7

```csharp
IBody baseBody = model.GetEntity("BeamBody" + i.ToString()) as IBody;
```

*Source: Tutorial/ProcessNet/General/4WDLoader/4WDLoader_General_English.html*

### Example 8

```csharp
IGeometry baseGeom = baseBody.GetEntity("HollowCircularBeam1") as IGeometry;
```

*Source: Tutorial/ProcessNet/General/4WDLoader/4WDLoader_General_English.html*

### Example 9

```csharp
IContactSolidContact solidContact = model.CreateContactSolidContact("solidContact" + i.ToString(), baseGeom, actionGeom);
```

*Source: Tutorial/ProcessNet/General/4WDLoader/4WDLoader_General_English.html*

### Example 10

```csharp
public void ProcessNetTutorialCreateSolidContact()
{
    int BodyNumStart = 20;  // Start creating contacts with body 20
    int BodyNumEnd = 30;    // Continue until body 30
    int BodyInterval = 51;  // Interval between body number on hose 1
                            // and corresponding body's number on
                            // hose 2 is 51

    for (int i = BodyNumStart; i <= BodyNumEnd; i++)
    {
        int j = i + BodyInterval;  // j is the index for the
                                   // corresponding bodies on hose #2
                                   //Do the contact for corresponding bodies

        IBody baseBody = model.GetEntity("BeamBody" + i.ToString()) as IBody;
        IGeometry baseGeom = baseBody.GetEntity("HollowCircularBeam1") as IGeometry;
        IBody actionBody = model.GetEntity("BeamBody" + j.ToString()) as IBody;
        IGeometry actionGeom = actionBody.GetEntity("HollowCircularBeam1") as IGeometry;
        IContactSolidContact solidContact = model.CreateContactSolidContact("solidContact"+ i.ToString(), baseGeom, actionGeom);

        solidContact.ContactProperty.StiffnessCoefficient.Value =1000;
        solidContact.ContactProperty.DampingCoefficient.Value = 0.1;
    }
}
```

*Source: Tutorial/ProcessNet/General/4WDLoader/4WDLoader_General_English.html*

### Example 11

```csharp
IContactSolidContact solidContact = model.CreateContactSolidContact("solidContact" + i.ToString(), baseGeom, actionGeom);
        solidContact.ContactProperty.StiffnessCoefficient.Value = 1000;
        solidContact.ContactProperty.DampingCoefficient.Value = 0.1;

        // Do the contact for body i+1 and body j
        solidContact = model.CreateContactSolidContact("solidContact" + i.ToString() + "a",
        (model.GetEntity("BeamBody" + Convert.ToString(i + 1)) as IBody).
        GetEntity("HollowCircularBeam1") as IGeometry,
        (model.GetEntity("BeamBody" + j.ToString()) as IBody).GetEntity("HollowCircularBeam1")
        as IGeometry);
        solidContact.ContactProperty.StiffnessCoefficient.Value = 1000;
        solidContact.ContactProperty.DampingCoefficient.Value = 0.1;

        // Do the contact for body i and body j+1
        solidContact = model.CreateContactSolidContact("solidContact" + Convert.ToString(i) + "b",
        (model.GetEntity("BeamBody" + i.ToString()) as IBody).GetEntity("HollowCircularBeam1")
        as IGeometry, (model.GetEntity("BeamBody" + Convert.ToString(j + 1))
        as IBody).GetEntity("HollowCircularBeam1") as IGeometry);
        solidContact.ContactProperty.StiffnessCoefficient.Value = 1000;
        solidContact.ContactProperty.DampingCoefficient.Value = 0.1;

    }
}
```

*Source: Tutorial/ProcessNet/General/4WDLoader/4WDLoader_General_English.html*

### Example 12

```csharp
public void ProcessNetTutorialCreateSolidContact_WithDialog()
{
    i��n��t�� ��B��o��d��y��N��u��m��S��t��a��r��t�� ��=�� ��2��0��;�� �� ��/��/�� ��S��t��a��r��t�� ��c��r��e��a��t��i��n��g�� ��c��o��n��t��a��c��t��s�� ��w��i��t��h�� ��b��o��d��y�� ��2��0��
    ��i��n��t�� ��B��o��d��y��N��u��m��E��n��d�� ��=�� ��3��0��;�� �� �� �� ��/��/�� ��C��o��n��t��i��n��u��e�� ��u��n��t��i��l�� ��b��o��d��y�� ��3��0��
    ��i��n��t�� ��B��o��d��y��I��n��t��e��r��v��a��l�� ��=�� ��5��1��;�� �� ��/��/�� ��I��n��t��e��r��v��a��l�� ��b��e��t��w��e��e��n�� ��b��o��d��y�� ��n��u��m��b��e��r�� ��o��n�� ��h��o��s��e�� ��1��
                            ��/��/�� ��a��n��d�� ��c��o��r��r��e��s��p��o��n��d��i��n��g�� ��b��o��d��y��'��s�� ��n��u��m��b��e��r�� ��o��n��
                            ��/��/�� ��h��o��s��e�� ��2�� ��i��s�� ��5��1��

    // Create a Form
    Form1 MyForm = new Form1();

    // Open the Dialog
    MyForm.ShowDialog();

    if (MyForm.DialogResult == System.Windows.Forms.DialogResult.OK)
    {
        int NumContacts = 0;
        int BodyNumStart = MyForm.BNumStart;
        int BodyNumEnd = MyForm.BNumEnd;
        int BodyInterval = MyForm.BodyInterval;

        for (int i = BodyNumStart; i <= BodyNumEnd; i++)
        {
            int j = i + BodyInterval;  // j is the index for the
                                       // corresponding bodies on
                                       // hose #2
                                       // Do the contact for corresponding bodies
            .
            .
            .
            solidContact.ContactProperty.DampingCoefficient.Value = 0.1;

            // Increment the number of contacts
            NumContacts = NumContacts + 1;

            if (MyForm.AddOffsetFlag)
            {
                Do the contact for body i+1 and body j
                .
                .
                .
                Do the contact for body i and body j+1
                .
                .
                .
                s
```

*Source: Tutorial/ProcessNet/General/4WDLoader/4WDLoader_General_English.html*

### Example 13

```csharp
namespace ProcessNet.csproj
{
    public partial class Form1 Form2 : Form
    {
        public int BNumStart;
        public int BNumEnd;
        public int BodyInterval;
        public bool AddOffsetFlag;

        public ��F��o��r��m��1��  Form2()
        {
            InitializeComponent();
        }

        private void ��F��o��r��m��1��_��L��o��a��d��  Form2_Load(object sender, EventArgs e)
        {
            textBox1.Text = "20";
            BNumStart = 20;
```

*Source: Tutorial/ProcessNet/General/4WDLoader/4WDLoader_General_English.html*

### Example 14

```csharp
public void ProcessNetTutorialPlotData()
{
    // Create an auto contact plotting dialog
    Form2 MyForm = new Form2();

    // Open the dialog
    MyForm.ShowDialog();

    // If the user clicked OK:
    if (MyForm.DialogResult == System.Windows.Forms.DialogResult.OK
    {
        // Get the TIME data
        double[] TIME = plotDocument.GetPlotData("4WD_Loader/TIME");

        // |||||||| Plot individual contact forces ||||||||

        // Active upper-left plot window
        plotDocument.ActivateView(0, 0);

        for (int bodyIndex = MyForm.BNumStart; bodyIndex <= MyForm.BNumEnd; bodyIndex++)
        {
            // Load up the contact name number array

            String[] contNum = {bodyIndex.ToString(), "", ""};

            if (MyForm.AddOffsetFlag)
            {
                contNum[1] = bodyIndex.ToString() + "a";
                contNum[2] = bodyIndex.ToString() + "b";
            }

            for (int contNumIndex = 0; contNumIndex < contNum.Length; contNumIndex++)
            {
                if (String.Compare(contNum[contNumIndex], "") != 0)
                {
                    // Get the contact data for this segment
                    double[] contact = plotDocument.GetPlotData("4WD_Loader/Contact/Solid Contact/solidContact" + contNum[contNumIndex] + "/FM_SolidContact");

                    // Plot vs. TIME
                    plotDocument.DrawPlot("Contact" + contNum[contNumIndex], TIME, contact);
                }
            }
        }
    }
}
```

*Source: Tutorial/ProcessNet/General/4WDLoader/4WDLoader_General_English.html*

### Example 15

```csharp
public void ProcessNetTutorialPlotData()
{
    // Create an auto contact plotting dialog
    Form2 MyForm = new Form2();

    // Open the dialog
    MyForm.ShowDialog();

    // If the user clicked OK:
    if (MyForm.DialogResult == System.Windows.Forms.DialogResult.OK
    {
        // Get the TIME data
        double[] TIME = plotDocument.GetPlotData("4WD_Loader/TIME");

        // Initialize variables for X-axis limits
        double timeAtFirstContact = TIME[TIME.Length - 1];
        double timeAtLastContact = 0;

        // |||||||| Plot individual contact forces ||||||||

        // Active upper-left plot window
        plotDocument.ActivateView(0, 0);

        for (int bodyIndex = MyForm.BNumStart; bodyIndex <= MyForm.BNumEnd; bodyIndex++)
        {
            // Load up the contact name number array
            String[] contNum = {bodyIndex.ToString(), "", ""};

            if (MyForm.AddOffsetFlag)
            {
                contNum[1] = bodyIndex.ToString() + "a";
                contNum[2] = bodyIndex.ToString() + "b";
            }

            for (int contNumIndex = 0; contNumIndex < contNum.Length; contNumIndex++)
            {
                if (String.Compare(contNum[contNumIndex], "") != 0)
                {
                    // Get the contact data for this segment
                    double[] contact = plotDocument.GetPlotData("4WD_Loader/Contact/Solid Contact/solidContact" + contNum[contNumIndex] + "/FM_SolidContact");

                    ��/��/�� ��P��l��o��t�� ��v��s��.�� ��T��I��M��E��
                    ��p��l��o��t��D��o��c��u��m��e��n��t��.��D��r��a��w��P��l��o��t��(��"��C��o��n��t��a��c��t��"��+�� ��c��o��n��t��N��u��m��[��c��o��n��t��N��u��m��I��n��d��e��x��]��,�� ��T��I��M��E��,�� ��c��o��n��t��a��c��t��)��;��

                    // Check for non-zero contact data, and determine
                    // time at first contact
                    int j;
                    bool madeContact = false;
                    for (j = 0; j
```

*Source: Tutorial/ProcessNet/General/4WDLoader/4WDLoader_General_English.html*

### Example 16

```csharp
#region namespace
using System;
using Microsoft.VisualBasic;
using System.Windows.Forms; //IWin32Window
using System.IO;

using FunctionBay.RecurDyn.ProcessNet;
//For C#
using FunctionBay.RecurDyn.ProcessNet.Chart;
//using FunctionBay.RecurDyn.ProcessNet.MTT2D;
//using FunctionBay.RecurDyn.ProcessNet.FFlex;
//using FunctionBay.RecurDyn.ProcessNet.RFlex;
//using FunctionBay.RecurDyn.ProcessNet.Tire;
```

*Source: Tutorial/ProcessNet/General/4WDLoader/4WDLoader_General_English.html*

### Example 17

```csharp
#region Common Variables

FunctionBay.RecurDyn.ProcessNet.RecurDyn.IRecurDynApp app = new
FunctionBay.RecurDyn.ProcessNet.RecurDyn.RDApplication();

static public IApplication application;
public IModelDocument modelDocument = null;
public IPlotDocument plotDocument = null;
public ISubSystem model = null;

public IReferenceFrame refFrame1 = null;
public IReferenceFrame refFrame2 = null;
#endregion
```

*Source: Tutorial/ProcessNet/General/4WDLoader/4WDLoader_General_English.html*

### Example 18

```csharp
#region Common Variables

FunctionBay.RecurDyn.ProcessNet.RecurDyn.IRecurDynApp app = new
FunctionBay.RecurDyn.ProcessNet.RecurDyn.RDApplication();

public void Initialize() //Initialize() will be called automatically before ProcessNet function call.
{
    application = app.RecurDynApplication as IApplication;
    ��a��p��p��l��i��c��a��t��i��o��n�� ��=�� ��R��e��c��u��r��D��y��n��A��p��p��l��i��c��a��t��i��o��n�� ��a��s�� ��I��A��p��p��l��i��c��a��t��i��o��n��;��
    modelDocument = application.ActiveModelDocument;
    plotDocument = application.ActivePlotDocument;

    if (modelDocument == null & plotDocument == null)
    {
        application.PrintMessage("No model file");
        modelDocument = application.NewModelDocument("Examples");
    }
          if (modelDocument != null)
    {
        model = modelDocument.Model;
    }
}
```

*Source: Tutorial/ProcessNet/General/4WDLoader/4WDLoader_General_English.html*

### Example 19

```csharp
using System.Windows.Forms;
using FunctionBay.RecurDyn.ProcessNet;

namespace Excavator
{
    public partial class ExcavatorDialog : Form
    {
        IApplication application;
        string strFilePath;
        string[,] strExcavatorPartName = new string[7, 2];
        public ExcavatorDialog(IApplication app)
        {
            InitializeComponent();
            application = app;
                   }
```

*Source: Tutorial/ProcessNet/General/Excavator/Excavator_General_English.html*

### Example 20

```csharp
using FunctionBay.RecurDyn.ProcessNet;
namespace Excavator
{
    class PNetFunction
    {
        static public IApplication application;
        public IModelDocument modelDocument = null;
        public IPlotDocument plotDocument = null;
        public ISubSystem model = null;

        public IReferenceFrame refFrame1 = null;
        public IReferenceFrame refFrame2 = null;

        public PNetFunction(IApplication app)
        {
        application = app;
        }
    }
}
```

*Source: Tutorial/ProcessNet/General/Excavator/Excavator_General_English.html*

