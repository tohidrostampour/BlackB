from pydantic import BaseModel


class BaseProfile(BaseModel):
    bio: str | None = None
    age: int | None = None
    phone: str | None = None


class ProfileRead(BaseProfile):
    user_id: int

    class Config:
        orm_mode = True


class ProfileUpdate(BaseProfile):
    bio: str | None = None
    age: str | None = None
    phone: str | None = None
