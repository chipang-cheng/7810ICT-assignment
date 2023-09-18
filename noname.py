# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.dataview

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

		bSizer14 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_checkBox4 = wx.CheckBox( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer14.Add( self.m_checkBox4, 0, wx.ALL, 5 )

		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"fieldName", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		bSizer14.Add( self.m_staticText1, 0, wx.ALL, 5 )

		self.m_textCtrl1 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer14.Add( self.m_textCtrl1, 0, wx.ALL, 5 )


		bSizer4.Add( bSizer14, 1, wx.EXPAND, 5 )


		leftSizer.Add( bSizer4, 1, wx.EXPAND, 5 )

		bSizer = wx.BoxSizer( wx.VERTICAL )

		self.m_dataViewListCtrl4 = wx.dataview.DataViewListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer.Add( self.m_dataViewListCtrl4, 0, wx.ALL, 5 )


		leftSizer.Add( bSizer, 1, wx.EXPAND, 5 )

		bottomSizer = wx.BoxSizer( wx.VERTICAL )

		countSizer = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )

		countSizer.Add( self.m_staticText4, 0, wx.ALL, 5 )

		self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )

		countSizer.Add( self.m_staticText5, 0, wx.ALL, 5 )


		bottomSizer.Add( countSizer, 0, wx.EXPAND, 5 )


		leftSizer.Add( bottomSizer, 1, wx.EXPAND, 5 )


		self.SetSizer( leftSizer )
		self.Layout()

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


