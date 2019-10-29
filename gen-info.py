# Gen a config file with these contents
# See distutils.dist:...find_config_files() for where to stick the config file
"""
[global]
command_packages=mypkg.distcommands
"""

# File must mypkg.distcommands.<command>, class is <command>(distutils.core.Command)

# Also, distutils.extension.read_setup_file() can read Modules/Setup
# Although I'm not sure that's strictly needed; the default seems to be good for
# core, we just need to extend it.

import sys
import os
import json
from distutils.core import Command
import distutils.command # noqa

SRC_DIR = '/home/astraluma/src/cpython'

# Mock some modules so our command is discoverable
sys.modules['distutils.command.ext_info'] = sys.modules['__main__']
sys.modules['distutils.command'].ext_info = sys.modules['__main__']


# Define our command
class ext_info(Command):
    description = "dump information about extensions"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print(json.dumps([
            vars(ext)
            for ext in self.distribution.ext_modules
        ]))


# Run setup.py
os.chdir(SRC_DIR)
sys.argv = ['setup.py', '--quiet', 'ext_info']
with open('setup.py', 'rt') as f:
    exec(f.read())
