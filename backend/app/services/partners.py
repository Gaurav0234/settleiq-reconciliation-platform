
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.partner import Partner
from app.schemas.partner import PartnerCreate, PartnerUpdate


def create_partner(db: Session, payload: PartnerCreate) -> Partner:
    partner = Partner(
        name=payload.name.strip(),
        partner_type=payload.partner_type,
        is_active=True,
    )

    db.add(partner)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("A partner with this name already exists")

    db.refresh(partner)
    return partner


def get_partner_by_id(db: Session, partner_id: int) -> Partner | None:
    return db.get(Partner, partner_id)


def get_all_partners(
    db: Session,
    include_inactive: bool = False,
) -> list[Partner]:
    query = select(Partner).order_by(Partner.created_at.desc())

    if not include_inactive:
        query = query.where(Partner.is_active.is_(True))

    return list(db.scalars(query).all())


def update_partner(
    db: Session,
    partner: Partner,
    payload: PartnerUpdate,
) -> Partner:
    updates = payload.model_dump(exclude_unset=True)

    if "name" in updates and updates["name"] is not None:
        updates["name"] = updates["name"].strip()

    for field, value in updates.items():
        setattr(partner, field, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("A partner with this name already exists")

    db.refresh(partner)
    return partner
