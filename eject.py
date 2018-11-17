from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import re
from subprocess import call, check_output

"""
Author: Seth Phillips
Program: Ejector-Seat

Creates a persistent eject icon in the MacOS menu bar to eject disk images
and external drives (USB drives, SD cards, etc).
Uses PyQT5 to create the menu bar icon, diskutil and df to retrieve
disk info and diskutil to eject the disks. 

TODO: Add more verbose info when Option-Clicking the icon
OR
TODO: Remount when Option-Clicking items
Decisions decisions.... or...

TODO: Preferences panel where the user can CHOOSE!

TODO: remove python dock icon

TODO: A lot more, but hey it works right?

"""

class interface():

    def get_disk_list(self):
        """
        Uses diskutil to retreive the /dev/ and /Volume/ paths of all drives,
        filters them by external and images, creates a disk_item for each one
        and stores them in self.disks.
        """
        diskutil_pattern = re.compile("(\/dev\/disk[0-999]) \((disk image|external, physical)\)")
        diskutil_output = check_output(["diskutil", "list"]).decode('ascii')
        df_output = check_output(["df"]).decode('ascii')

        diskutil_list = []
        # pattern = ""
        for m in diskutil_pattern.finditer(diskutil_output):
            # print("%s: %s" % (m.group(1), m.group(2)))
            diskutil_list.append(m.group(1))

        self.disks = []
        # print(df_output)
        for line in df_output.split('\n'):
            if line.startswith("/dev/"):
                dev_path = re.search("\/dev\/disk[0-999]", line.split()[0]).group(0)
                volume_path = re.search("/Volumes/.*$", line)
                if dev_path.startswith(tuple(diskutil_list)):
                    # print(volume_path.group(0))
                    self.disks.append(disk_item(dev_path, volume_path.group(0)))
        # print(disks)

    def __init__(self):
        """
        Handles PyQt5's initial construction. We're not creating a window here,
        the important part is creating tray, a QSystemTrayIcon that sits in the menu bar.
        """
        app = QApplication([])
        app.setQuitOnLastWindowClosed(False)

        # Create the icon
        icon = QIcon("EjectMediaIcon.png")

        # Create the tray
        tray = QSystemTrayIcon()
        tray.setIcon(icon)
        tray.setVisible(True)
        tray.activated.connect(self.add_disk_item)

        # Create the menu

        self.menu = QMenu()

        # Add the menu to the tray
        tray.setContextMenu(self.menu)
        app.exec_()

    def add_disk_item(self):
        """
        Called whenever the menu bar icon (tray, an instance of QSystemTrayIcon), is pressed.
        Clears the menu, gets the current disks in the system, and iterates through
        each disk_item in disks, connecting its triggered action to its eject function,
        then adds it to the menu.
        """
        self.menu.clear()
        self.get_disk_list()
        for disk in self.disks:
            disk.triggered.connect(disk.eject)
            self.menu.addAction(disk)




class disk_item(QAction):
    """
    Object representing relevant(external or disk images) disks on the system,
    implemented as a QAction that is added as an item in the menu.
    Constructor sets 3 basic attributes that may be referenced in later
    improvements(like holding option to show more disk info) TODO: <That
    and an eject function that simply passes the disk's /dev/ path
    to the diskutil eject command to eject it.
    """
    def __init__(self, dev_path, volume_path):
        self.dev_path = dev_path # /dev/disk0
        self.volume_path = volume_path # /Volumes/Example Disk
        self.name = self.volume_path.replace("/Volumes/", "") # Example Disk
        super(disk_item, self).__init__(self.name)

    def eject(self):
        call(["diskutil", "eject", self.dev_path])
        print(self.dev_path + " ejected")

def main():
    interface()

if __name__ == "__main__":
    main()
