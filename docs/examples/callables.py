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
        
        
async def callback6(**kwargs):
    print('callback6 was called')


loop = asyncio.get_event_loop()

# create the signal
signal = Signal(loop=loop)

# initialize the test class
test = Test()

tasks = [
    # connect the coroutine and standard function
    loop.create_task(signal.connect(callback1)),
    loop.create_task(signal.connect(callback2)),

    # connect the class methods
    loop.create_task(signal.connect(test.callback3)),
    loop.create_task(signal.connect(Test.callback4)),
    loop.create_task(signal.connect(Test.callback5)),

    # connect the async def function
    loop.create_task(signal.connect(callback6))
]

loop.run_until_complete(asyncio.wait(tasks))

# send the signal
loop.run_until_complete(loop.create_task(signal.send()))
