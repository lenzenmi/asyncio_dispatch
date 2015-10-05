.. asyncio_dispatch documentation master file, created by
   sphinx-quickstart on Fri Oct  2 14:26:44 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to asyncio_dispatch's documentation!
============================================

``aysincio_dispatch`` is a signal dispatcher for the :mod:`asyncio` event loop.

Synopsis
========

Many callbacks can be connected to a Signal. When the Signal is triggered using its ``send()`` method, all connected callbacks will be scheduled for asynchronous execution.

Connections can optionally be made using with types of filters, ``senders`` and ``keys``. If filters are used, the callback is only scheduled for execution if the Signal is sent with at least one matching ``sender`` or ``key``. A ``sender`` can be any object, while a ``key`` is more likely to be a ``string``. Under the hood, they use ``id()`` and ``hash()`` respectively.

Callbacks are invoked with keyword arguments that allow the callback to determine which Signal is calling it and which ``senders`` and ``keys`` were specified. Additional keyword arguments can be added to the Signal when it is instantiated, and their default values can be replaced when the Signal is sent.

Contents:

.. toctree::
   :maxdepth: 2
   
   introduction
   examples
   api
   


  

   


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

