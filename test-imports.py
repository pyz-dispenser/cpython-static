# Use a built-in module
import socket
import struct
import subprocess

# Direct native modules
import binascii
import mmap
import math
# import parser # See https://github.com/pyz-dispenser/cpython-static/pull/1
import readline
import resource
import termios

# Use a native module
import bz2
import contextvars
# import crypt # See https://github.com/pyz-dispenser/cpython-static/pull/1
import csv
import ctypes
import curses
import dbm
import decimal
import hashlib
import json
import lzma
import multiprocessing
import opcode
import queue
# import sqlite3
# import ssl
# import tkinter
import uuid

import asyncio  # At the end because it's complex and uses lots of stuff
