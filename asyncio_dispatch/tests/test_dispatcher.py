'''
Created on Apr 23, 2015

@author: mike
'''
import unittest
from unittest.mock import Mock, MagicMock
import asyncio
import gc
import sys

from ..dispatcher import Signal


# Utility classes for testing coroutines
class CoroutineMock:
    _is_coroutine = True
    _coro_methods = set()

    def __init__(self):
        self._coro_mock = MagicMock()
        self._coro_methods = set(dir(self._coro_mock))
        for method in self._coro_methods:
            setattr(self, method, getattr(self._coro_mock, method))

    def __getattribute__(self, name):
        if name in object.__getattribute__(self, '_coro_methods'):
            return object.__getattribute__(object.__getattribute__(self, '_coro_mock'), name)
        else:
            return object.__getattribute__(self, name)

    def __setattr__(self, name, value):
        if name in {'reset_mock', 'side_effect', 'return_value'}:
            return setattr(self._coro_mock, name, value)
        else:
            return object.__setattr__(self, name, value)

    def __call__(self, *args, **kwargs):
        return asyncio.coroutine(self._coro_mock)(*args, **kwargs)


class FunctionMock(MagicMock):
    _is_coroutine = False


class TestSignal(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.get_event_loop()

    def tearDown(self):
        pass

    def test_connect_send_all_no_args(self):

        callback = FunctionMock()

        signal = Signal(loop=self.loop)
        tasks = [self.loop.create_task(signal.connect(callback)),
                 self.loop.create_task(signal.send())]
        self.loop.run_until_complete(asyncio.wait(tasks))

        self.assertEqual(tasks[1].result(), 1)

        self.assertEqual(len(signal._all), 1)
        self.assertEqual(len(signal._by_keys), 0)
        self.assertEqual(len(signal._by_senders), 0)

        callback.assert_called_with(signal=signal, senders=set(), keys=set())

    def test_connect_send_all_no_args_multiple(self):

        callbacks = [FunctionMock(), FunctionMock(), FunctionMock(), FunctionMock()]

        signal = Signal(loop=self.loop)
        tasks = [self.loop.create_task(signal.connect(callbacks[0])),
                 self.loop.create_task(signal.connect(callbacks[1])),
                 self.loop.create_task(signal.connect(callbacks[2])),
                 self.loop.create_task(signal.connect(callbacks[3])),
                 self.loop.create_task(signal.send())]
        self.loop.run_until_complete(asyncio.wait(tasks))

        self.assertEqual(tasks[4].result(), 4)

        self.assertEqual(len(signal._all), 4)
        self.assertEqual(len(signal._by_keys), 0)
        self.assertEqual(len(signal._by_senders), 0)

        for callback in callbacks:
            callback.assert_called_with(signal=signal, senders=set(), keys=set())
            self.assertEqual(callback.call_count, 1)

    def test_dissconnect_all_no_args_multiple(self):

        callbacks = [FunctionMock(), FunctionMock(), FunctionMock(), FunctionMock()]

        signal = Signal(loop=self.loop)
        tasks = [self.loop.create_task(signal.connect(callbacks[0])),
                 self.loop.create_task(signal.connect(callbacks[1])),
                 self.loop.create_task(signal.connect(callbacks[2])),
                 self.loop.create_task(signal.connect(callbacks[3])),
                 self.loop.create_task(signal.send())]

        self.loop.run_until_complete(asyncio.wait(tasks))

        self.assertEqual(tasks[4].result(), 4)

        self.assertEqual(len(signal._all), 4)
        self.assertEqual(len(signal._by_keys), 0)
        self.assertEqual(len(signal._by_senders), 0)

        for callback in callbacks:
            callback.assert_called_with(signal=signal, senders=set(), keys=set())
            self.assertEqual(callback.call_count, 1)

        tasks = [signal.disconnect(callbacks[0])]
        self.loop.run_until_complete(asyncio.wait(tasks))

        # Order is important

        tasks = [self.loop.create_task(signal.send())]
        self.loop.run_until_complete(asyncio.wait(tasks))

        for callback in callbacks[1:]:
            callback.assert_called_with(signal=signal, senders=set(), keys=set())
            self.assertEqual(callback.call_count, 2)

        self.assertEqual(callbacks[0].call_count, 1)

    def test_weakref_all_no_args_multiple(self):

        fn1 = FunctionMock()
        fn2 = FunctionMock()
        fn3 = FunctionMock()
        fn4 = FunctionMock()

        signal = Signal(loop=self.loop)
        tasks = [self.loop.create_task(signal.connect(fn1)),
                 self.loop.create_task(signal.connect(fn2)),
                 self.loop.create_task(signal.connect(fn3)),
                 self.loop.create_task(signal.connect(fn4)),
                 self.loop.create_task(signal.send())]

        self.loop.run_until_complete(asyncio.wait(tasks))
        self.assertEqual(len(signal._all), 4)

        del(fn1)
        gc.collect()

        # cleanup happens during disconnect and send only.
        tasks = [self.loop.create_task(signal.send())]
        self.loop.run_until_complete(asyncio.wait(tasks))

        self.assertEqual(len(signal._all), 3)

    def test_strongref_all_no_args_multiple(self):

        fn1 = FunctionMock()
        fn2 = FunctionMock()
        fn3 = FunctionMock()
        fn4 = FunctionMock()

        signal = Signal(loop=self.loop)
        tasks = [self.loop.create_task(signal.connect(fn1, weak=False)),
                 self.loop.create_task(signal.connect(fn2)),
                 self.loop.create_task(signal.connect(fn3)),
                 self.loop.create_task(signal.connect(fn4)),
                 self.loop.create_task(signal.send())]

        self.loop.run_until_complete(asyncio.wait(tasks))
        self.assertEqual(len(signal._all), 4)

        del(fn1)
        gc.collect()

        # Should not be garbage collected
        tasks = [self.loop.create_task(signal.send())]
        self.loop.run_until_complete(asyncio.wait(tasks))

        self.assertEqual(len(signal._all), 4)

    def test_send_all_with_args_default(self):

        callback = FunctionMock()
        kwargs = {'arg1': 1, 'arg2': 2}

        signal = Signal(loop=self.loop, **kwargs)
        tasks = [self.loop.create_task(signal.connect(callback)),
                 self.loop.create_task(signal.send())]
        self.loop.run_until_complete(asyncio.wait(tasks))

        self.assertEqual(tasks[1].result(), 1)

        self.assertEqual(len(signal._all), 1)
        self.assertEqual(len(signal._by_keys), 0)
        self.assertEqual(len(signal._by_senders), 0)

        callback.assert_called_with(signal=signal, senders=set(), keys=set(), arg1=1, arg2=2)

    def test_send_all_with_args_changed(self):

        callback = FunctionMock()
        kwargs = {'arg1': 1, 'arg2': 2}

        signal = Signal(loop=self.loop, **kwargs)
        tasks = [self.loop.create_task(signal.connect(callback)),
                 # change the kwargs when run
                 self.loop.create_task(signal.send(arg1=2, arg2=3))]

        self.loop.run_until_complete(asyncio.wait(tasks))

        self.assertEqual(tasks[1].result(), 1)

        self.assertEqual(len(signal._all), 1)
        self.assertEqual(len(signal._by_keys), 0)
        self.assertEqual(len(signal._by_senders), 0)

        callback.assert_called_with(signal=signal, senders=set(), keys=set(), arg1=2, arg2=3)

    def test_send_all_with_args_wrong(self):

        callback = FunctionMock()
        kwargs = {'arg1': 1, 'arg2': 2}

        signal = Signal(loop=self.loop, **kwargs)
        tasks = [self.loop.create_task(signal.connect(callback)),

                 # change the kwargs when run
                 self.loop.create_task(signal.send(wrong_arg=2, arg2=3))]

        coro = asyncio.wait(tasks)
        self.loop.run_until_complete(coro)
        # checking the result of the send task should raise ValueError
        self.assertRaises(ValueError, tasks[1].result)

    def test_send_sender_no_args(self):
        callback = FunctionMock()
        sender = object()

        signal = Signal(loop=self.loop)

        tasks = [self.loop.create_task(signal.connect(callback, sender=sender)),
                 self.loop.create_task(signal.send())]

        self.loop.run_until_complete(asyncio.wait(tasks))
        self.assertFalse(callback.called)

        tasks = [self.loop.create_task(signal.send(sender=sender))]

        self.loop.run_until_complete(asyncio.wait(tasks))
        self.assertEqual(callback.call_count, 1)

    def test_send_method_sender_no_args(self):
        callback = FunctionMock()

        class Test:
            def method(self):
                pass

        instance = Test()

        sender = instance.method

        signal = Signal(loop=self.loop)

        tasks = [self.loop.create_task(signal.connect(callback, sender=sender)),
                 self.loop.create_task(signal.send())]

        self.loop.run_until_complete(asyncio.wait(tasks))
        self.assertFalse(callback.called)

        tasks = [self.loop.create_task(signal.send(sender=sender))]

        self.loop.run_until_complete(asyncio.wait(tasks))
        self.assertEqual(callback.call_count, 1)

    def test_send_senders_no_args(self):
        callback1 = FunctionMock()
        callback2 = FunctionMock()
        sender1 = object()
        sender2 = object()
        sender3 = object()

        signal = Signal(loop=self.loop)

        tasks = [self.loop.create_task(signal.connect(callback1, senders=[sender1])),
                 self.loop.create_task(signal.connect(callback2, senders=[sender2, sender3])),
                 self.loop.create_task(signal.send(sender=sender1))]

        self.loop.run_until_complete(asyncio.wait(tasks))
        self.assertEqual(callback1.call_count, 1)
        self.assertEqual(callback2.call_count, 0)

        tasks = [self.loop.create_task(signal.send(sender=sender2))]

        self.loop.run_until_complete(asyncio.wait(tasks))
        self.assertEqual(callback1.call_count, 1)
        self.assertEqual(callback2.call_count, 1)

        tasks = [self.loop.create_task(signal.send(senders=[sender2, sender3]))]

        self.loop.run_until_complete(asyncio.wait(tasks))
        self.assertEqual(callback1.call_count, 1)
        self.assertEqual(callback2.call_count, 2)

        tasks = [self.loop.create_task(signal.send(senders=[sender1, sender3]))]

        self.loop.run_until_complete(asyncio.wait(tasks))
        self.assertEqual(callback1.call_count, 2)
        self.assertEqual(callback2.call_count, 3)

    def test_send_key_no_args(self):
        callback = FunctionMock()
        key = 'some-key'

        signal = Signal(loop=self.loop)

        tasks = [self.loop.create_task(signal.connect(callback, key=key)),
                 self.loop.create_task(signal.send())]

        self.loop.run_until_complete(asyncio.wait(tasks))
        self.assertFalse(callback.called)

        tasks = [self.loop.create_task(signal.send(key=key))]

        self.loop.run_until_complete(asyncio.wait(tasks))
        self.assertEqual(callback.call_count, 1)

    def test_send_keys_no_args(self):
        callback1 = FunctionMock()
        callback2 = FunctionMock()
        key1 = 'key1'
        key2 = 'key2'
        key3 = 'key3'

        signal = Signal(loop=self.loop)

        tasks = [self.loop.create_task(signal.connect(callback1, keys=[key1])),
                 self.loop.create_task(signal.connect(callback2, keys=[key2, key3])),
                 self.loop.create_task(signal.send(key=key1))]

        self.loop.run_until_complete(asyncio.wait(tasks))
        self.assertEqual(callback1.call_count, 1)
        self.assertEqual(callback2.call_count, 0)

        tasks = [self.loop.create_task(signal.send(key=key2))]

        self.loop.run_until_complete(asyncio.wait(tasks))
        self.assertEqual(callback1.call_count, 1)
        self.assertEqual(callback2.call_count, 1)

        tasks = [self.loop.create_task(signal.send(keys=[key2, key3]))]

        self.loop.run_until_complete(asyncio.wait(tasks))
        self.assertEqual(callback1.call_count, 1)
        self.assertEqual(callback2.call_count, 2)

        tasks = [self.loop.create_task(signal.send(keys=[key1, key3]))]

        self.loop.run_until_complete(asyncio.wait(tasks))
        self.assertEqual(callback1.call_count, 2)
        self.assertEqual(callback2.call_count, 3)

    def test_disconnect_all(self):
        callback = FunctionMock()
        key = 'some-key'
        key2 = 'some-key2'
        sender = object()
        sender2 = object()

        signal = Signal(loop=self.loop)

        tasks = [self.loop.create_task(signal.connect(callback)),
                 self.loop.create_task(signal.connect(callback, sender=sender)),
                 self.loop.create_task(signal.connect(callback, senders=[sender, sender2])),
                 self.loop.create_task(signal.connect(callback, key=key)),
                 self.loop.create_task(signal.connect(callback, keys=[key, key2]))]

        self.loop.run_until_complete(asyncio.wait(tasks))

        # disconnect from all signals
        tasks = [self.loop.create_task(signal.disconnect(callback))]

        self.loop.run_until_complete(asyncio.wait(tasks))
        for task in tasks:
            task.result()

        tasks = [self.loop.create_task(signal.send()),
                 self.loop.create_task(signal.send(sender=sender)),
                 self.loop.create_task(signal.send(senders=[sender, sender2])),
                 self.loop.create_task(signal.send(key=key)),
                 self.loop.create_task(signal.send(keys=[key, key2])), ]

        self.loop.run_until_complete(asyncio.wait(tasks))
        for task in tasks:
            task.result()

        self.assertFalse(callback.called)

    def test_disconnect_sender(self):
        callback = FunctionMock()
        key = 'some-key'
        key2 = 'some-key2'
        sender = object()
        sender2 = object()

        signal = Signal(loop=self.loop)

        tasks = [self.loop.create_task(signal.connect(callback, sender=sender)),
                 self.loop.create_task(signal.connect(callback, senders=[sender, sender2])),
                 self.loop.create_task(signal.connect(callback, key=key)),
                 self.loop.create_task(signal.connect(callback, keys=[key, key2]))]

        self.loop.run_until_complete(asyncio.wait(tasks))

        # disconnect from all signals
        tasks = [self.loop.create_task(signal.disconnect(callback, sender=sender))]

        self.loop.run_until_complete(asyncio.wait(tasks))
        for task in tasks:
            task.result()

        tasks = [self.loop.create_task(signal.send(sender=sender))]

        self.loop.run_until_complete(asyncio.wait(tasks))
        for task in tasks:
            task.result()

        self.assertFalse(callback.called)

        tasks = [self.loop.create_task(signal.send(senders=[sender, sender2])),
                 self.loop.create_task(signal.send(key=key)),
                 self.loop.create_task(signal.send(keys=[key, key2]))]

        self.loop.run_until_complete(asyncio.wait(tasks))
        for task in tasks:
            task.result()

        self.assertEqual(callback.call_count, 3)

    def test_disconnect_senders(self):
        callback = FunctionMock()
        key = 'some-key'
        key2 = 'some-key2'
        sender = object()
        sender2 = object()

        signal = Signal(loop=self.loop)

        tasks = [self.loop.create_task(signal.connect(callback, sender=sender)),
                 self.loop.create_task(signal.connect(callback, senders=[sender, sender2])),
                 self.loop.create_task(signal.connect(callback, key=key)),
                 self.loop.create_task(signal.connect(callback, keys=[key, key2]))]

        self.loop.run_until_complete(asyncio.wait(tasks))

        # disconnect from all signals
        tasks = [self.loop.create_task(signal.disconnect(callback, senders=[sender]))]

        self.loop.run_until_complete(asyncio.wait(tasks))
        for task in tasks:
            task.result()

        tasks = [self.loop.create_task(signal.send(sender=sender))]

        self.loop.run_until_complete(asyncio.wait(tasks))
        for task in tasks:
            task.result()

        self.assertFalse(callback.called)

        tasks = [self.loop.create_task(signal.send(senders=[sender, sender2])),
                 self.loop.create_task(signal.send(key=key)),
                 self.loop.create_task(signal.send(keys=[key, key2]))]

        self.loop.run_until_complete(asyncio.wait(tasks))
        for task in tasks:
            task.result()

        self.assertEqual(callback.call_count, 3)

    def test_disconnect_key(self):
        callback = FunctionMock()
        key = 'some-key'
        key2 = 'some-key2'
        sender = object()
        sender2 = object()

        signal = Signal(loop=self.loop)

        tasks = [self.loop.create_task(signal.connect(callback, sender=sender)),
                 self.loop.create_task(signal.connect(callback, senders=[sender, sender2])),
                 self.loop.create_task(signal.connect(callback, key=key)),
                 self.loop.create_task(signal.connect(callback, keys=[key, key2]))]

        self.loop.run_until_complete(asyncio.wait(tasks))

        # disconnect from all signals
        tasks = [self.loop.create_task(signal.disconnect(callback, key=key))]

        self.loop.run_until_complete(asyncio.wait(tasks))
        for task in tasks:
            task.result()

        tasks = [self.loop.create_task(signal.send(key=key))]

        self.loop.run_until_complete(asyncio.wait(tasks))
        for task in tasks:
            task.result()

        self.assertFalse(callback.called)

        tasks = [self.loop.create_task(signal.send(senders=[sender, sender2])),
                 self.loop.create_task(signal.send(sender=sender)),
                 self.loop.create_task(signal.send(keys=[key, key2]))]

        self.loop.run_until_complete(asyncio.wait(tasks))
        for task in tasks:
            task.result()

        self.assertEqual(callback.call_count, 3)

    def test_disconnect_keys(self):
        callback = FunctionMock()
        key = 'some-key'
        key2 = 'some-key2'
        sender = object()
        sender2 = object()

        signal = Signal(loop=self.loop)

        tasks = [self.loop.create_task(signal.connect(callback, sender=sender)),
                 self.loop.create_task(signal.connect(callback, senders=[sender, sender2])),
                 self.loop.create_task(signal.connect(callback, key=key)),
                 self.loop.create_task(signal.connect(callback, keys=[key, key2]))]

        self.loop.run_until_complete(asyncio.wait(tasks))

        # disconnect from all signals
        tasks = [self.loop.create_task(signal.disconnect(callback, keys=[key]))]

        self.loop.run_until_complete(asyncio.wait(tasks))
        for task in tasks:
            task.result()

        tasks = [self.loop.create_task(signal.send(key=key))]

        self.loop.run_until_complete(asyncio.wait(tasks))
        for task in tasks:
            task.result()

        self.assertFalse(callback.called)

        tasks = [self.loop.create_task(signal.send(senders=[sender, sender2])),
                 self.loop.create_task(signal.send(sender=sender)),
                 self.loop.create_task(signal.send(keys=[key, key2]))]

        self.loop.run_until_complete(asyncio.wait(tasks))
        for task in tasks:
            task.result()

        self.assertEqual(callback.call_count, 3)

    def test_weakref_sender(self):
        callback = FunctionMock()
        sender = object()
        sender2 = object()

        signal = Signal(loop=self.loop)

        tasks = [self.loop.create_task(signal.connect(callback, senders=[sender, sender2]))]

        self.loop.run_until_complete(asyncio.wait(tasks))
        for task in tasks:
            task.result()

        # delete and do garbage cleanup
        del(callback)
        gc.collect()

        # tasks are pruned during a send

        tasks = [self.loop.create_task(signal.send(senders=[sender, sender2]))]

        self.loop.run_until_complete(asyncio.wait(tasks))
        for task in tasks:
            task.result()

        self.assertEqual(len(signal._by_senders), 0)
        self.assertEqual(len(signal._locks_senders), 0)

    def test_weakref_keys(self):
        callback = FunctionMock()
        key = 'key1'
        key2 = 'key2'

        signal = Signal(loop=self.loop)

        tasks = [self.loop.create_task(signal.connect(callback, keys=[key, key2]))]

        self.loop.run_until_complete(asyncio.wait(tasks))
        for task in tasks:
            task.result()

        # delete and do garbage cleanup
        del(callback)
        gc.collect()

        # tasks are pruned during a send

        tasks = [self.loop.create_task(signal.send(keys=[key, key2]))]

        self.loop.run_until_complete(asyncio.wait(tasks))
        for task in tasks:
            task.result()

        self.assertEqual(len(signal._by_keys), 0)
        self.assertEqual(len(signal._locks_keys), 0)

    def test_send_method(self):

        class Test:
            call_count = 0

            def method(self, *args, **kwargs):
                self.call_count += 1

        instance = Test()
        callback = instance.method

        signal = Signal(loop=self.loop)

        tasks = [self.loop.create_task(signal.connect(callback))]

        self.loop.run_until_complete(asyncio.wait(tasks))
        for task in tasks:
            task.result()

        tasks = [self.loop.create_task(signal.send())]

        self.loop.run_until_complete(asyncio.wait(tasks))
        for task in tasks:
            task.result()

        self.assertEqual(instance.call_count, 1)

    def test_send_coro(self):
        coro_callback = CoroutineMock()

        signal = Signal(loop=self.loop)

        tasks = [self.loop.create_task(signal.connect(coro_callback))]

        self.loop.run_until_complete(asyncio.wait(tasks))
        for task in tasks:
            task.result()

        tasks = [self.loop.create_task(signal.send())]

        self.loop.run_until_complete(asyncio.wait(tasks))
        for task in tasks:
            task.result()

        self.assertEqual(coro_callback.call_count, 1)

    def test_send_coro_args(self):
        coro_callback = CoroutineMock()
        kwargs = {'arg1': 1, 'arg2': 2}

        signal = Signal(loop=self.loop, **kwargs)

        tasks = [self.loop.create_task(signal.connect(coro_callback))]

        self.loop.run_until_complete(asyncio.wait(tasks))
        for task in tasks:
            task.result()

        tasks = [self.loop.create_task(signal.send(**kwargs))]

        self.loop.run_until_complete(asyncio.wait(tasks))
        for task in tasks:
            task.result()

        self.assertEqual(coro_callback.call_count, 1)
        coro_callback.assert_called_with(signal=signal, keys=set(), senders=set(),
                                         **kwargs)

    def test_send_method_coro(self):
        class Test:
            call_count = 0

            @asyncio.coroutine
            def method(self, *args, **kwargs):
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

    def test_exception(self):
        # test that our exception is being raised
        exception_handler = Mock()
        self.loop.set_exception_handler(exception_handler)

        callback = FunctionMock()
        callback.side_effect = Exception('BOOM!')

        signal = Signal(loop=self.loop)

        tasks = [self.loop.create_task(signal.connect(callback))]

        self.loop.run_until_complete(asyncio.wait(tasks))
        for task in tasks:
            task.result()

        tasks = [self.loop.create_task(signal.send())]

        self.loop.run_until_complete(asyncio.wait(tasks))
        for task in tasks:
            task.result()

        self.assertTrue(callback.called)
        self.assertTrue(exception_handler.called)

        # reset our exception handler
        self.loop.set_exception_handler(None)

    def test_exception_coro(self):
        # test that our exception is being raised
        exception_handler = Mock()
        self.loop.set_exception_handler(exception_handler)

        callback_coro = CoroutineMock()
        callback_coro.side_effect = Exception('BOOM!')

        signal = Signal(loop=self.loop)

        tasks = [self.loop.create_task(signal.connect(callback_coro))]

        self.loop.run_until_complete(asyncio.wait(tasks))
        for task in tasks:
            task.result()

        tasks = [self.loop.create_task(signal.send())]

        self.loop.run_until_complete(asyncio.wait(tasks))
        for task in tasks:
            task.result()

        self.assertTrue(callback_coro.called)
        self.assertTrue(exception_handler.called)

        # reset our exception handler
        self.loop.set_exception_handler(None)

    def test_static_method(self):
        # test that our exception is being raised
        count = 0

        class Test:
            @staticmethod
            def method(*args, **kwargs):
                nonlocal count
                count += 1

        callback = Test.method

        signal = Signal(loop=self.loop)

        tasks = [self.loop.create_task(signal.connect(callback))]

        self.loop.run_until_complete(asyncio.wait(tasks))
        for task in tasks:
            task.result()

        tasks = [self.loop.create_task(signal.send())]

        self.loop.run_until_complete(asyncio.wait(tasks))
        for task in tasks:
            task.result()

        self.assertEqual(count, 1)

    def test_static_method_coro(self):
        # test that our exception is being raised

        count = 0

        class Test:
            @staticmethod
            @asyncio.coroutine
            def method(*args, **kwargs):
                nonlocal count
                count += 1

        callback = Test.method

        signal = Signal(loop=self.loop)

        tasks = [self.loop.create_task(signal.connect(callback))]

        self.loop.run_until_complete(asyncio.wait(tasks))
        for task in tasks:
            task.result()

        tasks = [self.loop.create_task(signal.send())]

        self.loop.run_until_complete(asyncio.wait(tasks))
        for task in tasks:
            task.result()

        self.assertEqual(count, 1)

    def test_class_method(self):
        # test that our exception is being raised
        class Test:
            count = 0

            @classmethod
            def method(cls, *args, **kwargs):
                cls.count += 1

        callback = Test.method

        signal = Signal(loop=self.loop)

        tasks = [self.loop.create_task(signal.connect(callback))]

        self.loop.run_until_complete(asyncio.wait(tasks))
        for task in tasks:
            task.result()

        tasks = [self.loop.create_task(signal.send())]

        self.loop.run_until_complete(asyncio.wait(tasks))
        for task in tasks:
            task.result()

        self.assertEqual(Test.count, 1)

    def test_class_method_coro(self):
        # test that our exception is being raised
        class Test:
            count = 0

            @classmethod
            @asyncio.coroutine
            def method(cls, *args, **kwargs):
                cls.count += 1

        callback = Test.method

        signal = Signal(loop=self.loop)

        tasks = [self.loop.create_task(signal.connect(callback))]

        self.loop.run_until_complete(asyncio.wait(tasks))
        for task in tasks:
            task.result()

        tasks = [self.loop.create_task(signal.send())]

        self.loop.run_until_complete(asyncio.wait(tasks))
        for task in tasks:
            task.result()

        self.assertEqual(Test.count, 1)

    def test_restricted_keywords(self):
        keywords = ('callback', 'key', 'keys', 'sender', 'senders', 'weak')

        for key in keywords:
            kwargs = {key: 'value'}
            self.assertRaises(ValueError, Signal, **kwargs)


@unittest.skipIf((sys.version_info.major == 3) and (sys.version_info.minor < 5),
                 "async and await syntax did not exist before python version 3.5")
class TestSignal_Py35(unittest.TestCase):
    '''
    Tests new syntax available in python version 3.5 an later
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
