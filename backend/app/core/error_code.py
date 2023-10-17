from app.core.error import ErrorCodeBase
from fastapi import status as st


class ErrorCode(ErrorCodeBase):
    invalid_token_credentials = "invalid token credentials", st.HTTP_401_UNAUTHORIZED
    unsuccessful_authentication = "authentication is unsuccessful", st.HTTP_401_UNAUTHORIZED

    user_not_found = "user not found", st.HTTP_404_NOT_FOUND
    user_not_active = "user not active", st.HTTP_401_UNAUTHORIZED

    email_already_used = "email is already used"
    username_already_used = "username is already used"

    cleaning_not_found = "cleaning info not found", st.HTTP_404_NOT_FOUND
    cleaning_unauthorized_access = "unauthorized cleaning info access", st.HTTP_403_FORBIDDEN
