#!/usr/bin/env bash

display=":$(find /tmp/.X11-unix/* | sed 's#/tmp/.X11-unix/X##' | head -n 1)"
x11_pid=$(pgrep 'Xorg')
user=$(ps -o user= -p "$x11_pid")
dbus_socket="/run/user/$(id -u "$user")/bus"

sudo -u "$user" DISPLAY="$display" DBUS_SESSION_BUS_ADDRESS=unix:path="$dbus_socket" notify-send "$@"
