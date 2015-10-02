import asyncio
import pprint

from asyncio_dispatch import Signal


class Somebody:
    def message_received(self, signal, senders, keys, message):
        print('-' * 50)
        print('{} received a message'.format(self))
        print('-' * 50)
        if signal is SIGNAL1:
            print('SIGNAL #1 received')
        elif signal is SIGNAL2:
            print('SIGNAL #2 received')

        print('senders= ', end='')
        pprint.pprint(senders)
        print('keys= ', end='')
        pprint.pprint(keys)
        print('message= ', message)

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return self.__str__()


class Mike(Somebody):
    pass


class Ashley(Somebody):
    pass

mike = Mike()
ashley = Ashley()

loop = asyncio.get_event_loop()

# create the signals
SIGNAL1 = Signal(loop=loop, message=None)
SIGNAL2 = Signal(loop=loop, message=None)

# connect the signals. Mike and Ashley are each connected to different keys and senders.
loop.create_task(SIGNAL1.connect(mike.message_received,
                                 sender=ashley,
                                 keys=['important', 'books']))
loop.create_task(SIGNAL2.connect(mike.message_received,
                                 keys=['logs']))

loop.create_task(SIGNAL1.connect(ashley.message_received,
                                 sender=mike,
                                 keys=['love-notes', 'music']))
loop.create_task(SIGNAL2.connect(ashley.message_received,
                                 keys=['alert']))


# send the signal should be ignored by both Mike and Ashley
loop.create_task(SIGNAL1.send(message='nobody is listening'))
loop.create_task(SIGNAL2.send(message='nobody is listening'))

# Ashley sends Mike a message, and mike replies
loop.create_task(SIGNAL1.send(sender=ashley,
                              message='hello Mike!'))
loop.create_task(SIGNAL1.send(sender=mike,
                              message='hello Ashley!'))

# a important message and alert comes in
loop.create_task(SIGNAL1.send(key='important',
                              message='important message for Mike'))
loop.create_task(SIGNAL2.send(key='alert',
                              message='alert for Ashley'))

# then a book full of love notes
loop.create_task(SIGNAL1.send(keys=['books', 'love-notes'],
                              message="Mike is waiting for books, Ashley for love-notes"))

# if more than one sender or key match, only one execution of the callback is scheduled
loop.create_task(SIGNAL1.send(keys=['important', 'books', 'logs'],
                              message='Mike is subscribed to three keys, but only one message is sent!'))

# you get the idea

# run the event loop for 1 second and see what happens.
loop.run_until_complete(asyncio.sleep(1))
