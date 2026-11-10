from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ColumnMapping(Base):
    __tablename__ = "column_mappings"

    __table_args__ = (
        UniqueConstraint(
            "source_name",
            "file_type",
            "version",
            name="uq_column_mapping_source_version",
        ),
        CheckConstraint(
            "version > 0",
            name="ck_column_mapping_positive_version",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    source_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    file_type: Mapped[str] = mapped_column(
        String(40),
        nullable=False,
    )

    version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    mapping: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_by: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )