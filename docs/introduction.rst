Introduction
============

Prerequisites
-------------

Asyncio_dispatch works only with python 3.4 using the asyncio library.


Installation
------------

You can install the most recent asyncio_dispatch release from pypi using pip::

    pip install asyncio_dispatch
    
    
Contributions and Source
------------------------

Source code is available at https://github.com/lenzenmi/asyncio_dispatch

Any contributions will be welcomed, especially those to improve testing and compatibility with the new python 3.5 asynchronous syntax, or asyncio backports like *trollius* and *tulip*.

To ensure code quality and tests pass, please run both pytest and flake8 from the root project directory.

.. code:: bash
    
    pip install pytest flake8
    py.test
    flake8 --max-line-length=100 asyncio_dispatch


License
-------

Licensed under the MIT license.