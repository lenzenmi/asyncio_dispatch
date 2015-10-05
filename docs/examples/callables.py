import asyncio
from asyncio_dispatch import Signal


def callback1(**kwargs):
    print('callback1 was called')


@asyncio.coroutine
def callback2(**kwargs):
    print('callback2 was called')


async def callback3(**kwargs):
    print('callback3 was called')


class Test:
    def callback4(self, **kwargs):
        print('callback4 was called')

    @asyncio.coroutine
    def callback5(self, **kwargs):
        print('callback5 was called')

    async def callback6(self, **kwargs):
        print('callback6 was called')

    @classmethod
    def callback7(cls, **kwargs):
        print('callback7 was called')

    @staticmethod
    def callback8(**kwargs):
        print('callback8 was called')


loop = asyncio.get_event_loop()

# create the signal
signal = Signal(loop=loop)

# initialize the test class
test = Test()

tasks = [
    # connect the function and coroutines
    loop.create_task(signal.connect(callback1)),
    loop.create_task(signal.connect(callback2)),
    loop.create_task(signal.connect(callback3)),

    # connect the class methods
    loop.create_task(signal.connect(test.callback4)),
    loop.create_task(signal.connect(test.callback5)),
    loop.create_task(signal.connect(test.callback6)),
    loop.create_task(signal.connect(Test.callback7)),
    loop.create_task(signal.connect(Test.callback8)),
]

loop.run_until_complete(asyncio.wait(tasks))

# send the signal
loop.run_until_complete(loop.create_task(signal.send()))
