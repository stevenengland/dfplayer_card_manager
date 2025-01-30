@echo off
setlocal enabledelayedexpansion

REM Dismount-VHD -Path <path>\usbstick.vhdx if diskpart fails in the middle


net session >nul 2>&1
if %errorLevel% neq 0 (
    echo This script requires administrative privileges.
    echo Please run as administrator.
    exit /b 1
)

echo Checking used drives...
set "inUse="
for /f "tokens=2 delims==" %%D in ('wmic logicaldisk get deviceid /value') do (
    set "drive=%%D"
    if not "!drive!"=="" (
        echo Found drive: !drive!
        set "inUse=!inUse!!drive! "
    )
)
echo Currently in use drives: !inUse!

for %%L in (Z Y X W V U T S R Q P O N M L K J I H G F E D) do (
    echo "!inUse!" | findstr /i "%%L:" >nul && (
        echo Drive %%L: is in use
    ) || (
        echo Found free letter: %%L:
        set "MOUNT_LETTER=%%L:"
        goto :found_letter
    )
)
:found_letter
echo Selected drive letter: %MOUNT_LETTER%

:: Set variables
set "VDISK_FILE=%TEMP%\usbstick.vhdx"
set "VDISK_SIZE_MB=40"

:: Calculate size in bytes (10MB = 10 * 1024 * 1024)
set /a "VDISK_SIZE_BYTES=%VDISK_SIZE_MB% * 1024 * 1024"

echo Creating virtual disk file...
if exist "%VDISK_FILE%" del "%VDISK_FILE%"
del "%VDISK_FILE%" 2>nul
if exist "%VDISK_FILE%" (
  echo Failed to delete existing virtual disk file.
  exit /b 1
)

:: Create diskpart script
set "DISKPART_SCRIPT=%TEMP%\mount_usbstick.txt"
(
  echo create vdisk file="%VDISK_FILE%" maximum=%VDISK_SIZE_MB%
  echo select vdisk file="%VDISK_FILE%"
  echo attach vdisk
  echo create partition primary
  echo format fs=fat32 quick label=DFPLAYER
  echo assign letter=%MOUNT_LETTER:~0,1%
) > "%DISKPART_SCRIPT%"

echo Formatting and mounting virtual disk...
diskpart /s "%DISKPART_SCRIPT%"
if %errorLevel% neq 0 (
    echo Failed to format and mount virtual disk.
    del "%DISKPART_SCRIPT%"
    exit /b 1
)

REM Workaround to make the disk visible to Powershell
echo Remounting disk to be visible to powershell...
powershell -NoProfile -Command "Dismount-VHD -Path %VDISK_FILE%"
powershell -NoProfile -Command "Mount-VHD -Path %VDISK_FILE% -PassThru"

:: Clean up
del "%DISKPART_SCRIPT%"

echo Virtual disk created and mounted successfully at %MOUNT_LETTER%
