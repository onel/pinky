import sys
from . import Pinky

def main():
    a = sys.argv
    
    if len(a) != 2:
        print 'pinky receives just one argument: the html string'
        return

    result = Pinky.parse(a[1])

    return result