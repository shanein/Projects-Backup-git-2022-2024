from fastapi import HTTPException
from pydantic import BaseModel


class EmailAlreadyExists(HTTPException):
    def __init__(self):
        super().__init__(status_code=422, detail="Email déjà existant")


class UsernameTooShort(HTTPException):
    def __init__(self):
        super().__init__(status_code=422, detail="Le nom est trop court")


class SuccessResponse(BaseModel):
    success: bool = True
    message: str = "Success"
    data: dict = None
