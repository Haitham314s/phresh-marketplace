from enum import Enum

from fastapi import status as st, HTTPException


class Error:
    def __init__(self, message: str, error_code: int = st.HTTP_400_BAD_REQUEST):
        self.message = message
        self.error_code = error_code


class ErrorCodeBase(Error, Enum):
    def __new__(cls, message, error_code: int = st.HTTP_400_BAD_REQUEST):
        return Error(message, error_code)


class APIException(HTTPException):
    def __init__(self, error: Error, headers: dict[str, str] | None = None):
        super().__init__(status_code=error.error_code, detail=error.message, headers=headers)
