'''
    A middleware that handles the websocket connection and sends messages
    Any network related logic and code can be found here
'''

import asyncio, json, websockets, configs
from monitor import OBDInterface

class Middleware:
    def __init__(self, vehicle_id):
        self.vehicle_id = vehicle_id
        self.ws = None
        self.ready_event = asyncio.Event()
        self.obd_interface = None

    async def connect(self):
        self.ws = await websockets.connect(
            f'{configs.PROTOCOLS.get("wss")}{configs.SERVER_URL}/join/vehicle/{self.vehicle_id}'
        )
        self.on_open(self.ws)
        self.ready_event.set()

        # Keep the connection alive by sending a heartbeat every 30 seconds
        while True:
            await self.heartbeat()
            await self.handle_messages()
            await asyncio.sleep(5)

    async def heartbeat(self):
        # Send a heartbeat message to the server
        await self.ws.ping()

    async def send_message(self, mode, message, conn_id="", status="success", attachments=[]):
        # Create message in standard format
        msg = {
            "mode": mode,
            "vid": self.vehicle_id,
            "conn_id": conn_id,
            "status": status,
            "message": message,
            "attachments": attachments
        }

        await self.ws.send(str(json.dumps(msg)))

    async def handle_messages(self):
        async for message in self.ws:
            print('A message was recieved')
            print(message)

    def on_message(self, ws, message):
        data = json.loads(message)

        # If server requests for OBD data, get the values and send them
        if data.get('mode') == 'get_obd_data':
            if self.obd_interface:
                obd_data = {
                    "rpm": self.obd_interface.get_rpm(),
                    "speed": self.obd_interface.get_speed()
                }
                asyncio.create_task(self.send_message("response", obd_data, conn_id=data.get("conn_id")))
            else:
                asyncio.create_task(self.send_message("error", "OBD data not available"))

    def on_error(self, ws, error):
        # Handle errors here
        print(error)

    def on_close(self, ws):
        # Handle closing of websocket here
        pass

    def on_open(self, ws):
        print("Created room")