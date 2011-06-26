import os
import shutil
import stat
import sys
import zipfile
import tarfile
import string
import mkb_main
import mkb_util

import imp
import traceback

def run(mkb, global_path, args=None):
    '''start configure.py python scripts from project/subproject folders
    '''
    global_path = os.path.normcase(global_path)

    mkb_name = os.path.basename(mkb.options['mkb_in'])
    mkb_name = os.path.splitext(mkb_name)[0]

    print "Configuration for:",mkb_name
    configs = mkb.subprojects.keys() + [mkb.options['mkb_in'],]
    for c in configs:
        fullpath = os.path.normcase(c)
        name = os.path.splitext(os.path.basename(fullpath))[0]
        configpath = os.path.join(os.path.dirname(c),"configure.py")
        if not os.path.exists(configpath):
            continue
        f = None
        try:
            print "Loading configuration for the "+name
            f = open(configpath)
            m = imp.new_module(name)
            sys.modules[name] = m
            m = imp.load_module(name+".configure",f,configpath,("py","r",imp.PY_SOURCE))
            f.close()
            f = None
            if "run" in dir(m) and callable(m.run):
                print "Running configuration for the "+name
                m.run(fullpath, global_path, args)
            print "Configuration for the "+name+" is finished successfully"
        except Exception,ex:
            if f:
                f.close()
                f = None
            print "Configuration error for the "+name+":"
            traceback.print_exc()
            sys.stdin.readline()
        