from prompt_toolkit.widgets import MenuItem

from grand_geckos.tui.core import actions

menu_items = [
    MenuItem(
        "File",
        children=[
            MenuItem("New...", handler=actions.do_new_file),
            MenuItem("Save"),
            MenuItem("Save as..."),
            MenuItem("-", disabled=True),
            MenuItem("Exit", handler=actions.do_exit),
        ],
    ),
    MenuItem(
        "Edit",
        children=[
            MenuItem("Undo", handler=actions.do_undo),
            MenuItem("Cut", handler=actions.do_cut),
            MenuItem("Copy", handler=actions.do_copy),
            MenuItem("Paste", handler=actions.do_paste),
            MenuItem("Delete", handler=actions.do_delete),
            MenuItem("-", disabled=True),
            MenuItem("Find", handler=actions.do_find),
            MenuItem("Find next", handler=actions.do_find_next),
            MenuItem("Replace"),
            MenuItem("Select All", handler=actions.do_select_all),
            MenuItem("Time/Date", handler=actions.do_time_date),
        ],
    ),
    MenuItem(
        "View",
        children=[MenuItem("Status Bar", handler=actions.do_status_bar)],
    ),
]
