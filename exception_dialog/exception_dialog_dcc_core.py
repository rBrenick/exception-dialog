class ExceptionDialogCoreInterface(object):
    def get_base_except_hook(self):
        return None

    def register_exception_hook(self):
        return None

    def unregister_exception_hook(self, hook):
        return None

