import calendar
from datetime import date

from .payday import DEFAULT_STRATEGY, STRATEGIES, PaydayStrategy


def build_month_calendar(
    today: date,
    strategy: PaydayStrategy = DEFAULT_STRATEGY,
) -> dict:
    """Build all the context needed for the budget view, independent of any framework."""
    pd = strategy.get_payday(today.year, today.month)
    days_left = (pd - today).days - 1  # money arrives at 00:00 on payday

    _, last_dom = calendar.monthrange(today.year, today.month)
    all_days = []
    for day_num in range(1, last_dom + 1):
        d = date(today.year, today.month, day_num)
        if d < today:
            status = "past"
        elif d == pd:
            status = "payday"
        elif d > pd:
            status = "after"
        else:
            status = "budget"
        all_days.append({
            "iso": d.isoformat(),
            "day": d.day,
            "status": status,
        })

    budget_isos = [d["iso"] for d in all_days if d["status"] == "budget"]

    return {
        "today": today,
        "payday": pd,
        "payday_formatted": pd.strftime("%A, %d %B %Y"),
        "month_label": today.strftime("%B %Y"),
        "strategy_key": strategy.key,
        "strategy_label": strategy.label,
        "strategies": [{"key": s.key, "label": s.label} for s in STRATEGIES],
        "days_left": days_left,
        "payday_reached": days_left <= 0,
        "all_days_json": all_days,
        "budget_dates_json": budget_isos,
        "first_weekday": date(today.year, today.month, 1).weekday(),
    }
