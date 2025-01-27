#!/bin/bash

user_pid=$( (pgrep 'Xorg' || pgrep 'sway') | head -n1)
user=$(ps -o user= -p "$user_pid")
machinectl shell "$user"@ "$(which notify-send)" "$@"
