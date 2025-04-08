""" ANSI color codes """
BLACK = "\033[0;30m"
RED = "\033[0;31m"
GREEN = "\033[0;32m"
BROWN = "\033[0;33m"
BLUE = "\033[0;34m"
PURPLE = "\033[0;35m"
CYAN = "\033[0;36m"
LIGHT_GRAY = "\033[0;37m"
DARK_GRAY = "\033[1;30m"
LIGHT_RED = "\033[1;31m"
LIGHT_GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
LIGHT_BLUE = "\033[1;34m"
LIGHT_PURPLE = "\033[1;35m"
LIGHT_CYAN = "\033[1;36m"
LIGHT_WHITE = "\033[1;37m"
BOLD = "\033[1m"
FAINT = "\033[2m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"
BLINK = "\033[5m"
NEGATIVE = "\033[7m"
CROSSED = "\033[9m"
END = "\033[0m"
# cancel SGR codes if we don't write to a terminal
if not __import__("sys").stdout.isatty():
    for _ in dir():
        if isinstance(_, str) and _[0] != "_":
            locals()[_] = ""
else:
    # set Windows console in VT mode
    if __import__("platform").system() == "Windows":
        kernel32 = __import__("ctypes").windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        del kernel32

import sys, os
import plistlib, json
from deobfuscated import keys


def usage(): print(BOLD + "Usage:" + END + LIGHT_BLUE + " python" + END + LIGHT_CYAN + " __main__.py" + END + LIGHT_GREEN + " <path_to_plist_file>" + END)

if len(sys.argv) != 2:
    usage()
    sys.exit(1)

path = sys.argv[1]

if not os.path.exists(path):
    print(RED + BOLD + "Error:" + END + RED + " File '" + path + "' does not exist." + END)
    usage()
    sys.exit(1)

def main():
    try:
        with open(path, 'rb') as f:
            plist = plistlib.load(f)
            deobfuscated = deobfuscate_keys(plist)
            print(deobfuscated)

            new_path = os.curdir + "/results/" + ".".join(path.split("/")[-1].split(".")[:-1]) + "_deobfuscated.json"
            encoded = {k: v.decode('latin1') if isinstance(v, bytes) else v for k, v in deobfuscated["CacheExtra"].items()}
            json.dump(encoded, open(new_path, 'w'), indent=4)
            print(GREEN + "Saved to " + END + BOLD + new_path + END)
    except Exception as e:
        print(RED + BOLD + "Error: " + END + RED + str(e) + END)
        usage()
        sys.exit(1)

def deobfuscate_keys(plist):
    deobfuscated = {}
    for key in keys:
        if key in plist["CacheExtra"]:
            deobfuscated[keys[key]] = plist["CacheExtra"][key]
    plist["CacheExtra"] = deobfuscated
    return plist

if __name__ == "__main__":
    main()
