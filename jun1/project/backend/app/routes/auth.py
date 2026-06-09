from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from fastapi.security import (
    OAuth2PasswordRequestForm
)

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.models.user import User

from app.schemas.user_schema import (
    UserRegister
)

from app.services.auth_service import (
    hash_password,
    verify_password,
    create_access_token
)

from app.utils.response import (
    success_response,
    error_response
)

router = APIRouter()


# =========================
# REGISTER
# =========================
@router.post("/register")
def register(
    user: UserRegister,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(
            user.password
        )
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return success_response(
        "User registered successfully",
        {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email
        }
    )


# =========================
# LOGIN
# =========================
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    # 🔍 DEBUG: check all users in DB
    print("ALL USERS IN DB:", db.query(User).all())

    db_user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    # CHECK USER
    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email"
        )

    # CHECK PASSWORD
    if not verify_password(
        form_data.password,
        db_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    access_token = create_access_token(
        {"sub": db_user.email}
    )

    return {
        "success": True,
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": db_user.id,
            "name": db_user.name,
            "email": db_user.email
        }
    }