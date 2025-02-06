from artiq.coredevice.ad9910 import AD9910
from artiq.coredevice.urukul import CPLD


class DeviceReaderBase:

    def __init__(self):
        self._database = {}
        self._ip = '127.0.0.1'

    def Read(self, databaseModule):
        self._database: dict = databaseModule.device_db
        self._ip: str = databaseModule.core_addr

    def GetIPAddress(self) -> str:
        return self._ip

    def GetDeviceKeysByClass(self, targetDeviceClass) -> list:
        if targetDeviceClass is None:
            return []
        targetDeviceKeys = []
        targetClassName = targetDeviceClass.__name__
        for deviceStringKey in self._database:
            if self._database[deviceStringKey].get('class') == targetClassName:
                targetDeviceKeys.append(deviceStringKey)
        return targetDeviceKeys

    def GetDeviceData(self, key):
        return self._database.get(key)

class AD9910DriverGroup:
    def __init__(self, cpldController, channels):
        self._cpld = cpldController
        self._channels = channels

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        targetStr = 'cpld key:{} with dds:'.format(self._cpld)
        for key in self._channels:
            targetStr = targetStr + key + ';'
        return targetStr

    def GetChannelKeys(self):
        return self._channels

    def GetCPLDKey(self):
        return self._cpld

class AD9910Filter(DeviceReaderBase):

    def FindAD9910s(self) -> list[AD9910DriverGroup]:
        getAllDDSKeys = self.GetDeviceKeysByClass(AD9910)
        targetList: list[AD9910DriverGroup] = []
        buffer = {}
        for DDSKey in getAllDDSKeys:
            targetDDSData = self.GetDeviceData(DDSKey)
            cpldKey = targetDDSData['arguments']['cpld_device']
            if buffer.get(cpldKey) is None:
                buffer.update({cpldKey: []})
            buffer.get(cpldKey).append(DDSKey)
        for cpldKey in buffer:
            group = AD9910DriverGroup(cpldKey, buffer.get(cpldKey))
            targetList.append(group)
        return targetList

# for test only
if __name__ == '__main__':
    import device_db
    DDSFilter = AD9910Filter(device_db)
    deviceList = DDSFilter.FindAD9910s()
    for group in deviceList:
        print('found cpld: ' + group.GetCPLDKey())
        for channelKey in group.GetChannelKeys():
            print(channelKey)






