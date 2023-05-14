import auth, requests, configs, json, asyncio
from network import Middleware
from monitor import OBDInterface

def register():
    payload = {
        "company": "default",
        "model": "default"
    }

    response = requests.post(f'{configs.PROTOCOLS.get("https")}{configs.SERVER_URL}/vehicle/register', data=json.dumps(payload))
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

    # Run the middleware and data monitor concurrently
    await asyncio.gather(
        middleware.run(),
        data_monitor.start()
    )

if __name__ == '__main__':
    asyncio.run(main())