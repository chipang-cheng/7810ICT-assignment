import wx
import wx.dataview
import wx.xrc
import pandas as pd

# Import your generated classes (mainFrame and fileOpenDia)
from noname import mainFrame


class MyFrame(mainFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Bind the "File Open" menu item's event to the OnOpen method
        self.Bind(wx.EVT_MENU, self.OnOpen, self.fileOpen)

        self.controls = []

    def OnOpen(self, event):
        # Create a file dialog
        openFileDialog = wx.FileDialog(self, "Open a file", "", "",
                                       "CSV files (*.csv)|*.csv",
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        # Show the dialog and get the selected file path
        if openFileDialog.ShowModal() == wx.ID_OK:
            selected_file = openFileDialog.GetPath()
            #self.LoadCSV(selected_file)

        # Destroy the file dialog
        openFileDialog.Destroy()



if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame(None)
    frame.Show()
    app.MainLoop()