#!/usr/bin/env bash

display=":$(ls /tmp/.X11-unix/* | sed 's#/tmp/.X11-unix/X##' | head -n 1)"
user=$(ps -ef | grep '[X]org' | awk '{print $1}')
dbus_socket="/run/user/$(id -u $user)/bus"

sudo -u $user DISPLAY=$display DBUS_SESSION_BUS_ADDRESS=unix:path=$dbus_socket notify-send "$@"