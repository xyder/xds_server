from flask import render_template


def index():
    """
    The index view for the main interface app.
    """

    return render_template('main_interface/index.html')
