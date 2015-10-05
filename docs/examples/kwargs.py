import asyncio
from asyncio_dispatch import Signal


def callback(signal, senders, keys, my_kwarg, payload):
    print()
    print('-' * 50)

    if SIGNAL is signal:
        print('signals match as expected!')

    print('senders=', senders)
    print('keys=', keys)
    print('my_kwarg= {}'.format(my_kwarg))
    print('payload= {}'.format(payload))


loop = asyncio.get_event_loop()

# create the signal and define two custom keyword arguments: my_kwarg and payload
SIGNAL = Signal(loop=loop, my_kwarg='default', payload={})

# connect the callback to the signal - this method is a coroutine
loop.run_until_complete(loop.create_task(SIGNAL.connect(callback)))

# send the signal with default keyword arguments - this method is also a coroutine
loop.run_until_complete(loop.create_task(SIGNAL.send()))

# send the signal again with new values for my_kwarg and payload
loop.run_until_complete(
    loop.create_task(SIGNAL.send(my_kwarg='changed with send',
                                 payload={'anything': 'a dict can hold!',
                                          'really': 'powerfull'}))
)
