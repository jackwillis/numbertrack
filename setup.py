import sys
import cx_Freeze

base = None
if sys.platform == "win32":
    base = "Win32GUI"

cx_Freeze.setup( name = "Numbertrack",
                 version = "0.0.1",
                 description = "Numbertrack",
                 executables = [cx_Freeze.Executable("numbertrack.py", base=base)] )
