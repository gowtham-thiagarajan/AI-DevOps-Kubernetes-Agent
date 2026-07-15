"""
Authentication routes for user login and session management.
"""
from datetime import datetime
from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login")
async def login(email: str, password: str):
    """
    Authenticate user with email and password.
    For MVP, accept any non-empty email/password combination.
    In production, integrate with InsForge or your auth provider.
    """
    if not email or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required",
        )

    # Simple mock authentication
    # In production: verify against InsForge or database
    user = {
        "id": "user_123",
        "email": email,
        "name": email.split("@")[0].title(),
    }
    return {
        "status": "authenticated",
        "user": user,
        "session_token": f"session_{email}_{datetime.now().timestamp()}",
    }


@router.get("/me")
async def get_current_user():
    """
    Get current authenticated user.
    For MVP, return a mock user.
    In production, verify session token and fetch from database.
    """
    # Mock authenticated user
    # In production: validate session token from request headers
    user = {
        "id": "user_123",
        "email": "demo@kubernetes.io",
        "name": "Demo User",
    }
    return {
        "status": "authenticated",
        "user": user,
        "authenticated": True,
    }


@router.post("/logout")
async def logout():
    """
    Logout current user and clear session.
    """
    return {"status": "logged out"}

