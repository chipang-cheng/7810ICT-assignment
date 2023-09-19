import wx
import wx.xrc
import wx.dataview
import pandas as pd
import wx.grid

from noname import mainFrame

class MyFrame(mainFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Bind the "File Open" menu item's event to the OnOpen method
        self.Bind(wx.EVT_MENU, self.OnOpen, self.fileOpen)


    def OnOpen(self, event):
        # Create a file dialog
        openFileDialog = wx.FileDialog(self, "Open a file", "", "",
                                       "CSV files (*.csv)|*.csv",
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        # Show the dialog and get the selected file path
        if openFileDialog.ShowModal() == wx.ID_OK:
            selected_file = openFileDialog.GetPath()
            self.LoadCSV(selected_file)

        # Destroy the file dialog
        openFileDialog.Destroy()

    def LoadCSV(self, file_path):
        try:
            # Read CSV file using pandas
            df = pd.read_csv(file_path)

            # Clear existing data in the grid
            self.m_grid1.ClearGrid()

            # Populate the grid with pandas DataFrame
            self.m_grid1.DeleteRows(0, self.m_grid1.GetNumberRows())
            self.m_grid1.DeleteCols(0, self.m_grid1.GetNumberCols())
            self.m_grid1.AppendRows(len(df))
            self.m_grid1.AppendCols(len(df.columns))

            for i, col_name in enumerate(df.columns):
                self.m_grid1.SetColLabelValue(i, col_name)

            for i, row in enumerate(df.itertuples(index=False), start=0):
                for j, cell in enumerate(row):
                    self.m_grid1.SetCellValue(i, j, str(cell))

            self.AddControlsForColumns(df.columns)
        except Exception as e:
            wx.LogError(f"Error loading CSV file: {str(e)}")

    def AddControlsForColumns(self, columns):
        # Destroy the existing controls
        for child in self.m_scrolledWindow3.GetChildren():
            child.Destroy()

        # Create a grid sizer to manage the layout of rows
        grid_sizer = wx.GridSizer(len(columns), 3, 0, 0)

        for col_index, col_name in enumerate(columns):
            # Checkbox
            checkbox = wx.CheckBox(self.m_scrolledWindow3, wx.ID_ANY, "", wx.DefaultPosition, wx.DefaultSize, 0)
            grid_sizer.Add(checkbox, 0, wx.ALL, 5)

            # Static Text (CSV Header)
            static_text = wx.StaticText(self.m_scrolledWindow3, wx.ID_ANY, col_name, wx.DefaultPosition, wx.DefaultSize, 0)
            grid_sizer.Add(static_text, 0, wx.ALL, 5)

            # TextCtrl
            text_ctrl = wx.TextCtrl(self.m_scrolledWindow3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
            grid_sizer.Add(text_ctrl, 1, wx.ALL | wx.EXPAND, 5)

        # Set the grid sizer as the sizer for m_scrolledWindow3
        self.m_scrolledWindow3.SetSizer(grid_sizer)



if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame(None)
    frame.Show()
    app.MainLoop()