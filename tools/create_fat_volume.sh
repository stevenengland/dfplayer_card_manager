#!/bin/bash
set -e

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit 1
fi

IMG_FILE="usbstick.img"
MOUNT_POINT="/mnt/dfplayer_card_manager_usbstick"

echo "Checking if $MOUNT_POINT is already mounted"
if mountpoint -q "$MOUNT_POINT"; then
    echo "$MOUNT_POINT is already mounted. Stopping."
    exit 0
fi

echo "Checking if required tools are installed"
if ! command -v modprobe &> /dev/null; then
    echo "modprobe is not available. Installing."
    apt-get update
    apt-get install -y kmod
fi
if ! command -v mkfs.vfat &> /dev/null; then
    echo "mkfs.vfat is not available. Installing."
    apt-get update
    apt-get install -y dosfstools
fi

echo "Checking if g_mass_storage module is available"
if ! modprobe -n -v g_mass_storage &> /dev/null; then
    echo "g_mass_storage module is not available. Installing."
    apt-get update
    apt-get install -y linux-modules-extra-$(uname -r)
fi

echo "Creating FAT32 image file"
if [ ! -f "$IMG_FILE" ]; then
    dd if=/dev/zero of="$IMG_FILE" bs=1M count=10
fi

mkfs.vfat -F 32 "$IMG_FILE"

echo "Mounting image file"
mkdir "$MOUNT_POINT"
mount -o loop "$IMG_FILE" "$MOUNT_POINT"
modprobe g_mass_storage file=$(pwd)/"$IMG_FILE" stall=0 removable=1

