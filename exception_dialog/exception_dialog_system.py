import importlib
import logging
import os
import sys
import time
import traceback

active_dcc_is_maya = "maya" in os.path.basename(sys.executable)

if active_dcc_is_maya:
    from . import exception_dialog_dcc_maya as dcc_module

    dcc = dcc_module.ExceptionDialogMaya()
else:
    from . import exception_dialog_dcc_core as dcc_module

    dcc = dcc_module.ExceptionDialogCoreInterface()


class ExceptionDialogConstants:
    extension_file_prefix = "exception_dialog_ext"


class SessionInfo:
    disable_until_this_time = None
    disabled_for_this_session = False


class ExceptionHookHandler(object):
    previous_except_hook = None
    previous_dcc_except_hook = None

    dialog_instance = None


hook_cls = ExceptionHookHandler()
lk = ExceptionDialogConstants


def exception_triggered(exc_type=None, exc_value=None, exc_trace=None, *args, **kwargs):
    if SessionInfo.disabled_for_this_session:
        return

    if SessionInfo.disable_until_this_time and time.time() < SessionInfo.disable_until_this_time:
        return

    if not any([exc_trace, exc_value, exc_type]):
        exc_type, exc_value, exc_trace = sys.exc_info()

    win = hook_cls.dialog_instance
    if win is None or not win.isVisible():
        from . import exception_dialog_ui

        win = exception_dialog_ui.main()  # type: exception_dialog_ui.ExceptionDialogWindow
        hook_cls.dialog_instance = win

    win.set_latest_exception(exc_type, exc_value, exc_trace)

    for action_cls in get_exception_action_classes():
        if action_cls.is_automatic:
            action_cls.trigger_action(exc_type, exc_value, exc_trace)


class BaseExceptionAction(object):
    label = "[EXAMPLE]"
    icon_name = "default_icon"
    is_automatic = False
    show_button = True
    tool_tip = ""

    @staticmethod
    def trigger_action(exc_type, exc_value, exc_trace):
        logging.warning("trigger_action needs implementation for this class")


class AutomaticExceptionAction(BaseExceptionAction):
    is_automatic = True

    @staticmethod
    def trigger_action(exc_type, exc_value, exc_trace):
        pass


class SlackExceptionAction(BaseExceptionAction):
    label = "Get Help in Slack"
    icon_name = "slack_icon"
    show_button = False


class JiraExceptionAction(BaseExceptionAction):
    label = "Create Jira"
    icon_name = "jira_icon"
    show_button = False


def get_exception_action_classes():
    return BaseExceptionAction.__subclasses__()


def dcc_exception_triggered(*args, **kwargs):
    exception_triggered(*args, **kwargs)

    # call original DCC exception hook
    if hook_cls.previous_dcc_except_hook:
        return hook_cls.previous_dcc_except_hook(*args, **kwargs)


def normal_exception_triggered(*args, **kwargs):
    exception_triggered(*args, **kwargs)

    # call original exception hook
    if hook_cls.previous_except_hook:
        return hook_cls.previous_except_hook(*args, **kwargs)


def register_exception_hook():
    if sys.excepthook == normal_exception_triggered:
        print("Exception hook(s) already registered: {} - {}".format(__file__, normal_exception_triggered.__name__))
        return

    if not dcc.ui_available():
        print("Exception hook(s) did not register, due to UI not being available.")
        return

    hook_cls.previous_except_hook = sys.excepthook
    hook_cls.previous_dcc_except_hook = dcc.register_exception_hook(dcc_exception_triggered)
    sys.excepthook = normal_exception_triggered
    print("Registered Exception hook(s): {} - {}".format(__file__, normal_exception_triggered.__name__))


def unregister_exception_hook():
    if hook_cls.previous_except_hook:
        sys.excepthook = hook_cls.previous_except_hook
    if hook_cls.previous_dcc_except_hook:
        dcc.unregister_exception_hook(hook_cls.previous_dcc_except_hook)
    print("Unregistered Exception hook(s)")


def test_exception():
    blargh


def import_extensions(refresh=False):
    if refresh:
        modules_to_pop = []
        for mod_key in sys.modules.keys():
            if mod_key.startswith(lk.extension_file_prefix):
                modules_to_pop.append(mod_key)

        for mod_key in modules_to_pop:
            sys.modules.pop(mod_key)

    # look through sys.path for extension modules
    modules_to_import = list()
    for sys_path in sys.path:
        if not os.path.isdir(sys_path):
            continue

        # for every .py file with the proper prefix, import it
        for sys_path_name in os.listdir(sys_path):
            if not sys_path_name.startswith(lk.extension_file_prefix):
                continue

            module_name = os.path.splitext(sys_path_name)[0]
            modules_to_import.append(module_name)

    modules_to_import = list(set(modules_to_import))

    for module_import_str in modules_to_import:
        if not module_import_str:
            continue

        try:
            importlib.import_module(module_import_str)
            print("Imported extension: {}".format(module_import_str))
        except Exception as e:
            traceback.print_exc()
