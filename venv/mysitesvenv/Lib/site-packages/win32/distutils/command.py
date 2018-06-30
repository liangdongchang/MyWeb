import os
import shutil
import distutils.util
import pathlib

from distutils import log
from distutils.dep_util import newer_group
from contextlib import suppress
from setuptools.command.build_ext import build_ext
from typing import List, Set
from copy import copy

from .util import generate_libs, archive_headers, extract_headers
from .extension import WinExt
from ..compat import zipfile


# Special definitions for SWIG.
swig_interface_parents = {
    # source file base,     'base class' for generated COM support
    'mapi': None,  # not a class, but module
    'PyIMailUser': 'IMAPIContainer',
    'PyIABContainer': 'IMAPIContainer',
    'PyIAddrBook': 'IMAPIProp',
    'PyIAttach': 'IMAPIProp',
    'PyIDistList': 'IMAPIContainer',
    'PyIMailUser': 'IMAPIContainer',
    'PyIMAPIContainer': 'IMAPIProp',
    'PyIMAPIFolder': 'IMAPIContainer',
    'PyIMAPIProp': '',  # '' == default base
    'PyIMAPISession': '',
    'PyIMAPIStatus': 'IMAPIProp',
    'PyIMAPITable': '',
    'PyIMessage': 'IMAPIProp',
    'PyIMsgServiceAdmin': '',
    'PyIMsgStore': 'IMAPIProp',
    'PyIProfAdmin': '',
    'PyIProfSect': 'IMAPIProp',
    'PyIConverterSession': '',
    # exchange and exchdapi
    'exchange': None,
    'exchdapi': None,
    'PyIExchangeManageStore': '',
    # ADSI
    'adsi': None,  # module
    'PyIADsContainer': 'IDispatch',
    'PyIADsDeleteOps': 'IDispatch',
    'PyIADsUser': 'IADs',
    'PyIDirectoryObject': '',
    'PyIDirectorySearch': '',
    'PyIDsObjectPicker': '',
    'PyIADs': 'IDispatch',
}

# .i files that are #included, and hence are not part of the build.  Our .dsp
# parser isn't smart enough to differentiate these.
swig_include_files = [
    'mapilib',
    'adsilib',
]


class win32_build_ext(build_ext):
    def finalize_options(self) -> None:
        build_ext.finalize_options(self)

        self.swig_cpp = True  # hrm - deprecated - should use swig_opts=-c++??
        if not hasattr(self, 'plat_name'):
            # Old Python version that doesn't support cross-compile
            self.plat_name = distutils.util.get_platform()

        for ext in self.extensions:
            ext.library_dirs += [
                os.path.join(self.build_temp, d)
                for d in ext.build_temp_library_dirs
            ]

            for include_dir in copy(ext.include_dirs):
                rel = os.path.join(
                    *pathlib.Path(include_dir).parts[1:])
                ext.include_dirs += [
                    os.path.join(self.build_temp, 'include', rel)
                ]

        self.generated_files = []
        self.library_dirs += [self.build_temp]

    def archive_headers(self) -> None:
        header_zip = os.path.join(
            self.build_lib, 'win32', 'distutils', 'headers',
            '{}.zip'.format(self.distribution.get_name()))
        os.makedirs(os.path.dirname(header_zip), exist_ok=True)
        with zipfile.ZipFile(header_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
            archive_headers(zf)

    def extract_headers(self) -> None:
        include_dir = os.path.join(self.build_temp, 'include')
        with suppress(OSError):
            os.makedirs(include_dir)

        extract_headers(include_dir)

    def run(self) -> None:
        self.archive_headers()
        super().run()

    def build_extensions(self) -> None:
        # First, sanity-check the 'extensions' list
        self.check_extensions_list(self.extensions)

        libs = set()
        # Generate all external modules first
        for ext in self.extensions:
            libs.update(ext.external_modules)

        os.makedirs(self.build_temp, exist_ok=True)
        for lib in generate_libs(list(libs), self.plat_name):
            with suppress(FileNotFoundError):
                os.remove(os.path.join(self.build_temp, os.path.basename(lib)))

            try:
                shutil.move(lib, self.build_temp)
            except OSError:
                shutil.copy(lib, self.build_temp)

        self.extract_headers()
        if not hasattr(self.compiler, 'initialized'):
            # 2.3 and earlier initialized at construction
            self.compiler.initialized = True
        else:
            if not self.compiler.initialized:
                self.compiler.initialize()

        try:
            for ext in self.extensions:
                self.build_extension(ext)

        finally:
            for generated_file in self.generated_files:
                target = os.path.join(self.build_temp, generated_file)
                with suppress(OSError):
                    os.makedirs(os.path.dirname(target))
                with suppress(OSError):
                    shutil.move(generated_file, target)

            self.generated_files = []

    def find_swig(self) -> str:
        if 'SWIG' in os.environ:
            swig = os.environ['SWIG']
        else:
            # We know where our swig is
            swig = os.path.abspath(os.path.join('swig', 'swig.exe'))
        lib = os.path.join(os.path.dirname(swig), 'swig_lib')
        os.environ['SWIG_LIB'] = lib

        return swig

    def swig_sources(self, sources: List[str], extension: WinExt):
        new_sources = []
        swig_sources = []
        swig_targets = {}
        # XXX this drops generated C/C++ files into the source tree, which
        # is fine for developers who want to distribute the generated
        # source -- but there should be an option to put SWIG output in
        # the temp dir.
        # Adding py3k to the mix means we *really* need to move to generating
        # to the temp dir...
        target_ext = '.cpp'
        for source in sources:
            (base, sext) = os.path.splitext(source)
            if sext == '.i':  # SWIG interface file
                if os.path.split(base)[1] in swig_include_files:
                    continue
                swig_sources.append(source)
                # Patch up the filenames for various special cases...
                if os.path.basename(base) in swig_interface_parents:
                    swig_targets[source] = base + target_ext
                else:
                    new_target = '%s_swig%s' % (base, target_ext)
                    new_sources.append(new_target)
                    swig_targets[source] = new_target
            else:
                new_sources.append(source)

        if not swig_sources:
            return new_sources

        swig = self.find_swig()
        for source in swig_sources:
            swig_cmd = [swig, '-python', '-c++']
            swig_cmd.append(
                '-dnone', )  # we never use the .doc files.
            swig_cmd.extend(extension.extra_swig_commands)

            if distutils.util.get_platform() == 'win-amd64':
                swig_cmd.append('-DSWIG_PY64BIT')
            else:
                swig_cmd.append('-DSWIG_PY32BIT')
            target = swig_targets[source]
            with suppress(KeyError):
                interface_parent = swig_interface_parents[os.path.basename(
                    os.path.splitext(source)[0])]

                # Using win32 extensions to SWIG for generating COM classes.
                if interface_parent is not None:
                    # generating a class, not a module.
                    swig_cmd.append('-pythoncom')
                    if interface_parent:
                        # A class deriving from other than the default
                        swig_cmd.extend(
                            ['-com_interface_parent', interface_parent])

            # This 'newer' check helps python 2.2 builds, which otherwise
            # *always* regenerate the .cpp files, meaning every future
            # build for any platform sees these as dirty.
            # This could probably go once we generate .cpp into the temp dir.
            fqsource = os.path.abspath(source)
            fqtarget = os.path.abspath(target)
            rebuild = self.force or (extension and newer_group(
                extension.swig_deps + [fqsource], fqtarget))
            log.debug('should swig %s->%s=%s', source, target, rebuild)
            new_sources += [target]
            self.generated_files += [
                target, '{}.h'.format(os.path.splitext(target)[0])
            ]
            if rebuild:
                swig_cmd.extend(['-o', fqtarget, fqsource])
                log.info('swigging %s to %s', source, target)
                out_dir = os.path.dirname(source)
                cwd = os.getcwd()
                os.chdir(out_dir)
                try:
                    self.spawn(swig_cmd)
                finally:
                    os.chdir(cwd)
            else:
                log.info('skipping swig of %s', source)

        return list(set(new_sources))
