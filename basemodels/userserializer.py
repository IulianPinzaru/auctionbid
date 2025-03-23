from typing import Optional

from pydantic import BaseModel


class UserRegister(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    role: Optional[str] = "user"
    admin_register_key: Optional[str] = ""


class UserLogin(BaseModel):
    email: str
    password: str
