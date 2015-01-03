#/bin/sh

# Gphoto2 2.5.5 compiler and installer script v0.4.1
#
# This script is specifically created for Raspbian http://www.raspbian.org
# and Raspberry Pi http://www.raspberrypi.org but should work over any 
# Debian-based distribution

# Created and mantained by Gonzalo Cao Cabeza de Vaca
# Please send any feedback or comments to gonzalo.cao(at)gmail.com
# Updated for gPhoto2 2.5.1.1 by Peter Hinson
# Updated for gPhoto2 2.5.2 by Dmitri Popov
# Updated for gphoto2 2.5.5 by Mihai Doarna

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


if [ "$(whoami)" != "root" ]; then
	echo "Sorry, this script must be executed with sudo or as root"
	exit 1
fi

echo "Updating sources"

apt-get update

echo "Removing gphoto2 if exists"

apt-get remove -y gphoto2

echo "Installing dependencies"

apt-get install -y libltdl-dev libusb-dev libexif-dev libpopt-dev libudev-dev

echo "Creating temporary folder"

mkdir gphoto2-temp-folder
cd gphoto2-temp-folder

echo "gphoto2-temp-folder created"

echo "Downloading libusb 1.0.17"

if wget -q http://ftp.de.debian.org/debian/pool/main/libu/libusbx/libusbx_1.0.17.orig.tar.bz2
	then
		tar xjvf libusbx_1.0.17.orig.tar.bz2
		cd libusbx-1.0.17/
	else
		echo "Unable to get libusbx_1.0.17"
		echo "Cleaning and exiting..."
		exit 1
fi

echo "Compiling and installing libusb 1.0.17"

./configure
make
make install
cd ..

echo "Downloading libgphoto2 2.5.5.1"

if wget -q http://downloads.sourceforge.net/project/gphoto/libgphoto/2.5.5.1/libgphoto2-2.5.5.1.tar.bz2
	then
		tar xjf libgphoto2-2.5.5.1.tar.bz2
		cd libgphoto2-2.5.5.1
	else
		echo "Unable to get libgphoto2-2.5.5.1"
		echo "Cleaning and exiting..."
		exit 1
fi

echo "Compiling and installing libgphoto2 2.5.5.1"

./configure
make
make install
cd ..

echo "Downloading gphoto2 2.5.5"

if wget -q http://downloads.sourceforge.net/project/gphoto/gphoto/2.5.5/gphoto2-2.5.5.tar.gz
	then
		tar xzvf gphoto2-2.5.5.tar.gz
		cd gphoto2-2.5.5
	else
		echo "Unable to get gphoto2-2.5.5"
		echo "Cleaning and exiting..."
		exit 1
fi


echo "Compiling and installing gphoto2"

./configure
make
make install
cd ..

echo "Linking libraries"

ldconfig

echo "Generating udev rules, see http://www.gphoto.org/doc/manual/permissions-usb.html"

udev_version=$(udevd --version)

if   [ "$udev_version" -ge "201" ]
then
  udev_rules=201
elif [ "$udev_version" -ge "175" ]
then
  udev_rules=175
elif [ "$udev_version" -ge "136" ]
then
  udev_rules=136
else
  udev_rules=0.98
fi

/usr/local/lib/libgphoto2/print-camera-list udev-rules version $udev_rules group plugdev mode 0660 > /etc/udev/rules.d/90-libgphoto2.rules

if   [ "$udev_rules" = "201" ]
then
  echo "Generating hwdb file in /etc/udev/hwdb.d/20-gphoto.hwdb. Ignore the NOTE"
  /usr/local/lib/libgphoto2/print-camera-list hwdb > /etc/udev/hwdb.d/20-gphoto.hwdb
fi

echo "Removing temp files"

cd ..
rm -r gphoto2-temp-folder

echo "Removing some files to ensure the camera mounts properly"

rm /usr/share/dbus-1/services/org.gtk.Private.GPhoto2VolumeMonitor.service
rm /usr/share/gvfs/mounts/gphoto2.mount
rm /usr/share/gvfs/remote-volume-monitors/gphoto2.monitor
rm /usr/lib/gvfs/gvfs-gphoto2-volume-monitor

echo "Finished!! Enjoy it!"

gphoto2 --version

echo "Detect if any camera is plugged"

gphoto2 --auto-detect