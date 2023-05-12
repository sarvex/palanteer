# Palanteer scripting library
# Copyright (C) 2021, Damien Feneyrou <dfeneyrou@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import os
import sys
import glob
from setuptools import setup, find_packages, Extension

# Constants
isDevMode = False  # Enable to speed up development cycles. Shall be False for final installation
withStackTrace = False


# Deduce some parameters
np = os.path.normpath
r = "../"
src_list = (
    [
        f"{r}base/bsString.cpp",
        f"{r}base/bsOsLinux.cpp",
        f"{r}base/bsOsWindows.cpp",
    ]
    + glob.glob(f"{r}common/*.cpp")
) + glob.glob("palanteer_scripting/_cextension/*.cpp")
extra_link_args         = []
extra_compilation_flags = [
    "-DUSE_PL=1",
    "-DPL_EXPORT=1",
    "-DBS_NO_GRAPHIC",
    *["-I", np(f"{r}../c++"), "-I", np(f"{r}base"), "-I", np(f"{r}common")],
]
extra_compilation_flags.extend(
    [
        "-I",
        np(f"{r}external/zstd"),
        "-I",
        np(f"{r}external/zstd/common"),
        "-I",
        np(f"{r}external/zstd/compress"),
        "-I",
        np(f"{r}external/zstd/decompress"),
    ]
)
for folder in ["common", "compress", "decompress"]:
    src_list.extend(glob.glob(f"{r}external/zstd/{folder}/*.c"))

if isDevMode:
    # Developement mode (fast build & debug code)
    extra_compilation_flags.append("-DPL_NO_COMPRESSION=1")
    if sys.platform=="win32":
        extra_compilation_flags.append("/Zi")
        extra_link_args.append('/DEBUG')
    else:
        extra_compilation_flags.append("-O0")

if withStackTrace:
    extra_compilation_flags.append("-DPL_IMPL_STACKTRACE=1")
    if sys.platform=="linux":
        extra_link_args.extend(["-ldw", "-lunwind"])

if sys.platform=="win32":
	extra_compilation_flags.append("/DUNICODE")

# Normalize all source path (required for Windows)
src_list = [ np(s) for s in src_list ]

classifiers_list = [
    'Intended Audience :: Developers',
    "Intended Audience :: Science/Research",
    'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)'
    'Development Status :: 4 - Beta',
    "Programming Language :: Python :: 3",
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: Implementation :: CPython',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'Operating System :: POSIX :: Linux',
    'Topic :: Software Development',
    'Topic :: Software Development :: Testing'
]


# Build call
setup(name="palanteer_scripting",
      version="0.1.0",
      author="Damien Feneyrou",
      author_email="dfeneyrou@gmail.com",
      license="AGPLv3+",
      description="Palanteer scripting module",
      classifiers=classifiers_list,
      python_requires=">=3.7",
      #url="",
      packages=find_packages(),
      ext_modules=[
          Extension('palanteer_scripting._cextension',
                    sources           =src_list,
                    extra_compile_args=extra_compilation_flags,
                    extra_link_args   =extra_link_args),
      ],
      py_modules = ['palanteer_scripting._scripting'],
      zip_safe=False
      )
