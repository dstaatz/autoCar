'''
Robot.py

This is the main controller file

'''

import asyncio
import websockets
import logging
from server import Server
from car import Car
from settings import *


def main():
    '''
        Main Entrance to the program
    '''
    # Setup Logging
    # Debug Mode
    logging.basicConfig(format='%(levelname)s: %(asctime)s: %(message)s', level=logging.INFO)
    # Production Mode
    # logging.basicConfig(filename='log.log', format='%(asctime)s %(message)s', level=logging.INFO)

    # Get our logger
    logger = logging.getLogger(__name__)

    # Get event loop to work with
    loop = asyncio.get_event_loop()

    # Setup Robot
    car = Car()
    
    # Setup Server
    server = Server(SERVER_IP, SERVER_PORT, car)

    try:
        loop.run_until_complete(server.start_server())
        loop.run_forever()

    except KeyboardInterrupt:
        logger.info('Keyboard Interrupt. Closing Connection...')
    
    finally:
        # Stop the car
        car.stop()
        logger.info('Car stopped')

        # Set all tasks to be cancelled
        for task in asyncio.Task.all_tasks():
            task.cancel()
        
        # Run the event loop to trigger all the cancelled task
        loop.run_forever()
        logger.info('All task cancelled')

        # Close the loop
        loop.close()
        logger.info('Event loop closed')


if __name__ == '__main__':
    main()