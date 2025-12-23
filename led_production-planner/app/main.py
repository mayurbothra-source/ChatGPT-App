from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime

from app.models import Order, RMInventory
from app.planner import run_planner

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/plan", response_class=HTMLResponse)
def plan(
    request: Request,
    start_time: str = Form(...),
    dies: int = Form(...),
    leadframes: int = Form(...),
    tape_reels: int = Form(...),
    order_id: str = Form(...),
    reels: int = Form(...),
    dies_per_led: int = Form(...),
    priority: int = Form(...)
):
    order = Order(
        order_id=order_id,
        sku="AUTO",
        colour="NA",
        voltage=0,
        reels=reels,
        priority=priority,
        due_date=datetime.now(),
        dies_per_led=dies_per_led
    )

    rm = RMInventory(
        dies=dies,
        leadframes=leadframes,
        tape_reels=tape_reels
    )

    result = run_planner(
        orders=[order],
        rm=rm,
        start_time=datetime.fromisoformat(start_time)
    )

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "result": result}
    )
