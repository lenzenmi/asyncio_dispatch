README
======

``asyncio_dispatch`` is a is a signal dispatcher for the ``asyncio`` event loop found in Python versions 3.4 and up.

Example
-------

.. code:: python

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
    
    
Features
--------

* Callbacks can be a standard function, coroutine, method, staticmethod, or classmethod
* Multiple callbacks can be connected to the same signal
* Callbacks can be called with additional keyword arguments containing references to arbitrary objects
* Callbacks can be disconnected from a signal
* Signals can hold weak or strong references to callbacks, allowing for automatic disconnection if a reference to a callback is not maintained, or conversely to persist one-off ``lambda`` expressions without needing to maintain a reference
* Callbacks receive the ``Signal`` object that was used to schedule it, so multiple signals can be attached to the same callback and handled differently
* Callbacks can be connected with ``senders`` or ``keys`` which cause the callback to ignore the Signal unless it is sent with a matching *Object* or *str* 

License
-------

Released under the MIT license.

Installation
------------
.. code:: bash
    
    pip install asyncio_dispatch

    

