from fastapi import APIRouter, HTTPException, Response, Request
from jose import JWTError, jwt

from app.DB import get_session
from app.sql.sql_fxns import get_user_by_email, create_user
from app.core.security import (
    hash_password, verify_password,
    create_access_token, create_refresh_token,
    SECRET_KEY, ALGORITHM, ACCESS_EXPIRE_MIN, REFRESH_EXPIRE_DAYS
)

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup")
async def signup_user(user: dict):
    username = user.get("username")
    password = user.get("password")

    if not username or not password:
        return {"success": False, "message": "Email and password are required"}

    existing_user = get_user_by_email(username, next(get_session()))
    if existing_user:
        return {"success": False, "message": "User already exists"}

    create_user(username, hash_password(password), next(get_session()))
    return {"success": True, "message": "User created successfully"}

@router.post("/signin")
async def signin_user(user: dict, response: Response):
    username = user.get("username")
    password = user.get("password")

    existing_user = get_user_by_email(username, next(get_session()))
    if not existing_user or not verify_password(password, existing_user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(existing_user.user_id)
    refresh_token = create_refresh_token(existing_user.user_id)

    # local dev: secure=False (set True in production https)
    response.set_cookie("access_token", access_token, httponly=True, secure=False, samesite="lax",
                        max_age=ACCESS_EXPIRE_MIN * 60, path="/")
    response.set_cookie("refresh_token", refresh_token, httponly=True, secure=False, samesite="lax",
                        max_age=REFRESH_EXPIRE_DAYS * 24 * 60 * 60, path="/auth/refresh")
    
    return {"success": True}

@router.post("/refresh")
async def refresh(request: Request, response: Response):
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        user_id = int(payload["sub"])
        new_access = create_access_token(user_id)

        response.set_cookie("access_token", new_access, httponly=True, secure=False, samesite="lax",
                            max_age=ACCESS_EXPIRE_MIN * 60, path="/")

        return {"success": True}

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
