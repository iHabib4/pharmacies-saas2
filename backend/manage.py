#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

# --- Add this first ---
os.environ["GEOS_LIBRARY_PATH"] = "/opt/homebrew/opt/geos/lib/libgeos_c.dylib"
os.environ["GDAL_LIBRARY_PATH"] = "/opt/homebrew/opt/gdal/lib/libgdal.dylib"
os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = (
    "/opt/homebrew/opt/geos/lib:/opt/homebrew/opt/gdal/lib"
)

# --- Then Django imports ---
from django.core.management import execute_from_command_line

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

if __name__ == "__main__":
    execute_from_command_line(sys.argv)
