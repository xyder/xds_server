from importlib import import_module
import logging
from xds_server.server import settings


def try_import(module_name: str):
    """
    Function that imports the module and suppresses any import errors.
    :param module_name: the name of the module to be imported
    """

    try:
        return import_module(module_name)
    except ImportError:
        logging.warning('Missing module: %s' % module_name)
        return None


def import_submodule_from_apps(installed_apps: list, submodule_name: str):
    """
    Imports a submodule for all objects in the given apps dict.
    :param installed_apps: a list containing all apps from which the submodule will be imported
    :param submodule_name: the name of the submodule to be imported
    """

    for iapp in installed_apps:
        if submodule_name not in iapp.get('undefined', []):
            try_import('%s.%s' % (iapp['module'], submodule_name))


def import_admin_views():
    import_submodule_from_apps(installed_apps=settings.INSTALLED_APPS, submodule_name='admin')


def import_models():
    import_submodule_from_apps(installed_apps=settings.INSTALLED_APPS, submodule_name='models')
