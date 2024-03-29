from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy import select, update, func
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix="/posts", tags=['Posts'])


@router.get("/", response_model=List[schemas.PostVoted])
def get_posts(db: Session = Depends(get_db), current_user: models.Users = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: str = ''):

    filter_query = select(models.Posts).where(models.Posts.title.contains(search)).limit(limit).offset(skip)

    result = db.execute(filter_query.add_columns(func.count(models.Votes.user_id).label('votes')).
                        join(models.Votes, models.Posts.id == models.Votes.post_id, isouter=True).
                        group_by(models.Posts.id))

    posts = [{'post': post, 'votes': votes} for post, votes in result]

    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: models.Users = Depends(oauth2.get_current_user)):
    post_dict = post.dict()
    new_post = models.Posts(user_id=current_user.id, **post_dict)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{post_id}", response_model=schemas.PostVoted)
def get_post(post_id: int, db: Session = Depends(get_db),
             current_user: models.Users = Depends(oauth2.get_current_user)):

    result = db.execute(select(models.Posts, func.count(models.Votes.user_id).label('votes')).
                        join(models.Votes, models.Posts.id == models.Votes.post_id, isouter=True).
                        where(models.Posts.id == post_id).group_by(models.Posts.id)).first()

    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with ID {post_id} was not found')

    post = {'post': result[0], 'votes': result[1]}
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db),
                current_user: models.Users = Depends(oauth2.get_current_user)):
    deleted_post = db.get(models.Posts, post_id)

    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with ID {post_id} does not exist')

    if deleted_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Not authorized to perform the requested action')

    db.delete(deleted_post)
    db.commit()


@router.put("/{post_id}", response_model=schemas.PostResponse)
def update_post(post_id: int, post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: models.Users = Depends(oauth2.get_current_user)):
    updated_post = db.get(models.Posts, post_id)

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with ID {post_id} does not exist')

    if updated_post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Not authorized to perform the requested action')

    post_dict = post.dict()
    stmt = update(models.Posts).where(models.Posts.id == post_id).values(**post_dict)
    db.execute(stmt)
    db.commit()
    db.refresh(updated_post)

    return updated_post
