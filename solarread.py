#!/usr/bin/env python3

import asyncio
import uvloop
from autobahn.asyncio.wamp import ApplicationRunner

from readserial import Output, create_serial_connection
from sendreadings import MyComponent
import functools

ARDUINO = '/dev/ttyACM0'
SPEED = 115200
commqueue = asyncio.Queue()

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    coro = create_serial_connection(loop, Output, commqueue, ARDUINO ,baudrate=SPEED)
    try:
        #loop.run_until_complete(coro)
        runner = ApplicationRunner(url=u"ws://localhost:8080/ws", realm=u"realm1", extra={"commqueue":commqueue})
        import ipdb
        ipdb.set_trace()
        asyncio.ensure_future(coro, loop=loop)
        runner.run(MyComponent)
    except KeyboardInterrupt as e:
        print("Caught keyboard interrupt.")
        loop.run_forever()
    finally:
        loop.close()

