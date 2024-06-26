
from .. import model, schemas
from typing import List, Optional
from .. database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, Response, status, HTTPException, APIRouter
from app import oauth2 

router  = APIRouter(
    prefix="/posts",
    tags=['posts']
)




@router.get("/",status_code=status.HTTP_201_CREATED, response_model=List[schemas.Post])
def get_posts(db: Session= Depends(get_db),
              current_user: int =Depends(oauth2.get_current_user), limit: int =10, skip: int =0,
              search: Optional[str]=""):
    #cursor.execute("""SELECT * FROM kasi.post1;""")
    #post1 = cursor.fetchall()
    post1 = db.query(model.Post).filter(model.Post.title.contains(search)).limit(limit).offset(skip).all()

    return post1
 
@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post:schemas.PostCreate, db: Session= Depends(get_db), current_user: int =Depends(oauth2.get_current_user)):
     
    print(current_user.email)
    new_post=model.Post(
        ower_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    
    return new_post

@router.get ("/{id}", response_model=schemas.Post)
def get_post(id:int, response: Response, db: Session= Depends(get_db), current_user: int =Depends(oauth2.get_current_user)):
    
    post = db.query(model.Post).filter(model.Post.id == id).first()
   
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id:{id} was not found")
    #post = find_post(id)
    print(post)

    return post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session= Depends(get_db), current_user: int =Depends(oauth2.get_current_user)):
    
    post_query = db.query(model.Post).filter(model.Post.id == id)
    post =post_query.first()

   
    if post ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id:{id} doesnot exist ")
    
    if post.ower_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not authorized to perform Resquested Action ")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
   

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session= Depends(get_db), current_user: int =Depends(oauth2.get_current_user)):

    post_query  = db.query(model.Post).filter(model.Post.id == id)

    post=post_query.first()

    if post ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id:{id} doesnot exist ")
    
    if post.ower_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not authorized to perform Resquested Action ")
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    return post_query.first()