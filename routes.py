from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .database import SessionLocal
from .models import User
from .gemini_generator import generate_workout_gemini
from .gemini_flash_generator import generate_nutrition_tip_with_flash
from .updated_plan import update_workout_plan

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout(request: Request, name: str = Form(...), user_id: str = Form(...),
                     age: int = Form(...), weight: str = Form(...),
                     goal: str = Form(...), intensity: str = Form(...)):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            user = User(name=name, user_id=user_id, age=age, weight=weight,
                        goal=goal, intensity=intensity, original_plan="")
            db.add(user)
            db.flush()
        else:
            user.name, user.age, user.weight = name, age, weight
            user.goal, user.intensity = goal, intensity

        plan = generate_workout_gemini(name, age, weight, goal, intensity)
        tip = generate_nutrition_tip_with_flash(goal)
        user.original_plan = plan
        user.updated_plan = None
        user.nutrition_tip = tip
        db.commit()
        return templates.TemplateResponse("result.html",
            {"request": request, "user": user, "plan": plan, "tip": tip})
    finally:
        db.close()

@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(request: Request, user_id: str = Form(...), feedback: str = Form(...)):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            return templates.TemplateResponse("result.html",
                {"request": request, "error": "User ID not found."})
        base_plan = user.updated_plan or user.original_plan
        revised = update_workout_plan(base_plan, feedback)
        user.updated_plan = revised
        db.commit()
        return templates.TemplateResponse("result.html",
            {"request": request, "user": user, "plan": revised,
             "tip": user.nutrition_tip, "updated": True})
    finally:
        db.close()

@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request):
    db = SessionLocal()
    try:
        users = db.query(User).order_by(User.id.desc()).all()
        return templates.TemplateResponse("all_users.html",
            {"request": request, "users": users})
    finally:
        db.close()
