"""Tests for the public_form blueprint (public form submission)."""


def test_public_form_404_when_form_config_not_found(client):
    """GET /form/<id> with non-existent ID returns 404."""
    response = client.get("/form/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_public_form_get_displays_form(client, form_config):
    """GET /form/<id> displays the form with defined fields."""
    response = client.get(f"/form/{form_config.id}")
    assert response.status_code == 200
    assert b"Form" in response.data
    assert b"name" in response.data
    assert b"email" in response.data
    assert b"message" in response.data
    assert b'name="name"' in response.data
    assert b'name="email"' in response.data
    assert b'name="message"' in response.data
    assert b"<form" in response.data
    assert b'method="post"' in response.data


def test_public_form_post_saves_responses(client, form_config, app):
    """POST /form/<id> saves responses to database."""
    response = client.post(
        f"/form/{form_config.id}",
        data={
            "name": "Doe",
            "email": "john@example.com",
            "message": "My message",
        },
    )
    assert response.status_code == 302
    assert response.location.endswith(f"/form/{form_config.id}")

    with app.app_context():
        from app.extensions import db
        from app.models import FormResponses

        form_response = (
            db.session.query(FormResponses)
            .filter_by(form_config_id=form_config.id)
            .first()
        )
        assert form_response is not None
        assert form_response.responses == {
            "name": "Doe",
            "email": "john@example.com",
            "message": "My message",
        }
        assert form_response.ip_address is not None
        assert form_response.submitted_at is not None


def test_public_form_post_ignores_unauthorized_fields(client, form_config, app):
    """POST only keeps fields defined in form_config."""
    response = client.post(
        f"/form/{form_config.id}",
        data={
            "name": "Doe",
            "email": "john@example.com",
            "message": "OK",
            "pirate_field": "ignored_value",
        },
    )
    assert response.status_code == 302

    with app.app_context():
        from app.extensions import db
        from app.models import FormResponses

        form_response = (
            db.session.query(FormResponses)
            .filter_by(form_config_id=form_config.id)
            .first()
        )
        assert form_response is not None
        assert "pirate_field" not in form_response.responses
        assert form_response.responses["name"] == "Doe"


def test_public_form_post_flash_success(client, form_config):
    """After successful submission, a flash message is displayed."""
    response = client.post(
        f"/form/{form_config.id}",
        data={"name": "X", "email": "x@x.com", "message": "Y"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    # Flash message contains "response" or "submitted"
    assert b"response" in response.data.lower() or b"submitted" in response.data.lower()


def test_public_form_fields_dict_format(client, app):
    """Fields in dict format {name, label, type} are rendered correctly."""
    with app.app_context():
        from app.extensions import db, appbuilder
        from app.models import FormConfig

        user = appbuilder.sm.find_user(username="admin")
        config = FormConfig(
            fields=[
                {"name": "email", "label": "Email address", "type": "email"},
                {"name": "age", "type": "number"},
            ],
            created_by_fk=user.id,
            changed_by_fk=user.id,
        )
        db.session.add(config)
        db.session.commit()
        config_id = config.id

    response = client.get(f"/form/{config_id}")
    assert response.status_code == 200
    assert b"Email address" in response.data
    assert b'name="email"' in response.data
    assert b'type="email"' in response.data
    assert b'name="age"' in response.data
    assert b'type="number"' in response.data
