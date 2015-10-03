from setuptools import setup

with open('README.rst') as file:
    long_description = file.read()

setup(
    name="asyncio_dispatch",
    version="1.0.0",
    packages=['asyncio_dispatch'],
    package_data={
        # Include readme and license
        '': ['LICENSE.txt', 'README.rst'],
    },

    # Metadata
    author="Mike Lenzen",
    author_email="lenzenmi@gmail.com",
    description="asyncio_dispatch is a is a signal dispatcher for the ``asyncio`` event loop found in Python versions 3.4 and up.",
    long_description=long_description,
    keywords="asyncio_dispatch asyncio dispatch signal event",
    url="https://github.com/lenzenmi/asyncio_dispatch/",
    classifiers=[
                 'License :: OSI Approved :: MIT License',
                 'Intended Audience :: Developers',
                 'Programming Language :: Python :: 3.4',
                 'Topic :: Software Development :: Libraries',
                 'Development Status :: 4 - Beta'
                 ]
)
