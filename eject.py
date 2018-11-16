from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import re
from subprocess import call, check_output

"""
Saved regexs
(\/dev\/disk[0-999]) \((disk image|external, physical)\)




"""


def main():
    pattern = re.compile("(\/dev\/disk[0-999]) \((disk image|external, physical)\)")
    #diskutil_output = open("mock_diskutil_output.txt", "r").read()
    diskutil_output = check_output(["diskutil", "list"]).decode('ascii')

    # TODO: Add HR name to the disk

    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)

    # Create the icon
    icon = QIcon("EjectMediaIcon.png")

    # Create the tray
    tray = QSystemTrayIcon()
    tray.setIcon(icon)
    tray.setVisible(True)

    # Create the menu

    drive = []
    menu = QMenu()
    for i, m in enumerate(pattern.finditer(diskutil_output)):
        print("%s: %s" % (m.group(1), m.group(2)))
        drive.insert(i, QAction(m.group(1)))
        menu.addAction(drive[i])

    # Add the menu to the tray
    tray.setContextMenu(menu)

    app.exec_()


def eject_drive(dev_path):
    print(dev_path + "ejected.")


if __name__ == "__main__":
    main()
