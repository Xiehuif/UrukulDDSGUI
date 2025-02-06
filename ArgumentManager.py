from copy import deepcopy
from enum import Enum


class DDSArgument(Enum):
    Amplitude = 0
    Frequency = 1
    Phase = 2
    DeviceKey = 3

class DDSArgumentProfiles:

    def __init__(self):
        self._profiles = {}

    def SetData(self, deviceKey: str, data):
        self._profiles.update({deviceKey: data})

    def GetDatas(self):
        return deepcopy(self._profiles)

    def Clear(self):
        self._profiles = {}