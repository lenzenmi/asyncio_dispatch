README
======
.. image:: https://travis-ci.org/lenzenmi/asyncio_dispatch.svg?branch=master
    :target: https://travis-ci.org/lenzenmi/asyncio_dispatch

.. image:: https://readthedocs.org/projects/asyncio-dispatch/badge/?version=latest
    :target: http://asyncio-dispatch.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://coveralls.io/repos/lenzenmi/asyncio_dispatch/badge.svg?branch=master&service=github 
    :target: https://coveralls.io/github/lenzenmi/asyncio_dispatch?branch=master 



``asyncio_dispatch`` is a is a signal dispatcher for the ``asyncio`` event loop found in Python versions 3.4 and up.

Check out the `official documentation <http://asynqio-dispatch.readthedocs.org/en/latest/>`_

Synopsis
--------

Many callbacks can be connected to a Signal. When the Signal is triggered using its ``send()`` method, all connected callbacks will be scheduled for asynchronous execution.

Connections can optionally be made with two types of filters, ``senders`` and ``keys``. If filters are used, the callback is only scheduled for execution if the Signal is sent with at least one matching ``sender`` or ``key``. A ``sender`` can be any object, while a ``key`` is more likely to be a ``string``. Under the hood, they use ``id()`` and ``hash()`` respectively.

Callbacks are invoked with keyword arguments that allow the callback to determine which Signal is calling it and which ``senders`` and ``keys`` were specified. Additional keyword arguments can be added to the Signal when it is instantiated, and their default values can be replaced when the Signal is sent.

Example
-------

.. code:: python

    import asyncio
    from asyncio_dispatch import Signal
    
    
    @asyncio.coroutine
    def callback(**kwargs):
        print('callback was called!')
    
    
    loop = asyncio.get_event_loop()
    
    # create the signal
    signal = Signal(loop=loop)
    
    # connect the callback to the Signal - This is a coroutine!
    loop.run_until_complete(loop.create_task(signal.connect(callback)))
    
    # send the signal - This is also a coroutine!
    print('sending the signal.')
    loop.run_until_complete(loop.create_task(signal.send()))
    
    
The above example will print the following:

.. code:: bash

    sending the signal.
    callback was called!
    
Features
--------

* Supports the new async/await syntax found in python 3.5 and up
* Callbacks can be a function, asyncio.coroutine, async def, class method, @staticmethod, or @classmethod
* Multiple callbacks can be connected to the same signal
* Callbacks can be called with additional keyword arguments containing references to arbitrary objects
* Callbacks can be disconnected from a signal
* Signals can hold weak or strong references to callbacks, allowing for automatic disconnection if a reference to a callback is not maintained, or conversely to persist one-off ``lambda`` expressions without needing to maintain a reference
* Callbacks receive the ``Signal`` object that was used to schedule it, so multiple signals can be attached to the same callback and handled differently
* Callbacks can be connected with ``senders`` or ``keys`` which cause the Signal to ignore the callback unless the signal is sent with a matching *Object* or *str* 

License
-------

Released under the MIT license.

Installation
------------
.. code:: bash
    
    pip install asyncio_dispatch

    

