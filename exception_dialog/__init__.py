def main(*args, **kwargs):
    from . import exception_dialog_ui
    return exception_dialog_ui.main(*args, **kwargs)


def reload_modules():
    from . import exception_dialog_system
    exception_dialog_system.unregister_exception_hook()

    import sys
    if sys.version_info.major >= 3:
        from importlib import reload
    else:
        from imp import reload

    from . import exception_dialog_dcc_core
    from . import exception_dialog_ui
    reload(exception_dialog_dcc_core)
    reload(exception_dialog_system)
    reload(exception_dialog_ui)
    

def startup():
    from . import exception_dialog_system
    exception_dialog_system.register_exception_hook()




