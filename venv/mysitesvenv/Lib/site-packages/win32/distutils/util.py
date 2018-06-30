import os
import sys
import yaml
import shutil
import importlib
import tempfile
import pathlib
import functools
import platform

from toposort import toposort_flatten
from collections import deque
from contextlib import suppress
from copy import copy
from distutils.sysconfig import get_config_vars
from typing import List, Iterator, Tuple, Dict, Set
from packaging import markers

from .extension import WinExt
from ..compat import zipfile, MSVCCompiler, _find_exe, iglob


def find_directories(parent='.') -> Iterator[str]:
    """Recursively find directories that contain a module.yml

    No directories should be returned that have a parent
    containing module.yml
    """
    # FIXME: This implementation does not comply with the second point

    for fname in iglob(os.path.join(parent, '**/module.yml'), recursive=True):
        yield os.path.relpath(os.path.dirname(fname), parent)


def collect_extensions(parent='.') -> Iterator[WinExt]:
    """Collect all directories that contain a 'module.yml' recursively.

    The 'include' directory of each module is added by default to the include
    path, and 'include' directories from other extensions are added to the
    include path if they are listed in the 'modules'
    """

    # This is somewhat confusing, because the 'modules' key in the yaml
    # files specifies the dependencies for that module, the the 'modules'
    # variable contains the actual module configurations.
    modules = {}
    dependencies = {}
    build_order = ('.i', '.mc', '.rc', '.cpp')

    for dir in find_directories(parent):
        yml = os.path.join(parent, dir, 'module.yml')
        with open(yml) as fh:
            cfg = yaml.load(fh)

        if yml is None:
            raise ValueError('Invalid configuration file')

        name = dir.replace(os.sep, '.')
        modules[name] = cfg  # Module configuration
        dependencies[name] = set(cfg.setdefault('modules',
                                                []))  # Module dependencies

    external_modules = []
    for name in toposort_flatten(dependencies):
        src = os.path.join(parent, name.replace('.', os.sep), 'src')
        sources = []

        try:
            files = os.listdir(src)
        except FileNotFoundError:
            external_modules += [
                name
            ]  # Add this to external_modules for later generation
            continue

        for item in build_order:  # Add all sources present in the 'src' directory
            for fname in files:
                if fname.endswith(item):
                    sources.append(os.path.join(src, fname))

        include_dirs = []
        f = set()
        q = deque([name])
        i = 0

        # Simple dependency resolver algorithm:
        while q:
            i += 1
            assert i < 500  # To avoid infinite loop

            dep = q.popleft().replace('.', os.sep)  # Take one module
            include_dirs.extend([  # Add the include directories
                os.path.join(parent, dep, 'src'),
                os.path.join(parent, dep, 'include')
            ])
            f.add(dep.replace(os.sep,
                              '.'))  # Add the module's dependencies to the set
            q.extend([d for d in dependencies[name] if d not in f
                      ])  # Queue modules not already in the set for processing

        cfg = modules[name]
        del cfg['modules']  # Remove the 'modules' (depenencies) key

        # If the cfg has environment_markers, then parse it
        # NOTE: currently does not support removing dependencies
        if 'environment_markers' in cfg:
            marker = markers.Marker(cfg['environment_markers'])
            if not marker.evaluate():
                print('skipping: {} due to environment failure'.format(name))
                continue
            else:
                del cfg['environment_markers']

        if sys.version_info < (3, 5):
            cfg.setdefault('extra_link_args', []).append(get_link_arg())

        with suppress(KeyError):
            for i, depend in enumerate(cfg['depends']):
                cfg['depends'][i] = os.path.join(name, 'include', depend)

        for config_option in ['export_symbol_file', 'pch_header']:
            with suppress(KeyError):
                cfg[config_option] = os.path.join(
                    name.replace('.', os.sep), 'include', cfg[config_option])

        build_temp_library_dirs = set(
            [os.path.join(os.path.dirname(d), 'src') for d in include_dirs])

        cfg.setdefault('libraries', []).extend(
            set([
                get_implib_basename(os.path.dirname(d))
                for d in include_dirs[2:]
            ]))

        yield WinExt(
            name,
            sources=sources,
            include_dirs=copy(include_dirs),
            external_modules=copy(external_modules),
            build_temp_library_dirs=list(build_temp_library_dirs),
            **cfg)

        print('collected: {}'.format(name))


def create_compiler() -> MSVCCompiler:
    """Create and return a new MSVC compiler"""

    compiler = MSVCCompiler()
    compiler.initialize()

    if sys.version_info >= (3, 5):
        compiler.dumpbin = _find_exe("dumpbin.exe", compiler._paths)
    else:
        compiler.dumpbin = compiler.find_exe("dumpbin.exe")

    return compiler


def get_link_arg(plat_name='') -> str:
    """Get the /MACHINE specifier for MSVC"""
    if not plat_name and platform.architecture()[0] == '64bit':
        plat_name = 'amd64'

    if 'amd64' in plat_name:
        return '/MACHINE:X64'
    else:
        return '/MACHINE:X86'


def generate_libs(libs: List[str], plat_name: str) -> Iterator[str]:
    """Generate lib files to link against from python extensions."""
    tmpdir = tempfile.mkdtemp()
    compiler = create_compiler()

    for module in iter(importlib.import_module(lib) for lib in libs):
        pyd = module.__file__
        basename, ext = os.path.splitext(os.path.basename(pyd))

        assert ext == '.pyd'

        dll = os.path.join(tmpdir, '{}.dll'.format(basename))
        dname = os.path.join(tmpdir, '{}.def'.format(basename))
        lname = os.path.join(tmpdir, '{}.lib'.format(basename))

        shutil.copy(pyd, dll)

        with open(dname, 'w+') as definitions:
            definitions.write('EXPORTS\n')

            exports_dir = tempfile.mkdtemp()
            exports_file = os.path.join(exports_dir, 'exports.txt')
            dumpbin_args = ['/exports', dll, '/OUT:{}'.format(exports_file)]

            compiler.spawn([compiler.dumpbin] + dumpbin_args)

            with open(exports_file) as dump:
                while True:
                    if next(dump).strip().split() == [
                            'ordinal', 'hint', 'RVA', 'name'
                    ]:
                        break

                for line in dump:
                    if line.strip():
                        if line.strip() == 'Summary':
                            break
                        else:
                            definitions.write(
                                '{}\n'.format(line.strip().split()[-1]))

            shutil.rmtree(exports_dir)

        compiler.spawn([compiler.lib] + [
            '/def:{}'.format(dname), '/OUT:{}'.format(lname),
            get_link_arg(plat_name)
        ])

        yield lname


def archive_headers(zip_file: zipfile.ZipFile, parent='.') -> None:
    """Archive header files into the zip file"""
    for fname in iglob(os.path.join(parent, 'win32/**/*.h'), recursive=True):
        rel = os.path.join(
            *pathlib.Path(os.path.relpath(fname, parent)).parts[1:])
        with zip_file.open(rel, 'w') as fdst:
            with open(fname, 'rb') as fsrc:
                shutil.copyfileobj(fsrc, fdst)


def extract_headers(include_dir: str) -> None:
    """Extract all headers into the specified build_temp"""
    import win32.distutils

    for path in win32.distutils.__path__:
        for zname in iglob(os.path.join(path, 'headers', '*.zip')):
            with zipfile.ZipFile(zname) as z:
                z.extractall(include_dir)


@functools.lru_cache(maxsize=None)
def get_ext_suffix() -> str:
    """Get the extension suffix"""
    return get_config_vars()["EXT_SUFFIX"]


def get_implib_basename(name: str) -> str:
    """Get the basename of the implib generated for this extension"""
    # Use defensive programming
    root, path = os.path.splitext(os.path.basename(name + get_ext_suffix()))

    return root
