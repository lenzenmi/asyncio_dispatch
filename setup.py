from setuptools import setup
import asyncio_dispatch

setup(
    name="HelloWorld",
    version="1.0.0",
    packages=['asyncio_dispatch'],
    package_data={
        # Include readme and license
        '': ['LICENSE.txt', 'README.rst'],
    },

    # Metadata
    author="Mike Lenzen",
    author_email="lenzenmi@gmail.com",
    description="This is an Example Package",
    license="PSF",
    keywords="asyncio_dispatch is a is a signal dispatcher for the ``asyncio`` event loop found in Python versions 3.4 and up.",
    url="https://github.com/lenzenmi/asyncio_dispatch/",


)
