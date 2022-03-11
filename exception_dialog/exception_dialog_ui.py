import sys
import traceback
import time
from functools import partial

from . import exception_dialog_system as eds
from . import resources
from . import ui_utils
from .ui_utils import QtCore, QtWidgets, QtGui

# if running in standalone, create app
standalone_app = None
if not QtWidgets.QApplication.instance():
    standalone_app = QtWidgets.QApplication(sys.argv)


class ExceptionDialogWindow(ui_utils.CoreToolWindow):
    WINDOW_SIZE = (600, 400)

    def __init__(self):
        super(ExceptionDialogWindow, self).__init__()

        self._latest_exc_info = None

        self.ui = ExceptionDialogUI()
        self.setCentralWidget(self.ui)
        self.setWindowTitle("Exception Dialog")
        self.setWindowIcon(QtGui.QIcon(resources.get_image_path("warning_icon")))

        for sub_cls in eds.get_exception_action_classes():  # type: eds.BaseExceptionAction
            if sub_cls.is_automatic:
                continue
            if not sub_cls.show_button:
                continue
            self.add_action_button(
                sub_cls.label,
                icon=resources.get_image_path(sub_cls.icon_name),
                command=partial(self.trigger_exception_class, sub_cls),
            )

        self.add_action_button(
            "Copy to Clipboard",
            icon=resources.get_image_path("copy_icon"),
            command=self.copy_exception_to_clipboard,
        )
        self.add_action_button(
            "Close",
            icon=resources.get_image_path("close_icon"),
            command=self.close,
        )

        menu_bar = QtWidgets.QMenuBar()

        file_menu = menu_bar.addMenu("File")  # type: QtWidgets.QMenu

        file_menu.addAction(
            QtGui.QIcon(resources.get_image_path("close_icon")),
            "Exit",
            self.close,
            QtGui.QKeySequence("ESC")
        )

        disable_dialog_menu = menu_bar.addMenu("Disable Dialog")  # type: QtWidgets.QMenu

        disable_dialog_menu.addAction(
            QtGui.QIcon(resources.get_image_path("clock_icon")),
            "Disable Dialog - 1 Hour",
            partial(self.disable_dialog, 3600),  # time in seconds
        )

        disable_dialog_menu.addAction(
            QtGui.QIcon(resources.get_image_path("clock_icon")),
            "Disable Dialog - This Session",
            partial(self.disable_dialog, "session")
        )

        self.setMenuBar(menu_bar)

    def add_action_button(self, label="[EXAMPLE]", icon=None, command=None):
        btn = QtWidgets.QPushButton(label)
        btn.setMinimumHeight(40)

        if icon:
            btn.setIcon(QtGui.QIcon(icon))

        if command:
            btn.clicked.connect(command)

        self.ui.action_buttons_layout.addWidget(btn)

    def trigger_exception_class(self, cls):
        cls = cls  # type: eds.BaseExceptionAction
        cls.trigger_action(*self._latest_exc_info)

    def set_latest_exception(self, exc_type, exc_value, exc_trace):
        self._latest_exc_info = (exc_type, exc_value, exc_trace)

        full_exception_info = traceback.format_exception(exc_type, exc_value, exc_trace)
        full_exception_info.append("-" * 50)
        full_exception_info.append("\n")
        exc_text = "".join(full_exception_info)

        self.ui.exception_text_edit.moveCursor(QtGui.QTextCursor.End)
        self.ui.exception_text_edit.insertPlainText(exc_text)
        self.ui.exception_text_edit.moveCursor(QtGui.QTextCursor.End)

    def copy_exception_to_clipboard(self):
        clipboard = QtWidgets.QApplication.clipboard()  # type: QtGui.QClipboard
        clipboard.setText(self.ui.exception_text_edit.toPlainText())

        # select text to indicate something happened
        self.ui.exception_text_edit.selectAll()

    @staticmethod
    def disable_dialog(disable_time_amount):
        if disable_time_amount == "session":
            eds.SessionInfo.disabled_for_this_session = True
            return

        if isinstance(disable_time_amount, int):
            eds.SessionInfo.disable_until_this_time = time.time() + disable_time_amount


class ExceptionDialogUI(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(ExceptionDialogUI, self).__init__(*args, **kwargs)

        warning_icon_label = QtWidgets.QLabel(self)
        warning_icon_label.setPixmap(QtGui.QPixmap(resources.get_image_path("warning_icon")).scaled(64, 64))

        warning_label = QtWidgets.QLabel(self)
        warning_label.setAlignment(QtCore.Qt.AlignCenter)
        warning_label.setText("An Exception has Occurred")
        warning_label.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        warning_label.setStyleSheet("font-size: 28px;")

        self.exception_text_edit = QtWidgets.QTextEdit(self)
        self.exception_text_edit.setWordWrapMode(QtGui.QTextOption.NoWrap)

        self.action_buttons_layout = QtWidgets.QHBoxLayout()

        self.main_layout = QtWidgets.QVBoxLayout()
        warning_layout = QtWidgets.QHBoxLayout()
        warning_layout.addWidget(warning_icon_label)
        warning_layout.addWidget(warning_label)
        self.main_layout.addLayout(warning_layout)
        self.main_layout.addLayout(self.action_buttons_layout)
        self.main_layout.addWidget(self.exception_text_edit)
        self.setLayout(self.main_layout)


def main(refresh=False):
    win = ExceptionDialogWindow()
    win.main(refresh=refresh)

    if standalone_app:
        ui_utils.standalone_app_window = win
        sys.exit(standalone_app.exec_())

    return win


if __name__ == "__main__":
    main()
