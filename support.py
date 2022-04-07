from sys import platform as _sys_platform
from os import environ

if 'ANDROID_ARGUMENT' in environ:
    DEVICE = 'android'
elif _sys_platform in ('linux', 'linux2', 'linux3'):
    DEVICE = 'linux'
elif _sys_platform in ('win32', 'cygwin'):
    DEVICE = 'windows'

def Path( path):

    '''return suitable path for different platform/device'''

    if DEVICE == 'android':
        return '/data/data/org.test.cirgame/files/app/'+path
    elif DEVICE == 'linux':
        return './'+path
    elif DEVICE == 'windows':
        return path