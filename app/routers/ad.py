from typing import Annotated

import sqlalchemy
from fastapi import APIRouter, Depends, Path, Request, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas, models
from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter(
    prefix='',
    tags=['advertisement']
)


@router.get('', response_model=list[schemas.Ad], status_code=status.HTTP_200_OK)
async def ads_list(db_session: Annotated[Session, Depends(get_db)]):
    ad_instances = db_session.query(models.Advertise) \
        .filter_by(status=models.AdvertiseStatus.ACTIVE).all()
    return ad_instances


@router.get('/{id:int}', response_model=schemas.Ad, status_code=status.HTTP_200_OK)
async def ad_retrieve(
        _id: Annotated[int, Path(alias='id')],
        db_session: Annotated[Session, Depends(get_db)]
):
    ad_instance_q = db_session.query(models.Advertise) \
        .filter_by(id=_id, status=models.AdvertiseStatus.ACTIVE)
    ad_instance = ad_instance_q.first()
    if ad_instance_q.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ad doesn't exist.",
        )
    return ad_instance


@router.post(
    '',
    response_model=schemas.Ad,
    dependencies=[Depends(get_current_user)],
    status_code=status.HTTP_201_CREATED
)
async def ad_create(
        request: Request,
        ad: schemas.AdCreate,
        db_session: Annotated[Session, Depends(get_db)]
):
    ad_dict = {
        'owner_id': request.user.id,
        **ad.model_dump()
    }
    ad_instance = models.Advertise(**ad_dict)
    db_session.add(ad_instance)
    db_session.commit()
    db_session.refresh(ad_instance)
    return ad_instance


@router.put('/{id:int}', response_model=schemas.Ad, dependencies=[Depends(get_current_user)],
            status_code=status.HTTP_200_OK)
async def ad_update(
        request: Request,
        _id: Annotated[int, Path(alias='id')],
        ad: schemas.AdUpdate,
        db_session: Annotated[Session, Depends(get_db)]
):
    ad_instance_q = db_session.query(models.Advertise) \
        .filter_by(id=_id, status=models.AdvertiseStatus.ACTIVE, owner_id=request.user.id)
    if ad_instance_q.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ad doesn't exist.",
        )
    ad_instance_q = ad_instance_q.filter_by(owner_id=request.user.id)
    if ad_instance_q.first() is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can not access to this ad.",
        )
    ad_instance_q.update(ad.model_dump())
    db_session.commit()
    ad_instance = ad_instance_q.first()
    return ad_instance


@router.patch('/{id:int}', response_model=schemas.Ad, dependencies=[Depends(get_current_user)],
              status_code=status.HTTP_200_OK)
async def ad_partial_update(
        request: Request,
        _id: Annotated[int, Path(alias='id')],
        ad: schemas.AdPartialUpdate,
        db_session: Annotated[Session, Depends(get_db)]
):
    ad_instance_q = db_session.query(models.Advertise) \
        .filter_by(id=_id, status=models.AdvertiseStatus.ACTIVE)
    if ad_instance_q.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ad doesn't exist.",
        )
    ad_instance_q = ad_instance_q.filter_by(owner_id=request.user.id)
    if ad_instance_q.first() is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can not access to this ad.",
        )
    ad_instance_q.update(ad.model_dump(exclude_unset=True))
    db_session.commit()
    ad_instance = ad_instance_q.first()
    return ad_instance


@router.delete('/{id:int}', dependencies=[Depends(get_current_user)],
               status_code=status.HTTP_200_OK)
async def ad_delete(
        request: Request,
        _id: Annotated[int, Path(alias='id')],
        db_session: Annotated[Session, Depends(get_db)]
):
    ad_instance_q = db_session.query(models.Advertise) \
        .filter_by(id=_id, status=models.AdvertiseStatus.ACTIVE)
    if ad_instance_q.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ad doesn't exist.",
        )
    ad_instance_q = ad_instance_q.filter_by(owner_id=request.user.id)
    if ad_instance_q.first() is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can not access to this ad.",
        )
    # ad_instance_q.update({'status': models.AdvertiseStatus.INACTIVE})
    ad_instance = ad_instance_q.first()
    ad_instance.status = models.AdvertiseStatus.INACTIVE
    db_session.commit()
    print(_id)
    print(db_session.query(models.Advertise).filter_by(id=_id).first().status)


@router.get(
    '/{id:int}/comments',
    response_model=list[schemas.Comment],
    status_code=status.HTTP_200_OK
)
async def ad_comments_list(
        advertise_id: Annotated[int, Path(alias='id')],
        db_session: Annotated[Session, Depends(get_db)]
):
    ad_instance_q = db_session.query(models.Advertise).filter_by(id=advertise_id)
    if ad_instance_q.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ad doesn't exist.",
        )
    ad_comment_instances = db_session.query(models.Comment).filter_by(advertise_id=advertise_id).all()
    return ad_comment_instances


@router.post(
    '/{id:int}/comments',
    response_model=schemas.Comment,
    dependencies=[Depends(get_current_user)],
    status_code=status.HTTP_201_CREATED
)
async def ad_comment_create(
        request: Request,
        ad_id: Annotated[int, Path(alias='id')],
        comment: schemas.CommentCreate,
        db_session: Annotated[Session, Depends(get_db)]
):
    comment_dict = {
        'owner_id': request.user.id,
        'advertise_id': ad_id,
        **comment.model_dump()
    }
    comment_instance = models.Comment(**comment_dict)
    db_session.add(comment_instance)
    try:
        db_session.commit()
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="You post comment for this ad already.",
        )
    db_session.refresh(comment_instance)
    return comment_instance
