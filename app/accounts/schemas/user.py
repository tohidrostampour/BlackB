from pydantic import BaseModel, EmailStr


class BaseUser(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str


class BaseProfile(BaseModel):
    bio: str
    age: int
    phone: str


class UserCreateInput(BaseUser):
    pass


class UserUpdateInput(BaseUser):
    id: int


class UserReadModel(BaseUser):
    id: int
    name: str
    username: str
    email: str

    class Config:
        orm_mode = True


class ProfileUpdateInput(BaseProfile):
    id: int


class ProfileReadModel(BaseProfile):
    id: int

    class Config:
        orm_mode = True
