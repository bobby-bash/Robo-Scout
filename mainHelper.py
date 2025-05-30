import math
import constants
import requests
import aiohttp
import asyncio
import cv2 as cv
import numpy as np

def Main_getRobotCounts():
    return 1

def Main_getRobotPaths(robotId):
    return [(0,0,0,0), (3,0,0,3), (5,2,math.pi/4,5),
        (6,3,math.pi/2,7), (6,5,math.pi/2,8), (4,7,3*math.pi/4,10),
        (3,9,math.pi,12), (0,8,5*math.pi/4,14), (-1,6,3*math.pi/2,16),
        (-1,4,3*math.pi/2,18), (-1,0,0,20)]
    return [(-1, -1, math.pi, 0, 0), (0, 0, 0, 1, 0), (1, 0, 0, 2, 0), (2, 4, math.pi/2, 6, 0),
    (0, 4, -math.pi/2, 8, 0), (0, -6, -math.pi/2, 11, 0), (10, 0, math.pi/2, 20, 0),
    (10, 0, math.pi/2, 25, 0), (-2, -4, -math.pi/4, 35, 0)]

def _Main_robotVelSafetyFilter(velLeftPWM, velRightPWM):
    # clamp pwm between min and max
    leftPWM = min(max(velLeftPWM, constants.CONTROLS_MIN_PWM), constants.CONTROLS_MAX_PWM)
    rightPWM = min(max(velRightPWM, constants.CONTROLS_MIN_PWM), constants.CONTROLS_MAX_PWM)

    leftSpeed = abs(leftPWM - 90)
    rightSpeed = abs(rightPWM - 90)

    # calculate the scaling such that the faster motor is clamped to the max speed
    # and the slower motor is scaled down by the same ratio without loss in proportion
    scale = 1
    scale = min(scale, constants.CONTROLS_MAX_PWM_OFFSET / leftSpeed)
    scale = min(scale, constants.CONTROLS_MAX_PWM_OFFSET / rightSpeed)


    #### Apply scaling factor to PWM ####
    diffRight = rightPWM - constants.CONTROLS_MAX_PWM_OFFSET
    diffLeft = leftPWM - constants.CONTROLS_MAX_PWM_OFFSET

    rightPWM = int(90 + (diffRight * scale))
    leftPWM = int(90 + (diffLeft * scale))


    return leftPWM, rightPWM

async def _Main_SendOneRobotControl(session, robotId, velLeftLinear, velRightLinear, electromagnet_command):
    velLeftAng = velLeftLinear / constants.wheel_radius
    velRightAng = velRightLinear / constants.wheel_radius

    offset = 2

    # convert angular velocity to pwm
    scaleFactor = 7.5 # 1 PWM Duty Cycle = 7.5 mm/s


    leftPWM = 90 + (velLeftAng * scaleFactor)
    if velLeftAng > 0:
        leftPWM += offset
    elif velLeftAng < 0:
        leftPWM -= offset

    
    rightPWM = 90 - (velRightAng * scaleFactor)
    if velRightAng > 0:
        rightPWM -= offset
    elif velRightAng < 0:
        rightPWM += offset

    leftPWM, rightPWM = _Main_robotVelSafetyFilter(leftPWM, rightPWM)

    # TODO: change robot url
    robot_url = "http://parrot-robot1.local"
    robot_url = "http://192.168.70.102"
    
    if (electromagnet_command != constants.ELECTROMAGNET_DONT_SEND):
        emJson = {"dtype": "pallet",
                "power": (1 if electromagnet_command == constants.ELECTROMAGNET_ENABLE else 0)}
        async with session.post(robot_url, data=emJson) as resp:
            pass

    servoJson = {"dtype": "speed", 
                "servo1": int(leftPWM),
                "servo2": int(rightPWM)
            }
    async with session.post(robot_url, data=servoJson) as resp:
        pass

async def Main_SendRobotControls(robotCommands):
    async with aiohttp.ClientSession() as session:
        for i in range(len(robotCommands)):
            robotCommand = robotCommands[i]
            velLeftLinear, velRightLinear, electromagnet_command = robotCommand
            await _Main_SendOneRobotControl(session, i, velLeftLinear, velRightLinear, electromagnet_command)

def preconditionPath(path):
    # scroll through all the path points, if the next one has the same orientation, remove it
    # but keep straight line if one has deleted over 50 points
    i = 0
    pop_count = 0
    pop_threshold = 3
    while i < len(path) - 1:
        if path[i+1][4] == 1:
            path[i][4] = 1
        
        if path[i][2] == path[i+1][2] and pop_count < pop_threshold and path[i][4] == 0: #2 is theta index, hardcoded for now :)
            path.pop(i)
            pop_count += 1
        else:
            i += 1
            pop_count = 0
