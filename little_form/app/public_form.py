"""Blueprint for public form submission."""

from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from flask_wtf.csrf import generate_csrf
from .models import FormConfig, FormResponses
from .extensions import db
from flask_babel import lazy_gettext as _

public_form_bp = Blueprint("public_form", __name__, url_prefix="/form")


@public_form_bp.route("/<form_config_id>", methods=["GET", "POST"])
def submit(form_config_id: str):
    """Display the form and handle submission."""
    form_config = db.session.get(FormConfig, form_config_id)
    if form_config is None:
        abort(404)

    if request.method == "POST":
        fields = form_config.fields
        if not isinstance(fields, list):
            fields = []

        # Only keep fields defined in form_config
        responses = {}
        for field_name in fields:
            if isinstance(field_name, dict):
                name = field_name.get("name") or field_name.get("id")
            else:
                name = str(field_name).strip()
            if name:
                value = request.form.get(name)
                if value is not None:
                    responses[name] = value

        response = FormResponses(
            form_config_id=form_config_id,
            responses=responses,
            submitted_at=datetime.utcnow(),
            ip_address=request.remote_addr,
            user_agent=request.headers.get("User-Agent"),
        )
        db.session.add(response)
        db.session.commit()

        flash(_("Your response has been submitted successfully."), "success")
        return redirect(url_for("public_form.submit", form_config_id=form_config_id))

    # GET: display the form
    fields = form_config.fields
    if not isinstance(fields, list):
        fields = []

    # Normalize: list of names or list of dicts {name, label?, type?}
    normalized_fields = []
    for f in fields:
        if isinstance(f, dict):
            normalized_fields.append(
                {
                    "name": f.get("name") or f.get("id", ""),
                    "label": f.get("label") or f.get("name") or f.get("id", ""),
                    "type": f.get("type", "text"),
                }
            )
        else:
            name = str(f).strip()
            if name:
                normalized_fields.append(
                    {
                        "name": name,
                        "label": name.replace("_", " ").title(),
                        "type": "text",
                    }
                )

    return render_template(
        "public_form.html",
        form_config=form_config,
        fields=normalized_fields,
        submit_url=url_for("public_form.submit", form_config_id=form_config_id),
        csrf_token=generate_csrf(),
    )
