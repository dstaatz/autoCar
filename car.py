''' Describes the car and how to control it '''

# General imports
import asyncio

from components import *
from settings import *


class Car(object):

    def __init__(self):

        # Setup drive motors
        self.drive_motor = DCMotorComponent(
            DRIVE_MOTOR_P1,
            DRIVE_MOTOR_P2,
            DRIVE_MOTOR_HIGH,
            DRIVE_MOTOR_LOW,
            reverse=DRIVE_MOTOR_REVERSE
        )

        self.steer_motor = DCMotorComponent(
            STEER_MOTOR_P1,
            STEER_MOTOR_P2,
            STEER_MOTOR_HIGH,
            STEER_MOTOR_LOW,
            reverse=STEER_MOTOR_REVERSE
        )

    async def produce(self):
        pass
    
    def stop(self):
        pass
    
    async def update(self, data):
        
        drive_task = asyncio.ensure_future(self.drive_motor.update(data))
        steer_task = asyncio.ensure_future(self.steer_motor.update(data))

        # Wait for all tasks to be completed
        await asyncio.wait([
                drive_task,
                steer_task,
            ],
            return_when=asyncio.ALL_COMPLETED
        )

        
