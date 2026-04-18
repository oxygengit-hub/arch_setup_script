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
    print("\rSetup arch > /etc/hostname... Done")
    print("Setup locale, keymap, host done[+]")
    print("\n")


def create_user():
    username = "oxygen"
    password = "darok2007"

    print("Create user for system...", end="", flush=True)
    # useradd
    time.sleep(1)
    subprocess.run(["useradd", "-mG", "wheel", username])
    print("\rCreate user for system... Done")
    # passwor for user
    print(f"Appoint password for {username}...", end="", flush=True)
    subprocess.run(
        ["chpasswd"],
        input=f"{username}:{password}",
        text=True,
    )
    print(f"\rAppoint password for {username}... Done")
    # root password
    print("Appoint password for root...", end="", flush=True)
    subprocess.run(
        ["chpasswd"],
        input=f"{'root'}:{password}",
        text=True,
    )
    print("\rAppoint password for root... Done")
    print("Create user done[+], root get the password!")
    print("\n")


def setup_grub():
    print('mkdir /boot/efi...', flush=True, end='')
    time.sleep(1)
    subprocess.run(['mkdir', "/boot/efi"])
    print('\rmkdir /boot/efi...Done')

    output_lsblk = subprocess.run(['lsblk'], capture_output=True, text=True)
    dev_name = str(output_lsblk)[101:104]
    print(f"mount /dev/{dev_name} > /boot/efi...", flush=True, end='')
    time.sleep(1)
    subprocess.run(['mount', f'dev/{dev_name}1', '/boot/efi'])
    print(f'\rmount /dev{dev_name} > /boot/eif...Done')


    print('grub-install...', flush=True, end='')
    time.sleep(1)
    subprocess.run(['grub-install', '--target=x86_64-efi', '--efi-directory=/boot/efi', '--bootloader-id=GRUB'])
    print('\rgrub-install...Done')


    print("grub-mkconfig > /boot/grub/grub.cfg...", flush=True, end='')
    time.sleep(1)
    subprocess.run(["grub-mkconfig", '-o', '/boot/grub/grub.cfg'])
    print('\rgrub-mkconfig > /boot/grub/grub.cfg...Done')
    print('Setup grub done[+]')
    print('\n')



welcome_setup()
user_input = str(input("Starting to configure Arch Linux. Ready to continue?[y/n]:"))

if user_input.lower() == "y":
    setup_locale()
    setup_locale_gen()
    setup_lang_keymap_host()
    create_user()
    print('Raise NetworkManager...', flush=True, end='')
    subprocess.run(['systemctl', 'enable', 'NetworkManager'])
    time.sleep(1)
    print("Raise NetworkManger...Done[+]")
    setup_grub()
else:
    print("</>The setup was terminated</>")
    cowsay.cow("Bye.")


print("test")
