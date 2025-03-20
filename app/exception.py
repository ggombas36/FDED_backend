from fastapi import HTTPException

class UserExistsError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=409,  # Conflict
            detail={
                "code": "EXISTING_USERNAME",
                "message": "A felhasználónév már foglalt!"
            }
        )

class EmailExistsError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=409,  # Conflict
            detail={
                "code": "EXISTING_EMAIL",
                "message": "Ez az email cím már regisztrálva van!"
            }
        )