from typing import Any
from flask import render_template, current_app
from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.forms import DynamicForm
from wtforms import TextAreaField
from .models import FormConfig, FormResponses
import logging
from flask_babel import lazy_gettext as _

logger = logging.getLogger(__name__)


class FormConfigCustomForm(DynamicForm):  # type: ignore[misc]
    fields = TextAreaField(
        "Fields", description=_("Enter your tags separated by line breaks")
    )


class FormResponsesView(ModelView):  # type: ignore[misc]
    datamodel = SQLAInterface(FormResponses)
    base_permissions = ["can_list", "can_show"]
    list_columns = ["id", "form_config", "submitted_at", "ip_address", "responses"]
    show_columns = [
        "id",
        "form_config",
        "responses",
        "submitted_at",
        "ip_address",
        "user_agent",
    ]


class FormConfigView(ModelView):  # type: ignore[misc]
    datamodel = SQLAInterface(FormConfig)
    add_form = FormConfigCustomForm
    edit_form = FormConfigCustomForm
    list_columns = ["id", "fields", "created_by"]
    add_columns = ["fields"]
    edit_columns = ["fields"]
    show_columns = ["id", "fields", "public_form_url", "created_by"]
    label_columns = {"public_form_url": _("Submission URL")}
    related_views = [FormResponsesView]

    def prefill_form(self, form: FormConfigCustomForm, pk: Any) -> None:
        form.fields.data = "\n".join(form.fields.data) if form.fields.data else ""

    def pre_add(self, item: FormConfig) -> None:
        if isinstance(item.fields, str):
            item.fields = [v.strip() for v in item.fields.split("\n") if v.strip()]

    def pre_update(self, item: FormConfig) -> None:
        if isinstance(item.fields, str):
            item.fields = [v.strip() for v in item.fields.split("\n") if v.strip()]


@current_app.errorhandler(404)
def page_not_found(e: Any) -> tuple[str, int]:
    return (
        render_template(
            "404.html",
            base_template=current_app.appbuilder.base_template,
            appbuilder=current_app.appbuilder,
        ),
        404,
    )
