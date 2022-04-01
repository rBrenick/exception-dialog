import maya.utils
import maya.cmds as cmds
from . import exception_dialog_dcc_core


class ExceptionDialogMaya(exception_dialog_dcc_core.ExceptionDialogCoreInterface):
    def ui_available(self):
        in_batch_mode = cmds.about(batch=True)
        ui_is_available = not in_batch_mode
        return ui_is_available

    def register_exception_hook(self, hook_func):
        current_hook = maya.utils.formatGuiException
        maya.utils.formatGuiException = hook_func
        return current_hook

    def unregister_exception_hook(self, previous_hook):
        maya.utils.formatGuiException = previous_hook

