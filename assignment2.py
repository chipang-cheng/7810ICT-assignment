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

        # Bind the search button event to the SearchCSV method
        self.Bind(wx.EVT_BUTTON, self.SearchCSV, self.searchButton)
        self.grid_sizer = None
        self.Bind(wx.EVT_BUTTON, self.Reset, self.resetButton)
        self.gridPanelSizer = wx.BoxSizer(wx.VERTICAL)

        self.checkboxes = []
        self.text_controls = []

        # Create a panel to display statistics
        self.statsPanel = wx.Panel(self)
        self.statsText = wx.TextCtrl(self.statsPanel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.statsSizer = wx.BoxSizer(wx.VERTICAL)
        self.statsSizer.Add(self.statsText, 1, wx.EXPAND)
        self.statsPanel.SetSizer(self.statsSizer)



        # Add the stats panel to the main sizer
        bottomSizer = self.GetSizer().GetChildren()[2].GetSizer()
        bottomSizer.Add(self.statsPanel, 1, wx.EXPAND | wx.ALL, 5)


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
            self.df = pd.read_csv(file_path)

            # Clear existing data in the grid
            self.m_grid1.ClearGrid()

            # Populate the grid with pandas DataFrame
            self.m_grid1.DeleteRows(0, self.m_grid1.GetNumberRows())
            self.m_grid1.DeleteCols(0, self.m_grid1.GetNumberCols())
            self.m_grid1.AppendRows(len(self.df))
            self.m_grid1.AppendCols(len(self.df.columns))

            for i, col_name in enumerate(self.df.columns):
                self.m_grid1.SetColLabelValue(i, col_name)

            for i, row in enumerate(self.df.itertuples(index=False), start=0):
                for j, cell in enumerate(row):
                    self.m_grid1.SetCellValue(i, j, str(cell))

            self.AddControlsForColumns(self.df.columns)
            self.UpdateStatistics()
        except Exception as e:
            wx.LogError(f"Error loading CSV file: {str(e)}")
            print(str(e))


    def AddControlsForColumns(self, columns):
        # Destroy the existing controls
        for child in self.m_scrolledWindow3.GetChildren():
            child.Destroy()

        # Create separate lists to store references to checkboxes and text controls
        self.checkboxes = []
        self.text_controls = []

        # Create a grid sizer to manage the layout of rows
        self.grid_sizer = wx.GridSizer(len(columns), 3, 0, 0)

        for col_index, col_name in enumerate(columns):
            # Checkbox
            checkbox = wx.CheckBox(self.m_scrolledWindow3, col_index * 10, "", wx.DefaultPosition, wx.DefaultSize, 0)
            self.grid_sizer.Add(checkbox, 0, wx.ALL, 5)
            self.checkboxes.append(checkbox)

            # Static Text (CSV Header)
            static_text = wx.StaticText(self.m_scrolledWindow3, wx.ID_ANY, col_name, wx.DefaultPosition, wx.DefaultSize, 0)
            self.grid_sizer.Add(static_text, 0, wx.ALL, 5)

            # TextCtrl
            text_ctrl = wx.TextCtrl(self.m_scrolledWindow3, col_index * 10 + 1, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
            self.grid_sizer.Add(text_ctrl, 1, wx.ALL | wx.EXPAND, 5)
            self.text_controls.append(text_ctrl)

            # Bind checkbox event to the SearchCSV method
            self.Bind(wx.EVT_CHECKBOX, self.OnCheckboxChange, checkbox)

        # Set the grid sizer as the sizer for m_scrolledWindow3
        self.m_scrolledWindow3.SetSizer(self.grid_sizer)

        self.Layout()


    def OnCheckboxChange(self, event):
        # Handle checkbox change event here (if needed)
        pass

    def SearchCSV(self, event):
        # Get search criteria from checkboxes and text controls
        selected_fields = []
        search_texts = []

        # Iterate through the stored checkboxes and text controls
        for checkbox, text_ctrl in zip(self.checkboxes, self.text_controls):
            if checkbox.GetValue():
                selected_fields.append(text_ctrl.GetId() // 10)  # Extract the column index
                search_texts.append(text_ctrl.GetValue())

        # Check if no checkboxes are selected
        if not selected_fields:
            # Retrieve all records without filtering
            filtered_data = self.df.copy()
            columns_to_display = list(self.df.columns)
        else:
            # Filter the CSV data based on selected fields and search texts
            filtered_data = self.df.copy()
            columns_to_display = [self.df.columns[field] for field in selected_fields]

            for field, search_text in zip(selected_fields, search_texts):
                if search_text:
                    field_name = self.df.columns[field]
                    filtered_data = filtered_data[
                        filtered_data[field_name].str.contains(search_text, case=False, na=False)]

        # Clear the grid before updating it
        if self.m_grid1.GetNumberCols() > 0:
            self.m_grid1.DeleteCols(0, self.m_grid1.GetNumberCols())

        self.m_grid1.DeleteRows(0, self.m_grid1.GetNumberRows())

        # Update m_grid1 with filtered data and selected columns
        if not filtered_data.empty:
            self.m_grid1.AppendCols(len(columns_to_display))
            for i, col_name in enumerate(columns_to_display):
                self.m_grid1.SetColLabelValue(i, col_name)

            self.m_grid1.AppendRows(len(filtered_data))
            for i, row in enumerate(filtered_data.itertuples(index=False), start=0):
                for j, field in enumerate(selected_fields if selected_fields else range(len(self.df.columns))):
                    cell = row[field]
                    self.m_grid1.SetCellValue(i, j, str(cell))

        # Ensure that the grid expands to fill available space
        self.gridPanelSizer.Layout()  # Force a layout update
        self.UpdateStatistics()
        self.Layout()

    def Reset(self, event):
        # Uncheck all checkboxes
        for checkbox in self.checkboxes:
            checkbox.SetValue(False)

    def UpdateStatistics(self):
        if hasattr(self, 'df'):
            stats_data = []

            for col_index in range(self.m_grid1.GetNumberCols()):
                col_name = self.m_grid1.GetColLabelValue(col_index)

                if self.df[col_name].dtype == 'object':
                    header = f'{col_name}:'
                    unique_values = self.GetUniqueColumnValues(col_index)
                    for val in unique_values:
                        count = self.GetColumnValueCount(col_index, val)

                        # Ensure that count and len(self.df) are greater than 0
                        if count > 0 and len(self.df) > 0:
                            percentage = round((float(count) / len(self.df) * 100), 2)
                        else:
                            percentage = 0.0

                        # Create a dictionary for each statistic entry
                        stats_data.append({'Header': header, 'Value': val, 'Count': count, 'Percentage': percentage})

            # Create a DataFrame from the list of dictionaries
            stats = pd.DataFrame(stats_data)

            # Display statistics in the TextCtrl
            self.statsText.SetValue(stats.to_string(index=False))

    def CalculateStatistics(self):
        # Calculate statistics on the data currently displayed in the grid
        if hasattr(self, 'df'):
            stats_data = []

            for col_index, col_name in enumerate(self.df.columns):
                if self.df[col_name].dtype == 'object':
                    header = f'{col_name}:'
                    unique_values = self.GetUniqueColumnValues(col_index)
                    for val in unique_values:
                        count = self.GetColumnValueCount(col_index, val)

                        # Ensure that count and len(self.df) are greater than 0
                        if count > 0 and len(self.df) > 0:
                            percentage = round((float(count) / len(self.df) * 100), 2)
                        else:
                            percentage = 0.0

                        # Create a dictionary for each statistic entry
                        stats_data.append({'Header': header, 'Value': val, 'Count': count, 'Percentage': percentage})

            # Create a DataFrame from the list of dictionaries
            stats = pd.DataFrame(stats_data)

            return stats
        return None

    def GetUniqueColumnValues(self, col_index):
        # Get unique values in the specified column
        unique_values = set()

        # Ensure that col_index is valid
        if col_index >= 0 and col_index < self.m_grid1.GetNumberCols():
            for row_index in range(self.m_grid1.GetNumberRows()):
                # Check if row_index is valid
                if row_index >= 0 and row_index < self.m_grid1.GetNumberRows():
                    cell_value = self.m_grid1.GetCellValue(row_index, col_index)
                    unique_values.add(cell_value)

        return list(unique_values)

    def GetColumnValueCount(self, col_index, value):
        # Count occurrences of a value in the specified column
        count = 0

        # Ensure that col_index is valid
        if col_index >= 0 and col_index < self.m_grid1.GetNumberCols():
            for row_index in range(self.m_grid1.GetNumberRows()):
                # Check if row_index is valid
                if row_index >= 0 and row_index < self.m_grid1.GetNumberRows():
                    cell_value = self.m_grid1.GetCellValue(row_index, col_index)
                    if cell_value == value:
                        count += 1

        return count

if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame(None)
    frame.Show()
    app.MainLoop()
