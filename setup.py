from distutils.core import setup, Extension

ldModule = Extension('ldModule', sources = ['ldModule.c'])

setup (name = 'Name',
       version = '0.99',
       description = 'ldModule in C',
       ext_modules = [ldModule])