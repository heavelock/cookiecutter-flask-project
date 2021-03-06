# -*- coding: utf-8 -*-
"""
    {{cookiecutter.project_name}}
    {{'~' * (cookiecutter.project_name|length)}}

    {{cookiecutter.project_description}}

    :author: {{cookiecutter.full_name}} {{cookiecutter.email}}
    :copyright: (c) {{cookiecutter.year}} {{cookiecutter.full_name}}
    :license: {{cookiecutter.license}}, see LICENSE file.
"""

from flask import Flask, render_template
from {{cookiecutter.app_name}}.config import DevelopmentConfig
from {{cookiecutter.app_name}}.extensions import (
    assets, db, migrate, babel, login_manager, mail
)
from {{cookiecutter.app_name}} import modules


__version__ = '{{cookiecutter.version}}'


def create_app(config=None):
    if config is None:
        config = DevelopmentConfig()

    app = Flask(__name__)

    app.config.from_object(config)
    app.config.from_envvar('{{cookiecutter.app_name|upper}}_CONFIG', silent=True)

    assets.init_app(app)
    assets.from_yaml(app.config['ASSETS'])

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    babel.init_app(app)
    mail.init_app(app)

    @app.route('/')
    def home():
        return render_template('home.html')

    for name, url_prefix in app.config.get('MODULES', []):
        blueprint = getattr(getattr(modules, name), name)
        app.register_blueprint(blueprint, url_prefix=url_prefix)

    return app
