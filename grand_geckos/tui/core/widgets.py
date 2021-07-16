from curses import window
from functools import partial
from typing import Callable, Generic, List, Optional, Sequence, Tuple, TypeVar, Union

from prompt_toolkit.application.current import get_app
from prompt_toolkit.auto_suggest import AutoSuggest, DynamicAutoSuggest
from prompt_toolkit.buffer import Buffer, BufferAcceptHandler
from prompt_toolkit.completion import Completer, DynamicCompleter
from prompt_toolkit.document import Document
from prompt_toolkit.filters import (
    Condition,
    FilterOrBool,
    has_focus,
    is_done,
    is_true,
    to_filter,
)
from prompt_toolkit.formatted_text import (
    AnyFormattedText,
    StyleAndTextTuples,
    Template,
    to_formatted_text,
)
from prompt_toolkit.formatted_text.utils import fragment_list_to_text
from prompt_toolkit.history import History
from prompt_toolkit.key_binding import KeyBindings, KeyPressEvent
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout.containers import (
    AnyContainer,
    ConditionalContainer,
    Container,
    DynamicContainer,
    Float,
    FloatContainer,
    HSplit,
    VSplit,
    Window,
    WindowAlign,
)
from prompt_toolkit.layout import ScrollablePane
from prompt_toolkit.lexers import SimpleLexer
from prompt_toolkit.widgets import (
    Box,
    Frame,
    HorizontalLine,
)
from prompt_toolkit.layout.controls import (
    BufferControl,
    FormattedTextControl,
    GetLinePrefixCallable,
    SearchBufferControl,
)
from prompt_toolkit.layout.dimension import AnyDimension
from prompt_toolkit.layout.dimension import Dimension as D
from prompt_toolkit.layout.dimension import to_dimension
from prompt_toolkit.layout.margins import (
    ConditionalMargin,
    NumberedMargin,
    ScrollbarMargin,
)
from prompt_toolkit.layout.processors import (
    AppendAutoSuggestion,
    BeforeInput,
    ConditionalProcessor,
    PasswordProcessor,
    Processor,
)
from prompt_toolkit.lexers import DynamicLexer, Lexer
from prompt_toolkit.mouse_events import MouseEvent, MouseEventType
from prompt_toolkit.utils import get_cwidth
from prompt_toolkit.validation import DynamicValidator, Validator

class TitleView:
    def __init__(self, text: str = "Untitled") -> None:
        self.container = HSplit([
            Window(height=1),
            Window(
                height=2,
                content=FormattedTextControl([("class:title bold", text.upper())]),
                align=WindowAlign.CENTER,
                style="green bold",
            ),
        ])

    def __pt_container__(self) -> Container:
        return self.container

class PaddedContainer:
    def __init__(
        self,
        body: AnyContainer,
        style: str = "",
        width: AnyDimension = None,
        height: AnyDimension = None,
        key_bindings: Optional[KeyBindings] = None,
        modal: bool = False,
        padding: int = 1,
    ) -> None:
        style = "class:frame " + style
        self.container = HSplit(
            [
                Window(height=padding),
                VSplit([
                    Window(width=padding),
                    DynamicContainer(lambda: body),
                    Window(width=padding),
                ]),
                Window(height=padding),
            ],
            width=width,
            height=height,
            style=style,
            key_bindings=key_bindings,
            modal=modal,
        )

    def __pt_container__(self) -> Container:
        return self.container


class BodyView:
    def __init__(
        self,
        platform_list: List[str],
        credential_list: List[str],
        detail_list: List[str],
    ) -> None:
        platform_view = PanelView(platform_list, title="Platforms")
        credential_view = PanelView(credential_list, title="Credentials")
        detail_view = PanelView(detail_list, title="Details")
        self.body_views = [platform_view, credential_view, detail_view]
        self.focus_id = 0
        self.window = PaddedContainer(
            VSplit(self.body_views, padding = 1),
            padding = 1,
        )

    def focused_view(self):
        return self.body_views[self.focus_id]

    def focus_next(self):
        if self.focus_id < len(self.body_views) - 1:
            self.focus_id += 1
        else:
            self.focus_id = 0

    def focus_prev(self):
        if self.focus_id > 0:
            self.focus_id -= 1
        else:
            self.focus_id = len(self.body_views) - 1


    def __pt_container__(self) -> Container:
        return self.window


class PanelView:

    def __init__(self, content: List[str], title: str = "") -> None:
        self.title = title
        self.window = Frame(
            body=ScrollablePane(HSplit(self._make_list(content), padding=1)),
            title=self.title
        )
    
    def _make_list(self, data_list:  List[str]):
        view_list = [  Window(FormattedTextControl(window), width=D()) for window in data_list ]
        return view_list

    def __pt_container__(self) -> Container:
        return self.window

class CellView:
    
    def __init__(self, content: List[str]) -> None:
        self.window = Frame(
            body=ScrollablePane(HSplit(self._make_list(content), padding=1)),
            title="Platform"
        )
    
    def _make_list(self, data_list:  List[str]):
        view_list = [  Window(FormattedTextControl(window), width=D()) for window in data_list ]
        return view_list

    def __pt_container__(self) -> Container:
        return self.window


class SearchView:
    def __init__(
        self,
        search_buffer: Optional[Buffer] = None,
        text_if_not_searching: AnyFormattedText = "  Search(Ctrl+F)",
        prompt: AnyFormattedText = " Search: ",
        ignore_case: FilterOrBool = False,
    ) -> None:

        if search_buffer is None:
            search_buffer = Buffer()

        @Condition
        def is_searching() -> bool:
            return self.control in get_app().layout.search_links

        def get_before_input() -> AnyFormattedText:
            if not is_searching():
                return text_if_not_searching
            else:
                return prompt

        self.search_buffer = search_buffer

        self.control = SearchBufferControl(
            buffer=search_buffer,
            input_processors=[
                BeforeInput(get_before_input, style="class:search-toolbar.prompt")
            ],
            lexer=SimpleLexer(style="class:search-toolbar.text"),
            ignore_case=ignore_case,
        )

        self.window = VSplit([
            Window(width=1),
            Frame(Window(self.control, height=1, style="class:search-toolbar")),
            Window(width=1),
        ])

    def __pt_container__(self) -> Container:
        return self.window


class StatusView:
    def __init__(self, content: str = " Ctrl+X to exit") -> None:
        self.container = Window(FormattedTextControl(content), style="class:status", height=1)

    def __pt_container__(self) -> Container:
        return self.container
