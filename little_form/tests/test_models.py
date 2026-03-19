"""Tests for FormConfig and FormResponses models."""

from datetime import datetime, timezone


def test_form_config_public_form_url(app, form_config):
    """FormConfig.public_form_url returns the absolute URL of the public form."""
    config_id = form_config.id
    with app.test_request_context():
        from app.extensions import db
        from app.models import FormConfig

        config = db.session.get(FormConfig, config_id)
        url = config.public_form_url
        assert str(config_id) in url
        assert "/form/" in url
        assert url.startswith("http")


def test_form_responses_relation_form_config(app, form_config):
    """FormResponses is correctly linked to FormConfig via the relationship."""
    config_id = form_config.id
    with app.app_context():
        from app.extensions import db
        from app.models import FormConfig, FormResponses

        fr = FormResponses(
            form_config_id=config_id,
            responses={"name": "Test"},
            submitted_at=datetime.now(timezone.utc),
        )
        db.session.add(fr)
        db.session.commit()

        config = db.session.get(FormConfig, config_id)
        assert fr.form_config is not None
        assert fr.form_config.id == config_id
        assert fr in config.responses
