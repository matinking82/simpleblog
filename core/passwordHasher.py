import bcrypt
from fastapi import Depends
from typing import Annotated

class PasswordHasher:
    def __init__(self):
        pass

    def HashPassword(self, password):
        # Generate a salt and hash the password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

    def VerifyPassword(self, password, hashed_password):
        # Verify if the provided password matches the hashed password
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    
PasswordHasherDep = Annotated[PasswordHasher, Depends(PasswordHasher)]