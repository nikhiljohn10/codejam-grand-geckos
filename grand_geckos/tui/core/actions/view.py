from grand_geckos.tui.dashboard.state import ApplicationState


def do_status_bar():
    ApplicationState.show_status_bar = not ApplicationState.show_status_bar
