from __future__ import division, print_function

import sys, os, platform, os.path
import glob, shutil
import subprocess
import distutils.sysconfig

def remove(name):
    try:
        for file in glob.glob(name):
            try: os.remove(file)
            except: pass
    except: pass

if len(sys.argv) == 1: sys.exit()

if sys.argv[1] == "build":
    if len(sys.argv) > 2 and sys.argv[2] == "dist":
        if platform.system() == "Windows":
            import build_win
            sys.argv = sys.argv[:2]
            build_win.build()
        else:
            print(platform.system() + " not supported.")
    else:
        includes = distutils.sysconfig.get_python_inc()
        libs = os.path.join(includes, "../libs")
        
        subprocess.call("gcc -fPIC -O3 -c -o c/bitmask.o c/bitmask.c", shell=True)
        subprocess.call("gcc -I%s -fPIC -O3 -c -o c/_mask.o c/_mask.c" % includes, shell=True)
        subprocess.call("gcc -shared -o c/_mask.pyd c/bitmask.o c/_mask.o -L%s -lpython27" % libs, shell=True)
elif sys.argv[1] == "clean":
    remove("*.pyc")
    remove("c/*.pyc")
    remove("*.pyo")
    remove("c/*.o")
    remove("game_profile")
    remove("profile.txt")
    try: shutil.rmtree("dist")
    except: pass
elif sys.argv[1] == "test":
    import main
    main.GG2main()
