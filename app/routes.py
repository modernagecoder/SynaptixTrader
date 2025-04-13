import os
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def dashboard():
    dashboard_path = os.path.join(os.path.dirname(__file__), "..", "ui", "dashboard.html")
    with open(dashboard_path, "r") as f:
        return f.read()

@router.get("/api/performance")
def get_performance():
    # This endpoint will be populated by the main app's performance data.
    from app.main import performance  # Importing here to avoid circular dependency
    return performance

@router.get("/api/orders")
def get_orders():
    from app.main import orders  # Importing here to avoid circular dependency
    return orders
