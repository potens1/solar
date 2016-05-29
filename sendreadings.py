import asyncio
import uvloop
import readserial
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner


class MyComponent(ApplicationSession):
    def __init__(self, config=None):
        ApplicationSession.__init__(self, config)
        print("component created")

    async def onJoin(self, details):
        print("session ready")
        while True:
            print("Trying to read")
            value = await self.config.extra['commqueue'].get()
            print("Read {}".format(value))

    # def onLeave(self, details):
    #     print("session left")

    def onDisconnect(self):
        print("transport disconnected")

if __name__ == "__main__":
    runner = ApplicationRunner(url=u"ws://localhost:8080/ws", realm=u"realm1")
    runner.run(MyComponent)
