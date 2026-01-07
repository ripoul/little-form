from typing import Any
from flask import render_template, current_app
from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.forms import DynamicForm
from wtforms import TextAreaField
from .models import FormConfig
import logging

logger = logging.getLogger(__name__)


class FormConfigCustomForm(DynamicForm):  # type: ignore[misc]
    fields = TextAreaField(
        "Fields", description="Entrez vos tags séparés par des retours à la ligne"
    )


class FormConfigView(ModelView):  # type: ignore[misc]
    datamodel = SQLAInterface(FormConfig)
    add_form = FormConfigCustomForm
    edit_form = FormConfigCustomForm
    list_columns = ["id", "fields", "created_by"]
    add_columns = ["fields"]
    edit_columns = ["fields"]
    show_columns = ["id", "fields", "created_by"]

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
