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
            HorizontalLine(),
        ])

    def __pt_container__(self) -> Container:
        return self.container


class BodyView:
    def __init__(
        self,
        platform_view: List[AnyContainer],
        credential_view: List[AnyContainer],
        detail_view: List[AnyContainer],
    ) -> None:
        self.window = Frame(
            VSplit([
                Frame(body=HSplit(platform_view, padding=1), title="Platform"),
                Frame(body=HSplit(credential_view, padding=1), title="Credentials"),
                Frame(body=HSplit(detail_view, padding=1), title="Details"),
            ])
        )

    def __pt_container__(self) -> Container:
        return self.window


class SearchView:
    def __init__(
        self,
        search_buffer: Optional[Buffer] = None,
        text_if_not_searching: AnyFormattedText = "Ctrl+F to start search",
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

        self.window = Window(self.control, height=1, style="class:search-toolbar")

    def get_bindings(self) -> KeyBindings:

        kb = KeyBindings()

        @kb.add("c-f")
        def _find(event: KeyPressEvent) -> None:
            event.layout.focus(self.window)

        return kb

    def __pt_container__(self) -> Container:
        return self.window


class StatusView:
    def __init__(self, content: str = "Ctrl+X to exit") -> None:
        self.container = Window(FormattedTextControl(content), style="class:status", height=1)

    def __pt_container__(self) -> Container:
        return self.container
