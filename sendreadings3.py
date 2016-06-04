#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner


class MyComponent(ApplicationSession):
    def __init__(self, config=None):
        ApplicationSession.__init__(self, config)
        print("component created")
        self.q = self.config.extra['commqueue']
        self.tasks = []

    async def read_queue(self):
        while True:
            print("Reading queue")
            elem = await self.q.get()
            print("Received %d" % elem)

    async def give_life_sign(self):
        while True:
            await asyncio.sleep(2)
            print("Autobahn alive")

    async def onJoin(self, details):
        print(details)
        print("session ready")
        self.tasks.append(asyncio.ensure_future(self.read_queue()))
        self.tasks.append(asyncio.ensure_future(self.give_life_sign()))
        print("Done!")

    def onLeave(self, details):
        print("session left")
        for task in self.tasks:
            task.cancel()
        self.disconnect()

    def onDisconnect(self):
        print("transport disconnected")

if __name__ == "__main__":
    runner = ApplicationRunner(url=u"ws://localhost:8080/ws", 
                               realm=u"realm1",
                               extra={"commqueue":asyncio.Queue()})
    runner.run(MyComponent)
