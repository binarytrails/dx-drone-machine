# Author: Vsevolod Ivanov <seva@binarytrails.net>
# python3 client.py "http://<ip>:<port>"

import sys
import asyncio
import socketio

URL = str(sys.argv[1])
sio = socketio.AsyncClient()

@sio.event
async def connect():
    print('[+] connection established')

@sio.on('*')
async def catch_all(event, data):
    print("[+] {}\n{}".format(event, data))

@sio.event
async def disconnect():
    print('[-] disconnected from server')

async def main():
    await sio.connect(URL)
    await sio.wait()

if __name__ == '__main__':
    asyncio.run(main())
