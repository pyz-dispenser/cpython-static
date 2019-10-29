Static Python
=============

This is meant to be a maintained way to provide static python builds for multiple platforms.

Provided artifacts:
* `python` and `pythonw`
* `libpython`
* The standard library (zipfile)

Everything native should be compiled in.

TODO: Artifact URLs

Regenerating Setup.local
========================

`Setup.local` is the specific configuration for CI's build environment. It can vary, depending on what CPython's `setup.py` detects.

To rebuild it for the repo:
1. Pull `mods.json` from the modinfo job
2. Run `python3 gen-setup.py < mods.json > Setup.local`
3. Commit the new file

If you are doing your own build, you'll need to run `gen-info.py` yourself. (See the docstring in that script.)
