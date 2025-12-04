#!/usr/bin/env python3
"""
build_lib.py

General-purpose library compilation script for C/C++ sources.

Features:
- Builds shared or static libraries.
- Auto-detects platform and available compilers (gcc/clang or MSVC cl).
- Accepts include dirs, library dirs, link libraries, extra compile/link flags.
- Collects all .c/.cpp files under provided source directories or explicit list.
- Produces output in a build directory.

Usage examples:
  # build a shared lib from everything in src/
  python build_lib.py --sources src --output mylib --type shared

  # build a static lib from specific files with includes and libraries
  python build_lib.py --files src/a.c src/b.c --output mylib --type static \
      --include include --libdirs /usr/local/lib --libs m rt

  # verbose
  python build_lib.py --sources src --output mylib --type shared -v
"""

import argparse
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List

# ---------- Helpers ----------
def which(exe: str):
    return shutil.which(exe)

def find_sources(files_or_dirs: List[str]):
    p = []
    exts = (".c", ".cpp", ".cxx", ".cc", ".c++")
    for s in files_or_dirs:
        s_path = Path(s)
        if s_path.is_dir():
            for f in s_path.rglob("*"):
                if f.suffix.lower() in exts:
                    p.append(str(f))
        elif s_path.is_file():
            p.append(str(s_path))
        else:
            # allow glob-like patterns
            import glob
            for match in glob.glob(s):
                m = Path(match)
                if m.is_file() and m.suffix.lower() in exts:
                    p.append(str(m))
    # dedupe and sort
    return sorted(dict.fromkeys(p))

def run(cmd, verbose=False, check=True):
    if verbose:
        print("+ " + " ".join(cmd))
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if verbose:
        if proc.stdout:
            print(proc.stdout)
        if proc.stderr:
            print(proc.stderr, file=sys.stderr)
    if check and proc.returncode != 0:
        raise subprocess.CalledProcessError(proc.returncode, cmd, output=proc.stdout, stderr=proc.stderr)
    return proc

# ---------- Compiler selection ----------
class Compiler:
    name: str
    c_compiler: str
    cxx_compiler: str
    is_msvc: bool

    def __init__(self, name, c_compiler, cxx_compiler, is_msvc=False):
        self.name = name
        self.c_compiler = c_compiler
        self.cxx_compiler = cxx_compiler
        self.is_msvc = is_msvc

def detect_compiler(prefer=None) -> Compiler:
    system = platform.system()
    # If user prefers a specific compiler, try to use it
    if prefer:
        if which(prefer):
            # Assume it's both C and C++ compilers with same base (e.g. gcc/g++)
            base = prefer
            cxx = prefer.replace("gcc", "g++") if "gcc" in prefer else prefer
            return Compiler(prefer, prefer, cxx, is_msvc=False)
    # Windows: prefer MSVC 'cl' if available; otherwise try gcc (mingw) or clang
    if system == "Windows":
        if which("cl"):
            return Compiler("msvc", "cl", "cl", is_msvc=True)
        for exe in ("gcc", "clang", "g++", "clang++"):
            if which(exe):
                # map to both c and cxx
                c = "gcc" if exe in ("gcc",) else exe
                cxx = "g++" if exe in ("g++",) else exe
                return Compiler(exe, c, cxx, is_msvc=False)
    else:
        # POSIX: prefer clang then gcc if available
        for c in ("clang", "gcc"):
            if which(c):
                cxx = "clang++" if c == "clang" else "g++"
                if which(cxx) is None:
                    cxx = c  # fallback (rare)
                return Compiler(c, c, cxx, is_msvc=False)
        # fallback to any compiler in PATH
        for exe in ("cc", "c99"):
            if which(exe):
                return Compiler(exe, exe, exe, is_msvc=False)
    # If nothing found, error out
    raise EnvironmentError("No suitable C/C++ compiler found in PATH. Install gcc/clang or MSVC toolset.")

# ---------- Build logic ----------
def build(args):
    # Prepare file lists
    if args.files:
        sources = find_sources(args.files)
    elif args.sources:
        sources = find_sources(args.sources)
    else:
        # default: src/
        sources = find_sources(["src"])
    if not sources:
        raise SystemExit("No source files found. Provide --files or --sources that contain .c/.cpp files.")

    outdir = Path(args.build_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    system = platform.system().lower()

    compiler = detect_compiler(prefer=args.compiler)
    verbose = args.verbose

    # File lists by language (approx)
    c_files = [f for f in sources if Path(f).suffix.lower() == ".c"]
    cpp_files = [f for f in sources if Path(f).suffix.lower() in (".cpp", ".cxx", ".cc", ".c++")]

    # Decide output filename
    base_name = args.output
    if args.type == "shared":
        if system == "windows":
            # .dll (and an import lib .lib for MSVC)
            out_name = f"{base_name}.dll"
        elif system == "darwin":
            out_name = f"lib{base_name}.dylib"
        else:
            out_name = f"lib{base_name}.so"
    else:  # static
        if system == "windows":
            out_name = f"{base_name}.lib"
        else:
            out_name = f"lib{base_name}.a"

    out_path = outdir / out_name

    # Platform-specific flags
    include_flags = []
    for inc in args.include or []:
        include_flags += ["-I", inc] if not compiler.is_msvc else [f"/I{inc}"]

    libdir_flags = []
    for ld in args.libdirs or []:
        libdir_flags += ["-L", ld] if not compiler.is_msvc else [f"/LIBPATH:{ld}"]

    link_libs = []
    for lib in args.libs or []:
        if compiler.is_msvc:
            # MSVC: libraries passed directly as names (libname.lib or libname)
            link_libs.append(lib if lib.lower().endswith(".lib") else f"{lib}.lib")
        else:
            link_libs += ["-l" + lib]

    extra_cflags = args.cflags or []
    extra_ldflags = args.ldflags or []

    # If building static archive on POSIX, use ar
    if args.type == "static" and system != "windows":
        # compile object files then run ar
        obj_dir = outdir / "obj"
        obj_dir.mkdir(parents=True, exist_ok=True)
        objects = []
        compile_cmds = []
        # Compile each source to object
        for src in sources:
            src_path = Path(src)
            obj_path = obj_dir / (src_path.stem + ".o")
            objects.append(str(obj_path))
            if src_path.suffix.lower() == ".c":
                cc = compiler.c_compiler
            else:
                cc = compiler.cxx_compiler
            cmd = [cc, "-c", str(src_path), "-o", str(obj_path)]
            if not compiler.is_msvc:
                cmd += ["-fPIC"] if args.fpic else []
                cmd += include_flags
                cmd += extra_cflags
            else:
                cmd += include_flags
                cmd += extra_cflags
                # MSVC uses /Fo for object output, but our -o approach may not work with cl; handle cl separately
                if compiler.is_msvc:
                    # cl /c src.c /Foobj\src.obj
                    cmd = ["cl", "/nologo", "/c", str(src_path), f"/Fo{obj_path}"] + include_flags + extra_cflags
            compile_cmds.append(cmd)
        # Execute compile commands
        for cmd in compile_cmds:
            run(cmd, verbose=verbose)
        # Create archive with ar
        ar = which("ar") or "ar"
        ar_cmd = [ar, "rcs", str(out_path)] + objects
        run(ar_cmd, verbose=verbose)
        print(f"Built static library: {out_path}")
        return

    # Shared/Static link command (single-step for gcc/clang; MSVC uses different flags)
    if compiler.is_msvc:
        # MSVC (cl + link)
        # Build objects
        obj_dir = outdir / "obj"
        obj_dir.mkdir(parents=True, exist_ok=True)
        objects = []
        for src in sources:
            src_path = Path(src)
            obj_path = obj_dir / (src_path.stem + ".obj")
            objects.append(str(obj_path))
            # cl /c file.c /Foobj\file.obj [includes]
            cmd = ["cl", "/nologo", "/c", str(src_path), f"/Fo{obj_path}"] + include_flags + extra_cflags
            run(cmd, verbose=verbose)
        # Link step
        linker = "link"
        link_cmd = [linker, "/NOLOGO"]
        # output
        link_cmd += [f"/OUT:{out_path}"]
        if args.type == "shared":
            link_cmd += ["/DLL"]
        # object files
        link_cmd += objects
        # library dirs and libs
        for ld in args.libdirs or []:
            link_cmd += [f"/LIBPATH:{ld}"]
        for lib in args.libs or []:
            link_cmd += [lib if lib.lower().endswith(".lib") else f"{lib}.lib"]
        link_cmd += extra_ldflags
        run(link_cmd, verbose=verbose)
        print(f"Built (MSVC) {args.type} library: {out_path}")
        return
    else:
        # gcc/clang style
        # Determine whether to use c or c++ linker: if any cpp files present, use cxx compiler
        linker = compiler.cxx_compiler if cpp_files else compiler.c_compiler
        cmd = [linker]
        if args.type == "shared":
            cmd += ["-shared"]
            if args.fpic and platform.system().lower() != "darwin":
                # if fpic was requested, ensure compiled with -fPIC; when compiling single-step this flag matters for objects,
                # but adding to compiler invocation is OK for simple cases.
                pass
        # Position independent code flag for shared libs on some platforms
        if args.type == "shared" and platform.system().lower() != "darwin":
            # many systems need -fPIC on object files; adding to compile flags below already handled or user-provided
            pass
        cmd += ["-o", str(out_path)]
        # Inputs: sources
        cmd += sources
        # include dirs are usually used at compile time; when linking we don't need them — keep in case of single-step compile+link
        cmd += include_flags
        # libdirs and libs
        cmd += libdir_flags
        cmd += link_libs
        cmd += extra_cflags + extra_ldflags
        # Run
        run(cmd, verbose=verbose)
        print(f"Built {args.type} library: {out_path}")
        return

# ---------- CLI ----------
def parse_args():
    ap = argparse.ArgumentParser(description="Build a shared/static library from C/C++ sources.")
    group = ap.add_mutually_exclusive_group()
    group.add_argument("--files", nargs="+", help="Explicit source files or globs.")
    group.add_argument("--sources", nargs="+", help="Source directories to search recursively for .c/.cpp files.")
    ap.add_argument("--output", "-o", required=True, help="Base name for output library (no prefix/suffix).")
    ap.add_argument("--type", choices=("shared", "static"), default="shared", help="Library type to build.")
    ap.add_argument("--build-dir", default="build", help="Directory to place build artifacts.")
    ap.add_argument("--include", "-I", nargs="*", help="Include directories.")
    ap.add_argument("--libdirs", "-L", nargs="*", help="Library search directories.")
    ap.add_argument("--libs", nargs="*", help="Libraries to link (names, without lib prefix on POSIX).")
    ap.add_argument("--cflags", nargs="*", help="Extra flags passed to the compiler (compile stage).")
    ap.add_argument("--ldflags", nargs="*", help="Extra flags passed to the linker.")
    ap.add_argument("--compiler", help="Preferred compiler executable name (gcc/clang/cl).")
    ap.add_argument("--fpic", action="store_true", help="Compile position-independent code where applicable.")
    ap.add_argument("-v", "--verbose", action="store_true", help="Print commands and output.")
    return ap.parse_args()

if __name__ == "__main__":
    args = parse_args()
    try:
        build(args)
    except subprocess.CalledProcessError as e:
        print("Build failed.", file=sys.stderr)
        if e.stdout:
            print(e.stdout)
        if e.stderr:
            print(e.stderr, file=sys.stderr)
        sys.exit(e.returncode if isinstance(e.returncode, int) else 1)
    except Exception as e:
        print("Error:", e, file=sys.stderr)
        sys.exit(1)
