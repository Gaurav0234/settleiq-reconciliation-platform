
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


PartnerType = Literal["courier", "marketplace"]


class PartnerCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    partner_type: PartnerType

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 2:
            raise ValueError("Partner name must contain at least 2 characters")
        return value


class PartnerUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    partner_type: PartnerType | None = None
    is_active: bool | None = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str | None) -> str | None:
        if value is None:
            return value
        value = value.strip()
        if len(value) < 2:
            raise ValueError("Partner name must contain at least 2 characters")
        return value

    @model_validator(mode="after")
    def validate_update(self):
        if not self.model_fields_set:
            raise ValueError("At least one field must be provided")
        return self


class PartnerResponse(BaseModel):
    id: int
    name: str
    partner_type: PartnerType
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
