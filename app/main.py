from fastapi import FastAPI
from .import model
from .database import engine
from .Routers import post, user, auth
from .config import settings
from fastapi.middleware.cors import CORSMiddleware


model.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins =["https://www.google"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)





app.include_router(post.router)        
app.include_router(user.router)   
app.include_router(auth.router)

@app.get("/")
def root():
    return{"message":"hello world"}

        

        



