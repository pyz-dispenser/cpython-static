"""
Given the JSON from gen-info.py (on stdin), produce a Setup file (on stdout).

After changing Modules/Setup*, makesetup needs to be rerun. You can do this by
re-running ./configure, or by invoking makesetup yourself (see the end of
configure.ac).
"""
import collections
import json
import subprocess
import sys

# These modules are always omitted
BLACKLIST = {
    # Test modules
    # '_testcapi', '_testinternalcapi', '_testbuffer', '_testimportmultiple',
    # '_testmultiphase', '_xxtestfuzz',
    # Demos
    'xxlimited',
    # Not sure what this is or why it's in the source tree
    '_xxsubinterpreters',
    # Can't be built via Modules/Setup
    '_sqlite3',  # https://bugs.python.org/issue37839
    '_tkinter',  # conflicts around expat, will come back to it

    # PEP 594 ("Removing dead batteries from the standard library")
    # recommends removing these.
    # https://www.python.org/dev/peps/pep-0594/
    'spwd', 'parser', 'audioop', '_crypt', 'ossaudiodev', 'nis'
}

# Make defaultdict subclass that defaults to getting stuff from pkg-config
# Make routine to resolve


class PkgConfigDict(collections.defaultdict):
    def __getitem__(self, key):
        return super().__getitem__(key.lower())

    def __missing__(self, key):
        proc = subprocess.run(
            ['pkg-config', '--libs', '--static', key.lower()],
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL, encoding='utf-8',
        )
        if proc.returncode == 0:
            self[key] = [
                item
                for item in proc.stdout.strip().split(' ')
                # This assumes we're using vendored expat and we're compiling it in
                if item != '-lexpat'
            ]
            return self[key]
        else:
            raise KeyError(key)

    def recursive(self, key):
        """
        Gets data for a library, recursing into libraries it references
        """
        seen = set()
        unseen = {key.lower()}
        while unseen:
            lib = unseen.pop()
            seen.add(lib)

            try:
                data = self[lib]
            except KeyError:
                continue
            yield from data
            unseen.update({
                arg[2:].lower()
                for arg in data
                if arg.startswith('-l')
            } - seen)


pkg_config = PkgConfigDict()


def gen_args(mod):
    # Reverses what distutils.extension.read_setup_file() does.
    yield from mod['sources']
    if mod['name'] in ('math', 'cmath'):
        # Both math and cmath need _math.c
        yield '_math.c'
    yield from (f'-I{i}' for i in mod['include_dirs'])
    # makesetup can't handle -Dspam=eggs, https://bugs.python.org/issue37839
    yield from (
        f'-D{name}' #if val is None else f'-D{name}={val}'
        for name, val in mod['define_macros']
        if val in (None, 1, "1")
    )
    yield from (f'-U{i}' for i in mod['undef_macros'])
    if mod['name'] == '_testcapi':
        yield from ('-UPy_BUILD_CORE', '-UPy_BUILD_CORE_BUILTIN')
    yield from (
        i if i[:2] in ('-D', '-W') else f'-C{i}'
        for i in mod['extra_compile_args']
    )
    yield from (f'-l{i}' for i in mod['libraries'])
    yield from (f'-L{i}' for i in mod['library_dirs'])
    yield from (f'-R{i}' for i in mod['runtime_library_dirs'])
    assert not mod['extra_link_args']
    for lib in mod['libraries']:
        yield from pkg_config.recursive(lib.lower())


print("# Generated by gen-setup.py")
print("*static*")
print("")
for mod in json.load(sys.stdin):
    if mod['name'] in BLACKLIST:
        continue
    print(f"{mod['name']} {' '.join(gen_args(mod))}")

# Make extra sure about trailing newline
print("# Blank line required")
print("")
