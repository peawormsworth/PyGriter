# Griter

python class for Grey Code counting

[The source of this project is available here][src].

Structure
---------

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

Usage
-----

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



Related Topics
--------------

[Grey code - Wikipedia][grey_code]

Progress
--------

Educational code work in progress.

[src]: https://github.com/peawormsworth/PyGriter
[grey_code]: https://en.wikipedia.org/wiki/Gray_code
