from flask import Flask

from .extensions import appbuilder, db, migrate
from .public_form import public_form_bp
from flask_babel import lazy_gettext as _


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object("config")
    with app.app_context():
        db.init_app(app)
        appbuilder.init_app(app, db.session)  # ty: ignore[invalid-argument-type]
        from . import models, views  # noqa

        migrate.init_app(app, db)
        app.register_blueprint(public_form_bp)
        appbuilder.add_view_no_menu(views.FormResponsesView)
        appbuilder.add_view(
            views.FormConfigView,
            "My Forms",
            icon="fa-wpforms",
            category="Forms",
            category_label=_("Forms"),  # ty: ignore[invalid-argument-type]
            label=_("My Forms"),  # ty: ignore[invalid-argument-type]
        )
    return app
