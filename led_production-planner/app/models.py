from pydantic import BaseModel
from datetime import datetime

class Order(BaseModel):
    order_id: str
    sku: str
    colour: str
    voltage: int
    reels: int
    priority: int
    due_date: datetime
    dies_per_led: int

class RMInventory(BaseModel):
    dies: int
    leadframes: int
    tape_reels: int
