from asyncio import ensure_future
from prompt_toolkit.completion import PathCompleter
from grand_geckos.tui.layout.views.dialog import TextInputDialog
from prompt_toolkit.application.current import get_app
from grand_geckos.tui.state import ApplicationState
from grand_geckos.tui.layout.views.search import text_field
from grand_geckos.tui.layout.content import show_message, show_dialog_as_float


def do_open_file():
    async def coroutine():
        open_dialog = TextInputDialog(
            title="Open file",
            label_text="Enter the path of a file:",
            completer=PathCompleter(),
        )

        path = await show_dialog_as_float(open_dialog)
        ApplicationState.current_path = path

        if path is not None:
            try:
                with open(path, "rb") as f:
                    text_field.text = f.read().decode("utf-8", errors="ignore")
            except IOError as e:
                show_message("Error", "{}".format(e))

    ensure_future(coroutine())


def do_new_file():
    text_field.text = ""


def do_exit():
    get_app().exit()
