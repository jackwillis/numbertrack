import sys
import cx_Freeze

base = None
if sys.platform == "win32":
    base = "Win32GUI"

packages = []

# need a db module for shelve
for dbmodule in ['dbhash', 'gdbm', 'dbm', 'dumbdbm']:
    try:
        __import__(dbmodule)
    except ImportError:
        pass
    else:
        packages.append(dbmodule)

cx_Freeze.setup( name = "Numbertrack",
                 version = "0.0.1",
                 description = "Numbertrack",
                 options = {
                        "packages": packages
                    }
                 },
                 executables = [cx_Freeze.Executable("numbertrack.py", base=base)] )