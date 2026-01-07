from flask import Flask

from .extensions import appbuilder, db, migrate
from flask_babel import lazy_gettext as _


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("config")
    with app.app_context():
        db.init_app(app)
        appbuilder.init_app(app, db.session)
        from . import models, views  # noqa

        migrate.init_app(app, db)
        appbuilder.add_view(
            views.FormConfigView,
            "My Forms",
            icon="fa-wpforms",
            category="Forms",
            category_label=_("Forms"),
            label=_("My Forms"),
        )
    return app
