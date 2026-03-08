from .database import GhostDB


def open(name):
    """
    Open or create a Ghostlite database
    """

    return GhostDB(name)