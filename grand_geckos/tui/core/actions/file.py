from prompt_toolkit.application.current import get_app

from grand_geckos.tui.core.views.search import search_toolbar


def do_new_file():
    search_toolbar.text = ""


def do_exit():
    get_app().exit()
