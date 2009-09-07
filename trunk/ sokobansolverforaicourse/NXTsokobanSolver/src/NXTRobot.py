'''
Created on Sep 1, 2009

@author: zagnut
'''

from nxt.bluesock import BlueSock
from nxt.motor import * #IGNORE:W0614
from nxt.sensor import * #IGNORE:W0614
import pygame
from pygame.locals import *

class NXTRobot():
    """ Basic NXT robot class. Contains functions to make the
    robot move, turn, stop.. """
    
    def __init__(self, host):
        self.socket = BlueSock(host).connect()
        self.sensors = {}
        self.motor_left = None
        self.motor_right = None
        self.motor_hook = None
        
    def host_found(self):
        """ returns true if the nxt robot with the mac address
        , given in the constructor, has been found """
        return self.socket
        
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
    
    def _start_motor(self, motor, speed): #IGNORE:R0201
        """ start the given 'motor' running at 'speed' """
        motor.power = speed
        motor.mode = MODE_MOTOR_ON
        motor.run_state = RUN_STATE_RUNNING
        motor.tacho_limit = LIMIT_RUN_FOREVER
        motor.set_output_state()
        
    def _stop_motor(self, motor): #IGNORE:R0201
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
        
    def add_motor_hook(self, port):
        self.motor_hook = Motor(self.socket, port)
        #self.motor_hook.tacho_count = 0
        self.motor_hook.power = -100
        self.motor_hook.mode = MODE_MOTOR_ON | MODE_BRAKE
        self.motor_hook.run_state = RUN_STATE_RUNNING
        self.motor_hook.tacho_limit = 0
        for i in xrange(200): 
            self.motor_hook.set_output_state()  
        self.motor_hook.reset_position(0)
        self.motor_hook.set_output_state()
        
    def hook_grab(self):
        self.motor_hook.power = 100
        self.motor_hook.mode = MODE_MOTOR_ON | MODE_BRAKE
        self.motor_hook.run_state = RUN_STATE_RUNNING
        self.motor_hook.tacho_limit = -2000
        self.motor_hook.set_output_state()        
    
    def hook_stop(self):
        self.motor_hook.power = 0
        self.motor_hook.mode = MODE_MOTOR_ON | MODE_BRAKE
        self.motor_hook.run_state = RUN_STATE_RUNNING
        self.motor_hook.tacho_limit = -2000
        self.motor_hook.set_output_state() 
        
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
    
class Movement():
    def __init__(self, physicalMover, virtualMover):       
        self.physicalMover = physicalMover
        self.virtualMover = virtualMover
        
    def move_forward(self):
        if self.physicalMover != None:
            self.physicalMover.move_forward()
        if self.virtualMover != None:
            self.virtualMover.move_forward()

class Mover():
    def move_forward(self):
        raise "not implemented"
    
class MovementPhysical(Mover):
    def move_forward(self):
        print 'moving'
    
class MovementVirtual(Mover):    
    def move_forward(self):
        print 'moving'
    
def main_run_1():
    SOKOBAN_BOT = NXTRobot('00:16:53:0A:56:10') 
    try:
        if SOKOBAN_BOT.host_found():
            SOKOBAN_BOT.add_motor_left(PORT_B)
            SOKOBAN_BOT.add_motor_right(PORT_C)
            SOKOBAN_BOT.add_motor_hook(PORT_A)
            SOKOBAN_BOT.add_touch_sensor('touch1', PORT_1)
            print 'Connected to robot'
            while True:
                if SOKOBAN_BOT.get_sensor('touch1').get_sample():
                    SOKOBAN_BOT.hook_grab()
                    print SOKOBAN_BOT.motor_hook.get_output_state()
                else:
                    SOKOBAN_BOT.hook_stop()
                    print SOKOBAN_BOT.motor_hook.get_output_state()
        else:
            print 'Unable to find robot'
    except (KeyboardInterrupt, SystemExit):
        SOKOBAN_BOT.move_stop()
        SOKOBAN_BOT.disconnect()
        raise

def main_temp():
    x = Movement(MovementPhysical(), MovementVirtual())
    x.move_forward()
        
if __name__ == '__main__':
    main_temp()