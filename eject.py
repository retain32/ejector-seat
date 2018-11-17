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


    disks = []
    # print(df_output)
    for line in df_output.split('\n'):
        if line.startswith("/dev/"):
            dev_path = re.search("\/dev\/disk[0-999]", line.split()[0]).group(0)
            volume_path = re.search("/Volumes/.*$", line)
            if dev_path.startswith(tuple(diskutil_list)):
                # print(volume_path.group(0))
                disks.append(disk_item(dev_path, volume_path.group(0)))
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

    menu = QMenu()
    for disk in disks:
        disk.triggered.connect(disk.eject)
        menu.addAction(disk)

    # Add the menu to the tray
    tray.setContextMenu(menu)

    app.exec_()


class disk_item(QAction):

    def __init__(self, dev_path, volume_path):
        self.dev_path = dev_path # /dev/disk0
        self.volume_path = volume_path # /Volumes/Example Disk
        self.name = self.volume_path.replace("/Volumes/", "") # Example Disk
        super(disk_item, self).__init__(self.name)

    def eject(self):
        call(["diskutil", "eject", self.dev_path])


def eject_drive(dev_path):
    #call(["diskutil", "eject", dev_path])
    print(dev_path + " ejected.")


if __name__ == "__main__":
    main()
