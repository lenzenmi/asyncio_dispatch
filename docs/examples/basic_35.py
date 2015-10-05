import asyncio
from asyncio_dispatch import Signal


async def callback(**kwargs):
    print('callback was called')


async def connect_and_send_signal(signal, callback):
    await signal.connect(callback)
    print('sending the signal!')
    await signal.send()


loop = asyncio.get_event_loop()

# initialize the signal
signal = Signal(loop=loop)

# connect the callback to the signal and send the signal
loop.run_until_complete(connect_and_send_signal(signal, callback))
