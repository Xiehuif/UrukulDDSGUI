import importlib.util
import sys

from PyQt6 import QtWidgets

import DeviceUI
from DeviceDatabaseAgent import AD9910Filter


class DeviceUIManager:

    def __init__(self, mainWindowLayout: QtWidgets.QLayout):
        self._mainWindow = mainWindowLayout
        self._widgetGroup: list[QtWidgets.QWidget] = []
        self._uiGroup: list[DeviceUI.Ui_Form] = []
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
        deviceUI = DeviceUI.Ui_Form()
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

class DeviceDatabaseAssetsManager:

    def __init__(self, targetFilter):
        self._dbPath = None
        self._targetModule = None
        self._targetFilter: AD9910Filter = targetFilter
        self._moduleName = 'ARTIQDeviceDatabase'

    def AppointNewDatabase(self, uiManager: DeviceUIManager):
        dialog = QtWidgets.QFileDialog()
        pathTuple = dialog.getOpenFileName()
        path = pathTuple[0]
        print(path)
        self._dbPath = path

        spec = importlib.util.spec_from_file_location(self._moduleName, self._dbPath)
        module = importlib.util.module_from_spec(spec)
        sys.modules[self._moduleName] = module
        spec.loader.exec_module(module)

        self._targetFilter.Read(module)
        print(self._targetFilter.FindAD9910s())
        uiManager.RefreshUI(self._targetFilter)

