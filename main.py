import auth, requests, configs, json, asyncio
from network import Middleware
from monitor import OBDInterface

def register():
    payload = {
        "company": "test",
        "model": "test"
    }

    response = requests.post(f'{configs.PROTOCOLS.get("http")}{configs.SERVER_URL}/vehicle/register', data=json.dumps(payload))
    auth.set_creds(json.loads(response.content)["id"]["$oid"])

async def main():
    if not auth.is_authenticated():
        register()

    creds = auth.get_creds()
    middleware = Middleware(creds)

    # Create a task to connect the middleware to the WebSocket in the background
    connection_task = asyncio.create_task(middleware.connect())

    data_monitor = OBDInterface(creds, middleware)

    # Wait for the middleware to connect to the WebSocket before starting the data monitor
    await middleware.ready_event.wait()

    asyncio.create_task(data_monitor.start())

    # Keep the event loop running to receive messages and send heartbeats
    while True:
        await middleware.heartbeat()
        await asyncio.sleep(5)



if __name__ == '__main__':
    asyncio.run(main())