from typing import Iterable
from flask import Blueprint
from core.lib import try_import


def update_rule_dict(rule_dict: dict, initial_path: str, module_name: str = ''):
    """
    Copies a rule dict, initializes the module name if needed and builds the rule path.
    :param rule_dict: the rule dict from which most of the initial values will be copied
    :param initial_path: the path to which the rule path will be added
    :param module_name: the name of the module the rule is associated with. (optional)
    :return: the updated rule dict
    """

    # copy the old values to the resulting dict
    result = {k: v for k, v in rule_dict.items()}

    # updated the module name if needed
    result['module'] = result.get('module') or module_name

    # append the rule path to the initial path
    result['path'] = '{}{}'.format(initial_path, result['path']).replace('//', '/')

    return result


def url(path: str, **kwargs):
    """
    Returns a list of rule dictionaries.
    :param path: the path which will be used to create the rule
    :param kwargs: possible keys:
        include: specify a module to load
        endpoint_name: specifying this would assign a name for the endpoint, which will be retrievable using url_for
        event_name: specifying this will treat the entire rule as a web socket endpoint for the given event name
        view_func: the view which will contain the logic for this rule
    :return: a list of rules
    """

    result = []
    if 'include' not in kwargs:
        # return a dictionary containing the rule parameters
        kwargs['path'] = path
        result.append(kwargs)
    else:
        # return a list of rules fetched from the specified module
        module = kwargs['include']
        module_name = module if isinstance(module, str) else module.__name__
        rules_lists = try_import('{}.urls'.format(module_name))

        # check if there are rules
        if not rules_lists:
            return result

        # add and flatten the rules in a list of rules
        result.extend(update_rule_dict(rule, path, module_name)
                      for rules_list in rules_lists.urlpatterns
                      for rule in rules_list)

    return result


def sort_by_module(rules: Iterable):
    """
    Returns a dict with rules sorted by module name.
    :param rules: the unsorted list of rules
    :return: a dictionary with the sorted rules
    """

    result = {}

    for rule in rules:
        module_name = rule.get('module')
        result[module_name] = result.get(module_name, []) + [rule]

    return result


def register_blueprints(app):
    """
    Creates web socket endpoints or adds rules to a blueprint which is added to the Flask app.
    :param app: the Flask app
    """

    for module, rules in sort_by_module(url('', include='server')).items():
        # create blueprint
        module_name = module.split('.')[-1]
        bp = Blueprint(name=module_name,
                       import_name=module,
                       template_folder='templates',
                       static_folder='static',
                       static_url_path='/{}/static'.format(module_name))

        from core import socketio

        for rule in rules:
            if 'event_name' in rule:
                # create web socket
                socketio.on(rule['event_name'],
                            namespace=rule['path'])(rule['view_func'])
            else:
                # create endpoint rule
                args = {
                    'rule': rule['path'],
                    'view_func': rule['view_func'],
                }

                if 'endpoint_name' in rule:
                    args['endpoint'] = rule['endpoint_name']

                bp.add_url_rule(**args)

        app.register_blueprint(bp)
