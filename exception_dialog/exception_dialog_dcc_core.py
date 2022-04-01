class ExceptionDialogCoreInterface(object):
    def register_exception_hook(self, hook_func):
        print("method 'register_exception_hook' is undefined for {}".format(self.__class__.__name__))
        return None

    def unregister_exception_hook(self, previous_hook):
        print("method 'unregister_exception_hook' is undefined for {}".format(self.__class__.__name__))
        return None

