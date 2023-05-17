import asyncio
import websockets
import configs
import auth, requests, json, obd, urllib

connection = obd.OBD('/dev/ttyUSB0')

def register():
    payload = {
        "company": "default",
        "model": "default"
    }

    response = requests.post(f'{configs.PROTOCOLS.get("https")}{configs.SERVER_URL}/vehicle/register', data=json.dumps(payload))
    auth.set_creds(json.loads(response.content)["id"]["$oid"])

def get_stats():
    try:
        rpm = int(connection.query(obd.commands.RPM).value.magnitude)
        speed = int(connection.query(obd.commands.SPEED).value.magnitude)
        temperature = int(connection.query(obd.commands.COOLANT_TEMP).value.magnitude)
        odo = int(connection.query(obd.commands.DISTANCE_SINCE_DTC_CLEAR).value.magnitude)
    except:
        rpm, speed, temperature, odo = 0, 0, 0, 0

    return {
        "speed": speed,
        "rpm": rpm,
        "temp": temperature,
        "odo": odo,
        "gear": 0,
        "location": {
            "latitude": 0.0,
            "longitude": 0.0
        },
        "stressed": False
    }

def get_message(message, mode='broadcast', vid, conn_id="", status="success", attachments=[]):
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
            stats = get_stats()
            await websocket.send(json.dumps(get_message(stats, vehicle_id)))
            await asyncio.sleep(1)

asyncio.run(send_messages())
