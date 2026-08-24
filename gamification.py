import math

# XP deduction based on highest hint tier used
XP_MULTIPLIER = {
    0: 1.0,    # No hints = 100% XP
    1: 0.90,   # Nudge 1 = 90%
    2: 0.75,   # Nudge 2 = 75%
    3: 0.50,   # Structure = 50%
    4: 0.20,   # Solution = 20%
}

BASE_XP = {
    "easy": 20,
    "medium": 50,
    "hard": 100,
}

def calculate_xp(difficulty, max_hint_tier):
    base = BASE_XP.get(difficulty, 20)
    multiplier = XP_MULTIPLIER.get(max_hint_tier, 1.0)
    return max(4, int(base * multiplier))

def calculate_level(total_xp):
    return int(math.floor(math.sqrt(total_xp / 100))) + 1

def xp_for_level(level):
    return ((level - 1) ** 2) * 100

def get_level_progress(total_xp):
    current_level = calculate_level(total_xp)
    current_level_xp = xp_for_level(current_level)
    next_level_xp = xp_for_level(current_level + 1)
    
    if next_level_xp == current_level_xp:
        return 1.0
    
    progress = (total_xp - current_level_xp) / (next_level_xp - current_level_xp)
    return min(1.0, max(0.0, progress))

def update_streak(last_active_date, today):
    if last_active_date is None:
        return {"current_streak": 1, "streak_broke": False}
    
    from datetime import timedelta
    diff = (today - last_active_date).days
    
    if diff == 0:
        return {"current_streak": None, "streak_broke": False}  # Already active today
    elif diff == 1:
        return {"current_streak": "increment", "streak_broke": False}
    else:
        return {"current_streak": 1, "streak_broke": True}