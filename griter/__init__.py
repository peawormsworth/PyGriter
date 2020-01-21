# $Id: giter/__init__.py $
# Author: Jeff Anderson <truejeffanderson@gmail.com>
# Copyright: AGPL
"""
Griter - python class for Grey Code counting.

griter.Greystate  - greycode state machine with decrement options
griter.Greystring - greycode iterator in string manipulation format
griter.Greylog    - greycode iterator in integer format

from gitter import *
g = Greystate('101010')
g.inc()
print('next greystate is:', g)
g.dec()
print('before that it was:', g)

s = Greystring()
l = Greylog()
for i in range(10):
  print('%20s20s' % (s,l))

The primary purpose of these programs is to create counters with:
- no binary shift manipulations
- manipulate string symbols according to a grey code counter.
- use regex for symbol manipulation
- limit the steps on determining adjacent states

There is a very simple alternate process that creates the grey code.
It is entirely graphical. Simply add an additional hidden least significant 
digit to the end of your code. On each step flip that bit and also
flip the bit to the left of the right most 1 (bit that is true).
Following these two simple steps at each step will produce the
grey code in the remaining bit locations of your string.

It is not neccessary to convert greyscale to binary for incremental changes.

The addition of a hidden bit on the right provides parity tracking so there is
no reason to calculate it on each step. But also, the location of the bits on 
the right side of the string tell you everything you need to know about how to 
step forwards or backwards in the code without ever having to know that state of
the left most bits.

For that reason, I assumed there might be a single regex (regular expression) to
describe grey code increment process. I didn't find it. But it might be possible.
The process is just string manipulating based on its current state. A single
regex should cover it. Let me know if you find it.

These programs highlight these ideas.


Input is not validated.
Output are strings of grey-code reflected binary.

author: Jeffrey B Anderson - truejeffanderson at gmail.com
source: https://github.com/peawormsworth/PyGriter
   ref: https://en.wikipedia.org/wiki/Gray_code
"""

import re

class Greystate ():
    """
Greystate provides a symbol manipulation state machine.
options: code=string of symbols, symbols=2 char string, direction=boolean
methods: inc(), dec()

Warning: direction is a parity. If the parity is even, the count will
proceed "forward", if it is odd it will count the other way on increments.
However, forward and backwards are relative terms for a pattern that loops.
ie: forward = backwards (at a different spot in the pattern)
    """

    flip = lambda m,x: m.symbols[x == m.symbols[0]]

    def __init__ (self, code='000', symbols='01', direction=True):
        self.symbols    = symbols
        self.code       = code + symbols[not direction]
        self.before_one = re.compile(r'^(.*)(.)(%s[^%s]*)$' % ((symbols[1],)*2))

    def inc (self): self.go( 1)
    def dec (self): self.go(-1)

    def steps (self):
        return [ self.flip_last, self.flip_before_last_one ]

    # inc() and dec() are the same functions with steps processed in reverse...
    def go (self,order=1):
        for f in self.steps()[::order]: f()

    def flip_last (self):
        self.code = self.code[:-1] + self.flip(self.code[-1])

    def flip_before_last_one (self):
        try: 
            before,char,after = self.before_one.findall(self.code)[0]
            self.code = before + self.flip(char) + after
        except IndexError:
            pass

    def __str__ (self):
        return '%s' % self.code[:-1]

    def __repr__ (self):
        return "%r(code='%r',symbols='%r',direction='%r')" % (
            type(self).__name__, self.code[:-1], self.symbols, not self.code[-1])

    def __next__ (self):
        self.inc()
        return self.code



class Greystring ():
    """
Greystring provides a string symbol manipulation iterator.
options: code=string, symbols=2 char string, direction=boolean
usage: iterator

During inc() the last character in the string is flipped first
then the character before the last one set to symbol 2 is flipped
if the whole string is set to symbol 1, this 2nd step is skipped.
That is normal, because the parity is always flipped.
So although the state does not change the parity does and the state is
ready to continue the pattern on as a reflection of what it just did.
the double beat in the pattern represents a location where the display
has run out of characters to flip. The code would be changed at a bit
that exceeds the display length. ie: this is normal for grey code.
    """

    flip = lambda m,x: m.symbols[x == m.symbols[0]]

    def state  (self): return self.code[:-1]
    def parity (self): return self.code[ -1]

    def __init__ (self, code='000', symbols='01', parity=True):
        self.symbols    = symbols
        self.code       = code + symbols[not parity]
        self.before_one = re.compile(r'^(.*)(.)(%s[^%s]*)$' % ((symbols[1],)*2))

    def __next__ (self):
        self.code = self.state() + self.flip(self.parity())
        try:
            pre, char, post = self.before_one.findall(self.code)[0]
            self.code = pre + self.flip(char) + post
        except IndexError:
            pass
        return self.code

    def __iter__ (self):
        return self

    def __str__ (self):
        return '%s' % self.state()

    def __repr__ (self):
        return "%r(code='%r',symbols='%r',direction='%r')" % (
            type(self).__name__, self.state(), self.symbols, self.parity())


class Greylog ():
    """
Greylog provides an integer manipulation iterator.
options: code=int, parity=int
note: code input is a raw integer value of the greycode state value.
usage: iterator

next() flips the last bit and then the bit just prior to the most right bit 
set to 1. And n is largest power of 2 that divides the code evenly.
aka: count of zeros on the right side of binary code
    """

    def __init__ (self, code=0, parity=0):
        self.code = code * 2 + parity

    def __next__ (self):
        self.code = self.code ^ 1
        n = 2
        while n/2 < self.code and self.code % n == 0:
            n *= 2
        self.code = self.code ^ n
        return self

    def __iter__ (self):
        return self

    def __str__ (self):
        return '%s' % bin(self.code // 2)[2:]

    def __repr__ (self):
        return "%r(code='%r',parity='%r')" % (
            type(self).__name__, self.code // 2, self.code % 2)


