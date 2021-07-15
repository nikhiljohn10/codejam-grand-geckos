
from prompt_toolkit.application import Application
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.styles import Style
from prompt_toolkit.shortcuts import set_title
from grand_geckos.tui.layout.content import root_container
from grand_geckos.tui.layout.views.search import text_field

global_style = Style.from_dict(
    {
        "status": "reverse",
        "shadow": "bg:#440044",
    }
)


layout = Layout(root_container, focused_element=text_field)


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
