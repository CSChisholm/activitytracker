"""
Copyright (C) 2023  Craig S. Chisholm

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit, QPushButton, QHBoxLayout, QListWidget, QVBoxLayout, QLabel, QGridLayout, QScrollArea, QComboBox
from pyqtgraph import PlotWidget, plot, mkPen

ITEMS_HEIGHT = 640
ITEMS_WIDTH = 300
PLOT_WIDTH = 1200

def itemField(label,value,unit):
    return {'label': label, 'value': value, 'unit': unit}

items = {'test1': [itemField('testObject1',373,'potatoes'), itemField('testObject2',413,'kg')], 'test2': [itemField('testObject1',373,'potatoes')]}

class mainWindow(QMainWindow):
    '''Main window'''
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Activity Logger')
        self.generalLayout = QHBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)
        self._createMenu()
        self._createItemsBox()
        self.DisplayItems()
        self.itemsBox.setCurrentRow(0)
        self._createFieldsBox()
        self._createPlotBox()
    
    def _createMenu(self):
        menu = self.menuBar().addMenu('&Menu')
        menu.addAction('&New', self._new)
        menu.addAction('&Open', self._open)
        menu.addAction('&Save', self._save)
        menu.addAction('&Save As', self._saveAs)
        menu.addAction('&Exit', self.close)
        helpMenu = self.menuBar().addMenu('&Help')
        helpMenu.addAction('&Information', self._helpPopUp)
    
    def _createItemsBox(self):
        itemsLayout = QVBoxLayout()
        itemsLayout.addWidget(QLabel('Activities'))
        self.itemsBox = QListWidget()
        self.itemsBox.setFixedHeight(ITEMS_HEIGHT)
        self.itemsBox.setFixedWidth(ITEMS_WIDTH)
        itemsLayout.addWidget(self.itemsBox)
        self.activityButton = QPushButton('Add activity')
        itemsLayout.addWidget(self.activityButton)
        self.generalLayout.addLayout(itemsLayout)
    
    def _createFieldsBox(self):
        fieldsLayout = QVBoxLayout()
        fieldFormScroll = QScrollArea(self)
        fieldFormScrollContents = QWidget()
        self.fieldForm = QGridLayout(fieldFormScrollContents)
        currentItem = self.itemsBox.currentItem()
        if currentItem is not None:
            editBoxes = {field['label']: QLineEdit() for field in items[currentItem.text()]}
            for row, field in enumerate(items[currentItem.text()]):
                editBoxes[field['label']].setText(str(field['value']))
                self.fieldForm.addWidget(QLabel(field['label']),row,0)
                self.fieldForm.addWidget(editBoxes[field['label']],row,1)
                self.fieldForm.addWidget(QLabel(field['unit']),row,2)
        fieldFormScroll.setWidget(fieldFormScrollContents)
        fieldFormScroll.setFixedHeight(ITEMS_HEIGHT)
        fieldFormScroll.setFixedWidth(ITEMS_WIDTH)
        fieldFormScroll.setAlignment(Qt.AlignmentFlag.AlignLeft)
        fieldsLayout.addWidget(fieldFormScroll)
        self.fieldButton = QPushButton('Add field')
        fieldsLayout.addWidget(self.fieldButton)
        fieldsLayout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.generalLayout.addLayout(fieldsLayout)
    
    def _createPlotBox(self):
        plotLayout = QVBoxLayout()
        self.PlotTitle = QLabel('')
        plotLayout.addWidget(self.PlotTitle)
        self.plotWidget = PlotWidget()
        self.plotWidget.setBackground('w')
        self.plotpen = mkPen(color=(0,0,0),width=3)
        self.plotWidget.setFixedHeight(ITEMS_HEIGHT)
        self.plotWidget.setFixedWidth(PLOT_WIDTH)
        plotControlWidget = QHBoxLayout()
        plotControlWidget.addWidget(QLabel('PlotRange:'))
        self.plotRange = QComboBox()
        plotControlWidget.addWidget(self.plotRange)
        self.plotRange.addItems(['Last 7 days', 'Last 30 days', 'All time'])
        self.plotButton = QPushButton('Plot')
        plotControlWidget.addWidget(self.plotButton)
        self.savePlotButton = QPushButton('Save Plot')
        plotControlWidget.addWidget(self.savePlotButton)
        plotLayout.addWidget(self.plotWidget)
        plotLayout.addLayout(plotControlWidget)
        plotLayout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.generalLayout.addLayout(plotLayout)
    
    def DisplayItems(self):
        for key in items.keys():
            self.itemsBox.addItem(key)
    
    def _new(self):
        return
    
    def _save(self):
        return
    
    def _saveAs(self):
        return
    
    def _open(self):
        return
    
    def _helpPopUp(self):
        self.hWindow = HelpWindow()
        self.hWindow.show()
    
    def closeEvent(self, event):
        QApplication.closeAllWindows()
        event.accept()

class HelpWindow(QWidget):
    '''General information called by Help menu'''
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        helpText = self._helpText()
        for line in helpText:
            label = QLabel(line)
            label.setOpenExternalLinks(True)
            layout.addWidget(label)
        self.closeButton = QPushButton('OK')
        layout.addWidget(self.closeButton)
        self.setLayout(layout)
        self.closeButton.clicked.connect(self.close)
    
    def _helpText(self):
        with open('helptext.txt','r') as f:
            lines = f.readlines()
        return lines
        

# class controller:
#     '''Controller module'''
#     def __init__(self,model,view):
#         self._evaluate = model
#         self._view = view
#         self._connectSignalsAndSlots

def main():
    '''Main loop'''
    elApp = QApplication([])
    elWindow = mainWindow()
    elWindow.show()
    sys.exit(elApp.exec())

if (__name__=='__main__'):
    main()