import asyncio
from asyncio_dispatch import Signal


@asyncio.coroutine
def callback(**kwargs):
    print('callback was called')


loop = asyncio.get_event_loop()

# create the signal
signal = Signal(loop=loop)

# connect the coroutine callback to the Signal
loop.create_task(signal.connect(callback))

# send the signal
loop.create_task(signal.send())

# run the event loop for 1 second and see what happens.
loop.run_until_complete(asyncio.sleep(1))
