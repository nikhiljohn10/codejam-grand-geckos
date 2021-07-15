from asyncio import ensure_future
from prompt_toolkit.application.current import get_app
from prompt_toolkit.layout.containers import Float
from prompt_toolkit.filters import Condition
from prompt_toolkit.widgets import MenuContainer
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import Float
from prompt_toolkit.layout.menus import CompletionsMenu
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.containers import (
    ConditionalContainer,
    HSplit,
    VSplit,
    Window,
    WindowAlign,
)

from grand_geckos.tui.state import ApplicationState
from grand_geckos.tui.layout.menu import menu_items
from grand_geckos.tui.layout.views.search import text_field, search_toolbar
from grand_geckos.tui.layout.views.status import get_statusbar_text, get_statusbar_right_text
from grand_geckos.tui.layout.views.dialog import MessageDialog


bindings = KeyBindings()


@bindings.add("c-c")
def _(event):
    "Focus menu."
    event.app.layout.focus(root_container.window)


async def show_dialog_as_float(dialog):
    "Coroutine."
    float_ = Float(content=dialog)
    root_container.floats.insert(0, float_)

    app = get_app()

    focused_before = app.layout.current_window
    app.layout.focus(dialog)
    result = await dialog.future
    app.layout.focus(focused_before)

    if float_ in root_container.floats:
        root_container.floats.remove(float_)

    return result


def show_message(title, text):
    async def coroutine():
        dialog = MessageDialog(title, text)
        await show_dialog_as_float(dialog)

    ensure_future(coroutine())


body = HSplit(
    [
        text_field,
        search_toolbar,
        ConditionalContainer(
            content=VSplit(
                [
                    Window(
                        FormattedTextControl(get_statusbar_text), style="class:status"
                    ),
                    Window(
                        FormattedTextControl(get_statusbar_right_text),
                        style="class:status.right",
                        width=9,
                        align=WindowAlign.RIGHT,
                    ),
                ],
                height=1,
            ),
            filter=Condition(lambda: ApplicationState.show_status_bar),
        ),
    ]
)

menu = menu_items

root_container = MenuContainer(
    body=body,
    menu_items=menu,
    floats=[
        Float(
            xcursor=True,
            ycursor=True,
            content=CompletionsMenu(max_height=16, scroll_offset=1),
        ),
    ],
    key_bindings=bindings,
)
