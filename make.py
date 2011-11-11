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

if sys.argv[1] == "build":
    includes = distutils.sysconfig.get_python_inc()
    libs = os.path.join(includes, "../libs")
    
    subprocess.call("gcc -O3 -c -o c/bitmask.o c/bitmask.c")
    subprocess.call("gcc -I%s -O3 -c -o c/_mask.o c/_mask.c" % includes)
    subprocess.call("gcc -shared -o c/_mask.pyd c/bitmask.o c/_mask.o -L%s -lpython27" % libs)
    
elif sys.argv[1] == "dist":
    if platform.system() == "Windows":
        import build_win
        build_win.build()
    else:
        print(platform.system() + " not supported.")
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