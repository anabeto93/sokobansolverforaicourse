'''
Created on Sep 1, 2009

@author: zagnut
'''

from nxt.bluesock import BlueSock
from nxt.motor import *
from nxt.sensor import *

class NXTRobot():
    """ Basic NXT robot class. Contains functions to make the
    robot move, turn, stop.. """
    
    def __init__(self, host):
        self.socket = BlueSock(host)
        self.sensors = {}
        self.motor_left = None
        self.motor_right = None
        
    def host_found(self):
        """ returns true if the nxt robot with the mac address
        , given in the constructor, has been found """
        return self.socket
        
    def connect(self):
        """ connect to the robot """
        self.socket.connect()
    
    def disconnect(self):
        """ disconnect from the robot """
        self.socket.close()
    
    def move_forward(self, speed):
        """ move the robot forward at 'speed' """
        self._start_motor(self.motor_left, speed)
        self._start_motor(self.motor_right, speed)
    
    def move_stop(self):
        """ stop the robot """
        self._stop_motor(self.motor_left)
        self._stop_motor(self.motor_right)
    
    def _start_motor(self, motor, speed):
        """ start the given 'motor' running at 'speed' """
        motor.power = speed
        motor.mode = MODE_MOTOR_ON
        motor.run_state = RUN_STATE_RUNNING
        motor.tacho_limit = LIMIT_RUN_FOREVER
        motor.set_output_state()
        
    def _stop_motor(self, motor):
        """ stop the given 'motor' """
        motor.power = 0
        motor.mode = MODE_MOTOR_ON | MODE_BRAKE
        motor.run_state = RUN_STATE_RUNNING
        motor.tacho_limit = 0
        motor.set_output_state()

    def add_motor_left(self, port):
        """ add the left wheel motor the robot """
        self.motor_left = Motor(self.socket, port)
        
    def add_motor_right(self, port):
        """ add the right wheel motor the robot """
        self.motor_right = Motor(self.socket, port)
        
    def add_touch_sensor(self, name, port):
        """ add touch sensor to the robot """
        sensor = TouchSensor(self.socket, port)
        self.sensors[name] = sensor
    
    def add_light_sensor(self, name, port):
        """ add a light sensor to the robot """
        sensor = LightSensor(self.socket, port)
        self.sensors[name] = sensor
    
    def get_sensor(self, name):
        """ Returns the sensor with 'name' """
        return self.sensors[name]
        
if __name__ == '__main__':
    
    robot = NXTRobot('00:16:53:0A:56:10') 
    if robot.host_found():
        robot.connect()
        robot.add_touch_sensor('touch1', PORT_1)
        while True:
            if robot.get_sensor('touch1').get_sample():
                robot.move_forward(100)
                print 'Driving forward'
            else:
                robot.move_stop()
                print 'Stopped driving'
        robot.disconnect()
    else:
        print 'Unable to find robot'