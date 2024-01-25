# import cv2 as cv
# vcap = cv.VideoCapture("rtsp://192.168.1.2:8080/out.h264")

import asyncio
import socketio

sio = socketio.AsyncClient()

@sio.event
async def connect():
    print('connection established')

@sio.event
async def my_message(data):
    print('message received with ', data)
    await sio.emit('my response', {'response': 'my response'})

@sio.event
async def disconnect():
    print('disconnected from server')

async def main():
    await sio.connect('http://localhost:5000')
    await sio.wait()

if __name__ == '__main__':
    asyncio.run(main())
# while(1):

#     ret, frame = vcap.read()
#     cv.imshow('VIDEO', frame)
#     cv.waitKey(1)