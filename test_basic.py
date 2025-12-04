import subprocess
import os
import sys

def test_basic_build():
    # Run the build script
    result = subprocess.run(
        [sys.executable, "build_lib.py", "--sources", "src", "--output", "mylib", "--type", "shared"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    assert result.returncode == 0, "Build script failed"

    # Check that build directory was created
    assert os.path.isdir("build"), "No build directory created"
