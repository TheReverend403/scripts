#!/usr/bin/env bash

x11_pid=$(pgrep 'Xorg')
user=$(ps -o user= -p "$x11_pid")
machinectl shell "$user"@ "$(which notify-send)" "$@"
