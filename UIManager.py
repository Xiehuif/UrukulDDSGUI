import importlib.util
import sys

from PyQt6.QtWidgets import QLineEdit
from PyQt6 import QtWidgets, QtCore, QtGui

import ArgumentManager
import DeviceSingleToneUI
from DeviceDatabaseAgent import AD9910Filter


class DeviceUIManager:

    def __init__(self, mainWindowLayout: QtWidgets.QLayout):
        self._mainWindow = mainWindowLayout
        self._widgetGroup: list[QtWidgets.QWidget] = []
        self._uiGroup: list[DeviceSingleToneUI.Ui_Form] = []
        self._mainWindow.addStretch()
        self.AddDeviceUI()

    def _RefreshTargetUI(self, ui, filter):
        ui.targetDeviceComboBox.clear()
        for group in filter.FindAD9910s():
            for deviceKey in group.GetChannelKeys():
                ui.targetDeviceComboBox.addItem(deviceKey)

    def RefreshUI(self, filter: AD9910Filter):
        for ui in self._uiGroup:
            self._RefreshTargetUI(ui, filter)


    def AddDeviceUI(self, filter = None):
        widget = QtWidgets.QWidget()
        deviceUI = DeviceSingleToneUI.Ui_Form()
        deviceUI.setupUi(widget)
        self._mainWindow.insertWidget(len(self._widgetGroup), widget)
        self._widgetGroup.append(widget)
        self._uiGroup.append(deviceUI)
        if filter is None:
            return
        self._RefreshTargetUI(deviceUI, filter)

    def DeleteDeviceUI(self):
        if len(self._widgetGroup) == 1:
            return
        else:
            widget = self._widgetGroup.pop()
            ui = self._uiGroup.pop()
            self._mainWindow.removeWidget(widget)

    def GetWidgetNumber(self):
        return len(self._widgetGroup)

    def ArgumentParser(self):
        # only Single-Tone
        target = []
        for ui in self._uiGroup:
            # Get str
            targetDeviceKey = ui.targetDeviceComboBox.itemText()
            targetAmplitudeStr = ui.amplitudeValue.text()
            targetPhaseStr = ui.phaseValue.text()
            targetFrequencyStr = ui.frequencyValue.text()
            targetSwitchState = ui.enableCheckBox.checkState()

            # Get Unit
            targetFrequencyUnit = ui.frequencyUnitComboBox.itemText()

            # Convert type
            if targetSwitchState == QtCore.Qt.CheckState.Checked:
                switch = True
            else:
                switch = False
            amplitude = float(targetAmplitudeStr)
            phase = float(targetPhaseStr)
            frequency = float(targetFrequencyStr)
            if targetFrequencyUnit == 'MHz':
                print('used MHz')
                convertedFrequency = frequency * 1000000
            elif targetFrequencyUnit == 'KHz':
                print('used KHz')
                convertedFrequency = frequency * 1000

            # Generate
            currentDict = {
                ArgumentManager.DDSSingleToneArgument.DeviceKey : targetDeviceKey,
                ArgumentManager.DDSSingleToneArgument.Phase : phase,
                ArgumentManager.DDSSingleToneArgument.Frequency : convertedFrequency,
                ArgumentManager.DDSSingleToneArgument.Amplitude : amplitude,
                ArgumentManager.DDSSingleToneArgument.Switch : switch
            }

            target.append(currentDict)
        return target

