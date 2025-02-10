import sys

from PyQt6 import QtCore,QtWidgets,QtGui
from PyQt6.QtWidgets import QApplication, QLayout

import DeviceDatabaseAgent
import MainView
import UIManager
import DeviceSingleToneUI

# deviceUI 250* 200

if __name__ == '__main__':

    # init
    app = QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    mainUI = MainView.Ui_mainWindow()
    mainUI.setupUi(mainWindow)
    mainWindow.setMaximumSize(0, 0)

    # data logic
    ddsFilter = DeviceDatabaseAgent.AD9910Filter()
    databaseManager = DeviceDatabaseAgent.DeviceDatabaseAssetsManager(ddsFilter)


    # ui
    deviceUIManager = UIManager.DeviceUIManager(mainUI.deviceLayout.layout())


    mainUI.addViewerAction.triggered.connect(lambda: deviceUIManager.AddDeviceUI(ddsFilter))
    mainUI.deleteViewerAction.triggered.connect(lambda: deviceUIManager.DeleteDeviceUI())
    mainUI.loadDeviceDatabaseAction.triggered.connect(lambda :databaseManager.AppointNewDatabase(deviceUIManager))

    mainWindow.show()
    sys.exit(app.exec())