import sys

# Ignore tests that can't complete on older versions of python

collect_ignore = ["setup.py"]
if sys.version_info < (3, 5):
    collect_ignore.append("asyncio_dispatch/tests/test35_dispatcher.py")
