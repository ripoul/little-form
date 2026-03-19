from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin
from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.types import JSON
from uuid import uuid4


class FormConfig(Model, AuditMixin):  # type: ignore[misc]
    __tablename__ = "form_config"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    fields = Column(JSON, nullable=False)
    responses = relationship(
        "FormResponses",
        back_populates="form_config",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<FormConfig owner={self.created_by} fields={self.fields}>"

    @property
    def public_form_url(self) -> str:
        """Public URL for submitting responses (to use in a template)."""
        from flask import url_for

        return url_for("public_form.submit", form_config_id=self.id, _external=True)


class FormResponses(Model):  # type: ignore[misc]
    __tablename__ = "form_responses"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    form_config_id = Column(
        String(36),
        ForeignKey("form_config.id", ondelete="CASCADE"),
        nullable=False,
    )
    form_config = relationship("FormConfig", back_populates="responses")
    responses = Column(JSON, nullable=False)  # {"field_name": "value", ...}
    submitted_at = Column(DateTime, nullable=False)
    ip_address = Column(String(45), nullable=True)  # IPv6 max length
    user_agent = Column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<FormResponses form={self.form_config_id} at={self.submitted_at}>"
