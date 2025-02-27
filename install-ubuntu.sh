#!/usr/bin/bash

APP_NAME=fireflies-light-sync
APP_EXE=fireflies-light-sync
APP_LICENSE=LICENSE
APP_ICO=fireflies-light-sync.svg
APP_SHORTCUT=${APP_NAME}.desktop

EXE_PATH=$HOME/.local/bin
ICON_PATH=$HOME/.local/share/icons
SHORTCUT_PATH=$HOME/.local/share/applications

DST_EXE_PATH=${EXE_PATH}
DST_EXE_FILE=${DST_EXE_PATH}/${APP_EXE}
DST_ICON_FILE=${ICON_PATH}/${APP_ICO}
DST_SHORTCUT_FILE=${SHORTCUT_PATH}/${APP_SHORTCUT}


echo "Installing fireflies-light-sync..."

# Create directories
mkdir -p ${EXE_PATH}
mkdir -p ${ICON_PATH}
mkdir -p ${SHORTCUT_PATH}

# Copy files
cp ${APP_EXE} ${DST_EXE_PATH}
cp ${APP_ICO} ${DST_ICON_FILE}
cp ${APP_SHORTCUT} ${DST_SHORTCUT_FILE}

# Make executable
chmod +x ${DST_EXE_FILE}
chmod +x ${DST_SHORTCUT_FILE}

# Replace Icon= and Exec= with absolute path in .desktop shortcut
sed -i "s_Icon=_Icon=${DST_ICON_FILE}_g" ${DST_SHORTCUT_FILE}
sed -i "s_Exec=_Exec=${DST_EXE_FILE} %f_g" ${DST_SHORTCUT_FILE}

echo "Application installed in: ${EXE_PATH}"
echo "Installation completed"