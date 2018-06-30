import sys

if sys.version_info >= (3, 6):
    import zipfile
else:
    import zipfile36 as zipfile

if sys.version_info >= (3, 5):
    from glob import iglob
    from distutils._msvccompiler import MSVCCompiler, _find_exe
else:
    from glob2 import iglob as _iglob
    from distutils.msvccompiler import MSVCCompiler

    def iglob(path: str, recursive=True):
        return _iglob(path)

    def _find_exe(*args):
        raise NotImplementedError()
