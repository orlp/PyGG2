from __future__ import division, print_function

import sys, os, platform
import glob, shutil

def remove(name):
    try:
        for file in glob.glob(name):
            try: os.remove(file)
            except: pass
    except: pass

if sys.argv[1] == "build":
    if platform.system() == "Windows":
        import build_win
        build_win.build()
    else:
        print(platform.system() + " not supported.")
elif sys.argv[1] == "clean":
    remove("*.pyc")
    remove("*.pyo")
    remove("game_profile")
    remove("profile.txt")
    try: shutil.rmtree("dist")
    except: pass
elif sys.argv[1] == "test":
    import main
    main.GG2main()