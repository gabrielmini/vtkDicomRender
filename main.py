from vtk import *
from vtk.wx.wxVTKRenderWindowInteractor import wxVTKRenderWindowInteractor
import thread
import wx
import pydicom
import os

class VtkPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent

        # Top Sizer Configuration
        self.topSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.IMAGE_PATH = None
        self.ROOT_PIPE = None
        self.DICOM_IMAGES = None
        self.FIRST_IMAGE = None
        self.IMAGE_LARGEST_PIXEL = None
        self.IMAGE_SMALLEST_PIXEL = None

        self.loadView()  # Loading View

        # Initializing
        self.wxThresholdRadioBox.SetSelection(0)
        self.wxLowerSlider.Disable()


    def loadView(self):
        # LEFT
        #self.InteractorImageRenderWindow = wxVTKRenderWindowInteractor(self, -1)
        #self.InteractorImageRenderWindow.Enable(1)

        #self.topSizer.Add(self.InteractorImageRenderWindow, 1, wx.EXPAND| wx.RIGHT, 5)
        #self.ImageViewer = vtkImageViewer2()

        #a = wx.Panel(self, -1)
        #a.SetBackgroundColour("#00FF00")
        #self.topSizer.Add(a,1,wx.EXPAND|wx.RIGHT, 5)
        #self.wxImageSlider = wx.Slider(self, -1, style=wx.SL_VERTICAL | wx.SL_LEFT | wx.SL_MIN_MAX_LABELS | wx.EXPAND)
        #self.topSizer.Add(self.wxImageSlider, 0, wx.EXPAND)


            # RIGHT
        self.Interactor3DRenderWindow = wxVTKRenderWindowInteractor(self,-1)
        self.Interactor3DRenderWindow.Enable(1)

        self.topSizer.Add(self.Interactor3DRenderWindow, 1, wx.EXPAND)

        # Botton Sizer Configuration
        self.bottomSizer = wx.BoxSizer(wx.HORIZONTAL)

            # Load and Save Section
        self.loadSaveStaticBox = wx.StaticBox(self, -1, "Load and Save")
        self.wxLoadSaveStaticBox = wx.StaticBoxSizer(self.loadSaveStaticBox, wx.VERTICAL)
        self.wxLoadButton = wx.Button(self, -1, "Load Image", size=(100, 40))
        self.wxLoadSaveStaticBox.Add(self.wxLoadButton, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)
        self.wxSaveButton = wx.Button(self, -1, "Save Volume", size=(100, 40))
        self.wxLoadSaveStaticBox.Add(self.wxSaveButton, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 10)
        self.bottomSizer.Add(self.wxLoadSaveStaticBox, 0, wx.EXPAND | wx.RIGHT, 10)

            # Configuration Section
        self.configurationStaticBox = wx.StaticBox(self, -1, "Configuration")
        self.wxConfigurationStaticBox = wx.StaticBoxSizer(self.configurationStaticBox, wx.VERTICAL)
        self.wxThresholdRadioBox = wx.RadioBox(self, -1, "Threshold Configuration", (-1, -1), (-1, -1), ["Upper", "Lower", "Range"], 3, wx.RA_SPECIFY_COLS)

        self.wxConfigurationStaticBox.Add(self.wxThresholdRadioBox, 0, wx.EXPAND | wx.ALL, 5)
        self.bottomSizer.Add(self.wxConfigurationStaticBox, 1, wx.EXPAND)

                # Sliders
        self.wxLowerStaticText = wx.StaticText(self, -1, "Lower: 0")
        self.wxConfigurationStaticBox.Add(self.wxLowerStaticText, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 1)
        self.wxLowerSlider = wx.Slider(self, -1, minValue=0, maxValue=100)
        self.wxConfigurationStaticBox.Add(self.wxLowerSlider, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 1)
        self.wxUpperStaticText = wx.StaticText(self, -1, "Upper: 0")
        self.wxConfigurationStaticBox.Add(self.wxUpperStaticText, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 1)
        self.wxUpperSlider = wx.Slider(self, -1, minValue=0, maxValue=100)
        self.wxConfigurationStaticBox.Add(self.wxUpperSlider, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 1)

        # Filter Section
        self.filterStaticBox = wx.StaticBox(self, -1, "Filters")
        self.wxFilterStaticBox = wx.StaticBoxSizer(self.filterStaticBox, wx.VERTICAL)
        self.bottomSizer.Add(self.wxFilterStaticBox, 1, wx.EXPAND|wx.LEFT,10)

        # Root Sizer Configuration
        self.rootSizer = wx.BoxSizer(wx.VERTICAL)

        self.rootSizer.Add(self.topSizer, 2, wx.EXPAND | wx.ALL, 10)
        self.rootSizer.Add(self.bottomSizer, 1, wx.EXPAND | wx.ALL, 10)

        self.SetSizer(self.rootSizer)
        self.Layout()

        #Status Bar
        # Implement

        # Binds
        self.wxLoadButton.Bind(wx.EVT_BUTTON, self.OnButtonLoadImageClick)

        self.wxThresholdRadioBox.Bind(wx.EVT_RADIOBOX, self.OnWxThresholdRadioBoxChanged)
        self.wxUpperSlider.Bind(wx.EVT_SLIDER, self.OnWxUpperSliderChanged)
        self.wxLowerSlider.Bind(wx.EVT_SLIDER, self.OnWxLowerSliderChanged)

        # States
        self.wxSaveButton.Disable()

        self.loadSaveStaticBox.Disable()
        self.wxThresholdRadioBox.Disable()
        self.wxUpperSlider.Disable()




    def OnWxThresholdRadioBoxChanged(self, evt):
        selection = evt.Int

        self.wxLowerSlider.Disable()
        self.wxUpperSlider.Disable()

        if selection == 0:  # Upper
            self.wxUpperSlider.Enable()
            self.wxLowerStaticText.SetLabel("Lower: 0")
            self.wxLowerSlider.SetValue(0)

        elif selection == 1:  # Lower
            self.wxLowerSlider.Enable()
            self.wxUpperStaticText.SetLabel("Upper: 0")
            self.wxUpperSlider.SetValue(0)

        elif selection == 2:  # Range
            self.wxLowerSlider.Enable()
            self.wxUpperSlider.Enable()
        else:
            raise NotImplementedError()

    def OnWxUpperSliderChanged(self, evt):
        self.wxUpperStaticText.SetLabel("Upper: " +str(self.wxUpperSlider.GetValue()))

    def OnWxLowerSliderChanged(self, evt):
        self.wxLowerStaticText.SetLabel("Lower: " + str(self.wxLowerSlider.GetValue()))


    def showImage(self,imageData):
        raise NotImplementedError()
        self.ImageViewer.SeInputConnection(imageData.GetOutputPort())
        self.ImageViewer.SetupInteractor(self.InteractorImageRenderWindow)

        self.ImageViewer.Render()

    def OnButtonLoadImageClick(self, evt):
        dirDialog = wx.DirDialog(self,
                                 message="Select a Folder with Dicom Files",
                                 defaultPath=r"C:\Projects\IC\sample",  # Temporary
                                 #defaultPath=r"C:\Users\work\Desktop\dicoms\old\dentalTeste",  # Temporary
                                 style=wx.DD_DEFAULT_STYLE,)

        if dirDialog.ShowModal() == wx.ID_OK:
            self.loadDicomImages(dirDialog.GetPath())
            #self.wxSaveButton.Enable()


        dirDialog.Destroy()


    def loadDicomImages(self, dicomFilesPath):

        # TODO Implement verification if dicom files exists
        dicomPath = os.path.join(dicomFilesPath, os.listdir(dicomFilesPath)[1])
        try:
            dicomFile = pydicom.read_file(dicomPath)
        except Exception as e:
            raise e

        if 0x00280106 in dicomFile and 0x00280107 in dicomFile:
            self.IMAGE_SMALLEST_PIXEL = dicomFile[0x00280106].value  # SmallestImagePixelValue
            self.IMAGE_LARGEST_PIXEL = dicomFile[0x00280107].value  # LargestImagePixelValue
        else:
            self.IMAGE_SMALLEST_PIXEL = 0
            self.IMAGE_LARGEST_PIXEL = 100

        self.wxUpperSlider.SetRange(self.IMAGE_SMALLEST_PIXEL, self.IMAGE_LARGEST_PIXEL)
        self.wxLowerSlider.SetRange(self.IMAGE_SMALLEST_PIXEL, self.IMAGE_LARGEST_PIXEL)
        self.wxLowerSlider.Update()
        self.Layout()

        dicomImages = vtkDICOMImageReader()
        dicomImages.SetDirectoryName(dicomFilesPath)
        dicomImages.Update()

        self.DICOM_IMAGES = dicomImages
        self.adjustImageThreshold(800)
        #self.__plotImage(self.ROOT_PIPE)
        self.createVolume()
        self.decimateVolume(0.5)
        self.view3DImage(self.ROOT_PIPE)

        # View
        #self.wxConfigurationStaticBox.Enable()
        #self.wxFilterStaticBox.Enable()

    def createVolume(self):
        mesh_3d = vtkDiscreteMarchingCubes()
        mesh_3d.SetInputConnection(self.ROOT_PIPE.GetOutputPort())
        mesh_3d.GenerateValues(1, 1, 1)
        mesh_3d.Update()
        self.ROOT_PIPE = mesh_3d


    def __plotImage(self, imageData):
        raise NotImplementedError()
        self.ImageViewer.SetInputConnection(imageData.GetOutputPort())
        self.ImageViewer.SetupInteractor(self.InteractorImageRenderWindow)

        self.ImageViewer.Render()
        self.InteractorImageRenderWindow.Start()


    def adjustImageThreshold(self, lower_limit=None, upper_value=None):

        thresholdFilter = vtkImageThreshold()
        thresholdFilter.SetInputConnection(self.DICOM_IMAGES.GetOutputPort())

        if lower_limit is not None and upper_value is not None:  # Threshold By Range
            if lower_limit > upper_value:
                temp_value = upper_value
                upper_value = lower_limit
                lower_limit = temp_value
            thresholdFilter.ThresholdBetween(lower_limit, upper_value)

        elif lower_limit is not None and upper_value is None:  # Threshold By lower
            thresholdFilter.ThresholdByLower(lower_limit)

        elif upper_value is not None and lower_limit is None:  # Threshold By Upper
            thresholdFilter.ThresholdByUpper(upper_value)

        else:
            thresholdFilter.ThresholdByLower(255)

        thresholdFilter.SetInValue(0)
        thresholdFilter.ReplaceInOn()
        #thresholdFilter.SetOutValue(1)
        thresholdFilter.SetOutValue(1)
        thresholdFilter.ReplaceOutOn()
        thresholdFilter.Update()

        thresholdFilter.Update()
        self.ROOT_PIPE = thresholdFilter
        self.FIRST_IMAGE = thresholdFilter

        return thresholdFilter



    def saveStlFile(self, file_name="3d_volume"):
        writer = vtkSTLWriter()
        writer.SetInputConnection(self.ROOT_PIPE.GetOutputPort())
        writer.SetFileTypeToBinary()
        writer.SetFileName("".join([file_name, ".stl"]))
        writer.Write()

    def gaussianFilter(self, imageData):
        gaussianFilter = vtkImageGaussianSmooth()
        gaussianFilter.SetInputConnection(imageData.GetOutputPort())
        gaussianFilter.Update()
        return gaussianFilter

    def fillHoles(self):
        fillHolesFilter = vtkFillHolesFilter()
        fillHolesFilter.SetInputConnection(self.ROOT_PIPE.GetOutputPort())
        fillHolesFilter.SetHoleSize(1000.0)

        dataFixed = vtkPolyDataNormals()
        dataFixed.SetInputConnection(fillHolesFilter.GetOutputPort())
        dataFixed.ConsistencyOn()
        dataFixed.SplittingOff()
        dataFixed.Update()
        self.ROOT_PIPE = dataFixed
        return dataFixed

    def smoothVolume(self, type="laplacian", level=1):
        smooth = None

        if type == "laplacian":
            smooth = vtkSmoothPolyDataFilter()
            smooth.SetNumberOfIterations(level)

        elif type == "linear":
            smooth = vtkLinearSubdivisionFilter()
            smooth.SetNumberOfSubdivisions(level)

        elif type == "loop":
            smooth = vtkLoopSubdivisionFilter()
            smooth.SetNumberOfSubdivisions(level)

        elif type == "butterfly":
            smooth = vtkButterflySubdivisionFilter()
            smooth.SetNumberOfSubdivisions(level)

        else:
            print "Invalid Type assuming Laplacian"
            self.smoothVolume(type="laplacian", level=level)
            return

        smooth.SetInputConnection(self.ROOT_PIPE.GetOutputPort())
        smooth.Update()
        self.ROOT_PIPE = smooth

    def decimateVolume(self, reduction=0.1):
        if not 0 < reduction < 1:
            reduction = 0.3  # 30%

        decimatedVolume = vtkDecimatePro()
        decimatedVolume.SetInputConnection(self.ROOT_PIPE.GetOutputPort())
        decimatedVolume.SetTargetReduction(reduction)
        decimatedVolume.Update()
        self.ROOT_PIPE = decimatedVolume

    def view3DImage(self, imageData):
        polyDataMapper = vtkPolyDataMapper()
        polyDataMapper.ImmediateModeRenderingOn()
        polyDataMapper.SetInputConnection(imageData.GetOutputPort())

        polyDataMapper.Update()

        volume_3d = vtkActor()
        volume_3d.SetMapper(polyDataMapper)
        volume_3d.GetProperty().SetColor(0,0,1)

        renderer = vtkRenderer()
        renderer.AddActor(volume_3d)
        renderer.SetBackground(1.0, 1.0, 1.0)  # White

        self.Interactor3DRenderWindow.GetRenderWindow().AddRenderer(renderer)
        self.Layout()
        #self.InteractorRenderWindow.GetRenderWindow().SetSize(500,500)
        #self.InteractorRenderWindow.Initialize()

        #self.InteractorRenderWindow.GetRenderWindow().Render()
        #self.InteractorRenderWindow.Start()


def main():

    app = wx.App()

    main_frame = wx.Frame(None, size=(800,600))

    sizer = wx.BoxSizer(wx.VERTICAL)
    main_frame.SetSizer(sizer)

    frame = VtkPanel(main_frame)
    sizer.Add(frame,1,wx.EXPAND)

    main_frame.Show()
    main_frame.CenterOnScreen()
    app.MainLoop()

if __name__ == "__main__":
    main()





