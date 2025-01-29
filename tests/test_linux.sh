#!/bin/bash
set -e

MOUNT_POINT="/mnt/dfplayer_card_manager_usbstick"

DEVICE=$(findmnt -n -o SOURCE --target "$MOUNT_POINT")

if [ -z "$DEVICE" ]; then
    echo "No device found for mount point $MOUNT_POINT"
    exit 1
fi

echo "Device $DEVICE is linked to mount point $MOUNT_POINT"

echo "####### Check ####### "
dfplayer-card-manager -vvv check "$DEVICE"
echo "####### Clean ####### "
dfplayer-card-manager -vvv clean "$DEVICE"
echo "####### Sort ####### "
dfplayer-card-manager -vvv sort "$DEVICE"
echo "####### Sync ####### "
dfplayer-card-manager -vvv sync "$DEVICE" ./tests/test_assets/repositories/source

echo "Cleaning directory $MOUNT_POINT"
sudo rm -rf "$MOUNT_POINT"/*

echo "####### Check ####### "
sudo ./.venv/bin/dfplayer-card-manager -vvv check "$DEVICE"
echo "####### Clean ####### "
sudo ./.venv/bin/dfplayer-card-manager -vvv clean "$DEVICE"
echo "####### Sort ####### "
sudo ./.venv/bin/dfplayer-card-manager -vvv sort "$DEVICE"
echo "####### Sync ####### "
sudo ./.venv/bin/dfplayer-card-manager -vvv sync "$DEVICE" ./tests/test_assets/repositories/source

echo "Cleaning directory $MOUNT_POINT"
sudo rm -rf "$MOUNT_POINT"/*