#!/usr/bin/python3
from griter import *
import unittest

verbose = 1

class TestComparison(unittest.TestCase):

    bits = 18

    def test_comparison(self):
        """Compare output from classes run in parallel"""
        a = Greystring('0'*self.bits)
        b = Greystate ('0'*self.bits)
        c = Greylog(0)

        fmat = '%33s%33s%33s'
        print(fmat % ('Greystate','Greystring','Greylog'))
        if verbose: print(fmat % (a,b,c))
        for i in range(2**self.bits-1):
            next(a)
            next(b)
            next(c)
            if verbose: print(fmat % (a,b,c))
            lc = len(str(c))
            self.assertEqual(str(a),str(b))
            self.assertEqual(str(a)[-lc:],str(c))
            self.assertEqual(str(b)[-lc:],str(c))


# this isn't really a test at all
# but it looks neat and it will freak out testers
class TestSymbols(unittest.TestCase):

    bits = 20 

    def test_symbols(self):
        """Alternate code symbols"""
        a = Greylog()
        b = Greystate('_'*self.bits,symbols='_8')
        c = Greystring('|'*self.bits,symbols='|_')

        fmat = '%33s%33s%33s'
        for i in range(2**self.bits-1):
            next(a)
            next(b)
            next(c)
            if verbose: print(fmat % (a,b,c))



if __name__ == '__main__':

    unittest.main()
