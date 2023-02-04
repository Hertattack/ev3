import platform

if platform.uname().system == 'Linux':
    from .ev3 import scanning


    def GetScanner():
        return ev3.scanning.Scanner()
else:
    from .windows import scanning


    def GetScanner():
        return windows.scanning.Scanner()
