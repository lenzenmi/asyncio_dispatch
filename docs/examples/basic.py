import asyncio
from asyncio_dispatch import Signal


@asyncio.coroutine
def callback(**kwargs):
    print('callback was called!')


loop = asyncio.get_event_loop()

# create the signal
signal = Signal(loop=loop)

# connect the callback to the Signal - This is a coroutine!
loop.run_until_complete(loop.create_task(signal.connect(callback)))

# send the signal - This is also a coroutine!
print('sending the signal.')
loop.run_until_complete(loop.create_task(signal.send()))
