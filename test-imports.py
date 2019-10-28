# Use a built-in module
import socket
import struct
import subprocess

# Direct native modules
import mmap
import parser
import readline
import resource
import termios

# Use a native module
import bz2
import contextvars
import crypt
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
import tkinter
import uuid

import asyncio  # At the end because it's complex and uses lots of stuff
