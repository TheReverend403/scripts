#!/usr/bin/env python3

from contextlib import closing
import random
import subprocess
import os


def xclip(*args, data=None):
    base_command = ["xclip", "-selection", "CLIPBOARD", *args]

    if "-o" in args:
        with closing(
            subprocess.Popen(base_command, stdout=subprocess.PIPE).stdout
        ) as stdout:
            return stdout.read().decode("UTF-8")
    else:
        with closing(
            subprocess.Popen(base_command, stdin=subprocess.PIPE).stdin
        ) as stdin:
            stdin.write(data.encode("UTF-8"))


def notify(text):
    subprocess.Popen(["notify-send", os.path.basename(__file__), text])


def get_clipboard_text():
    return xclip("-o")


def set_clipboard_text(data):
    xclip(data=data)
    notify(data)


def main():
    text = get_clipboard_text()
    if not text:
        notify("No text found in clipboard!")
        return

    text = "".join(
        c.upper() if (i % 2 == 0 or random.random() <= 0.3) else c
        for i, c in enumerate(text.lower())
    )
    set_clipboard_text(text)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        notify(type(exc).__name__)
        raise exc
