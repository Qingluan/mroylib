#!/usr/bin/env python3
def eq(*args):
    fir = args[0]
    a = {fir}
    for i in args:
        if i not in a:
            return True
    return False


                                       

