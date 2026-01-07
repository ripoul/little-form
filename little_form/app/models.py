from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin
from sqlalchemy import Column, String
from sqlalchemy.types import JSON
from uuid import uuid4


class FormConfig(Model, AuditMixin):  # type: ignore[misc]
    __tablename__ = "form_config"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    fields = Column(JSON, nullable=False)

    def __repr__(self) -> str:
        return f"<FormConfig owner={self.created_by} fields={self.fields}>"
