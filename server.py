'''
Server

This is the server to be ran on the pi
'''
import asyncio
from concurrent.futures import CancelledError
import pickle
import logging
import websockets

p = 1

class TextColors:
    '''
        Set of definitions for terminal text color
    '''
    WARN = '\033[93m'	# Color used for warnings!
    CONF = '\033[94m'	# Color used for confirmations
    PRINT = '\033[92m'	# Color used to distinguish the standard output of p
    BOLD = '\033[1m'	# Bold text to amplify textclass textColors


class Server(object):
    '''
        Defines a server object to handle connections
    '''

    def __init__(self, ip, port, robot):
        '''
            Construct a server with an ip on a port
        '''
        self._active_connections = set()
        self.ip = ip
        self.port = port
        self.logger = logging.getLogger(__name__)
        self.server = None
        self.robot = robot

    async def start_server(self):
        '''
            Start the server
        '''
        self.logger.info('Server starting up at: {0}:{1}'.format(self.ip, self.port))
        self.server = await websockets.serve(self.handle_new_connection, self.ip, self.port, timeout=1)

    async def handle_new_connection(self, ws, path):
        '''
            Handle a new incoming connection to the server
        '''

        # Note the new connection
        self.logger.info('New connection to server at: {0}'.format(ws.remote_address))
        
        # Add the connection to the set
        self._active_connections.add(ws)

        # Run forever until connection is lost or exception raised
        try:
            while True:
                if not ws.open:
                    break
                # Wait for a message
                result = await ws.recv()

                # Handle the recieved message
                await self.handle_msg(result)
        finally:
            # Stop robot
            self.stop()
            self.logger.info('Robot stopped')

            # Close Connection
            if ws.open:
                await ws.close()
            self.logger.info('Connection closed: {}'.format(ws.remote_address))
            
            # Remove connection
            self._active_connections.remove(ws)
            self.logger.info('Connection removed: {}'.format(ws.remote_address))

    async def handle_msg(self, msg):
        # Load from pickle
        data = pickle.loads(msg)

        self.logger.debug('Recieved: {}'.format(data))

        # Update the robot with the recieved data
        if self.robot:
            await self.robot.update(data)

    async def send(self, msg):
        try:
            self.logger.debug("Sending: {}".format(msg))
            for ws in self._active_connections:
                asyncio.ensure_future(ws.send(msg))
        except:
            self.logger.info('Send failed')
            # self._active_connections = set()
            # asyncio.get_event_loop().close()

    async def shutdown(self):
        '''
            Shutdown the server if it exsits
        '''

        if self.server:
            self.server.close()
            await self.server.wait_closed()

    def stop(self):
        '''
            Stop the robot if it exsits
        '''

        # Stop the robot
        if self.robot:
            self.logger.info("Stopping the Robot")
            self.robot.stop()
    
        
def test_server():
    '''
        Sets up a test server with robot set to none on localhost for testing
    '''
    
    ip = '127.0.0.1' # localhost
    port = 8055
    
    # Setup logging
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

    # Create server object
    server = Server(ip, port, None)
    
    try:
        loop.run_until_complete(server.start_server())
        loop.run_forever()

    except KeyboardInterrupt:
        logger.info('Keyboard Interrupt. Closing Connections...')
    
    finally:
        # Shutdown the server
        task = asyncio.ensure_future(server.shutdown())
        loop.run_until_complete(task)

        # Close the loop
        loop.close()
        logger.info('Event loop closed')

if __name__ == '__main__':
    test_server()