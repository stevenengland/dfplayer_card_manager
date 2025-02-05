@echo off
setlocal EnableDelayedExpansion

set "REPO_DIR=.\tests\test_assets\repositories\source"

for /f "tokens=1,2,*" %%a in ('wmic logicaldisk get caption^,volumename^| find "DFPLAYER"') do (
  set "TARGET_DIR=%%a"
)

if not defined TARGET_DIR (
  echo Error: No drive with label 'DFPLAYER' found
  exit /b 1
)

echo Found device path: %TARGET_DIR%

echo Running with device path
echo ####### Check #######
dfplayer-card-manager -vvv check "%TARGET_DIR%"
echo "####### Clean ####### "
dfplayer-card-manager -vvv clean "%TARGET_DIR%"
echo "####### Sort ####### "
dfplayer-card-manager -vvv sort "%TARGET_DIR%"
echo "####### Sync ####### "
dfplayer-card-manager -vvv sync "%TARGET_DIR%" .\tests\test_assets\repositories\source
