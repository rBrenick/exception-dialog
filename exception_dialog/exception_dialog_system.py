import logging
import os
import sys

active_dcc_is_maya = "maya" in os.path.basename(sys.executable)

if active_dcc_is_maya:
    from . import exception_dialog_dcc_maya as dcc_module

    dcc = dcc_module.ExceptionDialogMaya()


class ExceptionHookHandler(object):
    previous_except_hook = None
    previous_dcc_except_hook = None

    dialog_instance = None


hook_cls = ExceptionHookHandler()


def exception_triggered(exc_type=None, exc_value=None, exc_trace=None, *args, **kwargs):
    if not any([exc_trace, exc_value, exc_type]):
        exc_type, exc_value, exc_trace = sys.exc_info()

    win = hook_cls.dialog_instance
    if win is None or not win.isVisible():
        from . import exception_dialog_ui

        win = exception_dialog_ui.main()  # type: exception_dialog_ui.ExceptionDialogWindow
        hook_cls.dialog_instance = win

    win.set_latest_exception(exc_type, exc_value, exc_trace)

    # call original exception hook
    if hook_cls.previous_except_hook:
        hook_cls.previous_except_hook(exc_type, exc_value, exc_trace)


class BaseExceptionAction(object):
    label = "[EXAMPLE]"
    icon_name = "slack_icon"

    @staticmethod
    def trigger_action(exc_trace, exc_value, exc_typ):
        logging.warning("trigger_action needs implementation for this class")


class SlackExceptionAction(BaseExceptionAction):
    label = "Get Help in Slack"
    icon_name = "slack_icon"


class JiraExceptionAction(BaseExceptionAction):
    label = "Create Jira"
    icon_name = "jira_icon"


def get_exception_action_classes():
    return BaseExceptionAction.__subclasses__()


def dcc_exception_triggered(*args, **kwargs):
    exception_triggered(*args, **kwargs)

    if hook_cls.previous_dcc_except_hook:
        hook_cls.previous_dcc_except_hook(*args, **kwargs)


def register_exception_hook():
    if sys.excepthook == exception_triggered:
        return

    hook_cls.previous_except_hook = sys.excepthook
    hook_cls.previous_dcc_except_hook = dcc.register_exception_hook(dcc_exception_triggered)
    sys.excepthook = exception_triggered
    print("Registered Exception hook: {} - {}".format(__file__, exception_triggered.__name__))


def unregister_exception_hook():
    if hook_cls.previous_except_hook:
        sys.excepthook = hook_cls.previous_except_hook
    if hook_cls.previous_dcc_except_hook:
        dcc.unregister_exception_hook(hook_cls.previous_dcc_except_hook)
    print("Unregistered Exception hook")


def test_exception():
    blargh
