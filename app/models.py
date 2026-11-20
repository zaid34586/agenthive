"""Production-ready SQLModel models for AgentHive SaaS."""
import os
from datetime import datetime, timezone
from typing import Optional, List
from enum import Enum as PyEnum

from sqlmodel import SQLModel, Session, create_engine, Field, select, Relationship
from sqlalchemy import Column, String, DateTime, Float, Integer, Boolean, Text, ForeignKey, Enum


# ============================================================================
# Enums
# ============================================================================
class UserRole(str, PyEnum):
    FREE = "free"
    PRO = "pro"
    BUSINESS = "business"
    ADMIN = "admin"


class TaskStatus(str, PyEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class SubscriptionStatus(str, PyEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    CANCELLED = "cancelled"
    PAST_DUE = "past_due"


class PaymentStatus(str, PyEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


# ============================================================================
# Database Configuration
# ============================================================================
DB_PATH = os.getenv("DATABASE_URL", "sqlite:///./data.db")

# Support both SQLite and PostgreSQL
if DB_PATH.startswith("postgresql"):
    engine = create_engine(DB_PATH, echo=False, future=True, pool_pre_ping=True)
else:
    engine = create_engine(DB_PATH, echo=False, future=True, connect_args={"check_same_thread": False})


def get_session() -> Session:
    return Session(engine, future=True)


def init_db():
    """Initialize database tables."""
    SQLModel.metadata.create_all(engine)


# ============================================================================
# Models
# ============================================================================


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True, max_length=255)
    password_hash: str = Field(max_length=255)
    full_name: Optional[str] = Field(default=None, max_length=100)
    role: UserRole = Field(default=UserRole.FREE, sa_column=Column(Enum(UserRole)))
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)
    email_verification_token: Optional[str] = Field(default=None, max_length=255)
    reset_token: Optional[str] = Field(default=None, max_length=255)
    reset_token_expires: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationships
    tasks: List["Task"] = Relationship(back_populates="user")
    subscriptions: List["Subscription"] = Relationship(back_populates="user")
    payments: List["Payment"] = Relationship(back_populates="user")
    usage_logs: List["UsageLog"] = Relationship(back_populates="user")


class Subscription(SQLModel, table=True):
    __tablename__ = "subscriptions"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    plan: str = Field(max_length=50)  # free, pro, business
    status: SubscriptionStatus = Field(default=SubscriptionStatus.ACTIVE)
    razorpay_subscription_id: Optional[str] = Field(default=None, max_length=100)
    razorpay_customer_id: Optional[str] = Field(default=None, max_length=100)
    current_period_start: Optional[datetime] = Field(default=None)
    current_period_end: Optional[datetime] = Field(default=None)
    cancel_at_period_end: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationships
    user: Optional[User] = Relationship(back_populates="subscriptions")


class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=255)
    description: str = Field(default="")
    status: TaskStatus = Field(default=TaskStatus.PENDING)
    result: Optional[str] = Field(default=None, sa_column=Column(Text))
    error: Optional[str] = Field(default=None, sa_column=Column(Text))
    agent_type: Optional[str] = Field(default=None, max_length=50)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationships
    user: Optional[User] = Relationship(back_populates="tasks")
    agent_logs: List["AgentLog"] = Relationship(back_populates="task")


class Payment(SQLModel, table=True):
    __tablename__ = "payments"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    razorpay_order_id: Optional[str] = Field(default=None, max_length=100)
    razorpay_payment_id: Optional[str] = Field(default=None, max_length=100)
    razorpay_signature: Optional[str] = Field(default=None, max_length=255)
    amount: int = Field(default=0)  # in paise/cents
    currency: str = Field(default="INR", max_length=10)
    status: PaymentStatus = Field(default=PaymentStatus.PENDING)
    plan: str = Field(max_length=50)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationships
    user: Optional[User] = Relationship(back_populates="payments")


class UsageLog(SQLModel, table=True):
    __tablename__ = "usage_logs"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    task_id: Optional[int] = Field(default=None, foreign_key="tasks.id")
    agent_name: str = Field(max_length=100)
    tokens_used: int = Field(default=0)
    cost: float = Field(default=0.0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationships
    user: Optional[User] = Relationship(back_populates="usage_logs")


class AgentLog(SQLModel, table=True):
    __tablename__ = "agent_logs"

    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="tasks.id", index=True)
    agent_name: str = Field(max_length=100)
    status: str = Field(max_length=50)
    message: str = Field(default="")
    data: Optional[str] = Field(default=None, sa_column=Column(Text))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Relationships
    task: Optional[Task] = Relationship(back_populates="agent_logs")


# ============================================================================
# Pydantic Schemas
# ============================================================================


class UserCreate(SQLModel):
    email: str
    password: str
    full_name: Optional[str] = None


class UserRead(SQLModel):
    id: int
    email: str
    full_name: Optional[str] = None
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(SQLModel):
    full_name: Optional[str] = None
    password: Optional[str] = None


class TaskCreate(SQLModel):
    title: str
    description: str = ""


class TaskRead(SQLModel):
    id: int
    user_id: int
    title: str
    description: str
    status: TaskStatus
    result: Optional[str] = None
    error: Optional[str] = None
    agent_type: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class SubscriptionRead(SQLModel):
    id: int
    plan: str
    status: SubscriptionStatus
    current_period_start: Optional[datetime]
    current_period_end: Optional[datetime]
    cancel_at_period_end: bool

    class Config:
        from_attributes = True


class PaymentRead(SQLModel):
    id: int
    amount: int
    currency: str
    status: PaymentStatus
    plan: str
    created_at: datetime

    class Config:
        from_attributes = True


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    email: Optional[str] = None


# Plan limits
PLAN_LIMITS = {
    "free": {"tasks_per_month": 5, "agents": ["head_agent", "trend_scout"]},
    "pro": {"tasks_per_month": 50, "agents": ["all"]},
    "business": {"tasks_per_month": -1, "agents": ["all", "priority"]},
}

PLAN_PRICES = {
    "free": 0,
    "pro": 49900,      # ₹499.00 in paise
    "business": 149900,  # ₹1,499.00 in paise
}
