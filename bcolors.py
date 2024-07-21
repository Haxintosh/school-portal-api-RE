# From Blender compilation script under GNU GPL
# https://svn.blender.org/svnroot/bf-blender/trunk/blender/build_files/scons/tools/bcolors.py
import datetime
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
class Logging:
    @staticmethod
    def warn(error, thread=""):
        if thread != "":
            thread = thread + "/"
        else:
            pass

        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S')}]" + f" [{bcolors.WARNING + thread}WARN{bcolors.ENDC}] {error}")

    @staticmethod
    def error(error, thread=""):
        if thread != "":
            thread = thread + "/"
        else:
            pass

        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S')}]" + f" [{bcolors.FAIL + thread}ERROR{bcolors.ENDC}] {error}")

    @staticmethod
    def info(error, thread=""):
        if thread != "":
            thread = thread + "/"
        else:
            pass

        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S')}]" + f" [{bcolors.OKBLUE + thread}INFO{bcolors.ENDC}] {error}")

    @staticmethod
    def ok(error, thread=""):
        if thread != "":
            thread = thread + "/"
        else:
            pass

        print(
            f"[{datetime.datetime.now().strftime('%H:%M:%S')}]" + f" [{bcolors.OKGREEN + thread}INFO{bcolors.ENDC}] {error}")
