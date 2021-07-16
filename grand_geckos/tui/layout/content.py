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

from grand_geckos.tui.layout.menu import menu_items
from grand_geckos.tui.layout.views.search import text_field
from grand_geckos.tui.layout.widgets import (
    TitleView,
    SearchView,
    BodyView,
    StatusView,
)

bindings = KeyBindings()


@bindings.add("c-x")
def _(event):
    event.app.exit()


@bindings.add("c-c")
def _(event):
    event.app.layout.focus(root_container.window)


search_view = SearchView()

body = HSplit([
    TitleView("Secret Crate of Grand Geckos"),
    search_view,
    BodyView(
        platform_view=[
            Window(FormattedTextControl("platform_view")),
        ],
        credential_view=[
            Window(FormattedTextControl("credential_view")),
        ],
        detail_view=[
            Window(FormattedTextControl("detail_view")),
        ],
    ),
    StatusView(),
])

menu = menu_items

root_container = MenuContainer(
    body=body,
    menu_items=menu,
    floats=[
        Float(
            xcursor=True,
            ycursor=True,
            content=CompletionsMenu(max_height=6, scroll_offset=1),
        ),
    ],
    key_bindings=bindings,
)
