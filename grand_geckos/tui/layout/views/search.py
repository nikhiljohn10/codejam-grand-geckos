from prompt_toolkit.widgets import SearchToolbar, TextArea
from prompt_toolkit.buffer import Buffer

search_buffer = Buffer()

search_toolbar = SearchToolbar(
    search_buffer=search_buffer,
    ignore_case=True,
)

text_field = TextArea(
    height=1,
    prompt=' Search: ',
    style='class:input-field',
    multiline=False,
    wrap_lines=False,
    search_field=search_toolbar
)
