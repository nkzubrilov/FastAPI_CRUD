from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix="/votes", tags=['Votes'])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote_post(vote: schemas.Vote, db: Session = Depends(get_db),
              current_user: models.Users = Depends(oauth2.get_current_user)):

    post = db.get(models.Posts, vote.post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {vote.post_id} does not exist')

    existing_vote = db.get(models.Votes, (current_user.id, vote.post_id))
    if vote.dir == 1:
        if existing_vote is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f'User {current_user.id} has already voted on post {vote.post_id}')
        new_vote = models.Votes(user_id=current_user.id, post_id=vote.post_id)
        db.add(new_vote)
        db.commit()
        return {'message': 'successfully added vote'}

    else:
        if existing_vote is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Vote does not exist')

        db.delete(existing_vote)
        db.commit()
        return {'message': 'successfully deleted vote'}
