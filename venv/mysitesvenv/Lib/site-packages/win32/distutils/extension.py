import string

from setuptools import Extension
from typing import List


class WinExt(Extension):
    # Base class for all win32 extensions, with some predefined
    # library and include dirs, and predefined windows libraries.
    # Additionally a method to parse .def files into lists of exported
    # symbols, and to read

    def __init__(
            self,
            name: str,
            sources: List[str],
            include_dirs: List[str]=[],
            define_macros: List[tuple]=None,
            undef_macros: List[str]=None,
            library_dirs: List[str]=[],
            libraries: List[str]=[],
            runtime_library_dirs: List[str]=None,
            extra_objects: List[str]=None,
            extra_compile_args: List[str]=None,
            extra_link_args: List[str]=None,
            export_symbols: List[str]=None,
            export_symbol_file: str=None,
            pch_header: str=None,
            windows_h_version: int=None,  # min version of windows.h needed.
            extra_swig_commands: List[str]=None,
            is_regular_dll: bool=False,  # regular Windows DLL?
            # list of headers which may not be installed forcing us to
            # skip this extension
            optional_headers: List[str]=[],
            depends: List[str]=None,
            platforms: List[str]=None,  # none means 'all platforms'
            unicode_mode: bool=None,
            # 'none'==default or specifically true/false.
            implib_name: str=None,
            delay_load_libraries: List[str]=[],
            external_modules: List[str]=[],  # Libs that needed for building
            build_temp_library_dirs: List[str]=[]):

        self.delay_load_libraries = delay_load_libraries
        libraries.extend(self.delay_load_libraries)

        if export_symbol_file:
            export_symbols = export_symbols or []
            export_symbols.extend(self.parse_def_file(export_symbol_file))

        # Some of our swigged files behave differently in distutils vs
        # MSVC based builds.  Always define DISTUTILS_BUILD so they can tell.
        define_macros = define_macros or []
        define_macros.append(('DISTUTILS_BUILD', None))
        define_macros.append(('_CRT_SECURE_NO_WARNINGS', None))

        self.pch_header = pch_header
        self.extra_swig_commands = extra_swig_commands or []
        self.windows_h_version = windows_h_version
        self.optional_headers = optional_headers
        self.is_regular_dll = is_regular_dll
        self.platforms = platforms
        self.implib_name = implib_name
        self.external_modules = external_modules
        self.build_temp_library_dirs = build_temp_library_dirs

        Extension.__init__(self, name, sources, include_dirs, define_macros,
                           undef_macros, library_dirs, libraries,
                           runtime_library_dirs, extra_objects,
                           extra_compile_args, extra_link_args, export_symbols)

        if not hasattr(self, 'swig_deps'):
            self.swig_deps = []
        self.extra_compile_args.extend(['/DUNICODE', '/D_UNICODE', '/DWINNT'])
        self.unicode_mode = unicode_mode

        if self.delay_load_libraries:
            self.libraries.append('delayimp')
            for delay_lib in self.delay_load_libraries:
                self.extra_link_args.append('/delayload:%s.dll' % delay_lib)

        if not hasattr(self, '_needs_stub'):
            self._needs_stub = False

    def parse_def_file(self, path: str) -> List[str]:
        # Extract symbols to export from a def-file
        result = []
        for line in open(path).readlines():
            line = line.rstrip()
            if line and line[0] in string.whitespace:
                tokens = line.split()
                if not tokens[0][0] in string.ascii_letters:
                    continue
                result.append(','.join(tokens))
        return result
