#!/usr/bin/env python
"""
A simple example of a Notepad-like text editor.
"""

from grand_geckos.tui.core import get_app


def run():
    get_app().run()


if __name__ == "__main__":
    run()
