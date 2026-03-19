import pytest
from app import create_app
from app.extensions import db, appbuilder
from app.models import FormConfig


@pytest.fixture()
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SECRET_KEY": "test-secret-key",
            "WTF_CSRF_ENABLED": False,
            "SERVER_NAME": "test.local",
        }
    )

    with app.app_context():
        db.create_all()
        role_admin = appbuilder.sm.find_role("Admin")
        if not role_admin:
            role_admin = appbuilder.sm.add_role("Admin")
        user = appbuilder.sm.find_user(username="admin")
        if not user:
            appbuilder.sm.add_user(
                username="admin",
                first_name="Admin",
                last_name="User",
                email="admin@test.com",
                role=role_admin,
                password="admin",
            )
        db.session.commit()

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def form_config(app):
    """Create a test FormConfig with fields."""
    with app.app_context():
        user = appbuilder.sm.find_user(username="admin")
        config = FormConfig(
            fields=["name", "email", "message"],
            created_by_fk=user.id,
            changed_by_fk=user.id,
        )
        db.session.add(config)
        db.session.commit()
        db.session.refresh(config)
        return config
