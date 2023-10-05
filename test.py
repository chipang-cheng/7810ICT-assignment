import unittest
import wx
import pandas as pd
import logging
from test_assignment2 import MyFrame as mframe

app = wx.App(False)
logging.basicConfig(level=logging.ERROR)

class TestMyFrame(unittest.TestCase):

    def setUp(self):
        self.frame = mframe(None)
        self.frame.Show(False)

    def tearDown(self):
        self.frame.Close(True)

    def test_LoadCSV(self,):
        empty_file_path = 'test.csv'
        self.frame.log_text.SetValue("")
        with self.assertLogs(level='ERROR'):
            self.frame.LoadCSV(empty_file_path)
        self.assertTrue(self.frame.first_load)
        file_path = 'Crash.csv'
        self.frame.LoadCSV(file_path)
        self.assertIsInstance(self.frame.df, pd.DataFrame)
        self.assertTrue(self.frame.first_load)
        self.assertTrue(self.frame.m_grid1.GetNumberRows() > 0)
        self.assertTrue(self.frame.m_grid1.GetNumberCols() > 0)

    def test_AddControlsForColumns(self):
        columns = ['Column1', 'Column2', 'Column3']
        self.frame.AddControlsForColumns(columns)
        self.assertEqual(len(self.frame.checkboxes), len(columns))
        self.assertEqual(len(self.frame.text_controls), len(columns))

    def test_OnCheckboxChange(self):
        checkbox = wx.CheckBox(self.frame.m_scrolledWindow3)
        checkbox.SetValue(True)
        self.frame.checkboxes = [checkbox]
        self.frame.OnCheckboxChange(None)
        self.assertEqual(self.frame.checked_checkboxes, 1)

    def test_SearchCSV(self):
        file_path = 'Crash.csv'
        self.frame.LoadCSV(file_path)
        invalid_input = 'InvalidInput'

        for checkbox in self.frame.checkboxes:
            checkbox.SetValue(True)
        with self.assertLogs(level='ERROR'):
            self.frame.SearchCSV([invalid_input])
        self.assertTrue(self.frame.first_load)

        self.assertGreater(self.frame.checked_checkboxes, 0)
        # Scenario 2: Search with checkboxes checked
        for checkbox in self.frame.checkboxes:
            checkbox.SetValue(True)
        self.frame.SearchCSV([])
        self.assertTrue(self.frame.m_grid1.GetNumberRows() > 0)
        self.assertEqual(self.frame.checked_checkboxes, len(self.frame.checkboxes))
        self.assertFalse(self.frame.first_load)

    def test_Reset(self):
        checkbox = wx.CheckBox(self.frame.m_scrolledWindow3)
        checkbox.SetValue(True)
        self.frame.checkboxes = [checkbox]
        self.frame.Reset(None)
        self.assertEqual(self.frame.checked_checkboxes, 0)

    def test_CalculateStatistics(self):
        file_path = 'Crash.csv'
        self.frame.LoadCSV(file_path)
        checkbox = wx.CheckBox(self.frame.m_scrolledWindow3)
        checkbox.SetValue(False)
        self.frame.checkboxes = [checkbox]
        stats = self.frame.CalculateStatistics()
        self.assertTrue(stats.empty)

        checkbox.SetValue(True)
        stats = self.frame.CalculateStatistics()
        self.assertIsInstance(stats, pd.DataFrame)

    def test_GetUniqueColumnValues(self):
        file_path = 'Crash.csv'
        self.frame.LoadCSV(file_path)
        unique_values = self.frame.GetUniqueColumnValues(0)
        self.assertIsInstance(unique_values, dict)

    def test_GetColumnValueCount(self):
        file_path = 'Crash.csv'
        self.frame.LoadCSV(file_path)
        count = self.frame.GetColumnValueCount(0, 'Value')
        self.assertIsInstance(count, int)

    def test_GenerateChart(self):
        file_path = 'Crash.csv'
        self.frame.LoadCSV(file_path)
        self.frame.log_text.SetValue("")
        invalid_header = 'InvalidHeader'
        self.frame.y_axis_choice = wx.ComboBox(self.frame)
        self.frame.y_axis_choice.SetStringSelection(invalid_header)

        with self.assertRaises(AssertionError) as context:
            self.frame.GenerateChart(None)
        self.assertIn(f"X-axis or Y-axis column not found in the grid.", str(context.exception))

        self.frame.y_axis_choice.SetStringSelection('Column1')
        self.frame.GenerateChart(None)
        self.assertEqual(self.frame.m_gauge3.GetValue(), 100)

    def test_UpdateGauge(self):
        max_value = 100
        self.frame.UpdateGauge(50, max_value)
        self.assertEqual(self.frame.m_gauge3.GetValue(), 50)

    def test_log_action(self):
        action_text = "Test action"
        self.frame.log_action(action_text)
        log_text = self.frame.log_text.GetValue()
        self.assertIn(action_text, log_text)

    def test_UpdateStatistics(self):
        # Scenario 1: First load
        self.frame.LoadCSV('Crash.csv')
        self.frame.UpdateStatistics()
        self.assertIn("Statistics analysis will be available after the first load.", self.frame.statsText.GetValue())

        # Scenario 2: No checkboxes checked
        self.checked_checkbox = 0
        self.frame.SearchCSV([])
        self.frame.UpdateStatistics()
        self.assertIn("Please check at least one checkbox for statistics analysis.", self.frame.statsText.GetValue())

        # Scenario 3: More than 5 checkboxes checked
        for checkbox in self.frame.checkboxes:
            checkbox.SetValue(True)
        self.frame.checked_checkboxes = 6  # Set to a value greater than 5
        self.frame.UpdateStatistics()
        self.assertIn("Please check no more than five checkboxes for statistics analysis.",
                      self.frame.statsText.GetValue())

        # Scenario 4: Valid statistics calculation
        self.frame.checked_checkboxes = 3  # Set to a valid value
        self.frame.UpdateStatistics()
        self.assertNotIn("Statistics analysis will be available after the first load.", self.frame.statsText.GetValue())
        self.assertNotIn("Please check at least one checkbox for statistics analysis.", self.frame.statsText.GetValue())
        self.assertNotIn("Please check no more than five checkboxes for statistics analysis.",
                         self.frame.statsText.GetValue())


if __name__ == '__main__':
    unittest.main()
