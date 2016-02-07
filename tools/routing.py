from importlib import import_module
import itertools
from flask import Blueprint
from xds_server.core.lib import try_import


def apply_prefix(prefix: str, t: list) -> tuple:
    """
    Joins a string and the first element of a tuple.
    :return: the modified tuple
    """

    return '%s%s' % (prefix, t[0]), t[1]


def apply_prefixes(prefix: str, routes: list) -> list:
    """
    Applies a prefix to a list of tuples.
    :return: the modified list.
    """

    ret = []
    for route in routes:
        ret.append(apply_prefix(prefix, route))
    return ret


def url(route: str, **kwargs: dict) -> list:
    """
    Returns a list of tuples that contains the given route and any attached arguments.
    If 'include=module_name' is specified as keyword argument then it will include the submodule 'urlpatterns' from
    the specified module.
    :param kwargs: The keyword arguments will be attached to the url tuple associated with the route.
    'include' as a keyword argument can specify the name of a module for which the submodule 'urlpatterns' will be
    loaded.
    :return: A list of tuples for the specified route/routes
    """

    ret = []
    if 'include' in kwargs:
        # load module from arg, flatten urlpatterns list and apply prefixes
        ret += apply_prefixes(route, itertools.chain(
            *import_module(kwargs['include'].__name__ + '.urls').urlpatterns))
    else:
        ret = [(route, kwargs)]
    return ret


def add_routes(app, prefix: str='', routes: list=()) -> None:
    """
    Registers the given routes to an app.
    :param prefix: a prefix that may be prepended to the all given routes.
    :param routes: a list of routes.
    """

    routes = routes or []
    routes = itertools.chain(*routes)

    for route in routes:
        prefixed = apply_prefix(prefix, route)
        app.add_url_rule(prefixed[0], **prefixed[1])


def build_blueprint(data):
    """
    Function that builds a bluprint with the given data.
    """

    urls_module = try_import('%s.urls' % data['module'])

    if not urls_module:
        return None

    bp = Blueprint(data['module'].split('.')[-1],
                   data['module'],
                   template_folder='templates',
                   static_folder='static')

    add_routes(bp, routes=urls_module.urlpatterns)
    return bp


def register_blueprints(app, installed_apps):
    """
    Function that iterates over all installed apps and builds the required blueprints.
    """

    for iapp in installed_apps:
        if 'urls' in iapp.get('undefined', []):
            continue

        bp = build_blueprint(iapp)
        if bp:
            app.register_blueprint(bp, url_prefix=iapp.get('prefix', ''))
