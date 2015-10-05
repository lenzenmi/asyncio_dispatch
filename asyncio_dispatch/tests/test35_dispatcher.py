import unittest
import asyncio

from .helpers import CoroutineMock
from ..dispatcher import Signal


class TestSignal_Py35(unittest.TestCase):
    '''
    Tests that require python 3.5 or newer.
    '''

    def setUp(self):
        self.loop = asyncio.get_event_loop()

    def tearDown(self):
        pass

    def test_async_await_syntax(self):

        async def connect_signal(signal, callback):
            await signal.connect(callback)

        async def send_signal(signal):
            await signal.send()

        coro_callback = CoroutineMock()

        signal = Signal(loop=self.loop)

        tasks = [self.loop.create_task(connect_signal(signal, coro_callback))]

        self.loop.run_until_complete(asyncio.wait(tasks))

        # make sure no exception was raised
        for task in tasks:
            task.result()

        # send a signal to the connected callback
        tasks = [self.loop.create_task(send_signal(signal))]

        self.loop.run_until_complete(asyncio.wait(tasks))

        # make sure no exception was raised
        for task in tasks:
            task.result()

        self.assertEqual(coro_callback.call_count, 1)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
