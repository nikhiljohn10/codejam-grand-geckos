from prompt_toolkit.application import Application
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.shortcuts import set_title
from prompt_toolkit.styles import Style
from prompt_toolkit.key_binding import KeyBindings, KeyPressEvent

from grand_geckos.tui.layout.content import root_container, search_view

global_style = Style.from_dict(
    {
        "status": "reverse",
        "shadow": "bg:#440044",
    }
)


def get_global_bindings() -> KeyBindings:

    kb = KeyBindings()

    @kb.add("c-x")
    def _find(event: KeyPressEvent) -> None:
        event.app.exit()

    return kb


layout = Layout(root_container, focused_element=search_view.search_buffer)


def get_app(theme=global_style):
    application = Application(
        layout=layout,
        enable_page_navigation_bindings=True,
        style=theme,
        mouse_support=True,
        full_screen=True,
        key_bindings=get_global_bindings(),
    )
    set_title("SECRET CRATE OF GRAND GECKOS")
    return application
