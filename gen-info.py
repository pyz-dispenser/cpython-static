# Also, distutils.extension.read_setup_file() can read Modules/Setup
# Although I'm not sure that's strictly needed; the default seems to be good for
# core, we just need to extend it.

import sys
import os

# This has to be as soon as possible, sysconfig uses it at the global level
assert '_PYTHON_PROJECT_BASE' in os.environ
sys._home = SRC_DIR = os.environ['_PYTHON_PROJECT_BASE']

import json
from pathlib import Path
from distutils.core import Command
import distutils.command # noqa

SRC_DIR = Path(SRC_DIR)

# Mock some modules so our command is discoverable
sys.modules['distutils.command.ext_info'] = sys.modules['__main__']
sys.modules['distutils.command'].ext_info = sys.modules['__main__']

# Grab the build info, if available
# FIXME: This is generated after the python build, can we mock it from the Makefile?
try:
    scd_filename = next(SRC_DIR.glob('build/lib.*/_sysconfigdata_*.py'))
except StopIteration:
    print("sysconfigdata not found", file=sys.stderr)
else:
    print(f"Loading {scd_filename}", file=sys.stderr)
    import importlib.util
    spec = importlib.util.spec_from_file_location(scd_filename.stem, scd_filename)
    scd_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scd_mod)
    sys.modules[scd_mod.__name__] = scd_mod
    os.environ['_PYTHON_SYSCONFIGDATA_NAME'] = scd_mod.__name__


# Define our command
class ext_info(Command):
    description = "dump information about extensions"
    user_options = []

    def initialize_options(self):
        self.extensions = []

    def finalize_options(self):
        self.extensions = self.distribution.ext_modules[:]
        # Mock out enough of setup.py's build_ext command to get the extension info
        buildext = globals()['PyBuildExt'](self.distribution)  # Class from setup.py
        buildext.build_extensions = lambda: None
        buildext.initialize_options()
        buildext.finalize_options()
        buildext.run()
        import sysconfig
        buildext.srcdir = sysconfig.get_config_var('srcdir')
        buildext.detect_modules()
        self.extensions += buildext.extensions

    def run(self):
        # This right here is the heart of what we're doing.
        # Everything else is just setup and mocking to get this info to this point.
        print(json.dumps([
            vars(ext)
            for ext in self.distribution.ext_modules
        ], indent=2))


# Run setup.py
os.chdir(SRC_DIR)
sys.argv = ['setup.py', '--quiet', 'ext_info']
exec(Path('setup.py').read_text())
