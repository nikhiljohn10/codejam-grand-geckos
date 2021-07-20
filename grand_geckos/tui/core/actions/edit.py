import datetime

from prompt_toolkit.application.current import get_app
from prompt_toolkit.search import start_search

from grand_geckos.tui.core.views.search import search_toolbar


def do_undo():
    search_toolbar.buffer.undo()


def do_cut():
    data = search_toolbar.buffer.cut_selection()
    get_app().clipboard.set_data(data)


def do_copy():
    data = search_toolbar.buffer.copy_selection()
    get_app().clipboard.set_data(data)


def do_delete():
    search_toolbar.buffer.cut_selection()


def do_find():
    start_search(search_toolbar.control)


def do_find_next():
    search_state = get_app().current_search_state

    cursor_position = search_toolbar.buffer.get_search_position(search_state, include_current_position=False)
    search_toolbar.buffer.cursor_position = cursor_position


def do_paste():
    search_toolbar.buffer.paste_clipboard_data(get_app().clipboard.get_data())


def do_select_all():
    search_toolbar.buffer.cursor_position = 0
    search_toolbar.buffer.start_selection()
    search_toolbar.buffer.cursor_position = len(search_toolbar.buffer.text)


def do_time_date():
    text = datetime.datetime.now().isoformat()
    search_toolbar.buffer.insert_text(text)
