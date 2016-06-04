#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import re
import struct
from serial import aio
import datetime

ARDUINO = '/dev/ttyACM0'
SPEED = 115200

HEADRE = re.compile(b'\\xaa(?:(?:\\xbb)|$)', re.S | re.M)

async def frame_received(data, queue):
    try:
        out = struct.unpack("<BI", data)
        print(datetime.datetime.now())
        if out[0]:
            print("Pannel 1: {}".format(out[1]/1000000))
        else:
            print("Pannel 2: {}".format(out[1]/1000000))
        await queue.put(out)
        print("Value in queue !")
        print(queue)
        return True
    except Exception as e:
        print(e)

async def data_received(queue, unprocessed, data):
    alldata = unprocessed + data
    index = HEADRE.search(alldata)
    if index:
        alldata = alldata[index.start():]
    else:
        alldata = b''
    currentoffset = 0
    while len(alldata) >= 7:
        messageStart = currentoffset + 2
        length = 5
        messageEnd = messageStart + 5
        if len(alldata) < messageEnd:
            break
        packet = alldata[messageStart:messageEnd]
        framebuilt = await frame_received(packet, queue)
        if not framebuilt:
            index = HEADRE.search(alldata, currentoffset +1,
                                        messageEnd)
            if index:
                currentoffset = index.start()
            else:
                currentoffset = messageEnd
        else:
            currentoffset = messageEnd

    unprocessed = alldata[currentoffset:]

async def serial_echo_client(queue, loop):
    reader, writer = await aio.open_serial_connection(url=ARDUINO, 
        baudrate=SPEED, loop=loop)
    _unprocessed = b""
    try:
        while True:
            data = await reader.read(1024)
            _ = await data_received(queue, _unprocessed, data)
    except KeyboardInterrupt:
        print("Ctrl-C received")
    finally:
        print('Close the socket')
        writer.close()
