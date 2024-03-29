from fastapi import status as st

from app.core.error import ErrorCodeBase


class ErrorCode(ErrorCodeBase):
    invalid_token_credentials = "Invalid token credentials", st.HTTP_401_UNAUTHORIZED
    unsuccessful_authentication = "Authentication is unsuccessful", st.HTTP_401_UNAUTHORIZED

    user_not_found = "User not found", st.HTTP_404_NOT_FOUND
    user_not_active = "Eser not active", st.HTTP_401_UNAUTHORIZED

    email_already_used = "Email is already used"
    username_already_used = "Username is already used"

    cleaning_not_found = "Cleaning info not found", st.HTTP_404_NOT_FOUND
    cleaning_unauthorized_access = "Unauthorized cleaning info access", st.HTTP_403_FORBIDDEN

    offer_method_not_allowed = "Offer method not allowed"
    offer_already_created = "Offer is already created"
    offer_unauthorized_access = "Unauthorized access to this offer", st.HTTP_403_FORBIDDEN
    offer_not_found = "Offer not found", st.HTTP_404_NOT_FOUND
    offer_has_wrong_status = "Offer has wrong status"

    evaluation_unauthorized_access = "Evaluation unauthorized access", st.HTTP_401_UNAUTHORIZED
    evaluation_already_created = "Evaluation review already created"
    evaluation_not_found = "Evaluation not found"

    system_not_implemented = "Systemm not implemented"
