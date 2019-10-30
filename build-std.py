"""
Scan CPython source for the standard library and build a zip
"""
from pathlib import Path
import sys
import zipfile

SRC_DIR = Path(sys.argv[1])

LIB_DIRS = [
    SRC_DIR / 'Lib',
    *(SRC_DIR / 'build').glob('lib.*')
]

with zipfile.ZipFile('stdlib.zip', 'w') as dest:
    for libdir in LIB_DIRS:
        for fname in (libdir).glob("**/*.py"):
            # The test suite is about half the Lib code
            if 'test' in fname.parts:
                continue
            dest.write(fname, fname.relative_to(libdir))
