"""Billing and subscription management module."""
import os
import time
from typing import Optional, List
from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from .models import (
    User, Subscription, Payment, UsageLog, Task, AgentLog,
    get_session, PLAN_LIMITS, PLAN_PRICES
)
from .auth import get_current_active_user

router = APIRouter(prefix="/api/billing", tags=["billing"])


@router.get("/plans")
async def get_plans():
    """Get all available subscription plans with pricing and limits."""
    return {
        "plans": [
            {
                "id": "free",
                "name": "Starter",
                "price": 0,
                "currency": "INR",
                "interval": "month",
                "description": "For individuals testing automation",
                "features": [
                    "5 tasks/month",
                    "Head Agent + Trend Scout",
                    "Basic analytics",
                ],
                "limits": PLAN_LIMITS["free"],
            },
            {
                "id": "pro",
                "name": "Pro",
                "price": PLAN_PRICES["pro"],
                "currency": "INR",
                "interval": "month",
                "description": "For serious creators & sellers",
                "features": [
                    "50 tasks/month",
                    "All 5 agents",
                    "Creative Studio (ads + video + UGC)",
                    "Social Media Manager",
                    "Auto-reply comments & DMs",
                    "Priority support",
                ],
                "limits": PLAN_LIMITS["pro"],
                "popular": True,
            },
            {
                "id": "business",
                "name": "Business",
                "price": PLAN_PRICES["business"],
                "currency": "INR",
                "interval": "month",
                "description": "For teams & agencies",
                "features": [
                    "Unlimited tasks",
                    "All 5 agents + priority routing",
                    "Multi-user workspace",
                    "Custom API integration",
                    "Dedicated support",
                    "White-label reports",
                ],
                "limits": PLAN_LIMITS["business"],
            },
        ]
    }


@router.post("/create-order")
async def create_payment_order(
    payload: dict,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    """Create a Razorpay order for subscription payment."""
    plan = payload.get("plan", "pro")
    
    if plan not in PLAN_PRICES:
        raise HTTPException(status_code=400, detail="Invalid plan")
    
    amount = PLAN_PRICES[plan]
    currency = "INR"
    
    razorpay_key_id = os.environ.get("RAZORPAY_KEY_ID", "")
    razorpay_key_secret = os.environ.get("RAZORPAY_KEY_SECRET", "")
    
    if not razorpay_key_id or not razorpay_key_secret:
        # Demo mode
        order_id = f"order_demo_{plan}_{int(time.time())}"
        # Save payment record as pending
        payment = Payment(
            user_id=current_user.id,
            razorpay_order_id=order_id,
            amount=amount,
            currency=currency,
            status="pending",
            plan=plan,
        )
        session.add(payment)
        session.commit()
        
        return {
            "id": order_id,
            "amount": amount,
            "currency": currency,
            "receipt": f"receipt_{plan}_{current_user.id}",
            "status": "created",
            "demo": True,
            "key_id": "demo",
            "message": "Demo mode — add RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET to .env for real payments",
        }
    
    try:
        import razorpay
        client = razorpay.Client(auth=(razorpay_key_id, razorpay_key_secret))
        order = client.order.create({
            "amount": amount,
            "currency": currency,
            "receipt": f"receipt_{plan}_{current_user.id}",
            "notes": {"user_id": str(current_user.id), "plan": plan},
        })
        
        # Save payment record
        payment = Payment(
            user_id=current_user.id,
            razorpay_order_id=order["id"],
            amount=amount,
            currency=currency,
            status="pending",
            plan=plan,
        )
        session.add(payment)
        session.commit()
        
        return {
            **order,
            "key_id": razorpay_key_id,
            "demo": False,
        }
    except ImportError:
        raise HTTPException(status_code=500, detail="Razorpay package not installed")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/verify")
async def verify_payment(
    payload: dict,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    """Verify payment and activate subscription."""
    razorpay_key_secret = os.environ.get("RAZORPAY_KEY_SECRET", "")
    
    order_id = payload.get("razorpay_order_id", "")
    payment_id = payload.get("razorpay_payment_id", "")
    signature = payload.get("razorpay_signature", "")
    plan = payload.get("plan", "pro")
    
    # Find payment record
    payment = session.exec(
        select(Payment).where(Payment.razorpay_order_id == order_id)
    ).first()
    
    if not payment:
        raise HTTPException(status_code=404, detail="Payment order not found")
    
    if not razorpay_key_secret:
        # Demo mode — auto approve
        payment.status = "completed"
        payment.razorpay_payment_id = payment_id or "demo"
        payment.razorpay_signature = signature or "demo"
        payment.updated_at = datetime.now(timezone.utc)
        session.add(payment)
        
        # Activate subscription
        now = datetime.now(timezone.utc)
        subscription = Subscription(
            user_id=current_user.id,
            plan=plan,
            status="active",
            current_period_start=now,
            current_period_end=now + timedelta(days=30),
        )
        session.add(subscription)
        session.commit()
        
        return {
            "status": "success",
            "plan": plan,
            "message": "Demo mode — subscription activated",
        }
    
    try:
        import razorpay
        client = razorpay.Client(
            auth=(os.environ.get("RAZORPAY_KEY_ID", ""), razorpay_key_secret)
        )
        client.utility.verify_payment_signature({
            "razorpay_order_id": order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature,
        })
        
        payment.status = "completed"
        payment.razorpay_payment_id = payment_id
        payment.razorpay_signature = signature
        payment.updated_at = datetime.now(timezone.utc)
        session.add(payment)
        
        # Activate subscription
        now = datetime.now(timezone.utc)
        subscription = Subscription(
            user_id=current_user.id,
            plan=plan,
            status="active",
            current_period_start=now,
            current_period_end=now + timedelta(days=30),
        )
        session.add(subscription)
        session.commit()
        
        return {
            "status": "success",
            "plan": plan,
            "message": "Payment verified — subscription activated",
        }
    except Exception as e:
        payment.status = "failed"
        payment.updated_at = datetime.now(timezone.utc)
        session.add(payment)
        session.commit()
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/usage")
async def get_usage(
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    """Get user's usage statistics."""
    now = datetime.now(timezone.utc)
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # Tasks this month
    tasks = session.exec(
        select(Task).where(
            Task.user_id == current_user.id,
            Task.created_at >= month_start
        )
    ).all()
    
    completed = len([t for t in tasks if t.status == "completed"])
    failed = len([t for t in tasks if t.status == "failed"])
    
    # Agent logs
    agent_logs = session.exec(
        select(AgentLog).join(Task).where(
            Task.user_id == current_user.id,
            AgentLog.created_at >= month_start
        )
    ).all()
    
    total_cost = sum(log.cost or 0 for log in agent_logs)
    total_tokens = sum(log.tokens_used or 0 for log in agent_logs)
    
    # Get plan limits
    subscription = session.exec(
        select(Subscription).where(
            Subscription.user_id == current_user.id,
            Subscription.status == "active"
        )
    ).first()
    plan = subscription.plan if subscription else "free"
    limits = PLAN_LIMITS.get(plan, PLAN_LIMITS["free"])
    
    return {
        "plan": plan,
        "tasks_this_month": len(tasks),
        "task_limit": limits["tasks_per_month"],
        "tasks_completed": completed,
        "tasks_failed": failed,
        "total_tokens_used": total_tokens,
        "total_cost": round(total_cost, 4),
        "remaining_tasks": (
            limits["tasks_per_month"] - len(tasks)
            if limits["tasks_per_month"] != -1
            else -1
        ),
    }


@router.post("/usage/log")
async def log_usage(
    payload: dict,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    """Log agent usage for billing/tracking."""
    task_id = payload.get("task_id")
    agent_name = payload.get("agent_name", "unknown")
    tokens_used = payload.get("tokens_used", 0)
    cost = payload.get("cost", 0.0)
    
    usage = UsageLog(
        user_id=current_user.id,
        task_id=task_id,
        agent_name=agent_name,
        tokens_used=tokens_used,
        cost=cost,
    )
    session.add(usage)
    session.commit()
    return {"status": "logged"}