import subprocess
import platform
import platform
import time
import cowsay
from termcolor import colored


def welcome_setup():
    print('')
    logo = [
        "      /\\",
        "     /  \\",
        "    /\\   \\",
        "   /      \\",
        "  /   ,,   \\",
        " /   |  |  -\\",
        "/_-''    ''-_\\",
    ]

    info = [
        "Arch Linux Setup Script",
        "Author: vvoxygen",
        "Version: 0.1",
        f"python version: {platform.python_version()}",
        "",
        "Initializing...",
    ]
    max_logo_width = max(len(line) for line in logo)

    for i in range(max(len(logo), len(info))):
        left = logo[i] if i < len(logo) else ""
        time.sleep(0.1)
        right = info[i] if i < len(info) else ""

        print(colored(left.ljust(max_logo_width + 4), 'blue') + right)
    print('')

def setup_locale():
    print('Setup locales...', end='', flush=True)
    time.sleep(1)
    locale_path = "/usr/share/zoneinfo/Europe/Moscow"
    localetime_path = "/etc/localtime"
    subprocess.run(['ln', '-sf', locale_path, localetime_path]) 
    print('\rSetup locales... Done')
    
    print('Setup hwclock...', end='', flush=True)
    subprocess.run(['hwclock','--systohc'])
    time.sleep(1)
    print('\rSetup hwclock... Done')
    print('Setup locale done[+]')
    print("\n")
    
    


welcome_setup()
user_input = str(input("Starting to configure Arch Linux. Ready to continue?[y/n]:"))

if user_input.lower() == "y":
    setup_locale()
else:
    print("</>The setup was terminated</>")
    cowsay.cow("Bye.")

print('test')
