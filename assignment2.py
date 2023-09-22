import wx
import wx.xrc
import wx.dataview
import pandas as pd
import wx.grid
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np
from noname import mainFrame


class MyFrame(mainFrame):
    column_mapping = {}

    def __init__(self, parent):
        super().__init__(parent)

        self.Bind(wx.EVT_MENU, self.GenerateChart, self.chart)

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

        self.first_load = True
        self.checked_checkboxes = 0

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

            # Convert ACCIDENT_DATE to the dd/mm/yyyy format
            self.df['ACCIDENT_DATE'] = pd.to_datetime(self.df['ACCIDENT_DATE'], format='%d/%m/%Y', errors='coerce')
            self.df['ACCIDENT_DATE'] = self.df['ACCIDENT_DATE'].dt.strftime('%d/%m/%Y')

            # Convert ACCIDENT_TIME to the hh/mm/ss format
            self.df['ACCIDENT_TIME'] = pd.to_datetime(self.df['ACCIDENT_TIME'], format='%H.%M.%S', errors='coerce')
            self.df['ACCIDENT_TIME'] = self.df['ACCIDENT_TIME'].dt.strftime('%H:%M:%S')

            self.df = self.df.fillna("Not specify")

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
            self.first_load = False
        except Exception as e:
            wx.LogError(f"Error loading CSV file: {str(e)}")

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
            # Skip 'OBJECTID' and 'ACCIDENT_NO' columns and their values
            if col_name in ['OBJECTID', 'ACCIDENT_NO']:
                continue

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
        self.checked_checkboxes = 0
        for checkbox in self.checkboxes:
            if checkbox.GetValue():
                self.checked_checkboxes += 1

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
        self.checked_checkboxes = 0

    def UpdateStatistics(self):
        if hasattr(self, 'df'):
            stats_data = []

            if self.first_load:
                # Display an info message for the first load
                self.statsText.SetValue("Statistics analysis will be available after the first load.")
            elif self.checked_checkboxes == 0:
                # Display a message when no checkboxes are checked
                self.statsText.SetValue("Please check at least one checkbox for statistics analysis.")
            elif self.checked_checkboxes > 5:
                # Display a message when more than five checkboxes are checked
                self.statsText.SetValue("Please check no more than five checkboxes for statistics analysis.")
            else:
                # Calculate and display statistics only when the condition is met
                for col_index in range(self.m_grid1.GetNumberCols()):
                    col_name = self.m_grid1.GetColLabelValue(col_index)

                    if col_name not in ['OBJECTID', 'ACCIDENT_NO']:
                        if self.df[col_name].dtype == 'object':
                            header = f'{col_name}:'
                            unique_values = self.GetUniqueColumnValues(col_index)
                            for val, val_data in unique_values.items():
                                count = val_data['Count']
                                percentage = val_data['Percentage']

                                # Create a dictionary for each statistic entry
                                stats_data.append(
                                    {'Header': header, 'Value': val, 'Count': count, 'Percentage': percentage})

                # Create a DataFrame from the list of dictionaries
                stats = pd.DataFrame(stats_data)

                # Display statistics in the TextCtrl
                self.statsText.SetValue(stats.to_string(index=False))

    def CalculateStatistics(self):
        # Calculate statistics on the data currently displayed in the grid
        if hasattr(self, 'df'):
            stats_data = []

            # Get the filtered data from the grid
            num_rows = self.m_grid1.GetNumberRows()
            num_cols = self.m_grid1.GetNumberCols()

            # Find the column index for selected headers
            selected_fields = [text_ctrl.GetId() // 10 for text_ctrl in self.text_controls if text_ctrl.GetValue()]
            filtered_data = self.df.copy()

            if selected_fields:
                # Apply filtering based on selected fields and search texts
                columns_to_display = [self.df.columns[field] for field in selected_fields]
                for field, search_text in zip(selected_fields,
                                              [text_ctrl.GetValue() for text_ctrl in self.text_controls]):
                    if search_text:
                        field_name = self.df.columns[field]
                        filtered_data = filtered_data[
                            filtered_data[field_name].str.contains(search_text, case=False, na=False)]

                # Iterate through the columns to calculate statistics
                for col_index in range(num_cols):
                    col_label = self.m_grid1.GetColLabelValue(col_index)
                    if col_label not in ['OBJECTID', 'ACCIDENT_NO'] and col_label in columns_to_display:
                        if self.df[col_label].dtype == 'object':
                            header = f'{col_label}:'

                            # Get unique values and their counts from the filtered data
                            unique_values, value_counts = np.unique(filtered_data.iloc[:, col_index],
                                                                    return_counts=True)

                            for val, count in zip(unique_values, value_counts):
                                percentage = (count / len(filtered_data)) * 100

                                # Create a dictionary for each statistic entry
                                stats_data.append(
                                    {'Header': header, 'Value': val, 'Count': count, 'Percentage': percentage})

            # Create a DataFrame from the list of dictionaries
            stats = pd.DataFrame(stats_data)

            return stats
        return None

    def GetUniqueColumnValues(self, col_index):
        # Get unique values in the specified column, counting occurrences and percentages based on filtered grid data
        unique_values = {}

        if col_index >= 0 and col_index < self.m_grid1.GetNumberCols():
            # Get the filtered data from the grid
            selected_fields = [text_ctrl.GetId() // 10 for text_ctrl in self.text_controls if text_ctrl.GetValue()]
            filtered_data = self.df.copy()

            if selected_fields:
                # Apply filtering based on selected fields and search texts
                columns_to_display = [self.df.columns[field] for field in selected_fields]
                for field, search_text in zip(selected_fields,
                                              [text_ctrl.GetValue() for text_ctrl in self.text_controls]):
                    if search_text:
                        field_name = self.df.columns[field]
                        filtered_data = filtered_data[
                            filtered_data[field_name].str.contains(search_text, case=False, na=False)]

            for row_index in range(self.m_grid1.GetNumberRows()):
                if row_index >= 0 and row_index < self.m_grid1.GetNumberRows():
                    cell_value = self.m_grid1.GetCellValue(row_index, col_index)

                    # Initialize or update the count for the unique value
                    val_data = unique_values.get(cell_value, {'Count': 0, 'Percentage': 0.0})
                    val_data['Count'] += 1
                    unique_values[cell_value] = val_data

            # Calculate percentages based on the count of unique values within the filtered data
            total_count = sum(val_data['Count'] for val_data in unique_values.values())
            for key, val_data in unique_values.items():
                val_data['Percentage'] = round((val_data['Count'] / total_count) * 100, 2)

        return unique_values

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

    def GenerateChart(self, event):
        # Create a list of available headers for the Y-axis (exclude ACCIDENT_DATE and ACCIDENT_TIME)
        y_axis_choices = [col for col in self.df.columns if col not in ['ACCIDENT_DATE', 'ACCIDENT_TIME']]

        # Create a dialog to select Y-axis column from available choices
        y_axis_dialog = wx.SingleChoiceDialog(self, "Select Y-axis column:", "Y-axis Selection",
                                              y_axis_choices)
        if y_axis_dialog.ShowModal() == wx.ID_OK:
            y_axis_choice = y_axis_dialog.GetStringSelection()

            # Create a dialog to select X-axis (ACCIDENT_DATE or ACCIDENT_TIME or both)
            x_axis_choices = ["ACCIDENT_DATE", "ACCIDENT_TIME", "Both"]
            x_axis_dialog = wx.SingleChoiceDialog(self, "Select X-axis:", "X-axis Selection",
                                                  x_axis_choices)
            if x_axis_dialog.ShowModal() == wx.ID_OK:
                x_axis_choice = x_axis_dialog.GetStringSelection()

                # Prepare data for the chart
                chart_data = defaultdict(lambda: defaultdict(int))

                # Get the number of rows and columns in the grid
                num_rows = self.m_grid1.GetNumberRows()
                num_cols = self.m_grid1.GetNumberCols()

                # Find the column index for X-axis and Y-axis headers
                x_axis_col = None
                y_axis_col = None

                for col_index in range(num_cols):
                    col_label = self.m_grid1.GetColLabelValue(col_index)
                    if col_label == x_axis_choice:
                        x_axis_col = col_index
                    elif col_label == y_axis_choice:
                        y_axis_col = col_index

                # Check if both X-axis and Y-axis columns were found
                if x_axis_col is not None and y_axis_col is not None:
                    # Create a DataFrame from the grid data
                    data = {'X': [], 'Y': []}
                    for row in range(num_rows):
                        try:
                            x_value = self.m_grid1.GetCellValue(row, x_axis_col)
                            y_value = self.m_grid1.GetCellValue(row, y_axis_col)

                            data['X'].append(x_value)
                            data['Y'].append(y_value)
                        except Exception as e:
                            wx.LogError(f"Error processing row {row}: {str(e)}")

                    df = pd.DataFrame(data)

                    # Format the X-axis labels based on the ACCIDENT_DATE values
                    if x_axis_choice == "ACCIDENT_DATE":
                        date_values = pd.to_datetime(df['X'], format='%d/%m/%Y', errors='coerce')

                        # Determine the date format for X-axis labels
                        date_diff = (date_values.max() - date_values.min()).days

                        if date_diff < 1:
                            x_date_format = "%d/%m/%Y"  # Display as dd/mm/yyyy for a single day
                        elif date_diff < 30:
                            x_date_format = "%d/%m"  # Display as dd/mm for a single month
                        elif date_diff < 365:
                            x_date_format = "%m/%Y"  # Display as mm/yyyy for multiple months in a year
                        else:
                            x_date_format = "%Y"  # Display as yyyy for multiple years

                        # Convert date values to the desired format
                        df['X'] = date_values.dt.strftime(x_date_format)

                    # Group data by X and Y values and count occurrences
                    grouped_data = df.groupby(['X', 'Y']).size().reset_index(name='Count')

                    # Create the chart
                    plt.figure(figsize=(12, 8))

                    unique_y_values = grouped_data['Y'].unique()
                    for y_value in unique_y_values:
                        y_data = grouped_data[grouped_data['Y'] == y_value]
                        plt.plot(y_data['X'], y_data['Count'], marker='o', label=f'{y_value}')

                    plt.xlabel(x_axis_choice)
                    plt.ylabel(f"{y_axis_choice} Count")
                    plt.title(f"Count by {x_axis_choice} for {y_axis_choice}")
                    plt.legend()
                    plt.grid(True)
                    plt.xticks(rotation=45)  # Rotate X-axis labels for better readability

                    plt.tight_layout()
                    plt.show()
                else:
                    wx.LogError(f"X-axis or Y-axis column not found in the grid.")

            x_axis_dialog.Destroy()

        y_axis_dialog.Destroy()


if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame(None)
    frame.Show()
    app.MainLoop()
