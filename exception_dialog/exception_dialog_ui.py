import sys

from . import ui_utils
from .ui_utils import QtWidgets, QtGui

existing_app = QtWidgets.QApplication.instance()

# if running in standalone, create app
standalone_app = None
if not existing_app:
    standalone_app = QtWidgets.QApplication(sys.argv)


class ExceptionDialogWindow(ui_utils.CoreToolWindow):
    WINDOW_SIZE = (600, 400)

    def __init__(self):
        super(ExceptionDialogWindow, self).__init__()

        self.ui = ExceptionDialogUI()
        self.setCentralWidget(self.ui)

    def add_exception_text(self, text):
        self.ui.exception_text_edit.moveCursor(QtGui.QTextCursor.End)
        self.ui.exception_text_edit.insertPlainText(text)
        self.ui.exception_text_edit.moveCursor(QtGui.QTextCursor.End)


class ExceptionDialogUI(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(ExceptionDialogUI, self).__init__(*args, **kwargs)

        self.exception_text_edit = QtWidgets.QTextEdit()
        self.exception_text_edit.setWordWrapMode(QtGui.QTextOption.NoWrap)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addWidget(self.exception_text_edit)
        self.setLayout(self.main_layout)


def main(refresh=False):
    win = ExceptionDialogWindow()
    win.main(refresh=refresh)

    if standalone_app:
        sys.exit(standalone_app.exec_())

    return win


if __name__ == "__main__":
    main()
