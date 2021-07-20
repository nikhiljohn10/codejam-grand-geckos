from prompt_toolkit.filters import Condition
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import (
    ConditionalContainer,
    Float,
    HSplit,
    VSplit,
    Window,
    WindowAlign,
)
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.menus import CompletionsMenu
from prompt_toolkit.widgets import MenuContainer, HorizontalLine

from grand_geckos.tui.core.menu import menu_items
from grand_geckos.tui.core.views.search import text_field
from grand_geckos.tui.core.widgets import (
    TitleView,
    SearchView,
    BodyView,
    StatusView,
)

bindings = KeyBindings()
search_view = SearchView()

@bindings.add("c-x")
def _(event):
    event.app.exit()

@bindings.add("c-c")
def _(event):
    event.app.layout.focus(root_container.window)

@bindings.add("c-f")
def _(event):
    event.layout.focus(search_view.window)

@bindings.add("c-x")
def _find(event):
    event.app.exit()

body_view = BodyView(
        platform_list=[
            "Google.com",
            "Facebook.com",
            "My Laptop",
            "Mai App",
            "Facebook.com",
            "My Laptop",
            "Mai App",
            "Facebook.com",
            "My Laptop",
            "Mai App",
        ],
        credential_list=[
            "Google.com",
            "Facebook.com",
            "My Laptop",
            "Mai App",
            "Facebook.com",
            "My Laptop",
            "Mai App",
            "Facebook.com",
            "My Laptop",
            "Mai App",
        ],
        detail_list=[
            "Google.com",
            "Facebook.com",
            "My Laptop",
            "Mai App",
        ],
    )

root_container = MenuContainer(
    body=HSplit([
        TitleView("Secret Crate of Grand Geckos"),
        search_view,
        body_view,
        StatusView(),
    ]),
    menu_items=menu_items,
    floats=[
        Float(
            xcursor=True,
            ycursor=True,
            content=CompletionsMenu(max_height=6, scroll_offset=1),
        ),
    ],
    key_bindings=bindings,
)
