#!/bin/bash
set -e

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit 1
fi

IMG_FILE="usbstick.img"
MOUNT_POINT="/Volumes/dfplayer_card_manager_usbstick"

echo "Checking if $MOUNT_POINT is already mounted"
if mount | grep -q " on $MOUNT_POINT "; then
    echo "$MOUNT_POINT is already mounted. Stopping."
    exit 0
fi

if [ ! -d "$MOUNT_POINT" ]; then
    echo "Creating $MOUNT_POINT"
    mkdir -p "$MOUNT_POINT"
fi

echo "Creating FAT32 image file"
if [ ! -f "$IMG_FILE" ]; then
    dd if=/dev/zero of="$IMG_FILE" bs=4M count=10
fi

echo "Attaching image file as a loop device..."
DEVICE=$(hdiutil attach -imagekey diskimage-class=CRawDiskImage -nomount "$IMG_FILE")


# Remove leading/trailing whitespace from device path
DEVICE=$(echo "$DEVICE" | xargs)
echo "Device $DEVICE has been attached"

echo "Formatting device $DEVICE with FAT32..."
newfs_msdos -F 32 "$DEVICE"

echo "Mounting device $DEVICE to $MOUNT_POINT..."
mount -t msdos "$DEVICE" "$MOUNT_POINT"

echo "Image file $IMG_FILE has been formatted and mounted to $MOUNT_POINT"

