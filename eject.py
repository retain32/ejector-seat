from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import re
from subprocess import call, check_output

"""
Saved regexs
(\/dev\/disk[0-999]) \((disk image|external, physical)\)




"""


def main():
    diskutil_pattern = re.compile("(\/dev\/disk[0-999]) \((disk image|external, physical)\)")
    diskutil_output = check_output(["diskutil", "list"]).decode('ascii')
    df_output = check_output(["df"]).decode('ascii')

    diskutil_list = []
    # pattern = ""
    for m in diskutil_pattern.finditer(diskutil_output):
        # print("%s: %s" % (m.group(1), m.group(2)))
        diskutil_list.append(m.group(1))

    disks = {}
    # print(df_output)
    for line in df_output.split('\n'):
        if line.startswith("/dev/"):
            pattern = re.compile("\/dev\/disk[0-999]")
            dev_path = re.search(pattern, line.split()[0]).group(0)
            volume_path = line.split()[8]
            if dev_path.startswith(tuple(diskutil_list)):

                disks[dev_path] = volume_path.split("/")[2]
    # print(disks)

    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)

    # Create the icon
    icon = QIcon("EjectMediaIcon.png")

    # Create the tray
    tray = QSystemTrayIcon()
    tray.setIcon(icon)
    tray.setVisible(True)

    # Create the menu

    # drive.insert(i, QAction(m.group(1)))
    # menu.addAction(drive[i])

    menu = QMenu()
    items = {}
    for disk in disks:
        items[disk] = (QAction(disks[disk]))
        items[disk].triggered.connect(lambda: eject_drive(disk))
        menu.addAction(items[disk])
        #TODO:Fix the triggered.connect call, it calls the last value of disk, not the one it was called from

    # Add the menu to the tray
    tray.setContextMenu(menu)

    app.exec_()


def eject_drive(dev_path):
    call(["diskutil", "eject", dev_path])
    print(dev_path + " ejected.")


if __name__ == "__main__":
    main()
