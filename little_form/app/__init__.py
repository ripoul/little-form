from flask import Flask

from .extensions import appbuilder, db, migrate


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("config")
    with app.app_context():
        db.init_app(app)
        appbuilder.init_app(app, db.session)
        from . import models, views  # noqa

        migrate.init_app(app, db)
        ...
    return app
