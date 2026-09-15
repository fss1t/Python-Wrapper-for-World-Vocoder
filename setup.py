from __future__ import absolute_import, print_function, with_statement

import sys
from glob import glob
from os.path import join

import numpy
from setuptools import Extension, find_packages, setup
from setuptools.command.build_ext import build_ext


_VERSION = '0.3.6'


world_src_top = join("lib", "World", "src")
world_sources = glob(join(world_src_top, "*.cpp"))

ext_modules = [
    Extension(
        name="pyworld.pyworld",
        include_dirs=[world_src_top, numpy.get_include()],
        sources=[join("pyworld", "pyworld.pyx")] + world_sources,
        language="c++")]


# WORLD's sources use C++20 features (e.g. std::bit_cast in harvest.cpp), but the
# compilers do not all default to a new enough standard. The flag spelling depends on
# the compiler, which is only known once build_ext has probed the toolchain.
_CXX_STD_FLAGS = {
    "msvc": ["/std:c++20"],
}
_CXX_STD_FLAGS_DEFAULT = ["-std=c++20"]


class build_ext_cxx20(build_ext):
    def build_extensions(self):
        flags = _CXX_STD_FLAGS.get(
            self.compiler.compiler_type, _CXX_STD_FLAGS_DEFAULT)
        for ext in self.extensions:
            ext.extra_compile_args = list(ext.extra_compile_args or []) + flags
        build_ext.build_extensions(self)

kwargs = {"encoding": "utf-8"} if int(sys.version[0]) > 2 else {}
setup(
    name="pyworld",
    description="PyWorld: a Python wrapper for WORLD vocoder",
    long_description=open("README.md", "r", **kwargs).read(),
    long_description_content_type="text/markdown",
    ext_modules=ext_modules,
    cmdclass={'build_ext': build_ext_cxx20},
    version=_VERSION,
    packages=find_packages(),
    package_data={"pyworld": ["py.typed", "*.pyi"]},
    install_requires=[
        'numpy',
        'importlib-metadata; python_version<"3.8"',
    ],
    extras_require={
        'test': ['nose'],
        'sdist': ['numpy', 'cython>=0.24'],
    },
    author="Pyworld Contributors",
    author_email="jeremycchsu@gmail.com",
    url="https://github.com/JeremyCCHsu/Python-Wrapper-for-World-Vocoder",
    keywords=['vocoder'],
    classifiers=[],
)
