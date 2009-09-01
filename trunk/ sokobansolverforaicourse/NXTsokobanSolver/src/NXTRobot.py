'''
Created on Sep 1, 2009

@author: zagnut
'''

from nxt.bluesock import BlueSock
from nxt.motor import *
from nxt.sensor import *

class NXTRobot():
    '''
    classdocs
    '''
    def __init__(self, host):
        self.socket = BlueSock(host)
        self.sensors = {}
        
    def HostFound(self):
        return self.socket
        
    def Connect(self):
        self.socket.connect()
    
    def Disconnect(self):
        self.socket.close()
    
    def SpinAround(self):
        self.motor.power = 100
        self.motor.mode = MODE_MOTOR_ON
        self.motor.run_state = RUN_STATE_RUNNING
        self.motor.tacho_limit = LIMIT_RUN_FOREVER
        self.motor.set_output_state()

    def StopSpin(self):
        self.motor.power = 0
        self.motor.mode = MODE_MOTOR_ON | MODE_BRAKE
        self.motor.run_state = RUN_STATE_RUNNING
        self.motor.tacho_limit = 0
        self.motor.set_output_state()

    def AddMotor(self, port):
        self.motor = Motor(self.socket, port)
        
    def AddSensor(self, port):
        pass
    
if __name__ == '__main__':
    robot = NXTRobot('00:16:53:0A:56:10') 
    if robot.HostFound():
        robot.Connect()
        touch = TouchSensor(x, PORT_1)
        while True:
            if touch.get_sample():
                robot.SpinAround()
                print 'span'
            else:
                robot.StopSpin()
                print 'span not'
        robot.Disconnect()
    else:
        print 'No NXT bricks found'