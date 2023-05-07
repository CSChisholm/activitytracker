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
import json
import os
import datetime
import copy
import numpy as np
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLineEdit, QPushButton, QHBoxLayout, QListWidget, QVBoxLayout, QLabel, QGridLayout, QScrollArea, QComboBox, QFileDialog, QDialog, QCalendarWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

def getVersion():
    with open('helptext.txt','r') as f:
        lines = f.readlines()
    for line in lines:
        if 'Version - ' in line:
            return line.split('Version - ')[-1].strip('\n')
VERSION_STRING = getVersion()

#Set geometry
ITEMS_HEIGHT = 450
ITEMS_WIDTH = 300
FIELDS_WIDTH = 300
PLOT_WIDTH = 600

#Set default directory
defaultDirectory = f'{os.path.expanduser("~")}/Documents/'

#File IO function
def loadFile(fileName: str) -> dict:
    with open(fileName,'r') as f:
        items = json.loads(f.read())
    return items

def saveFile(fileName: str, items: dict):
    with open(fileName,'w') as f:
        f.write(json.dumps(items))

def itemField(label: str, value: float, unit: str) -> dict:
    return {label: {'value': value, 'unit': unit}}

#GUI classes
class mainWindow(QMainWindow):
    '''Main window'''
    def __init__(self):
        super().__init__()
        self.items = {}
        self.itemsLoad = {}
        self.currentDirectory = defaultDirectory
        self.currentFile = ''
        self._setTitle()
        self.generalLayout = QHBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)
        self._createMenu()
        self._createItemsBox()
        self._displayItems()
        self._createFieldsBox()
        self._createPlotBox()
        self._displayFields()
    
    def _createMenu(self):
        menu = self.menuBar().addMenu('&Menu')
        menu.addAction('&New', self._new, shortcut='Ctrl+N')
        menu.addAction('&Open', self._open, shortcut='Ctrl+O')
        menu.addAction('&Save', self._save, shortcut='Ctrl+S')
        menu.addAction('&Save As', self._saveAs,shortcut='Ctrl+Shift+S')
        menu.addAction('&Exit', self.close, shortcut='Alt+F4')
        helpMenu = self.menuBar().addMenu('&Help')
        helpMenu.addAction('&Information', self._helpPopUp, shortcut='Ctrl+H')
    
    def _createItemsBox(self):
        itemsLayout = QVBoxLayout()
        self.cal0 = QCalendarWidget()
        itemsLayout.addWidget(self.cal0)
        self.currentDay = str(self.cal0.selectedDate().toJulianDay())
        self.itemsBox = QListWidget()
        self.itemsBox.setFixedHeight(ITEMS_HEIGHT)
        self.itemsBox.setFixedWidth(ITEMS_WIDTH)
        itemsLayout.addWidget(self.itemsBox)
        self.activityButton = QPushButton('Add activity')
        itemsLayout.addWidget(self.activityButton)
        self.generalLayout.addLayout(itemsLayout)
        self._new()
    
    def _createFieldsBox(self):
        fieldsLayout = QVBoxLayout()
        self.meanVal = QLabel('')
        self.maxVal = QLabel('')
        self.minVal = QLabel('')
        self.medianVal = QLabel('')
        self.stdVal = QLabel('')
        fieldsLayout.addWidget(self.meanVal)
        fieldsLayout.addWidget(self.maxVal)
        fieldsLayout.addWidget(self.minVal)
        fieldsLayout.addWidget(self.medianVal)
        fieldsLayout.addWidget(self.stdVal)
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
        self.editBoxes = {}
    
    def _createPlotBox(self):
        plotLayout = QVBoxLayout()
        calLayout = QHBoxLayout()
        self.cal1 = QCalendarWidget()
        self.cal2 = QCalendarWidget()
        calLayout.addWidget(self.cal1)
        calLayout.addWidget(self.cal2)
        plotLayout.addLayout(calLayout)
        self.figure = plt.figure()
        self.plotWidget = FigureCanvas(self.figure)
        self.plotWidget.setFixedHeight(ITEMS_HEIGHT)
        self.plotWidget.setFixedWidth(PLOT_WIDTH)
        plotControlWidget = QHBoxLayout()
        plotControlWidget.addWidget(QLabel('Plot Range:'))
        self.plotRange = QComboBox()
        plotControlWidget.addWidget(self.plotRange)
        self.plotRange.addItems(['Last 7 days', 'Last 30 days', 'All time', 'Custom'])
        plotControlWidget.addWidget(QLabel('Field:'))
        self.plotField = QComboBox()
        plotControlWidget.addWidget(self.plotField)
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
        for key in self.items[self.currentDay].keys():
            self.itemsBox.addItem(key)
        self.itemsBox.setCurrentRow(0)
    
    def _displayFields(self):
        fieldFormScrollContents = QWidget()
        self.fieldForm = QGridLayout(fieldFormScrollContents)
        currentItem = self.itemsBox.currentItem()
        if currentItem is not None:
            self.editBoxes = {key: QLineEdit() for key in self.items[self.currentDay][currentItem.text()].keys()}
            for row, key in enumerate(self.items[self.currentDay][currentItem.text()].keys()):
                self.editBoxes[key].setText(str(self.items[self.currentDay][currentItem.text()][key]['value']))
                self.fieldForm.addWidget(QLabel(key),row,0)
                self.fieldForm.addWidget(self.editBoxes[key],row,1)
                self.fieldForm.addWidget(QLabel(self.items[self.currentDay][currentItem.text()][key]['unit']),row,2)
        self.fieldFormScroll.setWidget(fieldFormScrollContents)
        self.plotField.clear()
        self.plotField.addItems(list(self.editBoxes.keys()))
    
    def _generatePlot(self):
        self.figure.clear()
        rangeSetting = self.plotRange.currentText()
        if rangeSetting=='All time':
            plotRangeKeys = sorted(list(self.items.keys()))
        else:
            endDay = QDate.currentDate().toJulianDay()
            if rangeSetting=='Last 7 days':
                startDay = endDay - 7
            elif rangeSetting=='Last 30 days':
                startDay = endDay - 30
            elif rangeSetting=='Custom':
                startDay = self.cal1.selectedDate().toJulianDay()
                endDay = self.cal2.selectedDate().toJulianDay()
            plotRangeKeys = [str(x) for x in range(startDay,endDay+1)]
        plotX = []
        plotY = []
        for key in plotRangeKeys:
            try:
                plotY.append(float(self.items[key][self.itemsBox.currentItem().text()][self.plotField.currentText()]['value']))
                plotX.append(float(key)-float(QDate.currentDate().toJulianDay()))
            except KeyError:
                pass
        ax = self.figure.add_subplot(111)
        ax.bar(plotX,plotY)
        ax.set_xlabel('Day')
        ax.set_ylabel(f'{self.plotField.currentText()} ({self.items[self.currentDay][self.itemsBox.currentItem().text()][self.plotField.currentText()]["unit"]})')
        self.plotWidget.draw()
        plotY = np.array([x for x in plotY if not x==0])
        self.meanVal.setText(f'Mean: {np.mean(plotY):.1f} {self.items[self.currentDay][self.itemsBox.currentItem().text()][self.plotField.currentText()]["unit"]}')
        self.maxVal.setText(f'Max: {max(plotY):.1f} {self.items[self.currentDay][self.itemsBox.currentItem().text()][self.plotField.currentText()]["unit"]}')
        self.minVal.setText(f'Min: {min(plotY):.1f} {self.items[self.currentDay][self.itemsBox.currentItem().text()][self.plotField.currentText()]["unit"]}')
        self.medianVal.setText(f'Median: {np.median(plotY):.1f} {self.items[self.currentDay][self.itemsBox.currentItem().text()][self.plotField.currentText()]["unit"]}')
        self.stdVal.setText(f'Standard deviation: {np.std(plotY):.1f} {self.items[self.currentDay][self.itemsBox.currentItem().text()][self.plotField.currentText()]["unit"]}')
    
    def _exportPlot(self):
        imName = QFileDialog.getSaveFileName(self,'',self.currentDirectory)[0]
        if imName[-4:]!='.png':
            imName+='.png'
        plt.savefig(imName)
    
    def _addActivity(self):
        self.activityDialogue = activityDialogue(self)
        self.activityDialogue.setWindowTitle('New Activity')
        self.activityDialogue.setWindowModality(Qt.ApplicationModal)
        self.activityDialogue.show()
    
    def _addField(self):
        self.fieldDialogue = fieldDialogue(self)
        self.fieldDialogue.setWindowTitle('New Field')
        self.fieldDialogue.setWindowModality(Qt.ApplicationModal)
        self.fieldDialogue.show()
    
    def _updateFields(self):
        currentItem = self.itemsBox.currentItem().text()
        for key in self.editBoxes.keys():
            self.items[self.currentDay][currentItem][key]['value'] = float(self.editBoxes[key].text())
    
    def _changeDay(self):
        self.currentDay = str(self.cal0.selectedDate().toJulianDay())
        if not self.currentDay in self.items.keys():
            self.items[self.currentDay] = self._copyDay()
        self._displayItems()
        self._displayFields()
    
    def _copyDay(self):
        today = QDate.currentDate().toJulianDay()
        mostRecentDay = str(max([int(key) for key in self.items.keys() if int(key)<=today]))
        newDay = {}
        for itemKey in self.items[mostRecentDay].keys():
            newDay.update({itemKey: {}})
            for fieldKey in self.items[mostRecentDay][itemKey].keys():
                newDay[itemKey].update(itemField(fieldKey,0,self.items[mostRecentDay][itemKey][fieldKey]['unit']))
        return newDay
    
    def _new(self):
        if self.itemsLoad!=self.items:
            self._unsavedChanges()
        else:
            self.saveFirst = False
            self.openOK = True
        if self.saveFirst:
            if not self.currentFile=='':
                self._save()
            else:
                self._saveAs()
        if self.openOK:
            self.items = {self.currentDay: {}}
            self.itemsLoad = copy.deepcopy(self.items)
            try:
                self._displayItems()
                self._displayFields()
            except AttributeError: #Still initialising
                pass
    
    def _save(self):
        if not self.currentFile=='':
            saveFile(self.currentFile,self.items)
        else:
            saveFile(f'{self.currentDirectory}activitytracker_{datetime.datetime.now().strftime("%Y-%m-%d_%I:%M%p")}.json',self.items)
        self.itemsLoad = copy.deepcopy(self.items)
        
    
    def _saveAs(self):
        fileName = QFileDialog.getSaveFileName(self,'',self.currentDirectory)[0]
        if not fileName=='':
            self.currentFile = fileName
            self.currentDirectory = fileName[:-len(fileName.split('/')[-1])]
            saveFile(fileName,self.items)
            self._setTitle()
            self.itemsLoad = copy.deepcopy(self.items)
    
    def _open(self):
        if self.itemsLoad!=self.items:
            self._unsavedChanges()
        else:
            self.saveFirst = False
            self.openOK = True
        if self.saveFirst:
            if not self.currentFile=='':
                self._save()
            else:
                self._saveAs()
        if self.openOK:
            fileName = QFileDialog.getOpenFileName(self,'',self.currentDirectory)[0]
            if not fileName=='':
                try:
                    self.cal0.setSelectedDate(QDate.currentDate())
                    self.currentDay = str(self.cal0.selectedDate().toJulianDay())
                    self.items = loadFile(fileName)
                    if not self.currentDay in self.items.keys():
                        self.items[self.currentDay] = self._copyDay()
                    self.itemsLoad = copy.deepcopy(self.items)
                    self._displayItems()
                    self._displayFields()
                    self.currentFile = fileName
                    self.currentDirectory = fileName[:-len(fileName.split('/')[-1])]
                    self._setTitle()
                except Exception:
                    pass
    
    def _helpPopUp(self):
        self.hWindow = helpWindow()
        self.hWindow.setWindowTitle(f'Activity Logger {VERSION_STRING} - Information')
        self.hWindow.show()
    
    def _unsavedChanges(self):
        self.wWindow = warningWindow(self)
        self.wWindow.setWindowTitle('Unsaved Changes')
        self.wWindow.setWindowModality(Qt.ApplicationModal)
        self.wWindow.exec_()
    
    def _setTitle(self):
        self.setWindowTitle(f'Activity Logger {VERSION_STRING} - {self.currentDirectory}')
    
    def closeEvent(self, event):
        self.saveFirst = False
        self.openOK = True
        if self.itemsLoad!=self.items:
            event.ignore()
            self._unsavedChanges()
        if self.saveFirst:
            if not self.currentFile=='':
                self._save()
            else:
                self._saveAs()
        if self.openOK:
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

class warningWindow(QDialog):
    '''Project change warning dialogue'''
    def __init__(self,parent):
        super().__init__()
        self.parent = parent
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Warning, project has been modified. Save changes?'))
        buttonsLayout = QHBoxLayout()
        self.acceptButton = QPushButton('Yes')
        self.noButton = QPushButton('No')
        self.cancelButton = QPushButton('Cancel')
        buttonsLayout.addWidget(self.acceptButton)
        buttonsLayout.addWidget(self.noButton)
        buttonsLayout.addWidget(self.cancelButton)
        layout.addLayout(buttonsLayout)
        self.setLayout(layout)
        self.noButton.clicked.connect(self._noClick)
        self.cancelButton.clicked.connect(self._cancelClick)
        self.acceptButton.clicked.connect(self._acceptClick)
    
    def _acceptClick(self):
        self.parent.openOK = True
        self.parent.saveFirst = True
        self.close()
    
    def _noClick(self):
        self.parent.openOK = True
        self.parent.saveFirst = False
        self.close()
    
    def _cancelClick(self):
        self.parent.openOK = False
        self.parent.saveFirst = False
        self.close()

class activityDialogue(QDialog):
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
        if (qText in self.parent.items[self.parent.currentDay].keys() or not len(qText)):
            return
        else:
            self.parent.items[self.parent.currentDay].update({qText: {}})
            self.parent._displayItems()
            self.close()

class fieldDialogue(QDialog):
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
        if not labelText in self.parent.items[self.parent.currentDay][itemKey].keys():
            try:
                self.parent.items[self.parent.currentDay][itemKey].update(itemField(labelText,float(valueText),unitText))
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
        self._view.cal0.selectionChanged.connect(self._view._changeDay)
        self._view.plotButton.clicked.connect(self._view._generatePlot)
        self._view.savePlotButton.clicked.connect(self._view._exportPlot)

def main():
    '''Main loop'''
    elApp = QApplication([])
    elWindow = mainWindow()
    elWindow.show()
    controller(model=None,view=elWindow)
    sys.exit(elApp.exec())

if (__name__=='__main__'):
    main()
