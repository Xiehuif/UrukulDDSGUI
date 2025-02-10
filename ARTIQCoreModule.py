from artiq.experiment import *
from artiq.coredevice.core import Core
from artiq.coredevice.urukul import CPLD
from artiq.coredevice.ad9910 import AD9910, PHASE_MODE_TRACKING, PHASE_MODE_CONTINUOUS
from artiq.language.environment import NumberValue, StringValue, BooleanValue


class Run9910(EnvExperiment):

    def prepare(self):
        # DDS Count
        self.ddsCount: int = 0
        for item in self.get_device_db():
            if self.get_device_db().get(item).get('class') == 'AD9910':
                self.ddsCount = self.ddsCount + 1
        # args
        totalCPLDKeys = ['0'] * self.ddsCount
        self.cpldKeys = []
        self.ddsKeys = ['0'] * self.ddsCount
        self.frequency = [0.0] * self.ddsCount
        self.phase = [0.0] * self.ddsCount
        self.amplitude = [0.0] * self.ddsCount
        self.switch = [0] * self.ddsCount
        # set cpld key and dds key
        index = 0
        for item in self.get_device_db():
            if self.get_device_db().get(item).get('class') == 'AD9910':
                targetCPLDKey = self.get_device_db().get(item).get('arguments').get('cpld_device')
                targetDDSKey = item
                totalCPLDKeys[index] = targetCPLDKey
                self.ddsKeys[index] = targetDDSKey
                index = index + 1
        self.cpldCount = 0
        for cpldKey in totalCPLDKeys:
            if cpldKey in totalCPLDKeys:
                self.cpldKeys.append(cpldKey)
                self.cpldCount = self.cpldCount + 1


    def build(self):
        self.core: Core = self.get_device("core")
        self.cpldDrivers = []
        self.ddsDrivers = []
        for cpldkey in self.cpldKeys:
            self.cpldDrivers.append(self.get_device(cpldkey))
        for i in range(self.ddsCount):
            key = self.ddsKeys[i]
            self.ddsDrivers.append(self.get_device(key))
            # args
            freq = self.get_argument('{}_freq'.format(key), NumberValue(default=100e6, type='float'))
            phase = self.get_argument('{}_phase'.format(key), NumberValue(default=0.0, type='float'))
            amp = self.get_argument('{}_amp'.format(key), NumberValue(default=1.0, type='float'))
            sw = self.get_argument('{}_sw'.format(key), NumberValue(default=0, type='int'))
            # set
            self.frequency[i] = freq
            self.phase[i] = phase
            self.amplitude[i] = amp
            self.switch[i] = sw

    @kernel
    def InitCPLD(self, cpldDriver: CPLD):
        self.core.break_realtime()
        cpldDriver.init()

    @kernel
    def InitDDS(self, ddsDriver: AD9910):
        self.core.break_realtime()
        ddsDriver.init()

    @kernel
    def run(self):
        self.core.reset()
        for driver in self.cpldDrivers:
            self.InitCPLD(driver)
        for i in range(self.ddsCount):
            driver: AD9910 = self.ddsDrivers[i]
            self.InitDDS(driver)
            if self.switch[i] == 0:
                driver.power_down()
                driver.cfg_sw(False)
            else:
                driver.cfg_sw(True)
                freq = self.frequency[i]
                phase = self.phase[i]
                amp = self.amplitude[i]
                self.core.break_realtime()
                driver.set(freq, phase, amp, PHASE_MODE_CONTINUOUS)




