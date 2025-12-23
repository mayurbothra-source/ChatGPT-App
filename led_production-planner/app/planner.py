from datetime import datetime, timedelta
from typing import List
from app.models import Order, RMInventory

LEDS_PER_REEL = 10000
DIE_UPH_EFFECTIVE = 81600

def run_planner(
    orders: List[Order],
    rm: RMInventory,
    start_time: datetime
):
    results = []
    current_time = start_time

    for order in sorted(orders, key=lambda o: o.priority):
        leds = order.reels * LEDS_PER_REEL
        dies_needed = leds * order.dies_per_led
        die_hours = dies_needed / DIE_UPH_EFFECTIVE

        if (
            rm.dies < dies_needed or
            rm.leadframes < leds or
            rm.tape_reels < order.reels
        ):
            results.append({
                "order_id": order.order_id,
                "status": "BLOCKED – RM SHORTAGE",
                "delivery": None
            })
            continue

        die_end = current_time + timedelta(hours=die_hours)

        rm.dies -= dies_needed
        rm.leadframes -= leds
        rm.tape_reels -= order.reels

        results.append({
            "order_id": order.order_id,
            "status": "SCHEDULED",
            "delivery": die_end.strftime("%Y-%m-%d %H:%M")
        })

        current_time = die_end

    return results
