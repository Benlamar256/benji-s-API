from fastapi import FastAPI

from .Routers import extract, compute_pt, start_time, stop_time
from .import model
from .database import engine
from .Routers import post, user, auth
from .config import settings
from fastapi.middleware.cors import CORSMiddleware
#from  import compute_pt
#from pythonProject15.extract import extract


model.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins =["*"]

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
app.include_router(compute_pt.router)
app.include_router(extract.router)
app.include_router(start_time.router)
app.include_router(stop_time.router)

@app.get("/")
def root():
    return{"message":"hello world"}

        

        



