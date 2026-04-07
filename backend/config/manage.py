import os

os.environ["GEOS_LIBRARY_PATH"] = "/opt/homebrew/opt/geos/lib/libgeos_c.dylib"
os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = "/opt/homebrew/opt/geos/lib"
