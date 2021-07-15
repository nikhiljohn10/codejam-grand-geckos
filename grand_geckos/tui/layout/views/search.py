
from prompt_toolkit.lexers import DynamicLexer, PygmentsLexer
from prompt_toolkit.widgets import SearchToolbar, TextArea
from grand_geckos.tui.state import ApplicationState

search_toolbar = SearchToolbar()
text_field = TextArea(
    lexer=DynamicLexer(
        lambda: PygmentsLexer.from_filename(
            ApplicationState.current_path or ".txt", sync_from_start=False
        )
    ),
    scrollbar=True,
    line_numbers=True,
    search_field=search_toolbar,
)
