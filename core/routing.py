from functools import partial
from importlib import import_module
import itertools
from flask import Blueprint

from core.lib import try_import


def apply_prefix(prefix: str, t: list) -> tuple:
    """
    Joins a string and the first element of a tuple.
    :return: the modified tuple
    """

    return '%s%s' % (prefix, t[0]), t[1]


def url(route_url: str = '', **kwargs: dict) -> list:
    """
    Generates a route/list of routes.
    :param kwargs: Any argument except 'include' and 'routes' will be used to make a route with the
    specified route_url
    'include': can specify a module for which module.urlpatterns will be loaded as routes and prefixed
    'routes': can specify a list of routes which will be loaded and prefixed
    :return: The list of loaded and prefixed routes
    """

    ret = []
    module = kwargs.pop('include', None)
    routes = kwargs.pop('routes', [])

    # create prefixer
    prefixer = partial(apply_prefix, route_url)

    if module:
        module_name = module if isinstance(module, str) else module.__name__

        # get module patterns
        module_patterns = import_module('%s.urls' % module_name).urlpatterns

        # apply prefix to all routes
        ret += list(map(prefixer, itertools.chain(*module_patterns)))

    if routes:
        ret += list(map(prefixer, itertools.chain(*routes)))

    # if there are arguments left, add as a new route directly on the route_url
    if kwargs:
        ret += [(route_url, kwargs)]

    return ret


def add_routes(app, prefix: str = '', routes: list = (), register_function: callable = None) -> None:
    """
    Registers the given routes to an app.
    :param prefix: a prefix that may be prepended to the all given routes.
    :param routes: a list of routes.
    :param register_function: a function that is called using the aggregated prefix and the
    parameters stored in the routes list
    """

    routes = routes or []
    routes = itertools.chain(*routes)
    register_function = register_function or app.add_url_rule

    for route in routes:
        prefixed = apply_prefix(prefix, route)
        register_function(prefixed[0], **prefixed[1])


def add_socket_rule(namespace: str = '', event_name: str = '', socket_func: callable = None) -> None:
    """
    Function that adds a socket rule to the socketio object.
    :param namespace: The namespace on which the socket will be listening
    :param event_name: The name of the event for which the view function will be called
    :param socket_func: The view function registered to the event
    """

    from core import socketio

    if not socket_func:
        def socket_func(_): pass

    socketio.on(event_name or '', namespace=namespace or '/')(socket_func)


def build_blueprint(data: dict = ()) -> Blueprint:
    """
    Function that builds a bluprint with the given data.
    :return: a Flask Blueprint object
    """

    module_name = data['module'].split('.')[-1]

    bp = Blueprint(module_name,
                   data['module'],
                   template_folder='templates',
                   static_folder='static',
                   static_url_path='/static')

    urls_module = try_import('%s.urls' % data['module'])
    if not urls_module:
        return bp

    # try registering sockets
    add_routes(bp, routes=getattr(urls_module, 'urlpatterns', []))

    # try registering routes
    add_routes(bp,
               prefix=data.get('prefix', ''),
               routes=getattr(urls_module, 'socketpatterns', []),
               register_function=add_socket_rule)
    return bp


def register_blueprints(app, installed_apps):
    """
    Function that iterates over all installed apps and builds the required blueprints.
    """

    for iapp in installed_apps:
        # skip if urls are specified as ignored
        if 'urls' in iapp.get('undefined', []):
            continue

        app.register_blueprint(build_blueprint(iapp), url_prefix=iapp.get('prefix', ''))
