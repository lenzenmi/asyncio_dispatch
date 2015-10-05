Examples
========

The :class:`asyncio_dispatch.Signal` class is used to connect and trigger callbacks.

.. note:: 

    It's suggested to look at all of the examples, the last two are the most interesting.

Basic example
^^^^^^^^^^^^^

In this example, the callback is connected to the signal. When ``Signal.send()`` is called, all connected callbacks without ``keys`` or ``senders`` will be executed. Since our single connected callback was connected without ``key`` or ``sender`` arguments, it will be run.

.. literalinclude:: examples/basic.py
    :language: python
    
The above example prints the following output
    
.. literalinclude:: examples/basic.out
    :language: bash         
    

Basic example with async/await syntax
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    
The same as above but with the new python 3.5 async/await syntax. The loop only runs long enough to send the signal and call the callback before exiting.

.. literalinclude:: examples/basic_35.py
    :language: python
    
The above example prints the following output
    
.. literalinclude:: examples/basic_35.out
    :language: bash     
    
Mulitple types of callables
^^^^^^^^^^^^^^^^^^^^^^^^^^^

In this example, 5 different types of callable are all connected to the same signal. When the signal is sent, all 5 callbacks will be scheduled for execution.

.. literalinclude:: examples/callables.py
    :language: python
    
The above example prints the following output
    
.. literalinclude:: examples/callables.out
    :language: bash  
     
    
Example with kwargs
^^^^^^^^^^^^^^^^^^^

Callbacks receive several kwargs when called. The default keyword arguments are ``signal``, ``senders``, and ``keys``. ``signal`` is the signal that called the callback. ``senders`` and ``keys`` each return a set containing all of the ``senders`` and ``keys`` specified when calling :meth:`asyncio_dispatch.Signal.send`. 

You can also add your own custom keyword arguments to a signal when it is instantiated. Each additional kwarg added to the signal has a default value. The value of the additional kwargs can be changed when the signal is sent.

.. literalinclude:: examples/kwargs.py
    :language: python

The above example prints the following output
    
.. literalinclude:: examples/kwargs.out
    :language: bash


Selective examples
^^^^^^^^^^^^^^^^^^

Sometimes you only want to receive a signal if a certain condition occurs. This can be done by adding ``senders`` or ``keys``.

.. literalinclude:: examples/selective.py
    :language: python
    
The above example prints the following output

    
.. literalinclude:: examples/selective.out
    :language: bash    
    