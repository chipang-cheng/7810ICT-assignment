# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.grid
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar


###########################################################################
## Class mainFrame
###########################################################################

class mainFrame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"2810ICT/7810ICT Group42 assignment2 - Analysis tools ",
                          pos=wx.DefaultPosition, size=wx.Size(703, 533),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetForegroundColour(wx.Colour(53, 56, 57))
        self.SetBackgroundColour(wx.Colour(244, 250, 255))

        self.menuBar = wx.MenuBar(0)
        self.menuFile = wx.Menu()
        self.fileOpen = wx.MenuItem(self.menuFile, wx.ID_ANY, u"File Open", wx.EmptyString, wx.ITEM_NORMAL)
        self.menuFile.Append(self.fileOpen)

        self.chart = wx.MenuItem(self.menuFile, wx.ID_ANY, u"Generate Chart", wx.EmptyString, wx.ITEM_NORMAL)
        self.menuFile.Append(self.chart)

        self.menuBar.Append(self.menuFile, u"File")

        self.SetMenuBar(self.menuBar)

        leftSizer = wx.GridSizer(0, 2, 0, 0)

        bSizer4 = wx.BoxSizer(wx.VERTICAL)

        bSizer13 = wx.BoxSizer(wx.HORIZONTAL)

        self.resetButton = wx.Button(self, wx.ID_ANY, u"Reset", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer13.Add(self.resetButton, 0, wx.ALL, 5)

        self.searchButton = wx.Button(self, wx.ID_ANY, u"Search", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer13.Add(self.searchButton, 0, wx.ALL, 5)

        bSizer4.Add(bSizer13, 0, wx.EXPAND, 5)

        bSizer10 = wx.BoxSizer(wx.VERTICAL)

        self.m_scrolledWindow3 = wx.ScrolledWindow(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                                   wx.HSCROLL | wx.VSCROLL)
        self.m_scrolledWindow3.SetScrollRate(5, 5)
        self.m_scrolledWindow3.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        grid_sizer = wx.GridSizer(0, 2, 0, 0)

        self.m_scrolledWindow3.SetSizer(grid_sizer)
        self.m_scrolledWindow3.Layout()
        grid_sizer.Fit(self.m_scrolledWindow3)
        bSizer10.Add(self.m_scrolledWindow3, 1, wx.EXPAND | wx.ALL, 5)

        bSizer4.Add(bSizer10, 1, wx.EXPAND, 5)

        leftSizer.Add(bSizer4, 1, wx.EXPAND, 5)

        bSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.m_grid1 = wx.grid.Grid(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)

        # Grid
        self.m_grid1.CreateGrid(5, 5)
        self.m_grid1.EnableEditing(True)
        self.m_grid1.EnableGridLines(True)
        self.m_grid1.EnableDragGridSize(False)
        self.m_grid1.SetMargins(0, 0)

        # Columns
        self.m_grid1.EnableDragColMove(False)
        self.m_grid1.EnableDragColSize(True)
        self.m_grid1.SetColLabelAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)

        # Rows
        self.m_grid1.EnableDragRowSize(True)
        self.m_grid1.SetRowLabelAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)

        # Label Appearance
        self.m_grid1.SetLabelBackgroundColour(wx.Colour(222, 231, 231))

        # Cell Defaults
        self.m_grid1.SetDefaultCellAlignment(wx.ALIGN_LEFT, wx.ALIGN_TOP)
        bSizer.Fit(self.m_grid1)
        bSizer.Add(self.m_grid1, 1, wx.ALL, 5)

        leftSizer.Add(bSizer, 0, wx.EXPAND, 5)

        bottomSizer = wx.BoxSizer(wx.VERTICAL)

        self.statsPanel = wx.Panel(self)
        self.statsText = wx.TextCtrl(self.statsPanel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.statsSizer = wx.BoxSizer(wx.VERTICAL)
        self.statsSizer.Add(self.statsText, 1, wx.EXPAND)
        self.statsPanel.SetSizer(self.statsSizer)

        bottomSizer.Add(self.statsPanel, 1, wx.EXPAND | wx.ALL, 5)

        leftSizer.Add(bottomSizer, 1, wx.EXPAND, 5)

        bSizer6 = wx.BoxSizer(wx.VERTICAL)

        self.m_scrolledWindow2 = wx.ScrolledWindow(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                                   wx.HSCROLL | wx.VSCROLL)
        self.m_scrolledWindow2.SetScrollRate(5, 5)

        # Create a sizer for self.m_scrolledWindow2
        scrolled_window2_sizer = wx.BoxSizer(wx.VERTICAL)

        self.log_text = wx.TextCtrl(self.m_scrolledWindow2, wx.ID_ANY, "", wx.DefaultPosition, wx.DefaultSize,
                                    wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL)
        scrolled_window2_sizer.Add(self.log_text, 1, wx.ALL | wx.EXPAND, 5)

        self.m_scrolledWindow2.SetSizer(scrolled_window2_sizer)
        self.m_scrolledWindow2.Layout()

        bSizer6.Add(self.m_scrolledWindow2, 1, wx.ALL | wx.EXPAND, 5)

        self.m_gauge3 = wx.Gauge(self, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL)
        self.m_gauge3.SetValue(0)
        gauge_sizer = wx.BoxSizer(wx.VERTICAL)
        gauge_sizer.Add(self.m_gauge3, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
        bSizer6.Add(gauge_sizer, 0, wx.ALL | wx.ALIGN_RIGHT, 0)

        leftSizer.Add(bSizer6, 1, wx.EXPAND, 5)

        self.SetSizer(leftSizer)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.Bind(wx.EVT_MENU, self.OnOpen, id=self.fileOpen.GetId())
        self.Bind(wx.EVT_MENU, self.GenerateChart, id=self.chart.GetId())
        self.resetButton.Bind(wx.EVT_BUTTON, self.Reset)
        self.searchButton.Bind(wx.EVT_BUTTON, self.SearchCSV)

    def __del__(self):
        pass

    # Virtual event handlers, override them in your derived class
    def OnOpen(self, event):
        event.Skip()

    def GenerateChart(self, event):
        event.Skip()

    def Reset(self, event):
        event.Skip()

    def SearchCSV(self, event):
        event.Skip()


class FileOpenDialog(wx.FileDialog):
    def __init__(self, parent):
        super().__init__(
            parent,
            "Open a file",
            "",
            "",
            "CSV files (*.csv)|*.csv",
            wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        )

    def __del__(self):
        pass


class YAxisDialog(wx.SingleChoiceDialog):
    def __init__(self, parent, choices):
        super().__init__(
            parent,
            "Select Y-axis column:",
            "Y-axis Selection",
            choices
        )

    def __del__(self):
        pass


class XAxisDialog(wx.SingleChoiceDialog):
    def __init__(self, parent, choices):
        super().__init__(
            parent,
            "Select X-axis:",
            "X-axis Selection",
            choices
        )

    def __del__(self):
        pass


class ChartPopup(wx.Dialog):
    def __init__(self, parent, figure, x_label, y_label):
        super(ChartPopup, self).__init__(parent, wx.ID_ANY, "Chart", size=(1000, 800),
                                         style=wx.DEFAULT_DIALOG_STYLE|wx.MAXIMIZE_BOX)

        self.figure = figure
        self.canvas = FigureCanvas(self, wx.ID_ANY, self.figure)

        self.toolbar = NavigationToolbar(self.canvas)
        self.toolbar.Realize()

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.toolbar, 0, wx.EXPAND)
        sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)

        self.SetSizer(sizer)
        self.Fit()

