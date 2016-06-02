from functools import partial
from importlib import import_module
from importlib.util import find_spec
import logging

from flask.ext.admin.contrib.sqla import ModelView
from server import settings


def try_import(module_name: str, ignore_not_found: bool = True):
    """
    Function that imports the module and suppresses any import errors.
    :param module_name: the name of the module to be imported
    :param ignore_not_found: if True, missing modules won't be reported.
    """

    try:
        return import_module(module_name)
    except ImportError as e:
        # skip error message if module existence is optional
        if ignore_not_found and not find_spec(module_name):
            return None

        msg = 'Error importing module "{}". The module might have errors.\nException message: {}'
        logging.warning(msg.format(module_name, e.msg))


def import_sub_module_from_apps(sub_module_name: str):
    """
    Imports a sub-module for all objects in the INSTALLED_APPS list.
    :param sub_module_name: the name of the sub-module to be imported
    """

    for i_app in settings.INSTALLED_APPS:
        try_import('{}.{}'.format(i_app, sub_module_name))


def create_admin_view(model, model_view=None):
    """
    Create a new admin view.
    :param model: the model for which the admin view will be created.
    :param model_view: custom model view that can be used instead of ModelView
    """

    from core import admin
    from core.database import db_session

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

    return '{}__{}'.format(prefix, s)


def get_custom_prefixer(prefix):
    """
    Builds a partial function of 'apply_prefix' with the given prefix.
    :param prefix: the prefix
    :return: a partial function
    """

    return partial(apply_prefix, prefix=prefix)


import_admin_views = partial(import_sub_module_from_apps, sub_module_name='admin')
import_models = partial(import_sub_module_from_apps, sub_module_name='models')
