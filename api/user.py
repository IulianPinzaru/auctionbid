from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from basemodels.userserializer import UserLogin
from basemodels.userserializer import UserRegister
from db.database import get_db
from utils.create_user import create_user
from utils.jwt import authenticate_user, create_access_token

router = APIRouter(prefix="/api/users")


@router.post("/register/", tags=["user"])
def create_new_user(user: UserRegister, db: Session = Depends(get_db)):
    if user.admin_register_key and user.role == "admin":
        user.role = "admin"
    else:
        user.role = "user"

    new_user = create_user(db, user)
    if not new_user:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={
                                "message": "Something went wrong while creating the user. Please try again later."})
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content={"message": f"Welcome {new_user.first_name} {new_user.last_name}!"})


@router.post("/token", tags=["user"])
def login(user: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user.email, user.password)
    if not user:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"message": "Invalid username or password"})
    return {"access_token": create_access_token({"email": user.email})}
