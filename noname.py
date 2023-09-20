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

###########################################################################
## Class mainFrame
###########################################################################

class mainFrame ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 703,533 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		self.menuBar = wx.MenuBar( 0 )
		self.menuFile = wx.Menu()
		self.fileOpen = wx.MenuItem( self.menuFile, wx.ID_ANY, u"File Open", wx.EmptyString, wx.ITEM_NORMAL )
		self.menuFile.Append( self.fileOpen )

		self.menuBar.Append( self.menuFile, u"File" )

		self.SetMenuBar( self.menuBar )

		leftSizer = wx.GridSizer( 0, 2, 0, 0 )

		bSizer4 = wx.BoxSizer( wx.VERTICAL )

		bSizer13 = wx.BoxSizer( wx.HORIZONTAL )

		self.resetButton = wx.Button( self, wx.ID_ANY, u"Reset", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer13.Add( self.resetButton, 0, wx.ALL, 5 )

		self.searchButton = wx.Button( self, wx.ID_ANY, u"Search", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer13.Add( self.searchButton, 0, wx.ALL, 5 )


		bSizer4.Add( bSizer13, 0, wx.EXPAND, 5 )

		bSizer10 = wx.BoxSizer( wx.VERTICAL )

		self.m_scrolledWindow3 = wx.ScrolledWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL )
		self.m_scrolledWindow3.SetScrollRate( 5, 5 )
		bSizer10.Add( self.m_scrolledWindow3, 1, wx.EXPAND |wx.ALL, 5 )


		bSizer4.Add( bSizer10, 1, wx.EXPAND, 5 )


		leftSizer.Add( bSizer4, 1, wx.EXPAND, 5 )

		bSizer = wx.BoxSizer( wx.VERTICAL )

		self.m_grid1 = wx.grid.Grid( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

		# Grid
		self.m_grid1.CreateGrid( 5, 5 )
		self.m_grid1.EnableEditing( True )
		self.m_grid1.EnableGridLines( True )
		self.m_grid1.EnableDragGridSize( False )
		self.m_grid1.SetMargins( 0, 0 )

		# Columns
		self.m_grid1.EnableDragColMove( False )
		self.m_grid1.EnableDragColSize( True )
		self.m_grid1.SetColLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Rows
		self.m_grid1.EnableDragRowSize( True )
		self.m_grid1.SetRowLabelAlignment( wx.ALIGN_CENTER, wx.ALIGN_CENTER )

		# Label Appearance

		# Cell Defaults
		self.m_grid1.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
		bSizer.Add( self.m_grid1, 1, wx.ALL, 5 )


		leftSizer.Add( bSizer, 0, wx.EXPAND, 5 )

		bottomSizer = wx.BoxSizer( wx.VERTICAL )


		leftSizer.Add( bottomSizer, 1, wx.EXPAND, 5 )


		self.SetSizer( leftSizer )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


