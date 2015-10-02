import asyncio
from asyncio_dispatch import Signal


@asyncio.coroutine
def callback1(**kwargs):
    print('callback1 was called')


def callback2(**kwargs):
    print('callback2 was called')


class Test:
    def callback3(self, **kwargs):
        print('callback3 was called')

    @classmethod
    def callback4(cls, **kwargs):
        print('callback4 was called')

    @staticmethod
    def callback5(**kwargs):
        print('callback5 was called')

loop = asyncio.get_event_loop()

# create the signal
signal = Signal(loop=loop)

# connect the coroutine and standard function
loop.create_task(signal.connect(callback1))
loop.create_task(signal.connect(callback2))

# connect the class methods
test = Test()
loop.create_task(signal.connect(test.callback3))
loop.create_task(signal.connect(Test.callback4))
loop.create_task(signal.connect(Test.callback5))

# send the signal
loop.create_task(signal.send())

# run the event loop for 1 second and see what happens.
loop.run_until_complete(asyncio.sleep(1))
