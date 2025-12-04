"""
project_config.py

Central configuration module for the library-build project.

This file allows you to:
- Define default source/include directories
- Set default C/C++ compiler flags
- Provide per-platform overrides
- Store common library dependencies
- Keep metadata in one place
"""

import platform
from pathlib import Path


# ---------------------------------------
# Project Metadata
# ---------------------------------------

PROJECT_NAME = "my_native_library"
VERSION = "1.0.0"
AUTHOR = "Your Name"
DESCRIPTION = "Native library build project using build_lib.py"


# ---------------------------------------
# Default Paths
# ---------------------------------------

ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "src"
INCLUDE_DIR = ROOT_DIR / "include"
BUILD_DIR = ROOT_DIR / "build"
OBJ_DIR = BUILD_DIR / "obj"


# ---------------------------------------
# Compiler and Build Defaults
# ---------------------------------------

DEFAULT_BUILD_TYPE = "shared"   # "shared" or "static"

DEFAULT_INCLUDE_DIRS = [
    str(INCLUDE_DIR)
]

DEFAULT_LIB_DIRS = []           # e.g. ["external/lib"]
DEFAULT_LIBS = []               # e.g. ["m", "pthread"]

DEFAULT_CFLAGS = [
    "-Wall",
    "-Wextra",
    "-O2",
]

DEFAULT_LDFLAGS = []


# ---------------------------------------
# Platform-Specific Overrides
# ---------------------------------------

SYSTEM = platform.system().lower()

if SYSTEM == "windows":
    DEFAULT_CFLAGS += []
    DEFAULT_LDFLAGS += []
elif SYSTEM == "darwin":  # macOS
    DEFAULT_LDFLAGS += ["-framework", "CoreFoundation"]
else:  # Linux or other Unix
    DEFAULT_LIBS += ["m"]  # math library automatically needed on Linux


# ---------------------------------------
# Exportable Configuration Dictionary
# ---------------------------------------

CONFIG = {
    "project_name": PROJECT_NAME,
    "version": VERSION,
    "author": AUTHOR,
    "description": DESCRIPTION,
    "source_dir": str(SRC_DIR),
    "include_dirs": DEFAULT_INCLUDE_DIRS,
    "lib_dirs": DEFAULT_LIB_DIRS,
    "libs": DEFAULT_LIBS,
    "cflags": DEFAULT_CFLAGS,
    "ldflags": DEFAULT_LDFLAGS,
    "build_dir": str(BUILD_DIR),
    "build_type": DEFAULT_BUILD_TYPE,
}
