import threading
import DobotDllType as dType
import time
import argparse
import json
from pprint import pprint
from collections import OrderedDict

class ScriptRobot():

    global CON_STR
    CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}
    
    def __init__(self,Json):
        self.Json=Json
        self.api=dType.load()
        self.state=""

    def Connect(self):
        #Connect Dobot
        self.state = dType.ConnectDobot(self.api, "", 115200)[0]
        dType.GetDeviceSN(self.api)
        dType.GetDeviceName(self.api)
        dType.GetDeviceVersion(self.api)
        dType.GetDeviceWithL(self.api)
        dType.GetPoseL(self.api)
        dType.GetKinematics(self.api)
        #dType.GetHOMEParams(self.api)
        print("Connect status:",CON_STR[self.state])
        if (self.state == dType.DobotConnect.DobotConnect_NoError):
            dType.SetQueuedCmdClear(self.api)
            return True
        else :
            dType.DisconnectDobot(self.api)
            return False
    """    
    def _MOVJ(self,data):
           dType.SetPTPCmd(self.api,dType.PTPMode.PTPMOVJXYZMode,float(data['X']),float(data['Y']),float(data['Z']),float(data['R']), isQueued = 1)
	
    def _MOVL(self,data):
           dType.SetPTPCmd(self.api,dType.PTPMode.PTPMOVLXYZMode,float(data['X']),float(data['Y']),float(data['Z']),float(data['R']), isQueued = 1)

    def _ARC(self,value,data):
           dType.SetARCCmd(self.api,[float(data['X']),float(data['Y']),float(data['Z']),0],[float(data['_X']),float(data['_Y']),float(data['_Z']),0], isQueued = 1)

    def moveTypes(self,value,data):
        if value=="MOVJ" :        
			return self._MOVJ(data)
        elif value=="MOVL" :        
            return self._MOVL(data)
        elif value=="ARC" :        
            return self._ARC(value,data)
    """
    def ParserMove(self):
        dType.SetQueuedCmdClear(self.api)
        json_data = open(self.Json)
        data = json.load(json_data, object_pairs_hook=OrderedDict)
       #def SetPTPCoordinateParams(api, xyzVelocity, xyzAcceleration, rVelocity,  rAcceleration,  isQueued=0):

        for move in data:
            #print "TEST_:"+data[move]['MotionStyle'],data[move]
            if data[move]['MotionStyle']=="MOVJ" :
                lastIndex=dType.SetPTPCmd(self.api,dType.PTPMode.PTPMOVJXYZMode,float(data[move]['X']),float(data[move]['Y']),float(data[move]['Z']),float(data[move]['R']), isQueued = 1)[0]
                dType.SetEndEffectorGripper(self.api, data[move]["Enabled"], data[move]['Gripper'], isQueued= 1)
                print(data[move]["Gripper"])
            if data[move]['PauseTime']!=0:
                lastIndex=dType.SetWAITCmd(self.api,float(data[move]['PauseTime']), isQueued = 1)[0]
            if data[move]['MotionStyle']=="MOVL" :        
                lastIndex=dType.SetPTPCmd(self.api,dType.PTPMode.PTPMOVLXYZMode,float(data[move]['X']),float(data[move]['Y']),float(data[move]['Z']),float(data[move]['R']), isQueued = 1)[0]
            if data[move]['MotionStyle']=="MOVJANGLE" :        
                lastIndex=dType.SetARCCmd(self.api,[float(data[move]['X']),float(data[move]['Y']),float(data[move]['Z']),0],[float(data[move]['_X']),float(data[move]['_Y']),float(data[move]['_Z']),0], isQueued = 1)[0]



        dType.SetQueuedCmdStartExec(self.api)

        while lastIndex > dType.GetQueuedCmdCurrentIndex(self.api)[0]:
#           dType.GetPose(self.api) Obtener la Posicion actual del robot
            dType.dSleep(100)

        dType.SetQueuedCmdStopExec(self.api)
        dType.GetKinematics(self.api)


        dType.DisconnectDobot(self.api)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script Robot')
    parser.add_argument('--Json', required=True, help='File name export json')
    args = parser.parse_args()
    R = ScriptRobot(args.Json)
    R.Connect()
    R.ParserMove()
