'''
    A middleware that handles the websocket connection and sends messages
    Any network related logic and code can be found here
'''

import asyncio, json, websockets, configs

class Middleware:
    def __init__(self, vehicle_id):
        self.vehicle_id = vehicle_id
        self.ws = None
        self.ready_event = asyncio.Event()

    async def connect(self):
        self.ws = await websockets.connect(
            f'{configs.PROTOCOLS.get("ws")}{configs.SERVER_URL}/join/vehicle/{self.vehicle_id}'
        )
        self.on_open(self.ws)
        self.ready_event.set()

        # Keep the connection alive by sending a heartbeat every 30 seconds
        while True:
            await self.heartbeat()
            await asyncio.sleep(30)

    async def send_message(self, mode, message, conn_id="", status="success", attachments=[]):
        # Create message in standard format
        msg = {
            "mode": mode,
            "vid": self.vehicle_id,
            "conn_id": conn_id,
            "status": status,
            "message": str(message),
            "attachments": attachments
        }

        await self.ws.send(json.dumps(msg))
    
    async def heartbeat(self):
        await self.ws.ping()

    def on_message(self, ws, message):
        # Handle incoming messages here
        pass

    def on_error(self, ws, error):
        # Handle errors here
        print(error)

    def on_close(self, ws):
        # Handle closing of websocket here
        pass

    def on_open(self, ws):
        print("Created room")
