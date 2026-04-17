import fileinput
import platform
import subprocess
import time

import cowsay
from termcolor import colored


def welcome_setup():
    print("")
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

        print(colored(left.ljust(max_logo_width + 4), "blue") + right)
    print("")


def setup_locale():
    print("Setup locales...", end="", flush=True)
    time.sleep(1)
    locale_path = "/usr/share/zoneinfo/Europe/Moscow"
    localetime_path = "/etc/localtime"
    subprocess.run(["ln", "-sf", locale_path, localetime_path])
    print("\rSetup locales... Done")

    print("Setup hwclock...", end="", flush=True)
    subprocess.run(["hwclock", "--systohc"])
    time.sleep(1)
    print("\rSetup hwclock... Done")
    print("Setup locale done[+]")
    print("\n")


def uncomment_line(comment, file_modified):
    with fileinput.FileInput(file_modified, inplace=True) as file:
        for line in file:
            if line.lstrip().startswith(f"#{comment}"):
                print(line.lstrip("#"), end="")
            else:
                print(line, end="")


def setup_locale_gen():
    print("Setup /etc/locale.gen ru_RU.UTF-8 and en_US.UTF-8...")
    path_locale_gen = "/etc/locale.gen"
    uncomment_line("ru_RU.UTF-8 UTF-8", path_locale_gen)
    uncomment_line("en_US.UTF-8 UTF-8", path_locale_gen)
    subprocess.run("locale-gen")
    print("Setup locale.gen done[+]")
    print("\n")


def create_config_file(path_file):
    subprocess.run(["touch", path_file])
    return open(path_file, "a")


def setup_lang_keymap_host():
    # locale.conf
    print("Setup lang > /etc/locale.conf...", end="", flush=True)
    time.sleep(1)
    path_locale_conf = "/etc/locale.conf"
    lang_file = create_config_file(path_locale_conf)
    subprocess.run(["echo", "LANG=en_US.UTF-8"], stdout=lang_file)
    print("\rSetup lang > /etc/locale.conf... Done")

    # vconsole.conf
    print("Setup keymap > /etc/vconsole.conf...", end="", flush=True)
    time.sleep(1)
    path_vconsole_conf = "/etc/vconsole.conf"
    vconsole_file = create_config_file(path_vconsole_conf)
    subprocess.run(["echo", "KEYMAP=ru"], stdout=vconsole_file)
    print("Setup keymap > /etc/vconsole.conf... Done")

    # host
    print("Setup arch > /etc/hostname...", end="", flush=True)
    time.sleep(1)
    path_host_conf = "/etc/hostname"
    host_file = create_config_file(path_host_conf)
    subprocess.run(["echo", "arch"], stdout=host_file)


welcome_setup()
user_input = str(input("Starting to configure Arch Linux. Ready to continue?[y/n]:"))

if user_input.lower() == "y":
    setup_locale()
    setup_locale_gen()
else:
    print("</>The setup was terminated</>")
    setup_lang_keymap_host()
    cowsay.cow("Bye.")


print("test")
