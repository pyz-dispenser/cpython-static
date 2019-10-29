import json
import sys


def gen_args(mod):
    # Reverses what distutils.extension.read_setup_file() does.
    yield from mod['sources']
    yield from (f'-I{i}' for i in mod['include_dirs'])
    yield from (
        f'-D{name}' if val is None else f'-D{name}={val}'
        for name, val in mod['define_macros']
    )
    yield from (f'-U{i}' for i in mod['undef_macros'])
    yield from (
        i if i.startswith('-D') else f'-C{i}'
        for i in mod['extra_compile_args']
    )
    yield from (f'-l{i}' for i in mod['libraries'])
    yield from (f'-L{i}' for i in mod['library_dirs'])
    yield from (f'-R{i}' for i in mod['runtime_library_dirs'])
    assert not mod['extra_link_args']


print("# Generated by gen-setup.py")
for mod in json.load(sys.stdin):
    print(f"{mod['name']} {' '.join(gen_args(mod))}")

# Make extra sure about trailing newline
print("")
