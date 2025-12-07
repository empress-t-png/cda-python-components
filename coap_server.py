import asyncio
from aiocoap import resource, Context, Message

class SensorResource(resource.Resource):
    async def render_put(self, request):
        print("Received CoAP PUT:", request.payload.decode())
        return Message(payload=b"Data received")

async def main():
    root = resource.Site()
    root.add_resource(('PIOT', 'ConstrainedDevice', 'SensorMsg'), SensorResource())
    root.add_resource(('PIOT', 'ConstrainedDevice', 'SystemPerfMsg'), SensorResource())
    await Context.create_server_context(root)
    await asyncio.get_running_loop().create_future()

asyncio.run(main())
