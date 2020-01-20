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
- a regex style symbol manipulation counter using strings.
- limit the steps on determining adjacent states

There is a very simple alternate process that creates the grey code.
It is entirely graphical. Simply add an additional hidden least significant 
digit to the end of your code. On each step flip that bit and also
flip the bit to the left of the right most 1 (bit that is true).
Following these two simple steps at each step will produce the
grey code in the remaining bit locations of your string.

The addition of a hidden bit on the right provides parity tracking so there is
no reason to calculate it on each step. But also, the location of the bits on 
the right side of the string tell you everything you need to know about how to 
step forwards or backwards in the code without ever having to know that state of
the left most bits.

These programs highlight these ideas.

Output is in grey-code reflected binary.

author: Jeffrey B Anderson - truejeffanderson at gmail.com
source: https://github.com/peawormsworth/PyGriter
   ref: https://en.wikipedia.org/wiki/Gray_code
"""

import re
import unittest

class Greystate ():
    """
Greystate provides a symbol manipulation state machine.
options: code=string, symbols=2 char string, direction=boolean
methods: inc(), dec()
    """

    flip = lambda m,x: m.symbols[x == m.symbols[0]]

    def __init__ (self, code='000', symbols='01', direction=True):
        self.symbols    = symbols
        self.code       = code + symbols[not direction]
        self.before_one = re.compile(r'^(.*)(.)(%s[^%s]*)$' % ((symbols[1],)*2))

    def dec (self): self.go(False)
    def inc (self): self.go(True )

    def flip_last (self):
        self.code = self.code[:-1] + self.flip(self.code[-1])

    def flip_before_last_one (self):
        try: 
            before,char,after = self.before_one.findall(self.code)[0]
            self.code = before + self.flip(char) + after
        except IndexError:
            pass

    def go (self, oriented=True):

        if oriented: self.flip_last()
        self.flip_before_last_one()
        if not oriented: self.flip_last()

    def __str__ (self):
        return '%s' % self.code[:-1]

    def __repr__ (self):
        return "%r(code='%r',symbols='%r',direction='%r')" % (
            type(self).__name__, self.code[:-1], self.symbols, not self.code[-1]
        )

    def __next__ (self):
        self.inc()
        return self.code



class Greystring ():
    """
Greystring provides a string symbol manipulation iterator.
options: code=string, symbols=2 char string, direction=boolean
usage: iterator
    """
    flip = lambda m,x: m.symbols[x == m.symbols[0]]

    def __init__ (self, code='000', symbols='01', direction=True):
        self.symbols    = symbols
        self.code       = code + symbols[not direction]
        self.before_one = re.compile(r'^(.*)(.)(%s[^%s]*)$' % ((symbols[1],)*2))

    def __next__ (self):
        state, parity = self.code[:-1], self.code[-1]
        self.code = state + self.flip(parity)
        try:
            pre, char, post = self.before_one.findall(self.code)[0]
            self.code = pre + self.flip(char) + post
        except IndexError:
            pass
        return self.code

    def __iter__ (self):
        return self

    def __str__ (self):
        return '%s' % self.code[:-1]

    def __repr__ (self):
        return "%r(code='%r',symbols='%r',direction='%r')" % (
            type(self).__name__, self.code[:-1], self.symbols, not self.code % 2
        )


class Greylog ():
    """
Greylog provides an integer manipulation iterator.
options: code=int, parity=int
note: code input is a raw integer value of the greycode state value.
usage: iterator
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
            type(self).__name__, self.code // 2, self.code % 2
        )



class TestGreystring (unittest.TestCase):
    verbose = 1
    expect = """
     000 001 011 010 110 111 101 100
     100 101 111 110 010 011 001 000
     000 001 011 010 110 111 101 100
     100 101 111 110 010 011 001 000
     000 001 011 010 110 111 101
""".split()

    def test_forward_reverse(m):
        g = Greystring('000')
        print('Check 35 strings starting from "%s"...' % (g))
        for e in m.expect:
            m.assertEqual(e,str(g))
            if m.verbose: print('%8s' % (g))
            g.inc()

    def test_reverse(m):
        #g = Greystring('101')
        g = Greystring('101')
        print('Check 35 strings back starting from "%s"...' % (g))
        for e in m.expect[::-1]:
            if m.verbose: print('%8s' % (g))
            m.assertEqual(e,str(g))
            g.dec()

    def test_big_count(m):
        g = Greystring('0'*20)
        for i in range(78329):
            print('g:',g)
            g.inc()
        print('final g:',g)


if __name__ == '__main__':

    unittest.main()

