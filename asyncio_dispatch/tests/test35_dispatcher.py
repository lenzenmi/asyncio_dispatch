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

    def test_dissconnect_all_no_args_multiple(self):

        callbacks = [CoroutineMock(), CoroutineMock(), CoroutineMock(), CoroutineMock()]

        signal = Signal(loop=self.loop)

        async def connect(signal):
            await signal.connect(callbacks[0]),
            await signal.connect(callbacks[1]),
            await signal.connect(callbacks[2]),
            await signal.connect(callbacks[3]),
            await signal.send()

        self.loop.run_until_complete(connect(signal))

        self.assertEqual(len(signal._all), 4)
        self.assertEqual(len(signal._by_keys), 0)
        self.assertEqual(len(signal._by_senders), 0)

        for callback in callbacks:
            callback.assert_called_with(signal=signal, senders=set(), keys=set())
            self.assertEqual(callback.call_count, 1)

        async def disconnect(signal):
            await signal.disconnect(callbacks[0])

        self.loop.run_until_complete(disconnect(signal))

        # Order is important
        tasks = [self.loop.create_task(signal.send())]
        self.loop.run_until_complete(asyncio.wait(tasks))

        for callback in callbacks[1:]:
            callback.assert_called_with(signal=signal, senders=set(), keys=set())
            self.assertEqual(callback.call_count, 2)

        self.assertEqual(callbacks[0].call_count, 1)

    def test_send_method_coro(self):
        class Test:
            call_count = 0

            async def method(self, *args, **kwargs):
                self.call_count += 1

        instance = Test()
        coro_callback = instance.method

        signal = Signal(loop=self.loop)

        tasks = [self.loop.create_task(signal.connect(coro_callback))]

        self.loop.run_until_complete(asyncio.wait(tasks))
        for task in tasks:
            task.result()

        tasks = [self.loop.create_task(signal.send())]

        self.loop.run_until_complete(asyncio.wait(tasks))
        for task in tasks:
            task.result()

        self.assertEqual(instance.call_count, 1)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
