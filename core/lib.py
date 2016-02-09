from functools import partial
from importlib import import_module
import logging
from flask.ext.admin.contrib.sqla import ModelView
from xds_server.server import settings


def try_import(module_name: str):
    """
    Function that imports the module and suppresses any import errors.
    :param module_name: the name of the module to be imported
    """

    try:
        return import_module(module_name)
    except ImportError:
        msg = ('Error importing module "%s".\n'
               'The module might have errors or was not specified as "undefined" in the settings file.')
        logging.warning(msg % module_name)
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
    """
    Import admin submodules.
    """

    import_submodule_from_apps(installed_apps=settings.INSTALLED_APPS, submodule_name='admin')


def import_models():
    """
    Import models submodules.
    """

    import_submodule_from_apps(installed_apps=settings.INSTALLED_APPS, submodule_name='models')


def create_admin_view(model, model_view=None):
    """
    Create a new admin view.
    :param model: the model for which the admin view will be created.
    :param model_view: custom model view that can be used instead of ModelView
    """

    from xds_server.core import admin
    from xds_server.core.database import db_session

    if not model_view:
        admin.add_view(ModelView(model, db_session))
    else:
        admin.add_view(model_view(model, db_session))


def apply_prefix(s, prefix):
    """
    Appends a prefix to the given string.
    :param s: the string
    :param prefix: the prefix
    :return: a string with this format: "prefix__string"
    """

    return '%s__%s' % (prefix, s)


def get_custom_prefixer(prefix):
    """
    Builds a partial function of 'apply_prefix' with the given prefix.
    :param prefix: the prefix
    :return: a partial function
    """

    return partial(apply_prefix, prefix=prefix)
