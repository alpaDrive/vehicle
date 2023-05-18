import asyncio, websockets, requests, json, obd, urllib
from utils import auth, configs, vehicle

connection = obd.OBD('/dev/ttyUSB0')
serial = serial.Serial('/dev/ttyS0')

def register():
    payload = {
        "company": "default",
        "model": "default"
    }

    response = requests.post(f'{configs.PROTOCOLS.get("https")}{configs.SERVER_URL}/vehicle/register', data=json.dumps(payload))
    auth.set_creds(json.loads(response.content)["id"]["$oid"])

def get_message(message, vid, mode='broadcast', conn_id="", status="success", attachments=[]):
        # Create message in standard format
        return {
            "mode": mode,
            "vid": vid,
            "conn_id": conn_id,
            "status": status,
            "message": message,
            "attachments": attachments
        }

async def send_messages():
    if not auth.is_authenticated():
        register()

    vehicle_id = auth.get_creds()
    uri = f'{configs.PROTOCOLS.get("wss")}{configs.SERVER_URL}/join/vehicle/{vehicle_id}'

    async with websockets.connect(uri) as websocket:
        while True:
            stats = vehicle.get_stats(connection, serial)
            await websocket.send(json.dumps(get_message(stats, vehicle_id)))
            await asyncio.sleep(1)

asyncio.run(send_messages())
