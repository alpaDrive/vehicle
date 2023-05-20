import asyncio, websockets, requests, json, obd, urllib, serial, os
import RPi.GPIO as GPIO
from utils import auth, configs, vehicle, gps
from datetime import datetime, timedelta

connection = obd.OBD('/dev/ttyUSB0')

GPIO.setmode(GPIO.BCM)
button_pin = 21
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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
    print('Trying to connect...')

    async with websockets.connect(uri) as websocket:
        print(f'{datetime.now().strftime("%H:%M:%S")}: Connected to server!')
        while True:
            if GPIO.input(button_pin) == GPIO.LOW:
                GPIO.cleanup()
                os.system("sudo shutdown -h now")
                quit()
            stats = vehicle.get_stats(connection)
            await websocket.send(json.dumps(get_message(stats, vehicle_id)))
            await asyncio.sleep(0.2)

# wait 2 minutes for GPS fix
end_time = datetime.now() + timedelta(minutes=2)
print(f'{datetime.now().strftime("%H:%M:%S")}: Wating for GPS signal...')
while datetime.now() < end_time :
    if gps.has_fix():
        print(f'{datetime.now().strftime("%H:%M:%S")}: Got GPS fix!')
        break

while True:
    try:
        asyncio.run(send_messages())
    except KeyboardInterrupt:
        quit()
    except:
        print(f'{datetime.now().strftime("%H:%M:%S")}: Lost connection with server...')
