#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import uvloop
from autobahn.asyncio.wamp import ApplicationRunner

from readserial2 import serial_echo_client
from sendreadings2 import MyComponent
import functools

ARDUINO = '/dev/ttyACM0'
SPEED = 115200
commqueue = asyncio.Queue()

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    coro = serial_echo_client(commqueue, loop)
    asyncio.ensure_future(coro, loop=loop)
    runner = ApplicationRunner(url=u"ws://localhost:8080/ws", 
                               realm=u"realm1", 
                               extra={"commqueue":commqueue})
    runner.run(MyComponent)
