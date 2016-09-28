import os
import re
import sys
import time
from termcolor import cprint, colored

j = os.path.join

def to_save(line,ty,root_dir):
    if not os.path.exists(os.path.join(root_dir,ty)):
        with open(os.path.join(root_dir,ty), "w") as fp:
            pass

    with open(os.path.join(root_dir,ty), "a+") as fp:
        print(line, file=fp)

def file_search(info, fs):
    for f in fs:
        cprint("--> file: %15s" % colored(f,attrs=['bold']), 'yellow', file=sys.stderr)
        with open(f) as fp:
            dic = {}
            for line in fp:
                l = line.strip()
                if re.search(re.compile('(%s)' % info), l):
                    yield l

def call_vim(tmp_file="/tmp/add.log.tmp.log"):
    from fabric.api import output
    from fabric.api import local
    output.running = False
    local("vim %s" % tmp_file)
    time.sleep(0.5)
    with open(tmp_file) as fp:
        text = fp.read()
        return text