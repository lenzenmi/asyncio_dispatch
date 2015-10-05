import asyncio
from asyncio_dispatch import Signal


def callback(signal, senders, keys, my_kwarg, payload):
    print('-' * 50)
    print()

    if SIGNAL is signal:
        print('signals match as expected!')

    print('senders=', senders)
    print('keys=', keys)
    print('my_kwarg= {}'.format(my_kwarg))
    print('payload= {}'.format(payload))


loop = asyncio.get_event_loop()

# create the signal and define two custom keyword arguments
SIGNAL = Signal(loop=loop, my_kwarg='default', payload={})

# connect the coroutine and standard function
loop.run_until_complete(loop.create_task(SIGNAL.connect(callback)))

# send the signal with default my_kwarg
loop.run_until_complete(loop.create_task(SIGNAL.send()))

# send the signal again with new my_kwarg and payload
loop.run_until_complete(
    loop.create_task(SIGNAL.send(my_kwarg='changed with send',
                                 payload={'anything': 'a dict can hold!',
                                          'really': 'powerfull'}))
)
