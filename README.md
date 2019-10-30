Static Python
=============

This is meant to be a maintained way to provide static python builds for multiple platforms.

Provided artifacts:
* `python` and `pythonw`
* `libpython`
* The standard library (zipfile)

Everything native should be compiled in.

Artifacts
=========

Linux AMD64
-----------

* `python`: https://api.cirrus-ci.com/v1/artifact/github/pyz-dispenser/cpython-static/debian/binary/cpython/python
* `libpython.a` (for linking into your own app): https://api.cirrus-ci.com/v1/artifact/github/pyz-dispenser/cpython-static/debian/library/cpython/libpython3.8.a
  (NOTE: All the required linker flags are not yet published)
* `stdlib.zip`: https://api.cirrus-ci.com/v1/artifact/github/pyz-dispenser/cpython-static/debian/stdlib/stdlib.zip



Regenerating Setup.local
========================

`Setup.local` is the specific configuration for CI's build environment. It can vary, depending on what CPython's `setup.py` detects.

To rebuild it for the repo:
1. Pull `mods.setup` from the modinfo job and copy it to `Setup.local`
2. Strip `/tmp/cirrus-ci-build/cpython/` from the file
3. Commit the new file

If you are doing your own build, you'll need to run `gen-info.py` yourself. (See the docstring in that script.)
