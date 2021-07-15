import datetime
from asyncio import ensure_future
from prompt_toolkit.search import start_search
from prompt_toolkit.application.current import get_app
from grand_geckos.tui.layout.views.search import text_field
from grand_geckos.tui.layout.views.dialog import TextInputDialog
from grand_geckos.tui.layout.content import show_message, show_dialog_as_float


def do_go_to():
    async def coroutine():
        dialog = TextInputDialog(title="Go to line", label_text="Line number:")

        line_number = await show_dialog_as_float(dialog)

        try:
            line_number = int(line_number)
        except ValueError:
            show_message("Invalid line number")
        else:
            text_field.buffer.cursor_position = (
                text_field.buffer.document.translate_row_col_to_index(
                    line_number - 1, 0
                )
            )

    ensure_future(coroutine())


def do_undo():
    text_field.buffer.undo()


def do_cut():
    data = text_field.buffer.cut_selection()
    get_app().clipboard.set_data(data)


def do_copy():
    data = text_field.buffer.copy_selection()
    get_app().clipboard.set_data(data)


def do_delete():
    text_field.buffer.cut_selection()


def do_find():
    start_search(text_field.control)


def do_find_next():
    search_state = get_app().current_search_state

    cursor_position = text_field.buffer.get_search_position(
        search_state, include_current_position=False
    )
    text_field.buffer.cursor_position = cursor_position


def do_paste():
    text_field.buffer.paste_clipboard_data(get_app().clipboard.get_data())


def do_select_all():
    text_field.buffer.cursor_position = 0
    text_field.buffer.start_selection()
    text_field.buffer.cursor_position = len(text_field.buffer.text)


def do_time_date():
    text = datetime.datetime.now().isoformat()
    text_field.buffer.insert_text(text)
