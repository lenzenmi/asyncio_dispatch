Introduction
============

Prerequisites
-------------

``asyncio_dispatch`` works with the :mod:`asyncio` library found in python versions 3.4 and up.

Installation
------------

You can install the most recent asyncio_dispatch release from pypi using pip::

    pip install asyncio_dispatch
    
    
Contributions and Source
------------------------

Source code is available at https://github.com/lenzenmi/asyncio_dispatch

Any contributions will be welcomed, especially those to improve testing and compatibility with the new python 3.5 asynchronous syntax, or asyncio backports like *trollius* and *tulip*.

Because the python syntax varies by python version, tests are run with tox against all supported versions. 

.. warning:: 
    
    The tox command must be run with python version 3.5 or greater.

**Run all tests**

.. code:: bash
    
    pip install tox
    tox 
    
    
**Run specific tox envoronment tests**

.. code:: bash
    
    pip install tox
    tox -e py35 # or py34
    tox -e flake8
    tox -e docs
    
**Run all tests for the python environments you have installed on your system**

.. code:: bash
    
    pip install tox
    tox --skip-missing-interpreters


License
-------

Licensed under the MIT license.