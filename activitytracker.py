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
from functools import partial
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit, QPushButton, QHBoxLayout, QListWidget, QVBoxLayout, QLabel, QGridLayout, QScrollArea, QComboBox
from pyqtgraph import PlotWidget, plot, mkPen

ITEMS_HEIGHT = 500
ITEMS_WIDTH = 150
FIELDS_WIDTH = 300
PLOT_WIDTH = 600

def itemField(label,value,unit):
    return {label: {'value': value, 'unit': unit}}

items = {'test1': {**itemField('testObject1',373,'potatoes'), **itemField('testObject2',413,'kg')}, 'test2': itemField('testObject1',118,'potatoes')}

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
        self._displayItems()
        self._createFieldsBox()
        self._displayFields()
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
        self.fieldFormScroll = QScrollArea(self)
        self.fieldFormScroll.setFixedHeight(ITEMS_HEIGHT)
        self.fieldFormScroll.setFixedWidth(FIELDS_WIDTH)
        self.fieldFormScroll.setAlignment(Qt.AlignmentFlag.AlignLeft)
        fieldsLayout.addWidget(self.fieldFormScroll)
        fieldButtons = QHBoxLayout()
        self.fieldButton = QPushButton('Add field')
        fieldButtons.addWidget(self.fieldButton)
        self.updateButton = QPushButton('Update fields')
        fieldButtons.addWidget(self.updateButton)
        fieldsLayout.addLayout(fieldButtons)
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
    
    def _displayItems(self):
        self.itemsBox.clear()
        for key in items.keys():
            self.itemsBox.addItem(key)
        self.itemsBox.setCurrentRow(0)
    
    def _displayFields(self):
        fieldFormScrollContents = QWidget()
        self.fieldForm = QGridLayout(fieldFormScrollContents)
        currentItem = self.itemsBox.currentItem()
        if currentItem is not None:
            self.editBoxes = {key: QLineEdit() for key in items[currentItem.text()].keys()}
            for row, key in enumerate(items[currentItem.text()].keys()):
                self.editBoxes[key].setText(str(items[currentItem.text()][key]['value']))
                self.fieldForm.addWidget(QLabel(key),row,0)
                self.fieldForm.addWidget(self.editBoxes[key],row,1)
                self.fieldForm.addWidget(QLabel(items[currentItem.text()][key]['unit']),row,2)
        self.fieldFormScroll.setWidget(fieldFormScrollContents)
    
    def _addActivity(self):
        self.activityDialogue = activityDialogue(self)
        self.activityDialogue.show()
    
    def _addField(self):
        self.fieldDialogue = fieldDialogue(self)
        self.fieldDialogue.show()
    
    def _updateFields(self):
        currentItem = self.itemsBox.currentItem().text()
        for key in self.editBoxes.keys():
            items[currentItem][key]['value'] = float(self.editBoxes[key].text())
    
    def _new(self):
        return
    
    def _save(self):
        return
    
    def _saveAs(self):
        return
    
    def _open(self):
        return
    
    def _helpPopUp(self):
        self.hWindow = helpWindow()
        self.hWindow.show()
    
    def closeEvent(self, event):
        QApplication.closeAllWindows()
        event.accept()

class helpWindow(QWidget):
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

class activityDialogue(QWidget):
    '''Add new Activity type'''
    def __init__(self,parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()
        entryFieldLayout = QHBoxLayout()
        entryFieldLayout.addWidget(QLabel('Name:'))
        self.textBox = QLineEdit()
        entryFieldLayout.addWidget(self.textBox)
        layout.addLayout(entryFieldLayout)
        buttons = QHBoxLayout()
        self.acceptButton = QPushButton('OK')
        buttons.addWidget(self.acceptButton)
        self.cancelButton = QPushButton('Cancel')
        buttons.addWidget(self.cancelButton)
        layout.addLayout(buttons)
        self.setLayout(layout)
        self.acceptButton.clicked.connect(self._accept)
        self.cancelButton.clicked.connect(self.close)
    
    def _accept(self):
        qText = self.textBox.text()
        if (qText in items.keys() or not len(qText)):
            return
        else:
            items.update({qText: {}})
            self.parent._displayItems()
            self.close()

class fieldDialogue(QWidget):
    '''Add fields to activity'''
    def __init__(self,parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()
        entryFieldLayout = QHBoxLayout()
        entryFieldLayout.addWidget(QLabel('Label:'))
        self.labelBox = QLineEdit()
        entryFieldLayout.addWidget(self.labelBox)
        entryFieldLayout.addWidget(QLabel('Value:'))
        self.valueBox = QLineEdit()
        entryFieldLayout.addWidget(self.valueBox)
        entryFieldLayout.addWidget(QLabel('Unit:'))
        self.unitBox = QLineEdit()
        entryFieldLayout.addWidget(self.unitBox)
        layout.addLayout(entryFieldLayout)
        buttons = QHBoxLayout()
        self.acceptButton = QPushButton('OK')
        buttons.addWidget(self.acceptButton)
        self.cancelButton = QPushButton('Cancel')
        buttons.addWidget(self.cancelButton)
        layout.addLayout(buttons)
        self.setLayout(layout)
        self.acceptButton.clicked.connect(self._accept)
        self.cancelButton.clicked.connect(self.close)
    
    def _accept(self):
        labelText = self.labelBox.text()
        valueText = self.valueBox.text()
        unitText = self.unitBox.text()
        itemKey = self.parent.itemsBox.currentItem().text()
        if not labelText in items[itemKey].keys():
            try:
                items[itemKey].update(itemField(labelText,float(valueText),unitText))
                self.parent._displayFields()
            except Exception:
                pass
            self.close()
        else:
            return

class controller:
    '''Controller module'''
    def __init__(self,model,view):
        self._evaluate = model
        self._view = view
        self._connectSignalsAndSlots()
    
    def _connectSignalsAndSlots(self):
        self._view.activityButton.clicked.connect(self._view._addActivity)
        self._view.itemsBox.currentItemChanged.connect(self._view._displayFields)
        self._view.fieldButton.clicked.connect(self._view._addField)
        self._view.updateButton.clicked.connect(self._view._updateFields)

def main():
    '''Main loop'''
    elApp = QApplication([])
    elWindow = mainWindow()
    elWindow.show()
    controller(model=None,view=elWindow)
    sys.exit(elApp.exec())

if (__name__=='__main__'):
    main()
