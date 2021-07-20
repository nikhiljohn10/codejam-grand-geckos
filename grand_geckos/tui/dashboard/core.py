from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings, KeyPressEvent
from prompt_toolkit.layout import Layout
from prompt_toolkit.shortcuts import set_title
from prompt_toolkit.styles import Style

from grand_geckos.tui.dashboard.layout import root_container, body_view

global_style = Style.from_dict(
    {
        "status": "reverse",
        "shadow": "bg:#440044",
    }
)

layout = Layout(root_container, focused_element=body_view.focused_view())


def get_app(theme=global_style):
    application = Application(
        layout=layout,
        enable_page_navigation_bindings=True,
        style=theme,
        mouse_support=True,
        full_screen=True,
    )
    set_title("SECRET CRATE OF GRAND GECKOS")
    return application
