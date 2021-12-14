import maya.utils
from . import exception_dialog_dcc_core


class ExceptionDialogMaya(exception_dialog_dcc_core.ExceptionDialogCoreInterface):

    def get_base_except_hook(self):
        return maya.utils._formatGuiException

    def register_exception_hook(self, hook_func):
        current_hook = maya.utils.formatGuiException
        maya.utils.formatGuiException = hook_func
        return current_hook

    def unregister_exception_hook(self, previous_hook):
        maya.utils.formatGuiException = previous_hook

