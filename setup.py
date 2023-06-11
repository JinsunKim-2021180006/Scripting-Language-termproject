from distutils.core import setup,Extension

setup(
    name='star',
    version='1.0',
    py_modules=['fileio','gps', 'main', 'map','noti','opensite','PastSearch','search','teller','weather'],
    ext_modules=[Extension('Cmodule', sources=['Cmodule.c'])]
)
