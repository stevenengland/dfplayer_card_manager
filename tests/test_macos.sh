#!/bin/bash
set -e

MOUNT_POINT="/Volumes/dfplayer_card_manager_usbstick"

DEVICE=$(mount | grep "$MOUNT_POINT" | awk '{print $1}')

DEVICE=$(echo "$DEVICE" | xargs)

if [ -z "$DEVICE" ]; then
    echo "No device found for mount point $MOUNT_POINT"
    exit 1
fi

echo "Device $DEVICE is linked to mount point $MOUNT_POINT"

set +e
echo "Running with device path"
echo "####### Check ####### "
dfplayer-card-manager -vvv check "$DEVICE"
#echo "####### Clean ####### "
#dfplayer-card-manager -vvv clean "$DEVICE"
#echo "####### Sort ####### "
#dfplayer-card-manager -vvv sort "$DEVICE"
#echo "####### Sync ####### "
#dfplayer-card-manager -vvv sync "$DEVICE" ./tests/test_assets/repositories/source

#set -e
#echo "Cleaning directory $MOUNT_POINT"
#sudo rm -rf "$MOUNT_POINT"/*

#set +e
#echo "Running with mount path"
#echo "####### Check ####### "
#dfplayer-card-manager -vvv check "$MOUNT_POINT"
#echo "####### Clean ####### "
#dfplayer-card-manager -vvv clean "$MOUNT_POINT"
#echo "####### Sort ####### "
#dfplayer-card-manager -vvv sort "$MOUNT_POINT"
#echo "####### Sync ####### "
#dfplayer-card-manager -vvv sync "$MOUNT_POINT" ./tests/test_assets/repositories/source

#set -e
#echo "Cleaning directory $MOUNT_POINT"
#sudo rm -rf "$MOUNT_POINT"/*

#set +e
#echo "####### Check ####### "
#sudo ./.venv/bin/dfplayer-card-manager -vvv check "$DEVICE"
#echo "####### Clean ####### "
#sudo ./.venv/bin/dfplayer-card-manager -vvv clean "$DEVICE"
#echo "####### Sort ####### "
#sudo ./.venv/bin/dfplayer-card-manager -vvv sort "$DEVICE"
#echo "####### Sync ####### "
#sudo ./.venv/bin/dfplayer-card-manager -vvv sync "$DEVICE" ./tests/test_assets/repositories/source

#set -e
#echo "Cleaning directory $MOUNT_POINT"
#sudo rm -rf "$MOUNT_POINT"/*