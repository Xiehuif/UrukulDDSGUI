from copy import deepcopy
from enum import Enum

import UIManager


class DDSSingleToneArgument(Enum):
    Amplitude = 0
    Frequency = 1
    Phase = 2
    DeviceKey = 3
    Switch = 4

class DDSArgumentProfiles:

    def __init__(self):
        self._profiles = {}

    def SetData(self, deviceKey: str, data):
        self._profiles.update({deviceKey: data})

    def GetDatas(self):
        return deepcopy(self._profiles)

    def Clear(self):
        self._profiles = {}

    def ReadFromUI(self, deviceUIManager: UIManager.DeviceUIManager):
        datas = deviceUIManager.ArgumentParser()
        for data in datas:
            deviceKey = data.get(DDSSingleToneArgument.DeviceKey)
            args = {}
            for item in DDSSingleToneArgument:
                if item == DDSSingleToneArgument.DeviceKey:
                    continue
                else:
                    args.update({item: data.get(item)})
            self.SetData(deviceKey, args)