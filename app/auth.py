"""Production authentication module with JWT, email verification, and subscriptions."""
import os
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlmodel import Session, select
import bcrypt

from .models import (
    User, UserCreate, UserRead, UserUpdate, Token, TokenData,
    Subscription, SubscriptionRead, Payment, PaymentRead,
    get_session, engine, init_db, UserRole
)

router = APIRouter(prefix="/auth", tags=["authentication"])

# --- JWT Configuration ---
SECRET_KEY = os.environ.get("JWT_SECRET", "change-this-in-production-min-32-chars!")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"iat": datetime.now(timezone.utc), "exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception

    user = session.exec(select(User).where(User.email == token_data.email)).first()
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def check_plan_limits(user: User, session: Session, required_agent: str = None):
    """Check if user can perform action based on their subscription plan."""
    from .models import PLAN_LIMITS, Task
    
    # Get user's active subscription
    subscription = session.exec(
        select(Subscription).where(
            Subscription.user_id == user.id,
            Subscription.status == "active"
        )
    ).first()
    
    plan = subscription.plan if subscription else "free"
    
    # Check task count for the month
    now = datetime.now(timezone.utc)
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    task_count = session.exec(
        select(Task).where(
            Task.user_id == user.id,
            Task.created_at >= month_start
        )
    ).all()
    
    limits = PLAN_LIMITS.get(plan, PLAN_LIMITS["free"])
    
    if limits["tasks_per_month"] != -1 and len(task_count) >= limits["tasks_per_month"]:
        raise HTTPException(
            status_code=403,
            detail=f"Monthly task limit reached for {plan} plan. Upgrade to continue."
        )
    
    # Check agent access
    if required_agent and required_agent not in limits.get("agents", []) and "all" not in limits.get("agents", []):
        raise HTTPException(
            status_code=403,
            detail=f"{required_agent} not available in {plan} plan. Upgrade to access."
        )
    
    return plan


# --- Auth Routes ---

@router.post("/signup", response_model=UserRead, status_code=201)
async def signup(user_in: UserCreate, session: Session = Depends(get_session)):
    """Create a new user account."""
    # Check if email exists
    existing = session.exec(select(User).where(User.email == user_in.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create user
    user = User(
        email=user_in.email,
        password_hash=hash_password(user_in.password),
        full_name=user_in.full_name,
        role=UserRole.FREE,
        is_active=True,
        is_verified=False,
        email_verification_token=secrets.token_urlsafe(32),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    # Create free subscription
    subscription = Subscription(
        user_id=user.id,
        plan="free",
        status="active",
        current_period_start=datetime.now(timezone.utc),
        current_period_end=datetime.now(timezone.utc) + timedelta(days=30),
    )
    session.add(subscription)
    session.commit()

    # TODO: Send verification email
    return user


@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    """Authenticate user and return JWT token."""
    user = session.exec(select(User).where(User.email == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Account deactivated")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserRead)
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.put("/me", response_model=UserRead)
async def update_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """Update user profile."""
    if user_update.full_name is not None:
        current_user.full_name = user_update.full_name
    if user_update.password is not None:
        current_user.password_hash = hash_password(user_update.password)
    
    current_user.updated_at = datetime.now(timezone.utc)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user


@router.get("/subscription", response_model=SubscriptionRead)
async def get_subscription(
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """Get user's current subscription."""
    subscription = session.exec(
        select(Subscription).where(Subscription.user_id == current_user.id).order_by(Subscription.created_at.desc())
    ).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="No subscription found")
    return subscription


@router.get("/payments", response_model=List[PaymentRead])
async def get_payments(
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """Get user's payment history."""
    payments = session.exec(
        select(Payment).where(Payment.user_id == current_user.id).order_by(Payment.created_at.desc())
    ).all()
    return payments


@router.post("/verify-email/{token}")
async def verify_email(token: str, session: Session = Depends(get_session)):
    """Verify email address."""
    user = session.exec(select(User).where(User.email_verification_token == token)).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid verification token")
    
    user.is_verified = True
    user.email_verification_token = None
    session.add(user)
    session.commit()
    return {"message": "Email verified successfully"}


@router.post("/forgot-password")
async def forgot_password(email: str, session: Session = Depends(get_session)):
    """Request password reset."""
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        return {"message": "If email exists, reset link sent"}  # Don't reveal if email exists
    
    user.reset_token = secrets.token_urlsafe(32)
    user.reset_token_expires = datetime.now(timezone.utc) + timedelta(hours=1)
    session.add(user)
    session.commit()
    
    # TODO: Send reset email
    return {"message": "Password reset link sent to your email"}


@router.post("/reset-password/{token}")
async def reset_password(token: str, new_password: str, session: Session = Depends(get_session)):
    """Reset password with token."""
    user = session.exec(select(User).where(User.reset_token == token)).first()
    if not user or not user.reset_token_expires or user.reset_token_expires < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")
    
    user.password_hash = hash_password(new_password)
    user.reset_token = None
    user.reset_token_expires = None
    session.add(user)
    session.commit()
    return {"message": "Password reset successfully"}