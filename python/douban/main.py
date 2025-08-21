import sys

from time_util import is_valid_time
from douban import get_douban

def init(argument):
    while True:
        if is_valid_time():
            get_douban(argument)

if __name__ == '__main__':

    if len(sys.argv) > 1:
        argument = sys.argv[1]
        if argument == 'm':
            init("m")
        else:
            init("p")
    else:
        init("m")
