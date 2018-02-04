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

        # setup robot
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

        self.logger.info('New connection to server at: {}'.format(ws.remote_address))
        self._active_connections.add(ws)

        # Run forever until connection is lost
        try:
            while True:
                # Wait for a message
                result = await ws.recv()

                # Handle the recieved message
                await self.handle_msg(result)
        finally:
            # Stop robot
            # # (I don't think this is nessasary but it's better to be safe then sorry)
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
            self._active_connections = set()
            asyncio.get_event_loop().close()

    async def shutdown(self):
        self.server.close()
        await self.server.wait_closed()

    def stop(self):
        # Stop the robot
        if self.robot:
            self.logger.info("Stopping the Robot")
            self.robot.stop()
    
        
def test():
    ip = '127.0.0.1'
    port = 8055
    
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

    server = Server(ip, port, None)
    asyncio.get_event_loop().run_until_complete(server.start_server())
    asyncio.get_event_loop().run_forever()

if __name__ == '__main__':
    test()