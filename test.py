#!/usr/bin/python3
from griter import *

for object in (Greystring, Greylog, Greystate):
#for object in (Greystring,):
    x = object()
    print(object.__name__)
    for i in range(20):
        print('%20s'%x)
        next(x)

exit;



