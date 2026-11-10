
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.routes.auth import get_current_user
from app.db.session import get_db
from app.models.partner import Partner
from app.models.user import User
from app.schemas.partner import PartnerCreate, PartnerResponse, PartnerUpdate
from app.services.partners import (
    create_partner,
    get_all_partners,
    get_partner_by_id,
    update_partner,
)


router = APIRouter(
    prefix="/api/v1/partners",
    tags=["Partners"],
)


@router.post(
    "",
    response_model=PartnerResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_partner_endpoint(
    payload: PartnerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return create_partner(db, payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@router.get("", response_model=list[PartnerResponse])
def list_partners(
    include_inactive: bool = Query(default=False),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_all_partners(db, include_inactive=include_inactive)


@router.get("/{partner_id}", response_model=PartnerResponse)
def retrieve_partner(
    partner_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    partner = get_partner_by_id(db, partner_id)

    if partner is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Partner not found",
        )

    return partner


@router.patch("/{partner_id}", response_model=PartnerResponse)
def update_partner_endpoint(
    partner_id: int,
    payload: PartnerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    partner = get_partner_by_id(db, partner_id)

    if partner is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Partner not found",
        )

    try:
        return update_partner(db, partner, payload)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
