from grand_geckos.tui.layout.views.search import text_field


def get_statusbar_text():
    return " Press Ctrl-C to open menu. "


def get_statusbar_right_text():
    return " {}:{}  ".format(
        text_field.document.cursor_position_row + 1,
        text_field.document.cursor_position_col + 1,
    )
