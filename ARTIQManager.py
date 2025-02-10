import ARTIQCoreModule
import ARTIQModifiedInterfaces
import ArgumentManager
import DeviceDatabaseAgent
import UIManager
from ArgumentManager import DDSSingleToneArgument

class ARTIQRunner:

    def __init__(self, argManager, databaseManager):
        self._argManager: ArgumentManager.DDSArgumentProfiles = argManager
        self._dbMgr: DeviceDatabaseAgent.DeviceDatabaseAssetsManager = databaseManager

    def Run(self):
        '''
        控制入口
        :return: None
        '''
        # 注意参数形式
        '''
            freq = self.get_argument('{}_freq'.format(key), NumberValue(default=100e6, type='float'))
            phase = self.get_argument('{}_phase'.format(key), NumberValue(default=0.0, type='float'))
            amp = self.get_argument('{}_amp'.format(key), NumberValue(default=1.0, type='float'))
            sw = self.get_argument('{}_sw'.format(key), NumberValue(default=0, type='int'))
        '''
        args = self._argManager.GetDatas()
        ARTIQRunnerArgs = {}
        for item in args:
            frequency = args.get(item).get(DDSSingleToneArgument.Frequency)
            phase = args.get(item).get(DDSSingleToneArgument.Phase)
            amp = args.get(item).get(DDSSingleToneArgument.Amplitude)
            sw = args.get(item).get(DDSSingleToneArgument.Switch)
            ARTIQRunnerArgs.update({'{}_freq'.format(item): frequency})
            ARTIQRunnerArgs.update({'{}_phase'.format(item): phase})
            ARTIQRunnerArgs.update({'{}_amp'.format(item): amp})
            ARTIQRunnerArgs.update({'{}_sw'.format(item): sw})
        ARTIQModifiedInterfaces.run(ARTIQCoreModule, ARTIQRunnerArgs, self._dbMgr.GetPath())

