Examples
========

The :class:`asyncio_dispatch.Signal` class is used to connect and trigger callbacks.

Basic example
^^^^^^^^^^^^^

In this example, the callback is connected to the signal. When the signal is sent, the execution of the callback will be scheduled. The event loop will run for 1 second before exiting.

.. literalinclude:: examples/basic.py
    :language: python
    
Mulitple types of callables
^^^^^^^^^^^^^^^^^^^^^^^^^^^

In this example, 5 different types of callable are all connected to the same signal. When the signal is sent, all 5 callbacks will be scheduled for execution.

.. literalinclude:: examples/callables.py
    :language: python
    
Example with kwargs
^^^^^^^^^^^^^^^^^^^

Signals always send some keyword arguments. It's good practice to always include a ``**kwargs`` argument in your callback in case you decide to change the number of keyword arguments sent later. The default kwargs are ``signal``, ``senders``, and ``keys``. ``senders`` and ``keys`` each return a set containing all the ``senders`` and ``keys`` specified when the signal was sent. 

You can add your own custom kwargs to a signal as shown. Each additional kwarg added to the signal has a default value that is specified when the signal is instantiated. The default value of the additional kwargs can be changed when the signal is sent.

.. literalinclude:: examples/kwargs.py
    :language: python

Selective examples
^^^^^^^^^^^^^^^^^^

Sometimes you only want to receive a signal if a certain condition occurs. This can be done by adding ``senders`` or ``keys``.

.. literalinclude:: examples/selective.py
    :language: python