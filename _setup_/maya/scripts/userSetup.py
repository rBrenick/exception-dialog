import inspect
import os
import site
import sys
import traceback


def _exception_dialog_site_dir_setup():
    dirname = os.path.dirname

    # Add site-packages to sys.path
    package_dir = dirname(dirname(dirname(dirname(inspect.getfile(inspect.currentframe())))))

    if package_dir not in sys.path:
        site.addsitedir(package_dir)


_exception_dialog_site_dir_setup()

try:
    import exception_dialog

    exception_dialog.startup()
except Exception as e:
    traceback.print_exc()
