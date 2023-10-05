import wx
import wx.xrc
import wx.dataview
import wx.grid
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from noname import mainFrame as mainFrame1, FileOpenDialog, YAxisDialog, \
    XAxisDialog, ChartPopup


class MyFrame(mainFrame1):

    def __init__(self, parent):
        super().__init__(parent)
        self.search_text = None
        self.log_action("Please select a CSV file to import.")
        self.checkboxes = []
        self.text_controls = []
        self.first_load = True
        self.checked_checkboxes = 0
        self.hideLayout()

    def hideLayout(self):
        self.m_scrolledWindow3.Hide()
        self.statsPanel.Hide()
        self.chart.Enable(False)
        self.searchButton.Hide()
        self.resetButton.Hide()
        self.m_grid1.Hide()

    def showLayout(self):
        self.m_scrolledWindow3.Show()
        self.statsPanel.Show()
        self.chart.Enable(True)
        self.searchButton.Show()
        self.resetButton.Show()
        self.m_grid1.Show()
        self.Layout()

    def OnOpen(self, event):
        openFileDialog = FileOpenDialog(self)
        if openFileDialog.ShowModal() == wx.ID_OK:
            selected_file = openFileDialog.GetPath()
            self.hideLayout()
            self.LoadCSV(selected_file)
            self.log_action(f"Opened file: {selected_file}")
        openFileDialog.Destroy()

    def LoadCSV(self, file_path):
        try:
            self.df = pd.read_csv(file_path)
            if not self.df.empty:
                rowsnum = len(self.df)
                self.df['ACCIDENT_DATE'] = pd.to_datetime(self.df['ACCIDENT_DATE'], format='%d/%m/%Y', errors='coerce')
                self.df['ACCIDENT_DATE'] = self.df['ACCIDENT_DATE'].dt.strftime('%d/%m/%Y')
                self.df['ACCIDENT_TIME'] = pd.to_datetime(self.df['ACCIDENT_TIME'], format='%H.%M.%S', errors='coerce')
                self.df['ACCIDENT_TIME'] = self.df['ACCIDENT_TIME'].dt.strftime('%H:%M:%S')
                self.df = self.df.fillna("Not specify")
                self.m_grid1.ClearGrid()
                self.m_grid1.DeleteRows(0, self.m_grid1.GetNumberRows())
                self.m_grid1.DeleteCols(0, self.m_grid1.GetNumberCols())
                self.m_grid1.AppendRows(len(self.df))
                self.m_grid1.AppendCols(len(self.df.columns))
                for i, col_name in enumerate(self.df.columns):
                    self.m_grid1.SetColLabelValue(i, col_name)

                for i, row in enumerate(self.df.itertuples(index=False), start=0):
                    for j, cell in enumerate(row):
                        self.m_grid1.SetCellValue(i, j, str(cell))
                    self.UpdateGauge(i + 1, rowsnum)
                self.AddControlsForColumns(self.df.columns)
                self.UpdateStatistics()
                self.first_load = True
                self.showLayout()
                self.log_action(f"Loaded CSV file: {file_path}")
        except Exception as e:
            wx.LogError(f"Error loading CSV file: {str(e)}")

    def AddControlsForColumns(self, columns):
        for child in self.m_scrolledWindow3.GetChildren():
            child.Destroy()
        self.checkboxes = []
        self.text_controls = []
        self.grid_sizer = wx.GridSizer(len(columns), 3, 0, 0)

        for col_index, col_name in enumerate(columns):
            if col_name in ['OBJECTID', 'ACCIDENT_NO']:
                continue
            checkbox = wx.CheckBox(self.m_scrolledWindow3, col_index * 10, "", wx.DefaultPosition, wx.DefaultSize, 0)
            self.grid_sizer.Add(checkbox, 0, wx.ALL, 5)
            self.checkboxes.append(checkbox)
            static_text = wx.StaticText(self.m_scrolledWindow3, wx.ID_ANY, col_name, wx.DefaultPosition, wx.DefaultSize,
                                        0)
            self.grid_sizer.Add(static_text, 0, wx.ALL, 5)
            text_ctrl = wx.TextCtrl(self.m_scrolledWindow3, col_index * 10 + 1, wx.EmptyString, wx.DefaultPosition,
                                    wx.DefaultSize, 0)
            self.grid_sizer.Add(text_ctrl, 1, wx.ALL | wx.EXPAND, 5)
            self.text_controls.append(text_ctrl)
            self.Bind(wx.EVT_CHECKBOX, self.OnCheckboxChange, checkbox)
        self.m_scrolledWindow3.SetSizer(self.grid_sizer)
        self.Layout()

    def OnCheckboxChange(self, event):
        self.checked_checkboxes = 0
        for checkbox in self.checkboxes:
            if checkbox.GetValue():
                self.checked_checkboxes += 1

    def SearchCSV(self, search_texts):
        selected_fields = []
        search_texts = []

        for checkbox, text_ctrl in zip(self.checkboxes, self.text_controls):
            if checkbox.GetValue():
                selected_fields.append(text_ctrl.GetId() // 10)
                search_texts.append(text_ctrl.GetValue())
        self.checked_checkboxes = len(selected_fields)
        if not selected_fields:
            filtered_data = self.df.copy()
            columns_to_display = list(self.df.columns)
        else:
            filtered_data = self.df.copy()
            columns_to_display = [self.df.columns[field] for field in selected_fields]
            for field, search_text in zip(selected_fields, search_texts):
                if search_text:
                    field_name = self.df.columns[field]
                    filtered_data = filtered_data[
                        filtered_data[field_name].str.contains(search_text, case=False, na=False)]
                    self.log_action(f"Searching for '{search_text}' in '{field_name}'")
        if filtered_data.empty:
            wx.LogError("No records found, please enter different value")
            return
        self.log_action(f"Search returned {len(filtered_data)} records" + "\n")
        if self.m_grid1.GetNumberCols() > 0:
            self.m_grid1.DeleteCols(0, self.m_grid1.GetNumberCols())
        self.m_grid1.DeleteRows(0, self.m_grid1.GetNumberRows())
        if not filtered_data.empty:
            self.m_grid1.AppendCols(len(columns_to_display))
            for i, col_name in enumerate(columns_to_display):
                self.m_grid1.SetColLabelValue(i, col_name)
            self.m_grid1.AppendRows(len(filtered_data))
            for i, row in enumerate(filtered_data.itertuples(index=False), start=0):
                for j, field in enumerate(selected_fields if selected_fields else range(len(self.df.columns))):
                    cell = row[field]
                    self.m_grid1.SetCellValue(i, j, str(cell))
                self.UpdateGauge(i + 1, len(filtered_data))
                self.first_load = False
        self.UpdateStatistics()
        self.Layout()

    def Reset(self, event):
        for checkbox in self.checkboxes:
            checkbox.SetValue(False)
        self.checked_checkboxes = 0

    def UpdateStatistics(self):
        if hasattr(self, 'df'):
            stats_data = []
            if self.first_load:
                self.statsText.SetValue("Statistics analysis will be available after the first load.")
            elif self.checked_checkboxes == 0:
                self.statsText.SetValue("Please check at least one checkbox for statistics analysis.")
            elif self.checked_checkboxes > 5:
                self.statsText.SetValue("Please check no more than five checkboxes for statistics analysis.")
            else:
                for col_index in range(self.m_grid1.GetNumberCols()):
                    col_name = self.m_grid1.GetColLabelValue(col_index)
                    if col_name not in ['OBJECTID', 'ACCIDENT_NO']:
                        if self.df[col_name].dtype == 'object':
                            header = f'{col_name}:'
                            unique_values = self.GetUniqueColumnValues(col_index)
                            for val, val_data in unique_values.items():
                                count = val_data['Count']
                                percentage = val_data['Percentage']
                                stats_data.append(
                                    {'Header': header, 'Value': val, 'Count': count, 'Percentage': percentage})
                stats = pd.DataFrame(stats_data)
                self.statsText.SetValue(stats.to_string(index=False))

    def CalculateStatistics(self):
        if hasattr(self, 'df'):
            stats_data = []
            num_cols = self.m_grid1.GetNumberCols()
            selected_fields = [text_ctrl.GetId() // 10 for text_ctrl in self.text_controls if text_ctrl.GetValue()]
            filtered_data = self.df.copy()
            if selected_fields:
                columns_to_display = [self.df.columns[field] for field in selected_fields]
                for field, search_text in zip(selected_fields,
                                              [text_ctrl.GetValue() for text_ctrl in self.text_controls]):
                    if search_text:
                        field_name = self.df.columns[field]
                        filtered_data = filtered_data[
                            filtered_data[field_name].str.contains(search_text, case=False, na=False)]
                for col_index in range(num_cols):
                    col_label = self.m_grid1.GetColLabelValue(col_index)
                    if col_label not in ['OBJECTID', 'ACCIDENT_NO'] and col_label in columns_to_display:
                        if self.df[col_label].dtype == 'object':
                            header = f'{col_label}:'
                            unique_values, value_counts = np.unique(filtered_data.iloc[:, col_index],
                                                                    return_counts=True)
                            for val, count in zip(unique_values, value_counts):
                                percentage = (count / len(filtered_data)) * 100
                                stats_data.append(
                                    {'Header': header, 'Value': val, 'Count': count, 'Percentage': percentage})
            stats = pd.DataFrame(stats_data)
            return stats
        return None

    def GetUniqueColumnValues(self, col_index):
        unique_values = {}
        if 0 <= col_index < self.m_grid1.GetNumberCols():
            selected_fields = [text_ctrl.GetId() // 10 for text_ctrl in self.text_controls if text_ctrl.GetValue()]
            filtered_data = self.df.copy()
            if selected_fields:
                for field, search_text in zip(selected_fields,
                                              [text_ctrl.GetValue() for text_ctrl in self.text_controls]):
                    if search_text:
                        field_name = self.df.columns[field]
                        filtered_data = filtered_data[
                            filtered_data[field_name].str.contains(search_text, case=False, na=False)]
            for row_index in range(self.m_grid1.GetNumberRows()):
                if 0 <= row_index < self.m_grid1.GetNumberRows():
                    cell_value = self.m_grid1.GetCellValue(row_index, col_index)
                    val_data = unique_values.get(cell_value, {'Count': 0, 'Percentage': 0.0})
                    val_data['Count'] += 1
                    unique_values[cell_value] = val_data
            total_count = sum(val_data['Count'] for val_data in unique_values.values())
            for key, val_data in unique_values.items():
                val_data['Percentage'] = round((val_data['Count'] / total_count) * 100, 2)
        return unique_values

    def GetColumnValueCount(self, col_index, value):
        count = 0
        if 0 <= col_index < self.m_grid1.GetNumberCols():
            for row_index in range(self.m_grid1.GetNumberRows()):
                if 0 <= row_index < self.m_grid1.GetNumberRows():
                    cell_value = self.m_grid1.GetCellValue(row_index, col_index)
                    if cell_value == value:
                        count += 1
        return count

    def GenerateChart(self, event):
        y_axis_choices = [col for col in self.df.columns if col not in ['ACCIDENT_DATE', 'ACCIDENT_TIME']]
        y_axis_dialog = YAxisDialog(self, y_axis_choices)
        if y_axis_dialog.ShowModal() == wx.ID_OK:
            y_axis_choice = y_axis_dialog.GetStringSelection()
            x_axis_choices = ["ACCIDENT_DATE", "ACCIDENT_TIME"]
            x_axis_dialog = XAxisDialog(self, x_axis_choices)
            if x_axis_dialog.ShowModal() == wx.ID_OK:
                x_axis_choice = x_axis_dialog.GetStringSelection()
                num_rows = self.m_grid1.GetNumberRows()
                num_cols = self.m_grid1.GetNumberCols()
                x_axis_col = None
                y_axis_col = None
                for col_index in range(num_cols):
                    col_label = self.m_grid1.GetColLabelValue(col_index)
                    if col_label == x_axis_choice:
                        x_axis_col = col_index
                    elif col_label == y_axis_choice:
                        y_axis_col = col_index
                if x_axis_col is not None and y_axis_col is not None:
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
                    if x_axis_choice == "ACCIDENT_DATE" and 'ACCIDENT_DATE' in self.df.columns:
                        date_values = pd.to_datetime(df['X'], format='%d/%m/%Y', errors='coerce')
                        date_diff = (date_values.max() - date_values.min()).days
                        if date_diff < 1:
                            x_date_format = "%d/%m/%Y"
                        elif date_diff <= 30:
                            x_date_format = "%d/%m"
                        elif date_diff <= 365:
                            x_date_format = "%m/%Y"
                        else:
                            x_date_format = "%Y"
                        df['X'] = date_values.dt.strftime(x_date_format)
                        grouped_data = df.groupby(['X', 'Y']).size().reset_index(name='Count')
                        fig, ax = plt.subplots(figsize=(8, 6))
                        unique_y_values = grouped_data['Y'].unique()
                        for y_value in unique_y_values:
                            y_data = grouped_data[grouped_data['Y'] == y_value]
                            ax.plot(y_data['X'], y_data['Count'], marker='o', label=f'{y_value}')
                        ax.set_xlabel(x_axis_choice)
                        ax.set_ylabel(f"{y_axis_choice} Count")
                        ax.set_title(f"Count by {x_axis_choice} for {y_axis_choice}")
                        ax.legend()
                        ax.grid(True)
                        ax.tick_params(axis='x', rotation=45)
                        fig.tight_layout()
                        chart_dialog = ChartPopup(self, fig, x_axis_choice, y_axis_choice)
                        chart_dialog.ShowModal()
                        self.log_action(f"Generated chart for Y-axis: {y_axis_choice}, X-axis: {x_axis_choice}")
                    elif x_axis_choice == "ACCIDENT_TIME" and 'ACCIDENT_DATE' in self.df.columns:
                        date_values = pd.to_datetime(self.df['ACCIDENT_DATE'] + ' ' + df['X'],
                                                     format='%d/%m/%Y %H:%M:%S',
                                                     errors='coerce')
                        df['Date'] = date_values.dt.date
                        df['Time'] = date_values.dt.time
                        df['Hour'] = date_values.dt.hour
                        date_range = (df['Date'].max() - df['Date'].min()).days
                        if date_range > 0:
                            df_grouped = df.groupby(['Hour', 'Y']).size().reset_index(name='Count')
                            df_grouped['Count'] = df_grouped.groupby('Hour')['Count'].transform(
                                lambda x: x / date_range)
                            fig, ax = plt.subplots(figsize=(8, 6))
                            for y_value in df_grouped['Y'].unique():
                                y_data = df_grouped[df_grouped['Y'] == y_value]
                                ax.plot(y_data['Hour'], y_data['Count'], marker='o', label=f'{y_value}')
                            ax.set_xlabel("Hour")
                            ax.set_ylabel(f"Average {y_axis_choice} Count")
                            ax.set_title(f"Average Count by Hour for {y_axis_choice}")
                            ax.legend()
                            ax.grid(True)
                            ax.set_xticks(range(24))
                            ax.tick_params(axis='x', rotation=45)
                            fig.tight_layout()
                            chart_dialog = ChartPopup(self, fig, x_axis_choice, y_axis_choice)
                            chart_dialog.ShowModal()
                            self.log_action(f"Generated chart for Y-axis: {y_axis_choice}, X-axis: {x_axis_choice}")
                else:
                    wx.LogError(f"X-axis or Y-axis column not found in the grid.")
                x_axis_dialog.Destroy()
            y_axis_dialog.Destroy()

    def UpdateGauge(self, current_value, max_value):
        if current_value >= max_value:
            self.m_gauge3.SetValue(100)
        else:
            progress = int((current_value / max_value) * 100)
            self.m_gauge3.SetValue(progress)

    def log_action(self, action_text):
        current_log = self.log_text.GetValue()
        new_log = current_log + action_text + "\n"
        self.log_text.SetValue(new_log)
        self.log_text.SetInsertionPointEnd()


if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame(None)
    frame.Show()
    app.MainLoop()
